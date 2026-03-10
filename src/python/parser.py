"""
Parser Module - Parse WeChat article HTML
"""

import re
from datetime import datetime
from .article import Article


class WeChatParser:
    """Parser for WeChat official account articles"""

    def __init__(self):
        self.html_entities = {
            '&nbsp;': ' ',
            '&ldquo;': '"',
            '&rdquo;': '"',
            '&lsquo;': "'",
            '&rsquo;': "'",
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&mdash;': '—',
            '&hellip;': '…'
        }

    def decode_html_entities(self, text: str) -> str:
        """Decode HTML entities"""
        if not text:
            return ''

        def replace_entity(match):
            entity = match.group(0)
            return self.html_entities.get(entity, entity)

        return re.sub(r'&[^;]+;', replace_entity, text)

    def extract_metadata(self, html: str) -> dict:
        """Extract metadata from HTML"""
        metadata = {
            'title': '',
            'author': '',
            'source_url': '',
            'published_date': '',
            'summary': ''
        }

        # Extract title
        title_match = re.search(r'var\s+msg_title\s*=\s*[\'"]([^\'"]*)[\'"]', html)
        if title_match:
            metadata['title'] = re.sub(r'\.html\([^)]*\)', '', title_match.group(1)).strip()

        # Extract author
        author_match = re.search(r'rich_media_meta_nickname[^>]*>([^<]+)<', html)
        if author_match:
            metadata['author'] = author_match.group(1).strip()

        if not metadata['author']:
            alt_author_match = re.search(r'var\s+msg_author_name\s*=\s*[\'"]([^\'"]*)[\'"]', html)
            if alt_author_match:
                metadata['author'] = alt_author_match.group(1).strip()

        # Extract source URL
        source_url_match = re.search(r'var\s+msg_source_url\s*=\s*[\'"]([^\'"]*)[\'"]', html)
        if source_url_match:
            metadata['source_url'] = source_url_match.group(1)

        # Extract published date
        date_match = re.search(r'var\s+msg_publish_time\s*=\s*[\'"]?(\d+)[\'"]?', html)
        if date_match:
            timestamp = int(date_match.group(1))
            metadata['published_date'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

        # Extract summary
        summary_match = re.search(r'var\s+msg_desc\s*=\s*[\'"]([^\'"]*)[\'"]', html)
        if summary_match:
            metadata['summary'] = self.decode_html_entities(summary_match.group(1))

        return metadata

    def extract_content(self, html: str) -> str:
        """Extract main content from HTML"""
        # Remove script and style tags
        cleaned = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
        cleaned = re.sub(r'<style[^>]*>.*?</style>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)

        # Find js_content container
        content_match = re.search(r'id=["\']js_content["\'][^>]*>([\s\S]*?)(?:</div>\s*</div>\s*</div>|$)', cleaned)

        if not content_match:
            # Try alternate content container
            alt_match = re.search(r'class=["\']rich_media_content[^"\']*', cleaned)
            if alt_match:
                container_start = alt_match.start()
                container_end = cleaned.find('</div>', container_start)
                if container_end > 0:
                    return self.process_content(cleaned[container_start:container_end])
            return ''

        return self.process_content(content_match.group(1))

    def process_content(self, html: str) -> str:
        """Process content HTML to plain text with Markdown formatting"""
        text = html

        # Handle images
        def replace_img(match):
            alt = match.group(1) if match.group(1) else ''
            return f'![{alt}]()' if alt else '[图片]'

        text = re.sub(r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*>', replace_img, text, flags=re.IGNORECASE)
        text = re.sub(r'<img[^>]*>', '[图片]', text, flags=re.IGNORECASE)

        # Handle links
        text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>([^<]*)</a>', r'[\2](\1)', text, flags=re.IGNORECASE)

        # Handle paragraphs
        text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)

        # Handle line breaks
        text = re.sub(r'<br[^>]*>', '\n', text, flags=re.IGNORECASE)

        # Handle headings
        text = re.sub(r'<h1[^>]*>', '\n\n# ', text, flags=re.IGNORECASE)
        text = re.sub(r'<h2[^>]*>', '\n\n## ', text, flags=re.IGNORECASE)
        text = re.sub(r'<h3[^>]*>', '\n\n### ', text, flags=re.IGNORECASE)
        text = re.sub(r'<h4[^>]*>', '\n\n#### ', text, flags=re.IGNORECASE)
        text = re.sub(r'</h[1-6]>', '\n', text, flags=re.IGNORECASE)

        # Handle bold and italic
        text = re.sub(r'<strong[^>]*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'</strong>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'<b[^>]*>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'</b>', '**', text, flags=re.IGNORECASE)
        text = re.sub(r'<em[^>]*>', '*', text, flags=re.IGNORECASE)
        text = re.sub(r'</em>', '*', text, flags=re.IGNORECASE)

        # Handle lists
        text = re.sub(r'<li[^>]*>', '\n- ', text, flags=re.IGNORECASE)
        text = re.sub(r'</li>', '', text, flags=re.IGNORECASE)

        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Decode HTML entities
        text = self.decode_html_entities(text)

        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()

    def parse(self, html: str, source_url: str = '') -> Article:
        """
        Parse HTML and return Article object

        Args:
            html: HTML content
            source_url: Source URL (optional)

        Returns:
            Article object
        """
        metadata = self.extract_metadata(html)
        content = self.extract_content(html)

        # Override source URL if provided
        if source_url and not metadata['source_url']:
            metadata['source_url'] = source_url

        return Article(
            title=metadata['title'],
            author=metadata['author'],
            source_url=metadata['source_url'],
            published_date=metadata['published_date'],
            content=content,
            summary=metadata['summary']
        )
