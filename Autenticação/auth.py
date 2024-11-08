import msal


class Auth:
    def __init__(self, CLIENT_ID, CLIENT_SECRET, TENANT_ID, SCOPE):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.TENANT_ID = TENANT_ID
        self.SCOPE = SCOPE

    def _app(self):
        CLIENT_ID = self.CLIENT_ID
        CLIENT_SECRET = self.CLIENT_SECRET
        AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"

        # Inicializando o cliente MSAL
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
        return app

    def get_access_token(self):
        result = self._app().acquire_token_silent(self.SCOPE, account=None)
        if not result:
            result = self._app().acquire_token_for_client(scopes=self.SCOPE)
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Falha ao obter o token de acesso:", result.get("error_description"))
