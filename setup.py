from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="wechat-article-downloader",
    version="1.0.0",
    author="chemaoxian",
    author_email="443224841@qq.com",
    description="Lightweight WeChat official account article downloader - extract articles to Markdown/JSON without browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chemaoxian/wechat-article-downloader",
    project_urls={
        "Bug Tracker": "https://github.com/chemaoxian/wechat-article-downloader/issues",
        "Documentation": "https://github.com/chemaoxian/wechat-article-downloader#readme",
    },
    package_dir={"wechat_article_downloader": "src/python"},
    packages=["wechat_article_downloader"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "wechat-download=wechat_article_downloader.cli:main",
            "wechat-article-downloader=wechat_article_downloader.cli:main",
        ],
    },
    keywords=[
        "wechat", "weixin", "article", "downloader", "scraper",
        "markdown", "cli", "crawler", "微信公众号"
    ],
)
