"""
Example: Download a WeChat article
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from python.downloader import WeChatDownloader


async def main():
    downloader = WeChatDownloader(
        timeout=30000,
        retry=3
    )

    # Download from URL
    url = 'https://mp.weixin.qq.com/s/xxx'
    print(f'Downloading: {url}')

    article = await downloader.download(url)

    print(f'\nTitle: {article.title}')
    print(f'Author: {article.author}')
    print(f'Content length: {len(article.content)} chars\n')

    # Save to directory
    await article.save_to_dir('./output', {'format': 'all'})
    print('Saved to ./output')


if __name__ == '__main__':
    asyncio.run(main())
