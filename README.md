# scrapy-dropbox
Dropbox feed exporter is a Scrapy Feed Exporter that allows you to export scrapy items to a dropbox folder.

## Usage

Import the package and add to your Scrapy settings:

```
DROPBOX_API_TOKEN = "DROPBOX_APP_TOKEN"

FEED_STORAGES = {
    'dbox': 'scrapy_dropbox.DropboxFeedStorage'
}

FEEDS = {
    (
        "dbox://dropbox/folder/to/save/%(name)s_%(time)s.csv"
    ): {
        "format": "csv",
        "encoding": "utf8",
    }
}
```

[See here](https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/) how to generate a Dropbox access token.



