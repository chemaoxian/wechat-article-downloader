"""
Custom Exceptions for WeChat Article Downloader
"""


class WeChatDownloaderError(Exception):
    """Base exception for WeChat Downloader"""
    pass


class DownloadError(WeChatDownloaderError):
    """Exception raised when downloading fails"""
    pass


class ParseError(WeChatDownloaderError):
    """Exception raised when parsing HTML fails"""
    pass


class SSRFError(WeChatDownloaderError):
    """Exception raised when SSRF protection blocks a request"""
    pass


class ValidationError(WeChatDownloaderError):
    """Exception raised when input validation fails"""
    pass


class TimeoutError(WeChatDownloaderError):
    """Exception raised when request times out"""
    pass


class FileError(WeChatDownloaderError):
    """Exception raised when file operations fail"""
    pass
