# Dropbox Exporter for Scrapy
[Scrapy feed export storage backend](https://doc.scrapy.org/en/latest/topics/feed-exports.html#storage-backends) for Dropbox.

## Requirements
-  Python 3.8+

## Installation
```bash
pip install git+https://github.com/scrapy-plugins/scrapy-feedexporter-dropbox
```

## Usage
* Add this storage backend to the [FEED_STORAGES](https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES) Scrapy setting. For example:
    ```python
    # settings.py
    FEED_STORAGES = {'dropbox': 'scrapy_dropbox.DropboxFeedStorage'}
    ```
* Configure [authentication](https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/) to generate access token and use it like following:
  
  For example,
  ```python
  DROPBOX_API_TOKEN = 'your generated access token here'
    ```

* Configure in the [FEEDS](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds) Scrapy setting the Dropbox URI where the feed needs to be exported.

    ```python
    FEEDS = {
        "dropbox://<folder_name>/<file_name.extension>": {
            "format": "json"
        }
    }
    ```
  
## Feed Options
- This exporter does not support setting `overwrite` [feed option](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-options) to `False` [(no support by dropbox for append operation)](https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/How-to-append-to-existing-file/td-p/271603)
  - If it's set to `False`, a warning will be logged.
  - Default is `True`, so if the file already exists, it will be overwritten
