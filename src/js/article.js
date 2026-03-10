/**
 * Article Class - Represents a WeChat official account article
 */
class Article {
  constructor({
    title = '',
    author = '',
    sourceUrl = '',
    publishedDate = '',
    content = '',
    summary = ''
  } = {}) {
    this.title = title;
    this.author = author;
    this.sourceUrl = sourceUrl;
    this.publishedDate = publishedDate;
    this.content = content;
    this.summary = summary;
    this.extractedAt = new Date().toISOString();
  }

  /**
   * Export article as Markdown format
   * @returns {string} Markdown string
   */
  toMarkdown() {
    const lines = [
      `# ${this.title}`,
      ''
    ];

    // Add metadata if available
    const metaItems = [];
    if (this.author) metaItems.push(`**作者**: ${this.author}`);
    if (this.sourceUrl) metaItems.push(`**链接**: ${this.sourceUrl}`);
    if (this.publishedDate) metaItems.push(`**发布时间**: ${this.publishedDate}`);
    metaItems.push(`**整理时间**: ${this.extractedAt}`);

    if (metaItems.length > 0) {
      lines.push(`> ${metaItems.join('  |  ')}`);
      lines.push('');
    }

    lines.push('---');
    lines.push('');
    lines.push(this.content);
    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('*本文由 [wechat-article-downloader](https://github.com/chemaoxian/wechat-article-downloader) 自动提取，仅供学习参考。*');

    return lines.join('\n');
  }

  /**
   * Export article as JSON object
   * @returns {object} JSON object
   */
  toJSON() {
    return {
      title: this.title,
      author: this.author,
      source_url: this.sourceUrl,
      published_date: this.publishedDate,
      content: this.content,
      summary: this.summary,
      extracted_at: this.extractedAt
    };
  }

  /**
   * Export article as plain text
   * @returns {string} Plain text string
   */
  toText() {
    return this.content.replace(/\n{3,}/g, '\n\n').trim();
  }

  /**
   * Save article to directory
   * @param {string} outputDir - Output directory path
   * @param {object} options - Save options
   * @param {string} options.format - Output format: 'md', 'json', 'txt', 'all'
   * @param {string} options.filename - Custom filename (without extension)
   * @returns {Promise<string[]>} List of saved file paths
   */
  async saveToDir(outputDir, options = {}) {
    const fs = require('fs');
    const path = require('path');

    const {
      format = 'md',
      filename = null
    } = options;

    // Create output directory if not exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Generate safe filename from title or custom filename
    // Remove dangerous characters and limit length
    let baseName = filename || this.title
      .replace(/[\/\\:*?"<>|]/g, '')
      .replace(/\s+/g, '-')
      .substring(0, 50);

    // Additional safety: use path.basename to prevent directory traversal
    const safeTitle = path.basename(baseName || 'article');

    const savedFiles = [];

    const saveFile = (ext, content) => {
      const filePath = path.join(outputDir, `${safeTitle}${ext}`);
      fs.writeFileSync(filePath, content, 'utf-8');
      savedFiles.push(filePath);
    };

    if (format === 'md' || format === 'all') {
      saveFile('.md', this.toMarkdown());
    }

    if (format === 'json' || format === 'all') {
      saveFile('.json', JSON.stringify(this.toJSON(), null, 2));
    }

    if (format === 'txt' || format === 'all') {
      saveFile('.txt', this.toText());
    }

    return savedFiles;
  }
}

module.exports = Article;
