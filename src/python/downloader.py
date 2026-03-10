"""
Downloader Module - Download WeChat article HTML
"""

import asyncio
import aiohttp
import socket
from urllib.parse import urlparse
from .parser import WeChatParser
from .article import Article
from .exceptions import (
    WeChatDownloaderError,
    DownloadError,
    TimeoutError,
    SSRFError,
    ValidationError
)


class WeChatDownloader:
    """Downloader for WeChat official account articles"""

    def __init__(
        self,
        timeout: int = 30000,
        retry: int = 3,
        user_agent: str = 'mobile',
        custom_ua: str = ''
    ):
        """
        Initialize downloader

        Args:
            timeout: Request timeout in milliseconds
            retry: Number of retries
            user_agent: User-Agent type ('mobile', 'desktop', 'custom')
            custom_ua: Custom User-Agent string
        """
        self.timeout = timeout
        self.retry = retry
        self.user_agent_type = user_agent
        self.custom_ua = custom_ua
        self.verbose = False

        self.user_agents = {
            'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0',
            'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def get_user_agent(self) -> str:
        """Get User-Agent string"""
        if self.user_agent_type == 'custom' and self.custom_ua:
            return self.custom_ua
        return self.user_agents.get(self.user_agent_type, self.user_agents['mobile'])

    def _is_private_ip(self, hostname: str) -> bool:
        """
        Check if hostname resolves to a private IP address

        Args:
            hostname: Hostname to check

        Returns:
            True if private IP, False otherwise
        """
        # Check for localhost aliases
        if hostname.lower() in ('localhost', 'internal', 'metadata', 'metadata.google.internal'):
            return True

        # Check for IPv6 loopback
        if hostname in ('::1', '::', 'fe80::1'):
            return True

        # Try to resolve hostname and check if it's a private IP
        try:
            # Get all IP addresses for the hostname
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
            for _, _, _, _, sockaddr in addr_info:
                ip = sockaddr[0]
                # Check for private IPv4 ranges
                if (ip.startswith('10.') or
                    ip.startswith('192.168.') or
                    ip.startswith('172.16.') or ip.startswith('172.17.') or
                    ip.startswith('172.18.') or ip.startswith('172.19.') or
                    ip.startswith('172.20.') or ip.startswith('172.21.') or
                    ip.startswith('172.22.') or ip.startswith('172.23.') or
                    ip.startswith('172.24.') or ip.startswith('172.25.') or
                    ip.startswith('172.26.') or ip.startswith('172.27.') or
                    ip.startswith('172.28.') or ip.startswith('172.29.') or
                    ip.startswith('172.30.') or ip.startswith('172.31.') or
                    ip.startswith('127.') or
                    ip.startswith('169.254.') or
                    ip.startswith('0.') or
                    ip.startswith('1.')):
                    return True
        except socket.gaierror:
            # If hostname can't be resolved, we'll let the request fail naturally
            pass

        return False

    def _validate_url(self, url: str) -> None:
        """
        Validate URL for security

        Args:
            url: URL to validate

        Raises:
            ValidationError: If URL is invalid or insecure
            SSRFError: If URL points to private IP
        """
        if not url or not isinstance(url, str):
            raise ValidationError('Invalid URL: URL must be a non-empty string')

        parsed = urlparse(url)

        # Check protocol
        if parsed.scheme not in ('http', 'https'):
            raise ValidationError(f'Invalid protocol: Only http and https are allowed. Got: {parsed.scheme}')

        # Check for private IP addresses
        if self._is_private_ip(parsed.hostname):
            raise SSRFError('Access to private IP addresses is not allowed')

    async def request(self, url: str, retry_count: int = 0) -> str:
        """
        Make HTTP request

        Args:
            url: URL to request
            retry_count: Current retry count

        Returns:
            Response body
        """
        headers = {
            'User-Agent': self.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }

        timeout = aiohttp.ClientTimeout(total=self.timeout / 1000)

        try:
            async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                async with session.get(url, allow_redirects=True) as response:
                    if response.status != 200:
                        raise DownloadError(f'Request failed with status code {response.status}')
                    return await response.text(encoding='utf-8')
        except asyncio.TimeoutError:
            if retry_count < self.retry:
                delay = pow(2, retry_count) * 1000
                await asyncio.sleep(delay / 1000)
                return await self.request(url, retry_count + 1)
            raise TimeoutError(f'Request timeout after {self.timeout}ms')
        except WeChatDownloaderError:
            raise
        except Exception as e:
            if retry_count < self.retry:
                delay = pow(2, retry_count) * 1000
                await asyncio.sleep(delay / 1000)
                return await self.request(url, retry_count + 1)
            raise DownloadError(f'Failed to download: {str(e)}')

    async def download(self, url: str) -> Article:
        """
        Download article from URL

        Args:
            url: WeChat article URL

        Returns:
            Parsed article

        Raises:
            ValueError: If URL is invalid or insecure
        """
        # Validate URL for security
        self._validate_url(url)

        html = await self.request(url)
        parser = WeChatParser()
        return parser.parse(html, url)

    async def parse(self, html: str, source_url: str = '') -> Article:
        """
        Parse article from HTML string

        Args:
            html: HTML content
            source_url: Source URL (optional)

        Returns:
            Parsed article
        """
        parser = WeChatParser()
        return parser.parse(html, source_url)

    async def batch_download(
        self,
        urls: list,
        output_dir: str = '',
        format: str = 'md',
        delay: int = 0
    ) -> list:
        """
        Batch download articles from URLs

        Args:
            urls: Array of URLs
            output_dir: Output directory
            format: Output format ('md', 'json', 'all')
            delay: Delay between requests in milliseconds

        Returns:
            Array of downloaded articles
        """
        results = []
        errors = []

        for i, url in enumerate(urls):
            try:
                if self.verbose:
                    print(f'[{i + 1}/{len(urls)}] Downloading: {url[:50]}...')
                article = await self.download(url)

                if output_dir:
                    saved_files = await article.save_to_dir(output_dir, {'format': format})
                    print(f'  Saved: {", ".join(saved_files)}')

                results.append(article)

                if delay > 0 and i < len(urls) - 1:
                    await asyncio.sleep(delay / 1000)
            except Exception as e:
                print(f'  Error: {str(e)}')
                errors.append({'url': url, 'error': str(e)})

        if errors:
            print(f'\nFailed to download {len(errors)} article(s):')
            for err in errors:
                print(f'  - {err["url"]}: {err["error"]}')

        return results
