import os
import sys
import logging
import signal
import atexit
from flask import Flask, jsonify, send_from_directory, request
from dotenv import load_dotenv
import os
from microservices.live_flight.live_flight import search_flight


from microservices.utils.registry_client import (
    REGISTRY_BASE_URL,
    REGISTRY_REGISTER_PATH,
    REGISTRY_DEREGISTER_PATH,
    register_with_registry,
    deregister_from_registry,
    health_response,
)

SERVICE_NAME = "live-flight"
SERVICE_DESCRIPTION = (
    "A service that retrieves live status data for a given flight."
)

SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:8084")

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVICE_NAME)

@app.route("/info", methods=["GET"])
def root():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "description": SERVICE_DESCRIPTION,
            "endpoints": {
                "health": "/health",
            },
            "registry": {
                "base_url": REGISTRY_BASE_URL,
                "register_path": REGISTRY_REGISTER_PATH,
                "deregister_path": REGISTRY_DEREGISTER_PATH,
            },
        }
    ), 200

@app.route("/health", methods=["GET"])
def health():
    body, status_code = health_response(SERVICE_NAME)
    return jsonify(body), status_code

# Serve Frontend
@app.route("/", methods=["GET"])
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')


# API: /api/flight?flight=WJA123
@app.route("/api/flight", methods=["GET"])
def get_flight():
    flight_number = request.args.get("flight")

    if not flight_number: # Empty input
        return jsonify({"error": "Missing ?flight="}), 400

    try:
        data = search_flight(flight_number)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_signal(signum, frame):
    logger.info("Received signal %s; attempting deregistration", signum)
    try:
        deregister_from_registry()
    finally:
        sys.exit(0)

def main():
    register_with_registry(
        service_name=SERVICE_NAME,
        service_description=SERVICE_DESCRIPTION,
        service_url=SERVICE_URL,
    )

    atexit.register(deregister_from_registry)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    port = int(os.getenv("PORT", "8084"))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
