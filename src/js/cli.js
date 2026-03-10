#!/usr/bin/env node

/**
 * WeChat Article Downloader CLI
 */

const fs = require('fs');
const path = require('path');
const { WeChatDownloader } = require('./index');

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    url: '',
    input: '',
    output: '',
    format: 'md',
    batch: '',
    verbose: false,
    help: false,
    ua: ''
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--verbose' || arg === '-v') {
      options.verbose = true;
    } else if (arg === '--url' || arg === '-u') {
      options.url = args[++i] || '';
    } else if (arg === '--input' || arg === '-i') {
      options.input = args[++i] || '';
    } else if (arg === '--output' || arg === '-o') {
      options.output = args[++i] || '';
    } else if (arg === '--format' || arg === '-f') {
      options.format = args[++i] || 'md';
    } else if (arg === '--batch' || arg === '-b') {
      options.batch = args[++i] || '';
    } else if (arg === '--ua') {
      options.ua = args[++i] || '';
    } else if (arg.startsWith('-')) {
      console.error(`Unknown option: ${arg}`);
      process.exit(1);
    } else {
      // Positional argument - treat as URL
      if (!options.url) {
        options.url = arg;
      }
    }
  }

  return options;
}

/**
 * Print help message
 */
function printHelp() {
  console.log(`
wechat-article-downloader - Download WeChat official account articles

USAGE:
  wechat-download [OPTIONS] [URL]
  wechat-download <URL>
  wechat-download --input <file.html> --output <dir>

OPTIONS:
  -u, --url <url>       WeChat article URL
  -i, --input <file>    Input HTML file path
  -o, --output <dir>    Output directory (default: stdout)
  -f, --format <fmt>    Output format: md, json, txt, all (default: md)
  -b, --batch <file>    Batch download from URL list file
  --ua <string>         Custom User-Agent
  -v, --verbose         Verbose output
  -h, --help            Show this help message

EXAMPLES:
  # Download from URL and print to stdout
  wechat-download https://mp.weixin.qq.com/s/xxx

  # Download and save to file
  wechat-download https://mp.weixin.qq.com/s/xxx -o ./output

  # Parse from HTML file
  wechat-download --input article.html --output ./output

  # Batch download
  wechat-download --batch urls.txt --output-dir ./articles

  # Output as JSON
  wechat-download https://mp.weixin.qq.com/s/xxx -f json

REPOSITORY:
  https://github.com/chemaoxian/wechat-article-downloader
`);
}

/**
 * Main function
 */
function sanitizeUrl(url) {
  if (!url) return url;
  try {
    const parsed = new URL(url);
    return parsed.protocol + "//" + parsed.host + parsed.pathname;
  } catch (e) {
    return url;
  }
}

async function main() {
  const options = parseArgs();

  if (options.help) {
    printHelp();
    process.exit(0);
  }

  // Validate input
  if (!options.url && !options.input && !options.batch) {
    console.error('Error: Please provide a URL, input file, or batch file');
    console.error('Use --help for usage information');
    process.exit(1);
  }

  const downloaderOptions = {};
  if (options.ua) {
    downloaderOptions.userAgent = 'custom';
    downloaderOptions.customUA = options.ua;
  }

  const downloader = new WeChatDownloader(downloaderOptions);

  try {
    // Batch download
    if (options.batch) {
      if (!fs.existsSync(options.batch)) {
        console.error(`Error: Batch file not found: ${options.batch}`);
        process.exit(1);
      }

      const urls = fs.readFileSync(options.batch, 'utf-8')
        .split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));

      if (!options.output) {
        console.error('Error: --output is required for batch download');
        process.exit(1);
      }

      await downloader.batchDownload(urls, {
        outputDir: options.output,
        format: options.format
      });

      console.log(`\nBatch download completed. Processed ${urls.length} URL(s).`);
      return;
    }

    // Download from URL
    if (options.url) {
      if (options.verbose) {
        console.log(`Downloading: ${options.url}`);
      }

      const article = await downloader.download(options.url);

      if (options.output) {
        const savedFiles = await article.saveToDir(options.output, {
          format: options.format
        });
        if (options.verbose) {
          console.log(`Saved: ${savedFiles.join(', ')}`);
        }
      } else {
        if (options.format === 'json') {
          console.log(JSON.stringify(article.toJSON(), null, 2));
        } else if (options.format === 'txt') {
          console.log(article.toText());
        } else {
          console.log(article.toMarkdown());
        }
      }
      return;
    }

    // Parse from HTML file
    if (options.input) {
      if (!fs.existsSync(options.input)) {
        console.error(`Error: Input file not found: ${options.input}`);
        process.exit(1);
      }

      const html = fs.readFileSync(options.input, 'utf-8');
      const article = await downloader.parse(html);

      if (options.output) {
        const savedFiles = await article.saveToDir(options.output, {
          format: options.format
        });
        if (options.verbose) {
          console.log(`Saved: ${savedFiles.join(', ')}`);
        }
      } else {
        if (options.format === 'json') {
          console.log(JSON.stringify(article.toJSON(), null, 2));
        } else if (options.format === 'txt') {
          console.log(article.toText());
        } else {
          console.log(article.toMarkdown());
        }
      }
    }
  } catch (error) {
    let errorMsg = error.message;
    if (options.url) {
      const safeUrl = sanitizeUrl(options.url);
      errorMsg = errorMsg.replace(options.url, safeUrl);
    }
    console.error("Error: " + errorMsg);
    if (options.verbose) {
      const safeStack = error.stack.replace(options.url, sanitizeUrl(options.url));
      console.error("Debug: " + safeStack);
    }
    process.exit(1);
  }
}

main();
