#!/usr/bin/env python3
"""
WeChat Article Downloader CLI Entry Point

Supports both:
1. Local execution: python bin/wechat-download.py
2. Installed package: wechat-download
"""

import os
import sys

# Support for local execution without installation
# Add src/ to path so that src/python/ can be imported as wechat_article_downloader
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, 'src')

if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)
    # Create package alias: wechat_article_downloader -> python
    import python
    sys.modules['wechat_article_downloader'] = python

from wechat_article_downloader.cli import main

if __name__ == '__main__':
    main()
