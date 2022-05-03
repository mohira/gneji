import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from src.gneji.file_upload.api import FileUploadAPI
from src.gneji.file_upload.errors import FileUploadAPIError
from src.gneji.file_upload.json_representation import FileMetadata
from src.gneji.prepare.get_service import get_service


def main():
    load_dotenv()

    credentials_dir = Path(__file__).parents[3] / 'credentials'

    token_path = credentials_dir / 'token.json'

    SCOPES = ['https://www.googleapis.com/auth/drive']

    drive_service = get_service(token_path, SCOPES)
    file_upload_api = FileUploadAPI(drive_service)

    metadata: FileMetadata = {
        'name': 'tmp.txt',
        'parents': [os.environ['TEST_DRIVE_FOLDER_ID']]
    }

    target_local_file = Path('tmp.txt')
    if not target_local_file.exists():
        print(f'Not Found: {target_local_file}', file=sys.stderr)
        exit(1)

    media = MediaFileUpload(target_local_file, mimetype='plain/text')

    try:
        files = file_upload_api.upload_newfile(media, metadata)  # 新規ファイル作成
        files = file_upload_api.overwrite(media, metadata)  # ファイルを上書き
        print(files)
    except FileUploadAPIError as e:
        print(e, file=sys.stderr)
        exit(1)
    except HttpError as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
