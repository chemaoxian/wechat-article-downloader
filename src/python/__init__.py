"""
WeChat Article Downloader - Python SDK

Lightweight WeChat official account article downloader
Extract articles to Markdown/JSON without browser
"""

from .article import Article
from .parser import WeChatParser
from .downloader import WeChatDownloader
from .exceptions import (
    WeChatDownloaderError,
    DownloadError,
    ParseError,
    SSRFError,
    ValidationError,
    TimeoutError,
    FileError
)

__all__ = [
    'Article',
    'WeChatParser',
    'WeChatDownloader',
    'WeChatDownloaderError',
    'DownloadError',
    'ParseError',
    'SSRFError',
    'ValidationError',
    'TimeoutError',
    'FileError'
]
__version__ = '1.0.0'
__author__ = 'Your Name'
