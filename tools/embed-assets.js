#!/usr/bin/env node
/**
 * 把 presets/*.css 与 vendor/paged.polyfill.js 以 base64 内嵌进 main.js 的
 * EMBEDDED-ASSETS 标记段。
 *
 * 为什么需要内嵌：Obsidian 商店/BRAT 安装插件时只会下载
 * main.js、manifest.json、styles.css 三个文件，
 * presets/ 与 vendor/ 不会存在，必须以 main.js 内嵌副本兜底。
 * 开发态插件仍优先读取真实文件，改 CSS 即改即测。
 *
 * 为什么是 base64：引擎源码含有 U+2028/U+2029 等无法安全进入
 * JS 字符串字面量的字符；base64 纯 ASCII，万无一失。
 * main.js 运行时用 decodeEmbeddedText() 解码。
 *
 * 用法：node tools/embed-assets.js   （每次改完 presets 或 vendor 后、发版前运行）
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const mainPath = path.join(root, 'main.js');

const b64 = (text) => Buffer.from(text, 'utf8').toString('base64');

const presetsDir = path.join(root, 'presets');
const presetsB64 = {};
let presetsBytes = 0;
for (const f of fs.readdirSync(presetsDir).sort()) {
  if (f.endsWith('.css')) {
    const text = fs.readFileSync(path.join(presetsDir, f), 'utf8');
    presetsB64[f] = b64(text);
    presetsBytes += text.length;
  }
}

const polyfill = fs.readFileSync(
  path.join(root, 'vendor', 'paged.polyfill.js'),
  'utf8'
);

const src = fs.readFileSync(mainPath, 'utf8');
const re =
  /\/\* ==== EMBEDDED-ASSETS:BEGIN[\s\S]*?\/\* ==== EMBEDDED-ASSETS:END ==== \*\//;
if (!re.test(src)) {
  console.error('main.js 中找不到 EMBEDDED-ASSETS 标记段');
  process.exit(1);
}

const block =
  '/* ==== EMBEDDED-ASSETS:BEGIN（由 tools/embed-assets.js 生成，请勿手改） ==== */\n' +
  '/* 商店安装只包含 main.js / manifest.json / styles.css，\n' +
  '   presets 与 Paged.js 引擎必须以 base64 内嵌于此作为兜底；\n' +
  '   开发态仍优先读取 presets/ 与 vendor/ 真实文件，便于直接改 CSS 迭代。 */\n' +
  `const EMBEDDED_ASSETS = { presetsB64: ${JSON.stringify(presetsB64)}, pagedPolyfillB64: ${JSON.stringify(b64(polyfill))} };\n` +
  '/* ==== EMBEDDED-ASSETS:END ==== */';

/* 注意：替换必须用函数形式——block 含引擎源码，
   字符串替换会把内容里的 $' $` $& 当成特殊模式展开，
   导致文件被复制成多份（血泪教训） */
fs.writeFileSync(mainPath, src.replace(re, () => block), 'utf8');
console.log(
  `OK: 内嵌 ${Object.keys(presetsB64).length} 个预设 (${(presetsBytes / 1024).toFixed(1)} KB) ` +
    `+ paged.polyfill.js (${(polyfill.length / 1024).toFixed(1)} KB) → main.js`
);
