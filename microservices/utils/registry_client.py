import os
import logging
from typing import Optional, Tuple

import requests

REGISTRY_BASE_URL = os.getenv("REGISTRY_BASE_URL", "http://host.docker.internal:7993")
REGISTRY_LOGIN_PATH = os.getenv("REGISTRY_LOGIN_PATH", "/login")
REGISTRY_REGISTER_PATH = os.getenv("REGISTRY_REGISTER_PATH", "/services")
REGISTRY_DEREGISTER_PATH = os.getenv("REGISTRY_DEREGISTER_PATH", "/services")

REGISTRY_ADMIN_USER = os.getenv("REGISTRY_ADMIN_USER", "admin")
REGISTRY_ADMIN_PASSWORD = os.getenv("REGISTRY_ADMIN_PASSWORD", "ADMIN")

SERVICE_ID: Optional[str] = None
DEREGISTERED: bool = False

logger = logging.getLogger("registry-client")

def _build_url(base: str, path: str) -> str:
    return f"{base.rstrip('/')}{path}"


def get_registry_token() -> Optional[str]:
    login_url = _build_url(REGISTRY_BASE_URL, REGISTRY_LOGIN_PATH)
    payload = {
        "username": REGISTRY_ADMIN_USER,
        "password": REGISTRY_ADMIN_PASSWORD,
    }

    try:
        resp = requests.post(login_url, json=payload, timeout=5)
        if resp.status_code != 200:
            logger.error("Registry login failed: %s %s", resp.status_code, resp.text)
            return None

        data = resp.json()
        token = data.get("token")
        if not token:
            logger.error("Registry login response did not contain 'token'")
            return None

        return token

    except Exception as e:
        logger.error("Error calling registry login endpoint: %s", e)
        return None


def register_with_registry(
    service_name: str,
    service_description: str,
    service_url: str,
) -> Optional[str]:
    global SERVICE_ID

    token = get_registry_token()
    if not token:
        logger.error("Skipping registration - could not obtain registry token")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": service_name,
        "description": service_description,
        "url": service_url,
    }

    register_url = _build_url(REGISTRY_BASE_URL, REGISTRY_REGISTER_PATH)

    try:
        resp = requests.post(register_url, json=payload, headers=headers, timeout=5)
        if resp.status_code not in (200, 201):
            logger.error(
                "Registry registration failed: %s %s",
                resp.status_code,
                resp.text,
            )
            return None

        data = resp.json() if resp.content else {}
        SERVICE_ID = data.get("UUID")

        logger.info(
            "Successfully registered with registry. Service ID: %s",
            SERVICE_ID,
        )

        return SERVICE_ID

    except Exception as e:
        logger.error("Error calling registry register endpoint: %s", e)
        return None


def deregister_from_registry() -> None:
    global SERVICE_ID, DEREGISTERED

    if DEREGISTERED:
        logger.info("Deregistration already performed; skipping.")
        return

    if not SERVICE_ID:
        logger.info("No SERVICE_ID set, skipping deregistration.")
        return

    token = get_registry_token()
    if not token:
        logger.error("Could not obtain registry token for deregistration; skipping.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    deregister_url = _build_url(REGISTRY_BASE_URL, REGISTRY_DEREGISTER_PATH)
    payload = {"id": SERVICE_ID}

    try:
        resp = requests.delete(
            deregister_url,
            headers=headers,
            json=payload,
            timeout=5,
        )

        if resp.status_code in (200, 204):
            logger.info(
                "Successfully deregistered service (ID: %s) from registry.",
                SERVICE_ID,
            )
            DEREGISTERED = True

        elif resp.status_code == 404:
            logger.info(
                "Service %s not found in registry during deregistration (404). "
                "Assuming already removed.",
                SERVICE_ID,
            )
            DEREGISTERED = True

        else:
            logger.error(
                "Registry deregistration failed: %s %s",
                resp.status_code,
                resp.text,
            )

    except Exception as e:
        logger.error("Error calling registry deregister endpoint: %s", e)


def health_response(service_name: str) -> Tuple[dict, int]:
    return {"status": "ok", "service": service_name}, 200
