import dropbox
import typing

from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage


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
            res = dbx.files_upload(file.read(), path, mute=True)
            print(f'Dropbox upload response: {res}')
        except dropbox.exceptions.ApiError as err:
            print('Dropbox API error', err)
            return None
