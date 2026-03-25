import json
import sys
from typing import Any
from urllib import error, request


BASE_URL = "https://gratefully-nonannihilable-clifford.ngrok-free.dev"
WEBHOOK_ENDPOINT = "/webhook/whatsapp"


def get_sample_whatsapp_payload(message_text: str) -> dict[str, Any]:
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15550000000",
                                "phone_number_id": "123456789",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Test User"},
                                    "wa_id": "919999999999",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "919999999999",
                                    "id": "wamid.HBgLOTExOTk5OTk5OTk5VAs...",
                                    "timestamp": "1710500000",
                                    "text": {"body": message_text},
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }


def build_webhook_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}{WEBHOOK_ENDPOINT}"


def post_payload(url: str, payload: dict[str, Any]) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req) as response:
            return response.status, response.read().decode("utf-8")
    except error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


if __name__ == "__main__":
    url = build_webhook_url(BASE_URL)
    test_messages = [
        "Hi",
        "Veg restaurants in Baner",
        "What is famous in FC Road",
        "Birthday suggestions",
    ]

    print("--- Starting Public Webhook Verification ---")
    print(f"Target URL: {url}")

    for msg in test_messages:
        print(f"\nSending: '{msg}'")
        payload = get_sample_whatsapp_payload(msg)

        try:
            status_code, response_text = post_payload(url, payload)
            if status_code == 200:
                try:
                    parsed = json.loads(response_text)
                    print(f"Reply: {parsed.get('reply', parsed)}")
                except json.JSONDecodeError:
                    print(f"Success 200: {response_text}")
            else:
                print(f"Error {status_code}: {response_text}")
        except Exception as exc:
            print(f"Request failed: {exc}")
            sys.exit(1)
