import logging
import os

from dropbox import Dropbox, files
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage

from .utils import parse_uri

logger = logging.getLogger(__name__)
CHUNK_SIZE = 4 * 1024 * 1024


class DropboxFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, api_token, *, feed_options):
        if feed_options is None:
            feed_options = {}

        if feed_options and feed_options.get("overwrite", True) is False:
            raise NotConfigured(
                "This feed exporter does not support append operation, so `overwrite` cannot be set to `False`."
                "Default is `True`, so files will always be overwritten"
            )

        dropbox_path = parse_uri(uri)
        if not dropbox_path:
            raise NotConfigured(
                "Please enter correct path with the format: "
                "'dropbox://folder_name/file_name.extension'"
            )
        self.dropbox_path = dropbox_path
        self.api_token = api_token

        self.dropbox_client = Dropbox(self.api_token)

        # validate credentials
        try:
            self.dropbox_client.users_get_current_account()
        except Exception as e:
            logger.exception(e)
            raise NotConfigured("Please provide valid credentials")

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return cls(
            uri,
            crawler.settings["DROPBOX_API_TOKEN"],
            feed_options=feed_options,
        )

    def get_file_size(self, file):
        return os.stat(file.name).st_size

    def upload_small_file(self, file):
        res = self.dropbox_client.files_upload(
            file.read(), self.dropbox_path, mute=True, mode=WriteMode("overwrite")
        )
        print(f"Dropbox small file upload response: {res}")

    def upload_large_file(self, file):
        res = None
        file_size = self.get_file_size(file)
        upload_session_start_result = self.dropbox_client.files_upload_session_start(
            file.read(CHUNK_SIZE)
        )
        cursor = files.UploadSessionCursor(
            session_id=upload_session_start_result.session_id, offset=file.tell()
        )
        commit = files.CommitInfo(path=self.dropbox_path, mode=WriteMode("overwrite"))
        while file.tell() < file_size:
            cursor.offset = file.tell()
            if (file_size - file.tell()) <= CHUNK_SIZE:
                res = self.dropbox_client.files_upload_session_finish(
                    file.read(CHUNK_SIZE), cursor, commit
                )

            else:
                self.dropbox_client.files_upload_session_append_v2(
                    file.read(CHUNK_SIZE), cursor
                )
        logger.info(f"Dropbox large file upload response: {res}")

    def _store_in_thread(self, file):
        """Upload a file.
        Return the request response, or None in case of error.
        """
        file.seek(0)
        try:
            file_size = self.get_file_size(file)
            if file_size <= CHUNK_SIZE:
                self.upload_small_file(file)
            else:
                self.upload_large_file(file)
        except ApiError as err:
            logger.error(f"Dropbox API error: {err}")
            return None
