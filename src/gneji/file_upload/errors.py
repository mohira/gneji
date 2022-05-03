class FileUploadAPIError(Exception):
    pass


class AlreadyExistsError(FileUploadAPIError):
    pass


class NotFoundError(FileUploadAPIError):
    pass


class MultipleSameNameFileExistError(FileUploadAPIError):
    pass


class MultipleFolderError(FileUploadAPIError):
    pass
