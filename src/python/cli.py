#!/usr/bin/env python3
"""
WeChat Article Downloader CLI
"""

import argparse
import asyncio
import sys
import os

from .downloader import WeChatDownloader
from .exceptions import WeChatDownloaderError

def _sanitize_url(url):
    """Sanitize URL by removing query parameters for safe logging"""
    if not url:
        return url
    from urllib.parse import urlparse, urlunparse
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path, '', '', ''))


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Download WeChat official account articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s https://mp.weixin.qq.com/s/xxx
  %(prog)s --input article.html --output ./output
  %(prog)s --batch urls.txt --output-dir ./articles
  %(prog)s https://mp.weixin.qq.com/s/xxx -f json
        '''
    )

    parser.add_argument('url', nargs='?', default='', help='WeChat article URL')
    parser.add_argument('-i', '--input', dest='input', help='Input HTML file path')
    parser.add_argument('-o', '--output', dest='output', help='Output directory')
    parser.add_argument('-f', '--format', dest='format', default='md',
                        choices=['md', 'json', 'txt', 'all'], help='Output format')
    parser.add_argument('-b', '--batch', dest='batch', help='Batch download from URL list file')
    parser.add_argument('--ua', dest='ua', default='', help='Custom User-Agent')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


async def main_async():
    """Main async function"""
    args = parse_args()

    # Validate input
    if not args.url and not args.input and not args.batch:
        print('Error: Please provide a URL, input file, or batch file', file=sys.stderr)
        print('Use --help for usage information', file=sys.stderr)
        sys.exit(1)

    # Setup downloader
    downloader_options = {}
    if args.ua:
        downloader_options['user_agent'] = 'custom'
        downloader_options['custom_ua'] = args.ua
    if args.verbose:
        downloader_options['verbose'] = True

    downloader = WeChatDownloader(**downloader_options)

    try:
        # Batch download
        if args.batch:
            if not os.path.exists(args.batch):
                print(f'Error: Batch file not found: {args.batch}', file=sys.stderr)
                sys.exit(1)

            with open(args.batch, 'r', encoding='utf-8') as f:
                urls = [
                    line.strip() for line in f
                    if line.strip() and not line.strip().startswith('#')
                ]

            if not args.output:
                print('Error: --output is required for batch download', file=sys.stderr)
                sys.exit(1)

            await downloader.batch_download(
                urls,
                output_dir=args.output,
                format=args.format
            )

            print(f'\nBatch download completed. Processed {len(urls)} URL(s).')
            return

        # Download from URL
        if args.url:
            if args.verbose:
                print(f'Downloading: {args.url}')

            article = await downloader.download(args.url)

            if args.output:
                saved_files = await article.save_to_dir(args.output, {'format': args.format})
                if args.verbose:
                    print(f'Saved: {", ".join(saved_files)}')
            else:
                if args.format == 'json':
                    import json
                    print(json.dumps(article.to_json(), indent=2, ensure_ascii=False))
                elif args.format == 'txt':
                    print(article.to_text())
                else:
                    print(article.to_markdown())
            return

        # Parse from HTML file
        if args.input:
            if not os.path.exists(args.input):
                print(f'Error: Input file not found: {args.input}', file=sys.stderr)
                sys.exit(1)

            with open(args.input, 'r', encoding='utf-8') as f:
                html = f.read()

            article = await downloader.parse(html)

            if args.output:
                saved_files = await article.save_to_dir(args.output, {'format': args.format})
                if args.verbose:
                    print(f'Saved: {", ".join(saved_files)}')
            else:
                if args.format == 'json':
                    import json
                    print(json.dumps(article.to_json(), indent=2, ensure_ascii=False))
                elif args.format == 'txt':
                    print(article.to_text())
                else:
                    print(article.to_markdown())

    except WeChatDownloaderError as e:
        # Log custom exceptions with sanitized message (no URL leakage)
        e_m=str(e);s=_sanitize_url(args.url)if args.url else None;e_m=e_m.replace(args.url,s)if args.url and s else e_m;print(f'Error: {e_m}',file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        # Log unexpected exceptions
        e_m=str(e)
        if args.url:
            s=_sanitize_url(args.url)
            e_m=e_m.replace(args.url,s)
        print(f'Error: {e_m}',file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point"""
    asyncio.run(main_async())


if __name__ == '__main__':
    main()
