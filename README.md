# PDF-export · 精美 PDF 导出（Obsidian 插件）

把 Obsidian 笔记导出为**带封面、目录、页眉页码、优雅分页**的 A4 PDF，
解决内置导出的"分页破碎、排版走样、没有正式文档感"三大问题。

Export your Obsidian notes to beautifully typeset A4 PDFs — cover page,
table of contents with real page numbers, headers and page numbers —
powered by the Paged.js pagination engine.

## 功能特性

- **三套排版预设**
  | 预设 | 气质 | 用途 |
  |------|------|------|
  | **正式报告** | 封面 + 目录（真实页码）+ 页眉页码，章节起新页 | 发同事/领导、归档 |
  | **预览快照** | 还原阅读视图的纸面翻译版 | 像预览一样留存 |
  | **紧凑打印** | 小字号密排、窄边距 | 打印纸质、讲义 |
- **忠实渲染**：用 Obsidian 自己的渲染管线，Dataview / Mermaid /
  Excalidraw / 数学公式 / 高亮 / Callout 都以真实渲染结果进入 PDF
- **图片自动内嵌**：本地附件（含 `![[wiki 嵌入]]` 与标准 Markdown 图片）
  自动转 base64 嵌入，离线可印
- **自适应任意仓库**：不假设仓库路径、附件位置或 Obsidian 链接格式；
  插件所需的排版预设与分页引擎已内嵌于 `main.js`，商店安装开箱即用
- **封面元数据**：自动读取 frontmatter 的 `title / subtitle / author /
  date / kicker`（也认中文键 `标题 / 副标题 / 作者 / 日期 / 栏目`），
  缺省用文件名、所在文件夹路径、当天日期
- **优雅降级**：环境不允许静默打印时，自动改导自包含 HTML 并给出
  浏览器打印指引

## 安装

### 社区插件商店（推荐）

设置 → 第三方插件 → 浏览，搜索 **PDF-export**，安装并启用。

### 手动安装

1. 从 [Releases](../../releases) 下载 `main.js`、`manifest.json`、`styles.css`
2. 放入 `<你的仓库>/.obsidian/plugins/j-studio-export/`
3. 重启 Obsidian，在设置 → 第三方插件中启用 **PDF-export**

## 使用

- 点击左侧栏 📥 图标，或 `Ctrl+P` 运行命令：

| 命令 | 作用 |
|------|------|
| `导出当前笔记为精美 PDF` | 弹窗选择预设与元素后导出 |
| `快速导出（跳过弹窗，使用默认预设）` | 一键按设置导出 |

### 设置项

默认预设 / 封面署名（author）/ 封面品牌文字（brand）/ 输出位置
（每次询问或直接写入笔记同目录）/ 导出后自动打开 / 自定义 CSS
（优先级最高的排版覆盖）。

## 工作原理

```
笔记 → Obsidian 渲染器（插件生态真实渲染）
     → 图片内嵌 base64 + 收集仓库全部 CSS
     → CSS 消毒（去掉 Paged.js 无法处理的 :is() 内逗号选择器、
       剥离 @media print）
     → 消毒后的样式仅屏幕态注入（@media screen）：
       Paged.js 在屏幕态用真实样式做分页测量（保真），
       打印态只走预设排版 CSS（稳定）
     → Paged.js 分页引擎（页码/页眉/目录页码由它生成）
     → 隐藏窗口 Chromium 静默打印 printToPDF
```

## 开发

无构建步骤，`main.js` 是纯 JavaScript：

```
manifest.json          # 插件清单
main.js                # 导出管线（含 base64 内嵌资产）
styles.css             # 弹窗/设置界面样式
presets/               # 排版预设（开发态真实文件，改 CSS 即改即测）
vendor/paged.polyfill.js  # Paged.js 0.4.3 分页引擎
tools/embed-assets.js  # 把 presets + vendor 以 base64 内嵌进 main.js
```

**发版前必跑**：

```bash
node tools/embed-assets.js   # 刷新 main.js 里的内嵌资产
```

> 商店/手动安装只会有 `main.js / manifest.json / styles.css` 三个文件，
> 因此 presets 与分页引擎必须内嵌于 `main.js` 兜底；
> 开发态则始终优先读取 `presets/`、`vendor/` 真实文件，方便迭代排版。

**调排版的两条军规**（保持屏幕/打印态度量一致）：

1. 影响度量的排版规则（字号、行距、间距）写在 `presets/*.css`，
   并用 `.jx-export .jx-content`（优先级 0-2-0）压过 app.css
   对 `.markdown-rendered` 的直接规则
2. 排版控制不要依赖 `@media print`——打印态只有预设生效

### 已知陷阱（血泪记录）

- Paged.js **必须用 0.4.3**（0.5.0-beta 的 margin box 与 break 是坏的）
- Paged.js 按逗号切选择器组时不识别括号：`:is(p,pre) + :is(h1,h2)`
  会被切成非法选择器 → 整个分页失败（产出 0 页）——收集的 CSS 必须
  先过消毒器
- `leader()` 不被支持（整条声明被丢弃）；目录点线用 flex + 点线 span
- app.css 的 `html, body { height: 100% }` 在打印态解析为 0px，
  会把第 1 页之后的内容全部裁掉——收集样式只能屏幕态注入
- Obsidian 渲染出的 `app://` 图片链接，host 之后接的是 **URL 编码的
  绝对路径**（不同版本格式不同），解析时必须先判断绝对/相对再拼路径

## 已知边界

- 音视频 / iframe 嵌入不会进入 PDF（会被隐藏）
- 复制 PDF 文本时个别汉字可能变成部首变体（Chromium + 思源黑体 CMap
  的已知怪癖，渲染不受影响）
- 仅支持桌面端（`isDesktopOnly`）

## 许可

MIT（插件本体）；内置 Paged.js 遵循其原有 MIT 许可。
