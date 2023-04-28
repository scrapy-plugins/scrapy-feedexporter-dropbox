import dropbox
import typing
import os

from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage
from dropbox.files import WriteMode


class DropboxFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):
        self.uri = uri

    def open(self, spider):
        self.api_token  = spider.crawler.settings['DROPBOX_API_TOKEN']
        return super().open(spider)

    def _store_in_thread(self, file):
        """Upload a file.
        Return the request response, or None in case of error.
        """
        file.seek(0)
        try:
            dbx = dropbox.Dropbox(self.api_token)
            path = self.uri.replace('dbox:/', '')
            res = None
            CHUNK_SIZE = 4 * 1024 * 1024
            file_size = os.stat(file.name).st_size
            if file_size <= CHUNK_SIZE:
                res = dbx.files_upload(file.read(), path, mute=True, mode=WriteMode('overwrite'))
            else:
                upload_session_start_result = dbx.files_upload_session_start(file.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id, offset=file.tell())
                commit = dropbox.files.CommitInfo(path=path)
                while file.tell() < file_size:
                    cursor.offset = file.tell()
                    if ((file_size - file.tell()) <= CHUNK_SIZE):
                        res = dbx.files_upload_session_finish(file.read(CHUNK_SIZE), cursor, commit)
                    else:
                        dbx.files_upload_session_append_v2(file.read(CHUNK_SIZE), cursor)
            print(f'Dropbox upload response: {res}')
        except dropbox.exceptions.ApiError as err:
            print('Dropbox API error', err)
            return None
