from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Файл с ключом сервисного аккаунта
SERVICE_ACCOUNT_FILE = ''   # мой json файл
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

# ID папки в моем Google Диске, куда будут сохраняться копии
TARGET_FOLDER_ID = '' # ID моей папки в гугл диске, куда сохраняется док

#  текст для документа
DEFAULT_DOC_BODY = """
FRONTEND - Raiymbek Baktybayev 😗

Задачи:

Ревью:

Встречи:

Другое:



FRONTEND - tlek suyerbassov 😎


FRONTEND - altair zhanseitov 🥷🏿


ANDROID - Daniyar Slamkul 😮


ANDROID - sabit mussabek 🌴


IOS - sultan seidalin 🚙


QA - Oleg Mashchenko 🦝 

Таски:

Не таски 👍


QA - Mariya Kadyrova 🎒

Таски:

Не таски 👍

СП


QA - Alina Lutfulla-Khodzhayeva 🦋

Таски:

Не таски 👍

СП
"""

def get_week_range_str():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    return f"{monday.strftime('%d/%m/%Y')} - {friday.strftime('%d/%m/%Y')}"

def create_google_doc():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    week_str = get_week_range_str()
    title = f"Демо {week_str}"

    # Шаг 1: создать документ(сервис акк)
    file_metadata = {
        'name': title,
        'mimeType': 'application/vnd.google-apps.document'
    }
    doc = drive_service.files().create(body=file_metadata, fields='id').execute()
    document_id = doc.get('id')

    # Шаг 2: добавить текст в документ
    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={
            'requests': [{
                'insertText': {
                    'location': {'index': 1},
                    'text': DEFAULT_DOC_BODY
                }
            }]
        }
    ).execute()

    # Шаг 3: сделать копию в целевой папке (в моем аккаунте)
    copied = drive_service.files().copy(
        fileId=document_id,
        body={
            'name': title,
            'parents': [TARGET_FOLDER_ID]
        },
        fields='id, webViewLink'
    ).execute()

    # Шаг 4: удалить оригинал с дефолтного акка гугла
    drive_service.files().delete(fileId=document_id).execute()

    return copied['webViewLink']
