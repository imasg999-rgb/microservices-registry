import os
import sys
import logging
import atexit

import requests
from flask import Flask, jsonify, request, send_from_directory

from microservices.utils.registry_client import (
    register_with_registry,
    deregister_from_registry,
    health_response,
)

from microservices.currency_converter.currency_converter import (
    convert_currency,
    CurrencyProviderError,
)

SERVICE_NAME = os.getenv("SERVICE_NAME", "currency_converter")
SERVICE_DESCRIPTION = "Currency conversion microservice"
SERVICE_URL = os.getenv("SERVICE_URL", "https://currency_converter:8443")

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(SERVICE_NAME)

app = Flask(__name__, static_folder="./frontend/build", static_url_path="/")


@app.route("/", methods=["GET"])
def serve_react_app():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/info", methods=["GET"])
def info():
    return jsonify(
        {
            "service": SERVICE_NAME,
            "description": SERVICE_DESCRIPTION,
            "endpoints": {
                "health": "/health",
                "convert": "/convert?from=USD&to=EUR&amount=100",
            },
        }
    ), 200


@app.route("/health", methods=["GET"])
def health():
    body, status = health_response(SERVICE_NAME)
    return jsonify(body), status


@app.route("/convert", methods=["GET"])
def convert_route():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount_str = request.args.get("amount", "1")

    if not from_currency or not to_currency:
        return jsonify({
            "error": "Missing required parameters 'from' and 'to'.",
            "example": "/convert?from=USD&to=EUR&amount=100",
        }), 400

    try:
        amount = float(amount_str)
    except ValueError:
        return jsonify({"error": "'amount' must be numeric."}), 400

    try:
        result = convert_currency(from_currency, to_currency, amount)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except CurrencyProviderError as e:
        return jsonify({"error": str(e)}), 502

    except requests.exceptions.Timeout:
        logger.exception("Timeout contacting currency provider")
        return jsonify({"error": "Currency provider timed out"}), 504

    except requests.RequestException:
        logger.exception("Network error contacting currency provider")
        return jsonify({"error": "Network error contacting provider"}), 502

    except Exception:
        logger.exception("Unexpected error in /convert")
        return jsonify({"error": "Internal server error"}), 500


def main():
    register_with_registry(
        service_name=SERVICE_NAME,
        service_description=SERVICE_DESCRIPTION,
        service_url=SERVICE_URL,
    )

    atexit.register(deregister_from_registry)

    port = int(os.getenv("PORT", "8443"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )


if __name__ == "__main__":
    main()
