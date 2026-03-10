"""
Tests for WeChat Article Downloader
"""

import pytest
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from python.article import Article
from python.parser import WeChatParser
from python.downloader import WeChatDownloader
from python.exceptions import WeChatDownloaderError, DownloadError, ParseError, SSRFError, ValidationError

# Sample HTML for testing
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Article</title>
    <script>var msg_title = 'Test Article Title';</script>
    <script>var msg_source_url = 'https://mp.weixin.qq.com/s/test';</script>
</head>
<body>
    <div id="js_content">
        <p>This is a test paragraph.</p>
        <p>Another paragraph with <strong>bold</strong> text.</p>
        <h3>Section Title</h3>
        <p>More content here.</p>
    </div>
</body>
</html>
"""


class TestArticle:
    """Tests for Article class"""

    def test_create_article(self):
        article = Article(
            title='Test Title',
            author='Test Author',
            content='Test content'
        )
        assert article.title == 'Test Title'
        assert article.author == 'Test Author'
        assert article.content == 'Test content'

    def test_to_markdown(self):
        article = Article(title='Test Title', content='Test content')
        md = article.to_markdown()
        assert '# Test Title' in md
        assert 'Test content' in md

    def test_to_json(self):
        article = Article(title='Test Title', content='Test content')
        json_data = article.to_json()
        assert json_data['title'] == 'Test Title'
        assert json_data['content'] == 'Test content'

    def test_to_text(self):
        article = Article(content='Line 1\n\n\nLine 2')
        text = article.to_text()
        assert 'Line 1\n\nLine 2' in text


class TestWeChatParser:
    """Tests for WeChatParser class"""

    def test_parse_html(self):
        parser = WeChatParser()
        article = parser.parse(SAMPLE_HTML, 'https://mp.weixin.qq.com/s/test')
        assert article.title == 'Test Article Title'
        assert 'This is a test paragraph' in article.content

    def test_decode_entities(self):
        parser = WeChatParser()
        text = parser.decode_html_entities('&ldquo;Hello&rdquo; &amp; World')
        assert text == '"Hello" & World'


class TestWeChatDownloader:
    """Tests for WeChatDownloader class"""

    def test_user_agent(self):
        downloader = WeChatDownloader()
        ua = downloader.get_user_agent()
        assert 'Mobile' in ua

    @pytest.mark.asyncio
    async def test_parse_html(self):
        downloader = WeChatDownloader()
        article = await downloader.parse(SAMPLE_HTML, 'https://mp.weixin.qq.com/s/test')
        assert article.title
        assert article.content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
