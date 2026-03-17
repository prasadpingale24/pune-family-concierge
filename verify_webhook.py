import json

def get_sample_whatsapp_payload(message_text: str):
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
                                "phone_number_id": "123456789"
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Test User"},
                                    "wa_id": "919999999999"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "919999999999",
                                    "id": "wamid.HBgLOTExOTk5OTk5OTk5VAs...",
                                    "timestamp": "1710500000",
                                    "text": {"body": message_text},
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    import requests
    import sys
    
    url = "http://localhost:8000/webhook/whatsapp"
    test_messages = [
        "Hi",
        "Veg restaurants in Baner",
        "What is famous in FC Road",
        "Birthday suggestions"
    ]
    
    print("--- Starting Webhook Verification ---")
    for msg in test_messages:
        print(f"\nSending: '{msg}'")
        payload = get_sample_whatsapp_payload(msg)
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Reply: {response.json()['reply']}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Make sure the FastAPI server is running (npm run dev or uvicorn app.main:app)")
            sys.exit(1)
