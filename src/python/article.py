"""
Article Class - Represents a WeChat official account article
"""

from datetime import datetime
import json
import os
import re


class Article:
    """Represents a WeChat official account article"""

    def __init__(
        self,
        title: str = '',
        author: str = '',
        source_url: str = '',
        published_date: str = '',
        content: str = '',
        summary: str = ''
    ):
        self.title = title
        self.author = author
        self.source_url = source_url
        self.published_date = published_date
        self.content = content
        self.summary = summary
        self.extracted_at = datetime.utcnow().isoformat() + 'Z'

    def to_markdown(self) -> str:
        """Export article as Markdown format"""
        lines = [
            f'# {self.title}',
            ''
        ]

        # Add metadata
        meta_items = []
        if self.author:
            meta_items.append(f'**作者**: {self.author}')
        if self.source_url:
            meta_items.append(f'**链接**: {self.source_url}')
        if self.published_date:
            meta_items.append(f'**发布时间**: {self.published_date}')
        meta_items.append(f'**整理时间**: {self.extracted_at}')

        if meta_items:
            lines.append(f'> {" | ".join(meta_items)}')
            lines.append('')

        lines.extend([
            '---',
            '',
            self.content,
            '',
            '---',
            '',
            '*本文由 [wechat-article-downloader](https://github.com/chemaoxian/wechat-article-downloader) 自动提取，仅供学习参考。*'
        ])

        return '\n'.join(lines)

    def to_json(self) -> dict:
        """Export article as JSON object"""
        return {
            'title': self.title,
            'author': self.author,
            'source_url': self.source_url,
            'published_date': self.published_date,
            'content': self.content,
            'summary': self.summary,
            'extracted_at': self.extracted_at
        }

    def to_text(self) -> str:
        """Export article as plain text"""
        return re.sub(r'\n{3,}', '\n\n', self.content).strip()

    async def save_to_dir(self, output_dir: str, options: dict = None) -> list:
        """
        Save article to directory

        Args:
            output_dir: Output directory path
            options: Save options
                - format: 'md', 'json', 'txt', 'all' (default: 'md')
                - filename: Custom filename without extension

        Returns:
            List of saved file paths
        """
        options = options or {}
        format_type = options.get('format', 'md')
        filename = options.get('filename')

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate safe filename
        # Remove dangerous characters and limit length
        safe_title = filename or re.sub(
            r'[\/\\:*?"<>|]', '',
            self.title
        ).replace(' ', '-').replace('--', '-')[:50]

        if not safe_title:
            safe_title = 'article'

        # Additional safety: use os.path.basename to prevent directory traversal
        safe_title = os.path.basename(safe_title)

        saved_files = []

        def save_file(ext: str, content: str):
            filepath = os.path.join(output_dir, f'{safe_title}{ext}')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files.append(filepath)

        if format_type in ('md', 'all'):
            save_file('.md', self.to_markdown())

        if format_type in ('json', 'all'):
            save_file('.json', json.dumps(self.to_json(), indent=2, ensure_ascii=False))

        if format_type in ('txt', 'all'):
            save_file('.txt', self.to_text())

        return saved_files

    def __str__(self) -> str:
        return f'Article(title="{self.title}", author="{self.author}")'

    def __repr__(self) -> str:
        return self.__str__()
