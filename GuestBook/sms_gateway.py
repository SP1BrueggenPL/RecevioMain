import requests
from swagger_client import SecurityApi, TokenSigninPayload, ApiClient, Configuration
from mysite import settings

class SMSGateway:
    def __init__(self):
        self.api_base = "https://10.30.70.20/api"
        self.verify_ssl = False  # ⚠️ tylko testy

        # ✅ LOGIN DO API I POBRANIE TOKENA
        configuration = Configuration()
        configuration.host = self.api_base
        configuration.verify_ssl = self.verify_ssl
        api_client = ApiClient(configuration)

        security_api = SecurityApi(api_client)
        login_payload = TokenSigninPayload(
            username=settings.SMS_GATEWAY_USER,
            password=settings.SMS_GATEWAY_PASS,
        )
        token_response = security_api.signin_post(login_payload)
        print("[DEBUG] Token response:", token_response.to_dict())

        self.token = getattr(token_response, "jwt", None)
        if not self.token:
            raise ValueError(f"Brak tokena w odpowiedzi: {token_response.to_dict()}")

    def send_sms(self, to: str, message: str):
        url = f"{self.api_base}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": message,
            "recipients": [{"to": to, "target": "number"}],
            "type": "default"  # ✅ poprawny typ wg dokumentacji
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                verify=self.verify_ssl
            )
            if response.status_code == 200:
                return {"status": "success", "response": response.json()}
            else:
                return {"status": "error", "error": response.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}
