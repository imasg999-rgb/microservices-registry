import os
import sys
import logging
import atexit
import signal

from flask import Flask, jsonify, request, send_from_directory

from microservices.utils.registry_client import (
    register_with_registry,
    deregister_from_registry,
    health_response,
)

from microservices.destination_wishlist.destination_wishlist import (
    get_destination_description,
    DestinationError,
)

SERVICE_NAME = os.getenv("SERVICE_NAME", "destination_wishlist")
SERVICE_DESCRIPTION = "Destination wishlist microservice"
SERVICE_URL = os.getenv("SERVICE_URL", "https://destination_wishlist:5002")

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(SERVICE_NAME)

app = Flask(__name__, static_folder="./static", static_url_path="/")


@app.route("/", methods=["GET"])
def serve_root():
    try:
        return send_from_directory(app.static_folder, "index.html")
    except FileNotFoundError:
        return jsonify(
            {
                "service": SERVICE_NAME,
                "description": SERVICE_DESCRIPTION,
                "endpoints": {
                    "health": "/health",
                    "destination_description": "/api/destination-description?name=Paris&country=France",  # example
                },
            }
        ), 200


@app.get("/health")
def health():
    body, status = health_response(SERVICE_NAME)
    return jsonify(body), status


@app.get("/api/destination-description")
def destination_description():
    name = (request.args.get("name") or "").strip()
    country = (request.args.get("country") or "").strip() or None

    try:
        result = get_destination_description(name=name, country=country)
        return jsonify(result), 200

    except ValueError as e:
        logger.warning("Bad request for destination description: %s", e)
        return jsonify({"error": str(e)}), 400

    except DestinationError as e:
        logger.error("Failed to load destination description: %s", e)
        return jsonify({"error": "Failed to load destination description."}), 502

    except Exception:
        logger.exception("Unexpected error loading destination description")
        return jsonify({"error": "Internal server error."}), 500


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

    port = int(os.getenv("PORT", "5002"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )


if __name__ == "__main__":
    main()
