# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security
- 🔒 Added SSRF protection - blocks private IP addresses and localhost
- 🔒 Added protocol whitelist - only http/https allowed
- 🔒 Added path traversal protection in file save operations
- 🔒 Added URL validation before requests

### Added
- 📝 Added SECURITY.md with security policy
- 📝 Added CONTRIBUTING.md with contribution guidelines
- 📝 Added CODE_OF_CONDUCT.md
- 📝 Added disclaimer to README.md

### Changed
- 📦 Updated package.json repository information
- 📦 Updated pyproject.toml repository information

---

## [1.0.0] - 2026-03-05

### Added
- 🎉 Initial release
- 📦 Node.js SDK with full API
- 🐍 Python SDK with asyncio support
- 💻 CLI tools for both Node.js and Python
- 📝 Multiple output formats: Markdown, JSON, Plain Text
- 🔄 Batch download support
- 🤖 MCP Skill integration
- 📖 Comprehensive documentation
- ✅ Test suites for both languages

### Features
- Zero external dependencies (Node.js version)
- Lightweight and fast (20-50KB output)
- Custom User-Agent support
- Automatic retry with exponential backoff
- HTML entity decoding
- Safe filename generation

---

## Legend
- `🎉` New features
- `🐛` Bug fixes
- `🔒` Security improvements
- `📝` Documentation
- `📦` Package/Build changes
- `⚡` Performance improvements
- `🔄` Changed
- `🧹` Cleanup/Refactoring

---

**Last Updated**: 2026-03-05
