# PDF-export · 精美 PDF 导出

> **仓库**：https://github.com/JerommeWEI/j-studio-export  
> **版本**：v0.3.0 · **作者**：[JerommeWEI](https://github.com/JerommeWEI)  
> **平台**：桌面端 Obsidian（`isDesktopOnly`）

把 Obsidian 笔记一键导出为**正式、可打印、可交付**的 A4 PDF：封面、目录（真实页码）、页眉、页脚页码、优雅分页——而不是内置导出那种「分页破碎、排版走样、没有文档感」的结果。

---

## 为什么需要这个插件

| 痛点 | 本插件的解法 |
|------|----------------|
| 内置 PDF 导出分页破碎、图表被截断 | Paged.js 分页引擎，表格跨页重复表头、段落孤行控制 |
| 样式走样，和阅读视图不一样 | 导出前收集仓库真实 CSS，消毒后注入排版 |
| 没有正式文档感（封面/目录/页眉页码） | 「正式报告」预设：封面 + 自动目录 + 页眉 + 页码 |
| 图表、Mermaid、数学公式导不出来 | 走 Obsidian 渲染器，图片内嵌 base64 |
| 想要和预览一致的留存 / 省纸打印 | 「预览快照」「紧凑打印」两套预设 |

适合：结题报告、标定/实验记录、周报归档、给同事领导的交付文档、纸质讲义。

---

## 快速开始

1. **安装**
   - 社区插件市场搜索 **PDF-export**（推荐）
   - 或手动：把 Release 里的 `main.js` / `manifest.json` / `styles.css` 放入  
     `.obsidian/plugins/j-studio-export/`
2. **启用**：设置 → 第三方插件 → 打开 **PDF-export**
3. **导出**
   - 点左侧栏 📄 下载图标，或
   - 命令面板（`Ctrl/Cmd+P`）运行命令：

| 命令 | 作用 |
|------|------|
| **导出当前笔记为精美 PDF** | 弹窗选择预设与元素后导出 |
| **快速导出（跳过弹窗，使用默认预设）** | 按设置里的默认预设直接导出 |

### 导出弹窗

- 顶部：**导出 PDF** / **导出 HTML**（HTML 可分享或浏览器 Ctrl+P 兜底）
- 三套预设卡片：正式报告 / 预览快照 / 紧凑打印
- 开关（卡片式，文字左、开关右）：封面页、目录页、页眉、页码

---

## 三套预设

| 预设 | 气质 | 适合 |
|------|------|------|
| **正式报告** | 封面 + 目录（真实页码）+ 页眉页码；一级标题起新页；A4 正式文档 | 交付、归档、给领导 |
| **预览快照** | 接近 Obsidian 阅读观感：行距更松、加粗正文 | 留存、截图对比 |
| **紧凑打印** | 小字号密排、窄边距 | 打印纸、讲义、省纸 |

**封面元数据**（frontmatter，缺省有合理回退）：

```yaml
title: 文档主标题
subtitle: 副标题
subject: 栏目/主题（如 Venus 产品）
author: 署名
date: 2026-10-13
kicker: 页眉小字（可选）
```

与文档标题相同的首个 H1 会自动隐藏，避免封面和正文重复。

---

## 工作原理

```
笔记 (.md)
  → Obsidian MarkdownRenderer（Dataview / Mermaid / Excalidraw / 数学 全真实渲染）
  → 图片内嵌 base64 + 收集仓库 CSS
  → CSS 消毒（丢掉 Paged.js 处理不了的选择器、剥离 @media print）
  → 样式仅屏幕态注入（分页测量用真实样式；打印态只走 presets/）
  → Paged.js 0.4.3 分页（页码 / 页眉 / 目录页码）
  → 隐藏窗口 Chromium 静默 printToPDF
```

无构建步骤：`main.js` 为纯 JavaScript。开发时改 `presets/*.css` 后重开插件即可；发版前运行 `node tools/embed-assets.js` 把预设打进 `main.js`。

---

## 版本记录

### v0.4.0

- **去掉导出里的复制按钮**：代码块上的 Obsidian「复制」图标不再进入 PDF（DOM 剥离 + CSS 兜底）
- **页首间隙真正统一**：间距改加在每一页内容区（`pagedjs_page_content`），代码块/段落/标题落在页首距离一致，且**不会在灰底代码块内部多出空白条**
- 社区审核告警清理：标准 MIT LICENSE、manifest 描述句末标点、减少无必要 `!important`

### v0.3.0

- **正文页首间隙统一**：分页点 `margin-top` 会被折叠，导致第 2 页起内容贴页眉；改为 `padding-top` 保证
  - 标题（h1–h4）与正文块（段落 / 列表 / 引用 / 代码 / 表格）共用同一「页眉 → 首行」间距
  - 正式报告页眉与正文间隙加大（`padding-bottom` 4mm → 7mm）
- 页中段落间距改为 `margin-bottom` + `padding-top`，避免统一间隙后段距爆炸

### v0.2.0

- **导出弹窗按钮修复**：底部按钮在部分主题下被裁切；改为置顶固定
- **弹窗可滚动**：内容过高时不再截断
- **开关选项卡片化**：底色分区，文字靠左、开关靠右
- 作者字段改为 **JerommeWEI**

### v0.1.0

- 首个版本：三套预设、Paged.js 分页、封面 / 目录 / 页眉页码、HTML 降级导出

---

## 设置项

| 设置 | 说明 |
|------|------|
| 默认预设 | 打开弹窗时预选的预设 |
| 作者名 | 封面署名 |
| 输出位置 | 每次询问（另存为）/ 写入笔记所在文件夹 |
| 导出后自动打开 | 导出完成后打开文件 |
| 自定义 CSS | 追加在所有预设之后，优先级最高 |

---

## 文件结构

```
j-studio-export/
├── manifest.json              # 插件清单（版本、作者、minAppVersion）
├── main.js                    # 导出管线 + 内嵌资产兜底
├── styles.css                 # 导出弹窗 / 设置界面
├── versions.json              # 版本 → minAppVersion 映射
├── presets/                   # 排版气质（日常迭代入口）
│   ├── _base.css              # 元素样式、分页保护、封面目录骨架
│   ├── report.css             # 正式报告
│   ├── snapshot.css           # 预览快照
│   └── compact.css            # 紧凑打印
├── vendor/paged.polyfill.js   # Paged.js 0.4.3
└── tools/embed-assets.js      # 发版前：把 presets/vendor 打进 main.js
```

`dev-test/` 为本地验证回路（不随 Release 分发）：

```bash
cd .obsidian/plugins/j-studio-export/dev-test
node build-test.js report    # 模拟内容 → HTML
node render.js report        # Chrome 渲染 → PDF + 截图
node verify.js report        # DOM/像素断言
node pdf-check.js report     # PDF 文本断言
```

---

## 排版迭代约定

1. 影响度量的规则（字号、行距、间距）写在 `presets/*.css`，用 `.jx-export .jx-content` 压过 app.css
2. **不要依赖 `@media print`**——打印态只走 presets
3. **页首间隙用 `padding-top`，不要依赖 `margin-top`**——分页点上 margin 会被折叠
4. 改完 presets 后执行 `node tools/embed-assets.js` 再发版

### 已知陷阱（Paged.js 血泪）

- 必须用 **Paged.js 0.4.3**（0.5.0-beta 的 margin box / break 是坏的）
- 选择器里的 `:is(a,b)` 含逗号会导致整个分页失败（0 页）——必须过 `css-sanitize`
- `leader()` 不支持；目录点线用 flex + 点线 span
- app.css 的 `html, body { height: 100% }` 打印态会裁掉第 2 页起内容——收集样式只做屏幕态注入

---

## 已知边界

- 代码块等宽字体用 Cascadia Code / Consolas（预览里的图标字体不适合代码）
- 毛玻璃 frosted 效果纸上不存在，快照预设已翻译成等价纸面排版
- 音视频 / iframe 嵌入不进入 PDF
- 复制 PDF 文本时个别汉字可能成部首变体（Chromium + 思源黑体 CMap 已知怪癖，渲染正常）
- 无法静默打印时自动降级为「导出自包含 HTML + 浏览器 Ctrl+P 指引」

### 权限说明（给审核与用户）

导出需要在**本机写入 PDF / HTML 文件**，因此使用 Node `fs` 写盘与读取 `presets/`、`vendor/` 静态资源；笔记内容读取走 Obsidian `vault.read` API。不会上传网络，不收集遥测。

---

## License

[MIT](LICENSE)。

内置 [Paged.js](https://gitlab.coko.foundation/pagedjs/pagedjs) v0.4.3，其自身亦为 MIT。
