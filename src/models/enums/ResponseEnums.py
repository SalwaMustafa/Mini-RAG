from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File_validate_successfuly"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "File uploaded success"
    FILE_UPLOADED_FAILED = "File uploaded failed"
    PROCESSING_FAILED = "Processing_failed"
    PROCESSING_SUCCESS = "Processing_success"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
