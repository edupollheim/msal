import requests
import base64
import os
from dotenv import load_dotenv
from Autenticação.auth import Auth

load_dotenv()


class OneDriveUploaderBase64:
    def __init__(self, base64_data, user_email, filename):
        """
        Inicializa a classe com os dados em base64, o email do usuário e o nome do arquivo a ser carregado no OneDrive.

        Args:
            base64_data (str): Dados do arquivo em formato base64.
            user_email (str): E-mail do usuário para o qual o upload será realizado.
            filename (str): Nome do arquivo a ser carregado no OneDrive.
        """
        self.base64_data = base64_data
        self.user_email = user_email
        self.filename = filename
        self.auth = Auth(
            CLIENT_ID=os.getenv("MICROSOFT_CLIENT_ID"),
            CLIENT_SECRET=os.getenv("MICROSOFT_CLIENT_SECRET"),
            TENANT_ID=os.getenv("MICROSOFT_TENANT_ID"),
            SCOPE=[os.getenv("MICROSOFT_SCOPE")]
        )
        self.token = self.auth.get_access_token()

    def decode_base64(self):
        """
        Decodifica os dados em base64 para formato binário (bytes).

        Returns:
            bytes: Dados decodificados em formato binário.
        """
        return base64.b64decode(self.base64_data)

    def upload_file(self, decoded_data):
        """
        Envia os dados binários para o OneDrive.

        Args:
            decoded_data (bytes): Dados do arquivo em formato binário.

        Returns:
            requests.Response: Resposta da requisição de upload.
        """
        url = f"https://graph.microsoft.com/v1.0/users/{self.user_email}/drive/root:/{self.filename}:/content"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/octet-stream"
        }

        response = requests.put(url, headers=headers, data=decoded_data)
        return response

    def handle_upload(self):
        """
        Orquestra o processo de upload do arquivo para o OneDrive.

        Realiza a decodificação dos dados base64 e envia o arquivo para o OneDrive.
        Exibe o resultado do upload com base no status da resposta.

        Returns:
            bool: True se o upload foi bem-sucedido, raise Exception caso contrário.
        """
        try:
            decoded_data = self.decode_base64()
            response = self.upload_file(decoded_data)

            if response.status_code == 201:
                return True
            else:
                raise Exception(f"Erro ao carregar arquivo: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception("Erro ao processar upload:", e)
