# gneji - Google Drive API Wrapper for Python

## Pronunciation【dʒɪːnedʒ】
"neji" is a Screw in Japaneses.

Google Drive -> Drive -> Driver -> Screw -> ネジ

You use a screw**driver** to turn a screw, right?

## Install

```
pip install -i https://test.pypi.org/simple/ gneji
```

## Usage

### 1. Create a Google Cloud Platform project and Create your client secret
A Google Cloud Platform project with the API enabled.

To create a project and enable an API, refer to [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project).

### 2. Create your token

```python
from pathlib import Path

from gneji.prepare.create_token import create_token


def main():
    token_path = Path('YOUR_TOKEN_PATH')  # If it does not exist, create a new one. 
    secret_path = Path('YOUR_SECRET_PATH')

    scopes = ['https://www.googleapis.com/auth/drive']

    create_token(token_path, secret_path, scopes)


if __name__ == '__main__':
    main()

```

If successful, the following message will be displayed.

```
Success! You got your token. Saved at /Users/mohira/src/github.com/mohira/gneji/credentials/token.json

Example: list your MyDrive files(Max: 3)
{'id': 'ABCDEFGHIJKELMNOPQRSTUVWXYZ12345A', 'name': 'a.txt'}
{'id': 'ABCDEFGHIJKELMNOPQRSTUVWXYZ12345B', 'name': 'b.txt'}
{'id': 'ABCDEFGHIJKELMNOPQRSTUVWXYZ12345C', 'name': 'c.txt'}
```

### 3. Call example - Upload a new file

```python
import sys
from pathlib import Path

from gneji.file_upload.api import FileUploadAPI
from gneji.file_upload.errors import FileUploadAPIError
from gneji.file_upload.json_representation import FileMetadata
from gneji.prepare.get_service import get_service
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def main():
    # set up API
    drive_service = get_service(token_path=Path('YOUR_TOKEN_PATH'), scopes=['https://www.googleapis.com/auth/drive'])
    api = FileUploadAPI(drive_service)

    # The file you want to upload
    media = MediaFileUpload(filename=Path('tmp.txt'), mimetype='plain/text')
    metadata: FileMetadata = {'name': 'tmp.txt', 'parents': ['DRIVE_FOLDER_ID']}

    # Upload new file
    try:
        file = api.upload_newfile(media, metadata)  # Create a new file in the folder
        print(file)
    except FileUploadAPIError as e:
        print(e, file=sys.stderr)
        exit(1)
    except HttpError as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()

```


