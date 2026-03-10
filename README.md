# WeChat Article Downloader

> 🚀 轻量级微信公众号文章下载工具 - 无需浏览器，一行命令提取为 Markdown/JSON

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js >=14](https://img.shields.io/badge/node-%3E%3D14-green.svg)](https://nodejs.org/)
[![Python >=3.7](https://img.shields.io/badge/python-%3E%3D3.7-blue.svg)](https://www.python.org/)

---

## ✨ 特性

- 🚀 **快速轻量** - 无需浏览器，纯脚本实现，输出仅 20-50KB
- 📦 **双语言支持** - Node.js 和 Python SDK
- 💻 **CLI 工具** - 命令行一键下载
- 📝 **多种格式** - Markdown、JSON、纯文本输出
- 🔄 **批量下载** - 支持 URL 列表批量处理
- 🤖 **MCP Skill** - 支持 Claude Code 等 MCP 客户端

---

## 📦 安装

> **注意**: npm 和 PyPI 包即将发布，目前请从 GitHub 安装使用

### 从 GitHub 安装

**Node.js**
```bash
git clone https://github.com/chemaoxian/wechat-article-downloader.git
cd wechat-article-downloader
npm install
```

**Python**
```bash
git clone https://github.com/chemaoxian/wechat-article-downloader.git
cd wechat-article-downloader
pip install -e .
```

---

## 🚀 快速开始

### Node.js

```javascript
const { WeChatDownloader } = require('wechat-article-downloader');

const downloader = new WeChatDownloader();
const article = await downloader.download('https://mp.weixin.qq.com/s/xxx');
console.log(article.toMarkdown());
```

### Python

```python
import asyncio
from wechat_article_downloader import WeChatDownloader

async def main():
    downloader = WeChatDownloader()
    article = await downloader.download('https://mp.weixin.qq.com/s/xxx')
    print(article.to_markdown())

asyncio.run(main())
```

### CLI

```bash
# 从 URL 下载
npx wechat-download https://mp.weixin.qq.com/s/xxx

# 或使用 Python
wechat-download https://mp.weixin.qq.com/s/xxx
```

---

## 📖 文档

### CLI 使用

```bash
# 从 URL 下载并打印 Markdown
wechat-download https://mp.weixin.qq.com/s/xxx

# 保存到文件
wechat-download https://mp.weixin.qq.com/s/xxx -o ./output

# 从 HTML 文件解析
wechat-download --input article.html --output ./output

# 指定输出格式（md, json, txt, all）
wechat-download https://mp.weixin.qq.com/s/xxx -f json

# 批量下载（每行一个 URL）
wechat-download --batch urls.txt --output-dir ./articles

# 自定义 User-Agent
wechat-download https://mp.weixin.qq.com/s/xxx --ua "custom-ua"

# 详细模式
wechat-download https://mp.weixin.qq.com/s/xxx -v
```

### Node.js SDK API

```javascript
const { WeChatDownloader, Article } = require('wechat-article-downloader');

// 创建下载器
const downloader = new WeChatDownloader({
  timeout: 30000,        // 请求超时（毫秒）
  retry: 3,             // 重试次数
  userAgent: 'mobile',  // 'mobile' | 'desktop' | 'custom'
  customUA: ''          // 自定义 User-Agent
});

// 下载文章
const article = await downloader.download('https://mp.weixin.qq.com/s/xxx');

// 从 HTML 解析
const article = await downloader.parse(htmlString);

// 访问属性
console.log(article.title);        // 标题
console.log(article.author);       // 作者
console.log(article.content);      // 正文
console.log(article.sourceUrl);    // 链接

// 导出格式
const md = article.toMarkdown();
const json = article.toJSON();
const text = article.toText();

// 保存文件
await article.saveToDir('./output', { format: 'all' });

// 批量下载
const articles = await downloader.batchDownload(urls, {
  outputDir: './articles',
  format: 'md',
  delay: 1000  // 请求间隔（毫秒）
});
```

### Python SDK API

```python
import asyncio
from wechat_article_downloader import WeChatDownloader, Article

async def main():
    # 创建下载器
    downloader = WeChatDownloader(
        timeout=30000,        # 请求超时（毫秒）
        retry=3,             # 重试次数
        user_agent='mobile'  # 'mobile' | 'desktop' | 'custom'
    )

    # 下载文章
    article = await downloader.download('https://mp.weixin.qq.com/s/xxx')

    # 从 HTML 解析
    article = await downloader.parse(html_string)

    # 访问属性
    print(article.title)         # 标题
    print(article.author)        # 作者
    print(article.content)       # 正文

    # 导出格式
    md = article.to_markdown()
    json_data = article.to_json()
    text = article.to_text()

    # 保存文件
    await article.save_to_dir('./output', {'format': 'all'})

    # 批量下载
    articles = await downloader.batch_download(
        urls,
        output_dir='./articles',
        format='md',
        delay=1000  # 请求间隔（毫秒）
    )

asyncio.run(main())
```

---

## 📝 输出格式

### Markdown

```markdown
# AI Coding 思考：从工具提效到范式变革，我们还缺什么？

> **作者**: 作者名  |  **链接**: https://mp.weixin.qq.com/s/xxx  |  **发布时间**: 2024-01-01  |  **整理时间**: 2024-01-02T10:00:00Z

---

正文内容...

---

*本文由 [wechat-article-downloader](https://github.com/yourusername/wechat-article-downloader) 自动提取，仅供学习参考。*
```

### JSON

```json
{
  "title": "AI Coding 思考：从工具提效到范式变革，我们还缺什么？",
  "author": "作者名",
  "source_url": "https://mp.weixin.qq.com/s/xxx",
  "published_date": "2024-01-01",
  "content": "正文内容...",
  "extracted_at": "2024-01-02T10:00:00Z"
}
```

---

## 🤝 MCP Skill 集成

在 Claude Code 中使用：

```
/user 下载这篇文章 https://mp.weixin.qq.com/s/xxx
```

工具会自动调用 `wechat-article-downloader` 提取文章内容。

---

## 💡 使用场景

**⚠️ 请确保您的使用符合当地法律法规和微信服务条款**

### 合规使用场景 ✅

- 📚 **个人学习归档** - 保存有价值的文章供个人学习参考
- 🧠 **知识管理** - 导入 Notion、Obsidian 等工具进行个人知识整理
- 📊 **学术研究** - 用于自然语言处理、文本分析等学术研究
- 📽️ **PPT 素材** - 提取内容作为演讲素材（需注明出处）
- 🤖 **技术开发** - 集成到个人项目或学习项目中

### 禁止使用场景 ❌

- 🚫 **商业用途** - 未经授权将下载内容用于商业盈利
- 🚫 **大规模爬虫** - 短时间内批量下载大量文章
- 🚫 **内容搬运** - 将下载内容发布到其他平台冒充原创
- 🚫 **数据售卖** - 出售下载的文章数据
- 🚫 **绕过付费墙** - 绕过微信公众号的付费内容机制

**详细说明请阅读 [免责声明](#-免责声明--disclaimer)**

---

## 🔍 技术原理

微信公众号文章有反爬措施，但通过模拟**移动端 User-Agent**可直接访问：

```
Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15
  (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0
```

HTML 解析流程：
1. 下载 HTML 页面
2. 提取 `js_content` 区域
3. 清理 script、style 标签
4. 转换 HTML 标签为 Markdown
5. 解码 HTML 实体
6. 格式化输出

---

## 📋 开发路线图

- ✅ Node.js SDK
- ✅ Python SDK
- ✅ CLI 工具
- 🔄 MCP Skill 支持
- 🔄 批量下载增强
- 🔄 图片下载选项

---

## 🙋 FAQ

**Q: 下载失败怎么办？**

A: 确保使用正确的 User-Agent。默认使用移动端 UA，如果遇到反爬，可以尝试自定义 UA。

**Q: 支持视频下载吗？**

A: 当前版本仅支持文章文本提取，不支持图片、视频等多媒体内容。

**Q: 批量下载有限制吗？**

A: 建议设置请求间隔（delay）避免触发反爬机制。

---

## ⚠️ 免责声明 / Disclaimer

### 中文版本

**重要提示**：使用本工具前，请仔细阅读并理解以下声明。

#### 1. 使用目的限制

- 本工具仅供**学习、研究和个人归档**使用
- **禁止用于任何商业用途**，除非您获得微信官方和相关版权方的明确授权
- 使用本工具可能违反《微信公众平台服务协议》和《微信软件许可及服务协议》

#### 2. 版权合规

- 下载的内容请**尊重原作者版权**
- 转载或引用需遵守相关授权规定，获得原作者许可
- 用户应自行承担内容使用的法律责任

#### 3. 技术合规

- 批量下载时请设置**合理的请求间隔**（建议 ≥1 秒），避免对服务器造成压力
- 请勿使用本工具进行大规模爬虫或数据采集行为
- 本工具内置 SSRF 防护和请求频率限制功能

#### 4. 隐私与数据

- 本工具**不存储、上传任何用户数据**，所有操作均在本地完成
- 您的 URL 列表、下载历史等信息不会被收集或传输
- 详见 [PRIVACY.md](PRIVACY.md)

#### 5. 版权投诉 (DMCA)

- 如认为本工具或下载内容侵犯您的版权，请通过 [DMCA.md](DMCA.md) 中规定的流程提交版权投诉
- 我们将在收到有效通知后 5 个工作日内处理
- 版权投诉邮箱：443224841@qq.com

#### 6. 法律风险提示

⚠️ **使用本工具可能存在以下法律风险**：

- 可能违反《中华人民共和国网络安全法》
- 可能违反《中华人民共和国反不正当竞争法》
- 可能涉及《中华人民共和国著作权法》相关条款
- 可能违反微信公众平台服务条款

具体详见 [DMCA.md](DMCA.md) 文件。

#### 6. 责任承担

**使用本工具产生的任何法律后果由使用者自行承担**，包括但不限于：
- 民事责任（如版权侵权赔偿）
- 行政责任（如违反网络管理规定）
- 其他法律责任

---

### English Version

**IMPORTANT**: Please read and understand the following disclaimer before using this tool.

#### 1. Usage Restrictions

- This tool is for **learning, research, and personal archiving** purposes ONLY
- **Commercial use is prohibited** without explicit authorization from WeChat and relevant copyright holders
- Using this tool may violate the "WeChat Public Platform Service Agreement" and "WeChat Software License and Service Agreement"

#### 2. Copyright Compliance

- Please **respect original authors' copyright** for downloaded content
- Reproduction or quotation requires compliance with relevant authorization regulations and permission from the original author
- Users are responsible for legal compliance of content usage

#### 3. Technical Compliance

- Please set **reasonable request intervals** (recommended ≥1 second) when batch downloading to avoid putting pressure on servers
- Do not use this tool for large-scale crawling or data collection
- This tool has built-in SSRF protection and request rate limiting

#### 4. Privacy & Data

- This tool does **NOT store or upload any user data**; all operations are completed locally
- Your URL lists, download history, and other information are not collected or transmitted
- See [PRIVACY.md](PRIVACY.md) for details

#### 5. Copyright Complaints (DMCA)

- If you believe this tool or downloaded content infringes your copyright, please submit a copyright complaint through the process specified in [DMCA.md](DMCA.md)
- We will process within 5 business days after receiving a valid notice
- Copyright complaint email: 443224841@qq.com

#### 6. Legal Risk Notice

⚠️ **Using this tool may involve the following legal risks**:

- May violate the "Cybersecurity Law of the People's Republic of China"
- May violate the "Anti-Unfair Competition Law of the People's Republic of China"
- May involve relevant provisions of the "Copyright Law of the People's Republic of China"
- May violate WeChat Public Platform terms of service

See [DMCA.md](DMCA.md) for details.

#### 6. Liability

**Users bear all legal consequences** resulting from the use of this tool, including but not limited to:
- Civil liability (such as copyright infringement compensation)
- Administrative liability (such as violations of network management regulations)
- Other legal liabilities

---

**By using this tool, you agree to abide by this disclaimer and all applicable laws and regulations.**

**使用本工具即表示您同意遵守本免责声明及所有适用的法律法规。**

---

## 📄 License

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📮 联系方式

- GitHub: [chemaoxian/wechat-article-downloader](https://github.com/chemaoxian/wechat-article-downloader)
- Email: 443224841@qq.com

> **注意**: npm 和 PyPI 包发布后，相关链接将在此处更新
