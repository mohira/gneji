from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class CredentialError(Exception):
    pass


def get_service(token_path: Path, scopes: list[str]):
    """
    事故を防ぐために、あえてリフレッシュしないようにしている。なので期限切れるたびに毎回トークン作成してね
    """
    if not token_path.exists():
        raise FileNotFoundError(f'token.json見つからないよ。探すか作るかして！: {token_path}')

    creds: Credentials = Credentials.from_authorized_user_file(str(token_path), scopes)

    if not creds.valid:
        raise CredentialError(f'無効なクレデンシャル: リフレッシュするなり再生成するなり頼むよ')

    return build('drive', 'v3', credentials=creds)
