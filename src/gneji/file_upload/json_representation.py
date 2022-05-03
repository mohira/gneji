from typing import TypedDict


class FileMetadata(TypedDict):
    """https://developers.google.com/drive/api/v3/reference/files/create#parametersを参考にして"""
    name: str  # アップロード時のファイル名
    parents: list[str]  # 未指定の場合はMyDrive / list型だけど要素数を複数指定した場合の挙動はよくわかってない(とりあえず1つでおk)


class File(TypedDict):
    """https://developers.google.com/drive/api/v3/reference/files#resource  パラメータ多すぎ"""
    kind: str
    id: str
    name: str
    mimeType: str


class FileListResponse(TypedDict):
    """https://developers.google.com/drive/api/v3/reference/files/list"""
    kind: str
    nextPageToken: str
    incompleteSearch: bool
    files: list[File]
