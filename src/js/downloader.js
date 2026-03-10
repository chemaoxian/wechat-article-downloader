/**
 * Downloader Module - Download WeChat article HTML
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

class WeChatDownloader {
  /**
   * Create downloader instance
   * @param {object} options - Downloader options
   * @param {number} options.timeout - Request timeout in milliseconds
   * @param {number} options.retry - Number of retries
   * @param {string} options.userAgent - User-Agent type: 'mobile', 'desktop', 'custom'
   * @param {string} options.customUA - Custom User-Agent string
   */
  constructor(options = {}) {
    this.timeout = options.timeout || 30000;
    this.retry = options.retry || 3;
    this.userAgentType = options.userAgent || 'mobile';
    this.customUA = options.customUA || '';

    this.userAgents = {
      mobile: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0',
      desktop: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    };
  }

  /**
   * Get User-Agent string
   * @returns {string} User-Agent
   */
  getUserAgent() {
    if (this.userAgentType === 'custom' && this.customUA) {
      return this.customUA;
    }
    return this.userAgents[this.userAgentType] || this.userAgents.mobile;
  }

  /**
   * Make HTTP request
   * @param {string} url - URL to request
   * @param {number} retryCount - Current retry count
   * @returns {Promise<string>} Response body
   */
  async request(url, retryCount = 0) {
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const client = parsedUrl.protocol === 'https:' ? https : http;

      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'GET',
        headers: {
          'User-Agent': this.getUserAgent(),
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'Connection': 'keep-alive'
        },
        timeout: this.timeout
      };

      const req = client.request(options, (res) => {
        let data = '';

        // Handle redirects
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          res.resume();
          this.request(res.headers.location, retryCount).then(resolve).catch(reject);
          return;
        }

        if (res.statusCode !== 200) {
          res.resume();
          const error = new Error(`Request failed with status code ${res.statusCode}`);
          error.statusCode = res.statusCode;
          reject(error);
          return;
        }

        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          resolve(data);
        });
      });

      req.on('error', (error) => {
        if (retryCount < this.retry) {
          // Retry with exponential backoff
          const delay = Math.pow(2, retryCount) * 1000;
          setTimeout(() => {
            this.request(url, retryCount + 1).then(resolve).catch(reject);
          }, delay);
        } else {
          reject(error);
        }
      });

      req.on('timeout', () => {
        req.destroy();
        reject(new Error(`Request timeout after ${this.timeout}ms`));
      });

      req.end();
    });
  }

  /**
   * Download article from URL
   * @param {string} url - WeChat article URL
   * @returns {Promise<Article>} Parsed article
   */
  async download(url) {
    const WeChatParser = require('./parser');

    if (!url || typeof url !== 'string') {
      throw new Error('Invalid URL: URL must be a non-empty string');
    }

    // Validate URL format and security
    try {
      const parsedUrl = new URL(url);

      // Security: Only allow http and https protocols
      if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
        throw new Error(`Invalid protocol: Only http and https are allowed. Got: ${parsedUrl.protocol}`);
      }

      // Security: Block private IP ranges to prevent SSRF
      const hostname = parsedUrl.hostname.toLowerCase();
      if (this._isPrivateIP(hostname)) {
        throw new Error('Access to private IP addresses is not allowed');
      }
    } catch (error) {
      if (error.message.includes('Invalid URL') || error.message.includes('Invalid protocol') || error.message.includes('private IP')) {
        throw error;
      }
      throw new Error(`Invalid URL format: ${url}`);
    }

    const html = await this.request(url);
    const parser = new WeChatParser();
    return parser.parse(html, url);
  }

  /**
   * Check if hostname is a private IP address
   * @param {string} hostname - Hostname to check
   * @returns {boolean} True if private IP
   * @private
   */
  _isPrivateIP(hostname) {
    // IPv4 private ranges
    const ipv4Patterns = [
      /^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,                          // 10.0.0.0/8
      /^172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}$/,          // 172.16.0.0/12
      /^192\.168\.\d{1,3}\.\d{1,3}$/,                              // 192.168.0.0/16
      /^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,                          // 127.0.0.0/8 (localhost)
      /^169\.254\.\d{1,3}\.\d{1,3}$/,                              // 169.254.0.0/16 (link-local)
      /^0\.0\.0\.0$/,                                               // 0.0.0.0
      /^1\.\d{1,3}\.\d{1,3}\.\d{1,3}$/                             // 1.0.0.0/8 (used in some SSRF bypasses)
    ];

    // IPv6 private patterns
    const ipv6Patterns = [
      /^::$/,                                                     // ::
      /^::1$/,                                                    // ::1 (localhost)
      /^fc[0-9a-f]{2}:/i,                                         // fc00::/7 (unique local)
      /^fd[0-9a-f]{2}:/i,                                         // fd00::/8
      /^fe80:/i                                                   // fe80::/10 (link-local)
    ];

    // Check for localhost aliases
    if (hostname === 'localhost' || hostname === 'internal' || hostname === 'metadata') {
      return true;
    }

    // Check IPv4 patterns
    for (const pattern of ipv4Patterns) {
      if (pattern.test(hostname)) {
        return true;
      }
    }

    // Check IPv6 patterns
    for (const pattern of ipv6Patterns) {
      if (pattern.test(hostname)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Parse article from HTML string
   * @param {string} html - HTML content
   * @param {string} sourceUrl - Source URL (optional)
   * @returns {Article} Parsed article
   */
  async parse(html, sourceUrl = '') {
    const WeChatParser = require('./parser');
    const parser = new WeChatParser();
    return parser.parse(html, sourceUrl);
  }

  /**
   * Batch download articles from URLs
   * @param {string[]} urls - Array of URLs
   * @param {object} options - Batch options
   * @param {string} options.outputDir - Output directory
   * @param {string} options.format - Output format: 'md', 'json', 'all'
   * @param {number} options.delay - Delay between requests in milliseconds
   * @returns {Promise<Article[]>} Array of downloaded articles
   */
  async batchDownload(urls, options = {}) {
    const {
      outputDir = '',
      format = 'md',
      delay = 0
    } = options;

    const results = [];
    const errors = [];

    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];

      try {
        console.log(`[${i + 1}/${urls.length}] Downloading: ${url}`);
        const article = await this.download(url);

        if (outputDir) {
          const savedFiles = await article.saveToDir(outputDir, { format });
          console.log(`  Saved: ${savedFiles.join(', ')}`);
        }

        results.push(article);

        // Delay between requests
        if (delay > 0 && i < urls.length - 1) {
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      } catch (error) {
        console.error(`  Error: ${error.message}`);
        errors.push({ url, error: error.message });
      }
    }

    if (errors.length > 0) {
      console.warn(`\nFailed to download ${errors.length} article(s):`);
      errors.forEach(({ url, error }) => {
        console.warn(`  - ${url}: ${error}`);
      });
    }

    return results;
  }
}

module.exports = WeChatDownloader;
