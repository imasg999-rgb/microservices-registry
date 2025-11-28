import os
import sys
import logging
import signal
import atexit

from flask import Flask, jsonify

from microservices.utils.registry_client import (
    REGISTRY_BASE_URL,
    REGISTRY_REGISTER_PATH,
    REGISTRY_DEREGISTER_PATH,
    register_with_registry,
    deregister_from_registry,
    health_response,
)

SERVICE_NAME = "microservice-working-template-service"
SERVICE_DESCRIPTION = (
    "Template microservice that registers nd deregisters with the registry service."
)

SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:6000")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVICE_NAME)


@app.route("/", methods=["GET"])
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

    port = int(os.getenv("PORT", "6000"))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
