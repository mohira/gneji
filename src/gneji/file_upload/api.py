from dataclasses import dataclass
from typing import Optional

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

from .errors import AlreadyExistsError, MultipleFolderError, MultipleSameNameFileExistError, NotFoundError
from .json_representation import File, FileListResponse, FileMetadata


@dataclass(frozen=True)
class FileUploadAPI:
    """https://developers.google.com/drive/api/v3/reference/files#methods

    # MEMO: APIなら同名ファイルのアップロードが可能(IDで区別しているから)。 WebUIだと同名アップロードはできない。WebUIだと`foo (1)`みたいなファイル名になるよね
    # MyDriveにuploadは不可能という仕様にした。実装が楽だから(フラグが不要)。MyDriveの肥大化も防げる。
    """
    drive_service: Resource

    def upload_newfile(self, media: MediaFileUpload, metadata: FileMetadata) -> File:
        """新規ファイルを指定したフォルダにアップロードする"""
        self._check_parent_folder(metadata)

        already_exists, _ = self._already_exists(metadata)

        if already_exists:
            filename, folder_id = metadata['name'], metadata['parents'][0]
            raise AlreadyExistsError(
                f'Already exists: {filename=}, {folder_id=}, url={self._folder_url(folder_id)}')
        else:
            return self._create(metadata, media)

    def overwrite(self, media: MediaFileUpload, metadata: FileMetadata) -> File:
        """指定したフォルダの既存ファイルを上書きする。バージョンが更新される"""
        self._check_parent_folder(metadata)

        already_exists, file_id = self._already_exists(metadata)

        if already_exists:
            return self._update(media, file_id)
        else:
            # 存在しない場合にUploadにすると気づけない可能性が高いのでエラーにしている
            filename, folder_id = metadata['name'], metadata['parents'][0]
            raise NotFoundError(
                f'Not exists in the drive: {filename=}, {folder_id=}, url={self._folder_url(folder_id)}')

    def _already_exists(self, metadata: FileMetadata) -> tuple[bool, Optional[str]]:
        filename, folder_id = metadata['name'], metadata['parents'][0]

        query = f"name = '{filename}' and '{folder_id}' in parents and trashed=false"

        response: FileListResponse = self._search_files(query)
        already_exists = len(response['files']) != 0

        if already_exists:
            if n := len(response['files']) != 1:
                raise MultipleSameNameFileExistError(
                    f'同名ファイルは複数あると上書きを間違えるかダメ。{filename}は{n}ファイルあった。url={self._folder_url(folder_id)}')
            return True, response['files'][0]['id']
        else:
            return False, None

    def _search_files(self, query):
        """https://developers.google.com/drive/api/guides/search-files"""
        return self.drive_service.files().list(q=query).execute()

    def _update(self, media: MediaFileUpload, file_id: str):
        """https://developers.google.com/drive/api/v3/reference/files/update"""
        return self.drive_service.files().update(fileId=file_id, media_body=media).execute()

    def _create(self, metadata: FileMetadata, media: MediaFileUpload):
        """https://developers.google.com/drive/api/v3/reference/files/create"""
        return self.drive_service.files().create(body=metadata, media_body=media).execute()

    @staticmethod
    def _check_parent_folder(metadata: FileMetadata):
        if len(metadata['parents']) != 1:
            raise MultipleFolderError('folder_idは1つだけ指定するようにしてね。ということは、MyDriveにUploadもできない仕様です。')

    @staticmethod
    def _folder_url(folder_id: str) -> str:
        return f'https://drive.google.com/drive/folders/{folder_id}'
