import os
import logging
import sys

from flask import Flask, jsonify, request, send_from_directory
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

app = Flask(__name__, static_folder="./frontend/build", static_url_path="/")


@app.route("/", methods=["GET"])
def serve_root():
    try:
        return send_from_directory(app.static_folder, "index.html")
    except FileNotFoundError:
        # Frontend not built yet – return JSON instead
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
    return jsonify({"status": "ok"}), 200


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


if __name__ == "__main__":
    # For local dev
    port = int(os.getenv("PORT", "5002"))
    app.run(host="0.0.0.0", port=port, debug=True)
