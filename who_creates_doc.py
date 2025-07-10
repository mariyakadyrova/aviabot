from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = ''  # имя моего JSON-файла

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/documents']
)

print(f"Документ будет создан от имени: {creds.service_account_email}")
