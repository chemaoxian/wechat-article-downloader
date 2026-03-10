/**
 * Parser Module - Parse WeChat article HTML
 */

class WeChatParser {
  /**
   * Decode HTML entities
   * @param {string} text - Text with HTML entities
   * @returns {string} Decoded text
   */
  decodeHTMLEntities(text) {
    if (!text) return '';

    const entities = {
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
    };

    return text.replace(/&[^;]+;/g, (match) => entities[match] || match);
  }

  /**
   * Extract metadata from HTML
   * @param {string} html - HTML content
   * @returns {object} Metadata object
   */
  extractMetadata(html) {
    const metadata = {
      title: '',
      author: '',
      sourceUrl: '',
      publishedDate: '',
      summary: ''
    };

    // Extract title from msg_title variable
    const titleMatch = html.match(/var\s+msg_title\s*=\s*['"]([^'"]*)['"]/);
    if (titleMatch) {
      metadata.title = titleMatch[1].replace(/\.html\([^)]*\)/g, '').trim();
    }

    // Extract author from rich_media_meta_nickname
    const authorMatch = html.match(/rich_media_meta_nickname[^>]*>([^<]+)</);
    if (authorMatch) {
      metadata.author = authorMatch[1].trim();
    }

    // Try alternate author pattern
    if (!metadata.author) {
      const altAuthorMatch = html.match(/var\s+msg_author_name\s*=\s*['"]([^'"]*)['"]/);
      if (altAuthorMatch) {
        metadata.author = altAuthorMatch[1].trim();
      }
    }

    // Extract source URL
    const sourceUrlMatch = html.match(/var\s+msg_source_url\s*=\s*['"]([^'"]*)['"]/);
    if (sourceUrlMatch) {
      metadata.sourceUrl = sourceUrlMatch[1];
    }

    // Extract published date
    const dateMatch = html.match(/var\s+msg_publish_time\s*=\s*['"]?(\d+)['"]?/);
    if (dateMatch) {
      const timestamp = parseInt(dateMatch[1]);
      metadata.publishedDate = new Date(timestamp * 1000).toISOString().split('T')[0];
    }

    // Extract summary
    const summaryMatch = html.match(/var\s+msg_desc\s*=\s*['"]([^'"]*)['"]/);
    if (summaryMatch) {
      metadata.summary = this.decodeHTMLEntities(summaryMatch[1]);
    }

    return metadata;
  }

  /**
   * Extract main content from HTML
   * @param {string} html - HTML content
   * @returns {string} Extracted content
   */
  extractContent(html) {
    // Remove script and style tags
    let cleaned = html.replace(/<script[^>]*>[^]*?<\/script>/gi, '');
    cleaned = cleaned.replace(/<style[^>]*>[^]*?<\/style>/gi, '');

    // Find js_content container
    const contentMatch = cleaned.match(/id=["']js_content["'][^>]*>([\s\S]*?)(?:<\/div>\s*<\/div>\s*<\/div>|$)/);

    if (!contentMatch) {
      // Try alternate content container
      const altMatch = cleaned.match(/class=["']rich_media_content[^"']*/);
      if (altMatch) {
        const containerStart = altMatch.index;
        const containerEnd = cleaned.indexOf('</div>', containerStart);
        if (containerEnd > 0) {
          return this.processContent(cleaned.substring(containerStart, containerEnd));
        }
      }
      return '';
    }

    return this.processContent(contentMatch[1]);
  }

  /**
   * Process content HTML to plain text with Markdown formatting
   * @param {string} html - HTML content
   * @returns {string} Processed content
   */
  processContent(html) {
    let text = html;

    // Handle images - keep alt text or add placeholder
    text = text.replace(/<img[^>]*alt=["']([^"']*)["'][^>]*>/gi, (match, alt) => {
      return alt ? `![${alt}]()` : '[图片]';
    });
    text = text.replace(/<img[^>]*>/gi, '[图片]');

    // Handle links
    text = text.replace(/<a[^>]*href=["']([^"']*)["'][^>]*>([^<]*)<\/a>/gi, '[$2]($1)');

    // Handle paragraphs
    text = text.replace(/<p[^>]*>/gi, '\n\n');
    text = text.replace(/<\/p>/gi, '\n');

    // Handle line breaks
    text = text.replace(/<br[^>]*>/gi, '\n');

    // Handle headings
    text = text.replace(/<h1[^>]*>/gi, '\n\n# ');
    text = text.replace(/<h2[^>]*>/gi, '\n\n## ');
    text = text.replace(/<h3[^>]*>/gi, '\n\n### ');
    text = text.replace(/<h4[^>]*>/gi, '\n\n#### ');
    text = text.replace(/<\/h[1-6]>/gi, '\n');

    // Handle bold and italic
    text = text.replace(/<strong[^>]*>/gi, '**');
    text = text.replace(/<\/strong>/gi, '**');
    text = text.replace(/<b[^>]*>/gi, '**');
    text = text.replace(/<\/b>/gi, '**');
    text = text.replace(/<em[^>]*>/gi, '*');
    text = text.replace(/<\/em>/gi, '*');

    // Handle lists
    text = text.replace(/<li[^>]*>/gi, '\n- ');
    text = text.replace(/<\/li>/gi, '');

    // Handle blockquote
    text = text.replace(/<section[^>]*class=["'][^"']*blockquote/gi, '\n> ');
    text = text.replace(/<\/section>/gi, '');

    // Remove remaining HTML tags
    text = text.replace(/<[^>]+>/g, '');

    // Decode HTML entities
    text = this.decodeHTMLEntities(text);

    // Clean up whitespace
    text = text.replace(/\n{3,}/g, '\n\n');
    text = text.trim();

    return text;
  }

  /**
   * Parse HTML and return Article object
   * @param {string} html - HTML content
   * @param {string} sourceUrl - Source URL
   * @returns {Article} Parsed article
   */
  parse(html, sourceUrl = '') {
    const Article = require('./article');

    const metadata = this.extractMetadata(html);
    const content = this.extractContent(html);

    // Override source URL if provided
    if (sourceUrl && !metadata.sourceUrl) {
      metadata.sourceUrl = sourceUrl;
    }

    return new Article({
      title: metadata.title,
      author: metadata.author,
      sourceUrl: metadata.sourceUrl,
      publishedDate: metadata.publishedDate,
      content,
      summary: metadata.summary
    });
  }
}

module.exports = WeChatParser;
