from unittest.mock import MagicMock, patch

import pytest
from scrapy.utils.test import get_crawler

from scrapy_dropbox import CHUNK_SIZE, DropboxFeedStorage
from scrapy_dropbox.utils import parse_uri


@patch("scrapy_dropbox.Dropbox")
def test_dropbox_feed_storage_init(mock_dropbox):
    uri = "dropbox://myfolder/export.csv"
    settings = {"DROPBOX_API_TOKEN": "api-token"}
    crawler = get_crawler(settings_dict=settings)

    storage = DropboxFeedStorage.from_crawler(crawler, uri)

    mock_dropbox_instance = mock_dropbox.return_value
    mock_dropbox_instance.users_get_current_account.side_effect = MagicMock()

    assert storage.api_token == settings["DROPBOX_API_TOKEN"]
    assert storage.dropbox_path == "/myfolder/export.csv"
    assert mock_dropbox_instance.users_get_current_account.call_count == 1


@patch("scrapy_dropbox.DropboxFeedStorage.get_file_size")
@patch("scrapy_dropbox.DropboxFeedStorage.upload_small_file")
@patch("scrapy_dropbox.DropboxFeedStorage.upload_large_file")
@patch("scrapy_dropbox.Dropbox")
def test_dropbox_store_large_file(
    mock_dropbox, mock_upload_large_file, mock_upload_small_file, mock_get_file_size
):
    uri = "dropbox://myfolder/export.csv"
    settings = {"DROPBOX_API_TOKEN": "api-token"}
    crawler = get_crawler(settings_dict=settings)

    storage = DropboxFeedStorage.from_crawler(crawler, uri)

    file = MagicMock()
    mock_dropbox_instance = mock_dropbox.return_value
    mock_dropbox_instance.users_get_current_account.side_effect = MagicMock()

    mock_upload_large_file.return_value = MagicMock()
    mock_upload_small_file.return_value = MagicMock()
    mock_get_file_size.return_value = 10000

    storage._store_in_thread(file)

    file.seek.assert_called_once_with(0)
    assert storage.upload_small_file.call_count == 1
    assert storage.upload_large_file.call_count == 0


@patch("scrapy_dropbox.DropboxFeedStorage.get_file_size")
@patch("scrapy_dropbox.DropboxFeedStorage.upload_small_file")
@patch("scrapy_dropbox.DropboxFeedStorage.upload_large_file")
@patch("scrapy_dropbox.Dropbox")
def test_dropbox_store_small_file(
    mock_dropbox, mock_upload_large_file, mock_upload_small_file, mock_get_file_size
):
    uri = "dropbox://myfolder/export.csv"
    settings = {"DROPBOX_API_TOKEN": "api-token"}
    crawler = get_crawler(settings_dict=settings)

    storage = DropboxFeedStorage.from_crawler(crawler, uri)

    file = MagicMock()
    mock_dropbox_instance = mock_dropbox.return_value
    mock_dropbox_instance.users_get_current_account.side_effect = MagicMock()

    mock_upload_large_file.return_value = MagicMock()
    mock_upload_small_file.return_value = MagicMock()
    mock_get_file_size.return_value = 4 * CHUNK_SIZE

    storage._store_in_thread(file)

    file.seek.assert_called_once_with(0)
    assert storage.upload_small_file.call_count == 0
    assert storage.upload_large_file.call_count == 1


@pytest.mark.parametrize(
    "uri, expected_result",
    [
        ("dropbox://folder/file.txt", "/folder/file.txt"),
        ("invalid_scheme://folder/file.txt", None),
        ("dropbox://folder/file_without_extension", None),
        ("", None),
    ],
)
def test_parse_uri(uri, expected_result):
    assert parse_uri(uri) == expected_result
