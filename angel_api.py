import pyotp


class AngelSession:

    def __init__(self, api_key, client_code, password, totp_secret):
        self.api_key = api_key
        self.client_code = client_code
        self.password = password
        self.totp_secret = totp_secret

    def login(self):
        otp = pyotp.TOTP(self.totp_secret).now()
        print(f"🔐 Logging in with OTP: {otp}")

    def place_order(self, signal):
        print(f"✅ Placing order: {signal}")
