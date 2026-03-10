/**
 * Tests for WeChat Article Downloader
 */

const assert = require('assert');
const { WeChatDownloader, WeChatParser, Article } = require('../../src/js/index');

// Sample HTML for testing
const sampleHtml = `
<!DOCTYPE html>
<html>
<head>
  <title>Test Article</title>
  <script>var msg_title = 'Test Article Title';</script>
  <script>var msg_source_url = 'https://mp.weixin.qq.com/s/test';</script>
</head>
<body>
  <div id="js_content">
    <p>This is a test paragraph.</p>
    <p>Another paragraph with <strong>bold</strong> text.</p>
    <h3>Section Title</h3>
    <p>More content here.</p>
  </div>
</body>
</html>
`;

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    const result = fn();
    if (result instanceof Promise) {
      result.then(() => {
        passed++;
        console.log(`  ✓ ${name}`);
      }).catch((err) => {
        failed++;
        console.log(`  ✗ ${name}: ${err.message}`);
      });
    } else {
      passed++;
      console.log(`  ✓ ${name}`);
    }
  } catch (err) {
    failed++;
    console.log(`  ✗ ${name}: ${err.message}`);
  }
}

console.log('\nArticle Tests:');

test('should create article with properties', () => {
  const article = new Article({
    title: 'Test Title',
    author: 'Test Author',
    content: 'Test content'
  });
  assert.strictEqual(article.title, 'Test Title');
  assert.strictEqual(article.author, 'Test Author');
  assert.strictEqual(article.content, 'Test content');
});

test('should export to Markdown', () => {
  const article = new Article({
    title: 'Test Title',
    content: 'Test content'
  });
  const md = article.toMarkdown();
  assert.ok(md.includes('# Test Title'));
  assert.ok(md.includes('Test content'));
});

test('should export to JSON', () => {
  const article = new Article({
    title: 'Test Title',
    content: 'Test content'
  });
  const json = article.toJSON();
  assert.strictEqual(json.title, 'Test Title');
  assert.strictEqual(json.content, 'Test content');
});

console.log('\nWeChatParser Tests:');

const parser = new WeChatParser();

test('should parse HTML and extract metadata', () => {
  const article = parser.parse(sampleHtml, 'https://mp.weixin.qq.com/s/test');
  assert.strictEqual(article.title, 'Test Article Title');
  assert.ok(article.content.includes('This is a test paragraph'));
});

test('should decode HTML entities', () => {
  const text = parser.decodeHTMLEntities('&ldquo;Hello&rdquo; &amp; World');
  assert.strictEqual(text, '"Hello" & World');
});

console.log('\nWeChatDownloader Tests:');

const downloader = new WeChatDownloader({ timeout: 5000 });

test('should have correct user agent', () => {
  const ua = downloader.getUserAgent();
  assert.ok(ua.includes('Mobile'));
});

test('should parse HTML without downloading', async () => {
  const article = await downloader.parse(sampleHtml, 'https://mp.weixin.qq.com/s/test');
  assert.ok(article.title);
  assert.ok(article.content);
});

// Wait for async tests and print summary
setTimeout(() => {
  console.log(`\n${passed} passed, ${failed} failed\n`);
  if (failed > 0) {
    process.exit(1);
  }
}, 100);
