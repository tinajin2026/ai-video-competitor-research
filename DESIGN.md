---
name: AI VIDEO / 竞品研究站
description: Factory 视觉体系下的行业工作台与独立竞品研究，以趋势、精确数据和来源支持行动
colors:
  bg: "#101010"
  lift: "#1d1a18"
  stroke: "#3d3a39"
  graphite: "#4d4947"
  muted: "#b8b3b0"
  faint: "#8a8380"
  text: "#eee"
  orange: "#ee6018"
  green: "#a0ca92"
typography:
  company-title:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "38px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "-.035em"
  research-thesis:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-.02em"
  research-section:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 400
    lineHeight: 1.4
  research-prose:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.8
  research-table:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.6
  headline:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "26px"
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "-.03em"
  title:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 500
    lineHeight: 1.4
  body:
    fontFamily: "Geist, 'PingFang SC', system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  data:
    fontFamily: "'Geist Mono', ui-monospace, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  metric:
    fontFamily: "'Geist Mono', ui-monospace, monospace"
    fontSize: "30px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "-.03em"
rounded:
  control: "4px"
  surface: "6px"
  dialog: "8px"
spacing:
  inline: "8px"
  compact: "12px"
  group: "16px"
  surface: "20px"
  panel-gap: "24px"
  section: "28px"
  research-columns: "32px"
  research-section: "48px"
components:
  button-neutral:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
  button-export:
    backgroundColor: "{colors.text}"
    textColor: "{colors.bg}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
  search:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
  surface:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.surface}"
    padding: "20px"
  scope-tag:
    backgroundColor: "{colors.lift}"
    textColor: "{colors.muted}"
    padding: "2px 5px"
---

# Design System: AI VIDEO / 竞品研究站

## Overview

**Creative North Star: "Factory 市场分析工作台"**

黑色画布、骨白文字与暖灰细线组织可操作的数据和可连续阅读的研究。Geist 承担正文与标题，Geist Mono 承担数字、日期和图表读数；橙绿用于变化、选择与状态。图表、表格、来源和文字分析构成页面的主要视觉材料。

本记录延续已确认的 Factory 世界，描述 `src/dashboard.css` 与 `src/research.css` 的实际实现。工作台采用紧凑层级，独立研究页增加标题、段落行距与章节间距，以容纳较长的中文分析。两种密度共用颜色、字体、边框、控件与数字语言；研究页的阅读字号是现有身份的扩展。

**Key Characteristics:**
- 黑色画布、暖灰细线与中性操作控件。
- Geist 正文与 Geist Mono 数据，依靠字号与对齐组织层级。
- 工作台密集比较，独立研究页顺序阅读并保留操作入口。
- 桌面并列呈现，手机顺序阅读，宽表格在局部容器滚动。

实现依据：`src/dashboard.css`、`src/research.css`、`scripts/company_page.py`、`scripts/html_parts.py`、`scripts/build.py`；生成结果见 `public/index.html`、`public/companies/index.html`、`public/competitors/higgsfield/index.html`、`public/signals/index.html` 与 `public/methodology/index.html`。视觉核验材料位于 `../work/public-site-qa/` 的 `company-desktop.jpg`、`company-mobile.jpg`、`directory-desktop.jpg`、`directory-mobile.jpg`、`macro-desktop.jpg`；截图记录特定时刻，后续修正以源样式和重新构建结果为准。产品范围与数据约束由 `PRODUCT.md` 管理。

## Colors

### Primary
Bone（`text`）用于正文、选中导航线、导出按钮和选中动作筛选；Obsidian Canvas（`bg`）承载页面与数据面板。

### Secondary
Metric Green（`green`）表达正向变化、关注与比较选择，并提供键盘焦点。Signal Orange（`orange`）表达负向变化、范围警示和浅色控件的焦点。图表中的系列色结合图例解释，不将所有绿色系列理解为增长。

### Neutral
Carbon Lift（`lift`）承载按钮悬停、范围标签与条形底轨。Ash Stroke（`stroke`）形成细线边界；Graphite（`graphite`）用于中性条形；Pale Stone（`muted`）用于辅助文字；Warm Granite（`faint`）只承担更次要的品牌补充文字。

**The Data Color Rule.** 操作底色保持中性；橙绿服务于变化、选择、警示和焦点，不承担大面积装饰。

**The Evidence Rule.** 颜色与数值、文字或图例共同表达信息；未知值不可借颜色伪装成确定结果。

## Typography

**Display / Body Font:** Geist，中文回退至 PingFang SC，再回退至系统无衬线字体。
**Label / Mono Font:** Geist Mono，回退至 ui-monospace、monospace。

本地 WOFF2 随站点发布，采用 `font-display: swap`。常规文字为 400；工作台标题和强调为 500。没有独立营销展示字体。

### Hierarchy
- **Company title:** `company-title` 用于研究页身份；手机缩至 32px。
- **Research thesis:** `research-thesis` 用于公司研究判断；手机缩至 22px。
- **Research section:** `research-section` 用于研究与方法章节；研究页手机缩至 20px。
- **Workbench headline / title:** `headline` 与 `title` 保留紧凑工作台；手机分别缩至 23px 与 16px。
- **Research prose:** `research-prose` 用于目录说明与实验内容；实验在手机为 14px。研究判断与动作正文通常为 14px、1.8 行高，方法正文为 15px、1.85 行高。公司简介为 15px、1.65 行高，手机为 14px。研究段落宽度多在 66–90ch，实验内容为 70ch。
- **Research table:** `research-table` 承担公司页精确数据，目录行采用相同字号、1.7 行高。表头与元信息比数据轻；目录公司名为 17px。
- **Data / metric:** 等宽数字与右对齐用于工作台数值列，`metric` 用于大统计。统计在 1100px 以下为 26px，760px 以下为 25px。研究页会话数据为 24px 等宽数字。

工作台表格与说明多为 12px，表头和图表轴多为 11px；10px 仅保留于局部域名、范围与辅助元信息。较大的研究正文和更宽松的行距服务连续阅读，不把工作台小字扩展成长文标准。

**The Quiet Hierarchy Rule.** 通过字号、对比和对齐区分层级；研究标题可以放大，数字不承担装饰性英雄标题。

## Layout

页面与导航最大宽度为 1440px，桌面左右留白 36px；1100px 以下为 24px，760px 以下为 18px。桌面导航最小高 64px。手机导航换行后横向滚动，保留全部入口。

工作台保留五视图结构：总览、对比、动作、渠道、产品与定价。总览四项统计后为 1.6:1 趋势与赛道双栏，再接月度矩阵；1100px 以下双栏为 1.4:1，760px 以下变单栏，统计变两列。跨视图筛选与研究目录入口保持可见。

独立研究页先呈现身份、口径、章节导航和四项统计，再以 .88:1.3 双栏并排呈现研究判断与趋势图，间距 40px。1100px 以下标题操作移到下方，双栏变为 1:1.15、间距 24px；760px 以下依文档顺序阅读。研究章节以顶边细线与 48px 上间距分隔，手机收紧至 34px。渠道与关键词等双栏间距 32px，手机上下排列。

目录使用搜索、赛道和排序工具条；手机搜索独占一行，标签保持不折字，输入框允许收缩。目录最小表宽 900px；常规研究表最小宽 600px。宽表与工作台矩阵仅在自身容器滚动，不依赖整页横向滚动。工作台动作表在手机变成纵向记录；研究页动作原本就是纵向记录。

实验说明桌面采用 200px 标签列与内容列，间距 32px；手机变顺序段落。价格条桌面分为套餐、条款和来源三列，中屏两列，手机单列。方法页内容最大宽度 960px。

## Elevation & Depth

界面不使用投影、辉光或背景模糊。边框、留白和中性底色变化形成层次。工作台保留的证据对话框使用黑色 80% 不透明遮罩，仅隔离模态内容。独立公司研究通过页面地址打开。

**The Flat Surface Rule.** 数据容器默认与画布同色，用细边框和间距分组。

## Shapes

控件与链接按钮使用 `control` 圆角；趋势面板使用 `surface` 圆角；证据对话框使用 `dialog` 圆角。范围标签和条形图保留直角，常规边框为单像素。研究章节主要采用开放式内容与水平分隔线，不额外包成卡片。

## Components

### Buttons / Inputs
中性按钮与选择框为深底浅字、细边框，标准最小高 34px；搜索框最小高 36px。导出按钮及选中动作筛选反转明暗。按钮悬停使用 lift，不可用时半透明并使用默认指针。链接按钮沿用控件边框与圆角。

键盘焦点为 2px 绿色轮廓、偏移 3px；浅底控件使用橙色。状态变化即时，无额外入场或滚动动画；减少动态效果媒体查询关闭过渡与平滑滚动。复制链接等操作在当前页提供文字反馈。

### Navigation
工作台五个标签入口使用 tab / tabpanel 与同步选中状态。研究站顶栏四个链接通向行业总览、竞品研究、X 动态、数据与方法；当前项提高对比并使用底边线。公司章节导航上下各有细线，允许横向滚动。面包屑、公司切换器和同组比较链接串联各研究页。

### Tables / Tags
表格以细线分隔，产品名称、域名、范围标签和研究主题各自占据稳定层级。工作台数值列等宽且右对齐；公司研究表保留正文式数据行。表格实际存在的列与来源口径保持一致。范围标签以 lift 底、muted 字说明独立主域、母域或迁移等条件。

目录筛选结果用状态文字反馈，空结果提供调整搜索或赛道的指引。工作台比较最多六家，所选项以可移除的紧凑按钮表示。

### Charts / Statistics
统计条用竖线分组，手机变两列。趋势图自适应容器，等宽坐标、淡虚线网格、可换行图例和精确读数组成完整图表。时间范围选择器与可展开的逐月精确表保留在图表附近。条形渠道同时显示名称、份额和折算数值，颜色不替代文字。

### Research Records
公司判断是正文标题与实测窗口解释的组合；其下的绿色状态文本描述实际趋势，不作为装饰眉题。动作记录由日期、类型、标题、正文和来源构成，以细线分隔。实验说明将做法、判断标准和后续跟踪排列为同一个阅读单元；不将研究建议伪装成已达成结果。

### Sources / Empty States
来源与统计月份在相关数据附近出现，页脚复述流量月份与重新请求日期。方法页以连续段落说明时间、范围和更新方式。X 动态当前显示明确空状态与更新说明，使用常规文字及细边框通知块；不生成占位曲线或虚构动态。采集不足也保留公司身份与研究入口。

### Evidence Dialog
工作台证据对话框最大宽度 1120px、最高 90vh，桌面内边距 24px、手机 18px。研究摘记与来源容器可独立滚动、长链接可换行。公司档案的完整阅读与分享由独立 HTML 承担。

## Do's and Don'ts

### Do:
- **Do** 使用黑色画布、暖灰分隔和骨白文字保持 Factory 的分析质感。
- **Do** 让数值、统计月份、范围与来源互相可追溯。
- **Do** 为连续研究正文保留较大的字号与足够行距。
- **Do** 保留键盘焦点、精确值入口、筛选结果和操作反馈。
- **Do** 在手机顺序排列长文与动作，宽表格保持局部滚动。

### Don't:
- **Don't** 将未知值呈现为零，或将估算写成后台实测。
- **Don't** 用大面积强调色、投影或辉光替代数据层级。
- **Don't** 将工作台的小型元信息字号推广成长正文默认字号。
- **Don't** 把数据采集日期当作统计月份，或把空动态区表现成实时接入。

未固化为规范：排序箭头等文字图形不是图标系统；局部 10px 元信息不是新正文标准。未出现于本站的营销大标题、浅色宣传卡、装饰眉题及入场动画不从视觉参考中移植。截图中曾出现的手机搜索标签折字为修复项，不记录为布局规则。
