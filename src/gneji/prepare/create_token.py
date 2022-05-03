from __future__ import print_function

import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def create_token(token_path: Path, secret_path: Path, scopes: list[str]) -> None:
    """client_secret から スコープに応じて token.json を生成する。

    動作確認もその場で行う。
    """
    if not secret_path.exists():
        print(f'File Not Found: {secret_path}; secret未作成の場合はDevelopersConsoleで作成してね。', file=sys.stderr)
        return

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    if (not creds) or (not creds.valid):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with token_path.open(mode='w') as token:
            token.write(creds.to_json())

    print(f'Success! You got your token. Saved at {token_path}\n')

    print('Example: list your MyDrive files(Max: 3)')
    # 動作確認: HttpErrorなどが起こりうるが、サンプルなので例外処理はしないでおく
    service = build('drive', 'v3', credentials=creds)

    # マイドライブのファイルを10件取得してみる
    results = service.files().list(pageSize=3, fields='nextPageToken, files(id, name)').execute()
    if items := results.get('files', []):
        for item in items:
            print(item)
    else:
        print('No files found.')


def main():
    credentials_dir = Path(__file__).parents[3] / 'credentials'

    token_path = credentials_dir / 'token.json'
    secret_path = credentials_dir / 'secret.json'

    SCOPES = ['https://www.googleapis.com/auth/drive']
    create_token(token_path, secret_path, SCOPES)


if __name__ == '__main__':
    main()
