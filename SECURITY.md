# Security Policy

## 🔒 Security-First Design

This project is built with security in mind:

- **No hardcoded credentials** - No API keys, tokens, or passwords in the codebase
- **SSRF Protection** - Built-in protection against Server-Side Request Forgery attacks
  - Blocks private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, etc.)
  - Blocks localhost and metadata endpoints
  - Only allows http/https protocols
- **Path Traversal Protection** - Safe filename handling prevents directory traversal
- **No Data Storage** - All operations are local, no user data is stored or transmitted

## 🛡️ Security Features

### URL Validation

Both Node.js and Python implementations include:

```javascript
// Protocol whitelist
if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
  throw new Error('Only http and https are allowed');
}

// Private IP blocking
if (this._isPrivateIP(hostname)) {
  throw new Error('Access to private IP addresses is not allowed');
}
```

### Safe File Operations

```javascript
// Filename sanitization
const safeTitle = path.basename(
  this.title.replace(/[\/\\:*?"<>|]/g, '').substring(0, 50)
);
```

## 📋 Best Practices for Users

1. **Request Rate Limiting**: When using batch download, set appropriate delays between requests
   ```javascript
   await downloader.batchDownload(urls, { delay: 1000 }); // 1 second delay
   ```

2. **Respect robots.txt**: This tool doesn't automatically check robots.txt. Please be respectful of target websites.

3. **Legal Compliance**: Only download content you have the right to access and use.

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability, please follow responsible disclosure:

1. **Do NOT** create a public GitHub issue
2. Email the maintainer directly at: 443224841@qq.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## 📅 Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity, typically within 30 days

## 🙏 Acknowledgments

Security researchers who responsibly disclose vulnerabilities will be acknowledged in our security advisories (with your permission).

---

**Last Updated**: 2026-03-05
