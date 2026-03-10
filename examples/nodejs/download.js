/**
 * Example: Download a WeChat article
 */

const { WeChatDownloader } = require('wechat-article-downloader');

async function main() {
  const downloader = new WeChatDownloader({
    timeout: 30000,
    retry: 3
  });

  // Download from URL
  const url = 'https://mp.weixin.qq.com/s/xxx';
  console.log(`Downloading: ${url}`);

  const article = await downloader.download(url);

  console.log(`\nTitle: ${article.title}`);
  console.log(`Author: ${article.author}`);
  console.log(`Content length: ${article.content.length} chars\n`);

  // Save to directory
  await article.saveToDir('./output', { format: 'all' });
  console.log('Saved to ./output');
}

main().catch(console.error);
