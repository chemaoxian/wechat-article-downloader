/**
 * WeChat Article Downloader
 *
 * LightWeight WeChat official account article downloader
 * Extract articles to Markdown/JSON without browser
 *
 * @example
 * const { WeChatDownloader, Article } = require('wechat-article-downloader');
 *
 * const downloader = new WeChatDownloader();
 * const article = await downloader.download('https://mp.weixin.qq.com/s/xxx');
 * console.log(article.toMarkdown());
 *
 * @module wechat-article-downloader
 */

const WeChatDownloader = require('./downloader');
const WeChatParser = require('./parser');
const Article = require('./article');

module.exports = {
  WeChatDownloader,
  WeChatParser,
  Article
};
