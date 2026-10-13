# PDF-export · 精美 PDF 导出

> 仓库：https://github.com/JerommeWEI/j-studio-export  
> 版本：**v0.2.0** · 作者：**JerommeWEI**

为 J-Studio 仓库定制的 Obsidian 导出插件：把笔记渲染成**带封面、目录、页眉页码、优雅分页**的 A4 PDF，解决内置导出的"分页破碎、排版走样、没有正式文档感"三大问题。

## 更新记录

### v0.2.0

- **导出弹窗按钮修复**：部分主题/布局下底部按钮被裁切不可见；现将「导出 PDF / 导出 HTML」固定在弹窗顶部，任何情况下都可点击
- **弹窗可滚动**：强制 `.modal` 高度上限并允许滚动，避免内容被截断
- **开关选项重排**：封面页/目录页/页眉/页码改为整行卡片——底色划分区域，文字靠左、开关靠右

### v0.1.0

- 首个版本：三套预设、Paged.js 分页、封面/目录/页眉页码

## 启用方法

1. 打开 Obsidian → 设置 → 第三方插件（Community plugins）
2. 在已安装列表中找到 **PDF-export**，打开开关（若列表没有，先重启 Obsidian）
3. 左侧栏会出现 📄 导出图标，或用 Ctrl+P 运行命令：

| 命令 | 作用 |
|------|------|
| `导出当前笔记为精美 PDF` | 弹窗选择预设与元素后导出 |
| `快速导出（跳过弹窗）` | 直接用设置里的默认预设 |

## 三套预设

| 预设 | 气质 | 用途 |
|------|------|------|
| **正式报告** | 封面 + 目录（真实页码）+ 页眉页码，章节起新页 | 发同事/领导、归档 |
| **预览快照** | 还原 quiet-notes 阅读视图：加粗正文、行距 2.0 | 像预览一样留存 |
| **紧凑打印** | 9.5pt 密排、窄边距 | 打印纸质、讲义 |

封面元数据来源：frontmatter 的 `title / subtitle / subject / author / date / kicker`，缺省用文件名、文件夹路径、今天日期。与文档标题相同的首个 H1 会自动隐藏（避免封面+正文重复）。

## 工作原理

```
笔记 → Obsidian 渲染器（Dataview/Mermaid/Excalidraw/数学都真实渲染）
     → 图片内嵌 base64 + 收集仓库全部 CSS
     → CSS 消毒（css-sanitize.js：去掉 Paged.js 无法处理的
       :is() 内逗号选择器、剥离 @media print）
     → 消毒后的样式仅屏幕态注入（@media screen）：
       Paged.js 在屏幕态用真实样式做分页测量（保真），
       打印态只走 presets/ 的排版 CSS（稳定，规避 app.css
       的 html/body height:100% 等打印态怪癖）
     → Paged.js 分页引擎（页码/页眉/目录页码由它生成）
     → 隐藏窗口 Chromium 静默打印 printToPDF
```

无构建步骤：`main.js` 是纯 JavaScript，改完在 Obsidian 里关闭再开启插件即可生效。

**改 CSS 时的两条军规**（保持屏幕/打印态度量一致）：
1. 影响度量的排版规则（字号、行距、间距）写在 `presets/*.css`，
   并用 `.jx-export .jx-content`（优先级 0-2-0）压过 app.css
   对 `.markdown-rendered` 的直接规则
2. 排版控制不要依赖 `@media print`——打印态只有 presets 生效

## 已知陷阱（血泪记录）

- Paged.js **必须用 0.4.3**（0.5.0-beta 的 margin box 与 break 是坏的）
- Paged.js 按逗号切选择器组时不识别括号：`:is(p,pre) + :is(h1,h2)`
  被切成非法选择器 → **整个分页失败（产出 0 页）**——这就是
  css-sanitize.js 存在的原因，收集的 CSS 必须过它
- `leader()` 不被支持（整条声明被丢弃）；目录点线用 flex + 点线 span
- app.css 的 `html, body { height: 100% }` 在打印态解析为 0px，
  会把第 1 页之后的内容全部裁掉——收集样式只能屏幕态注入
- margin box 内容生成在 `.pagedjs_margin-content::after` 伪元素里，
  调试时查 textContent 会误判为空

## 如何迭代排版（最重要的一节）

**日常调样式**：编辑 `presets/` 下的 CSS，重启插件（或重启 Obsidian）后导出即见效果。
所有预设共享 `_base.css`（元素样式、分页保护、封面目录骨架），每套预设只做覆盖。
也可以不改文件，直接在 设置 → 自定义 CSS 里写覆盖规则（优先级最高）。

**本地验证回路**（不打开 Obsidian 也能测排版）：

```
cd .obsidian/plugins/j-studio-export/dev-test
node build-test.js report     # 用模拟内容生成 test-report.html
node render.js report         # 本机 Chrome 渲染 → PDF + 截图
node verify.js report         # DOM/像素级断言（页码、页眉、溢出…）
node pdf-check.js report      # PDF 文本内容断言
```

## 文件结构

```
j-studio-export/
├── manifest.json        # 插件清单
├── main.js              # 导出管线（纯 JS）
├── styles.css           # 弹窗/设置界面样式
├── vendor/paged.polyfill.js   # Paged.js 0.4.3（分页引擎）
├── presets/             # ← 排版气质都在这里
│   ├── _base.css
│   ├── report.css
│   ├── snapshot.css
│   └── compact.css
└── dev-test/            # 本地测试回路（node 依赖已装好）
```

## 已知边界

- 代码块等宽字体导出时用 Cascadia Code / Consolas（预览里的 3DS Fonticon 是图标字体，不适合代码）
- 毛玻璃 frosted 效果在纸上不存在，快照预设已翻译成等价的纸面排版
- 音视频/iframe 嵌入不会进入 PDF（会被隐藏）
- 复制 PDF 文本时个别汉字可能变成部首变体（Chromium + 思源黑体 CMap 的已知怪癖，渲染不受影响）
- 若环境不允许静默打印，会自动降级为"导出自包含 HTML + 浏览器 Ctrl+P 指引"

## 设置项

默认预设 / 作者名（封面署名）/ 输出位置（每次询问或直接写笔记同目录）/ 导出后自动打开 / 自定义 CSS。
