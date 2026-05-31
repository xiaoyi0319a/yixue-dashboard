# 报告库新增流程（Jekyll版）

> 2026-05-31 迁移完成 | 37只报告已全部 Markdown 化

---

## 新增报告（3步）

### 1. 创建 Markdown 文件

在 `_reports/` 目录下新建文件，命名规则：`{股票代码}.md`

```yaml
---
code: 688400
title: 凌云光
subtitle: 机器视觉+AI龙头 · JAI并表 · 具身智能 · CPO概念
date: 2026-05-14
version: V4.3
analyst: 小羿
data_date: 2026-05-14
---

<!-- 下方写报告内容，支持 HTML + Markdown 混排 -->
<div class="section">
  <h2>📋 执行摘要</h2>
  ...
</div>
```

**YAML 字段说明**：
| 字段 | 必填 | 说明 |
|:-----|:----:|:-----|
| `code` | ✅ | 6位股票代码 |
| `title` | ✅ | 公司名称 |
| `subtitle` | ✅ | 概念标签（用 `·` 分隔）|
| `date` | ✅ | 分析日期（YYYY-MM-DD）|
| `version` | ✅ | 分析版本（如 V4.3）|
| `analyst` | ✅ | 分析师 |
| `data_date` | 可选 | 数据截止日期 |

### 2. 提交推送

```bash
cd /root/.openclaw/workspace/yixue-dashboard
git add _reports/688400.md
git commit -m "新增报告：凌云光 688400"
git push
```

### 3. 自动生效

GitHub Pages 会在 1-2 分钟内自动构建，新报告访问地址：

```
https://xiaoyi0319a.github.io/yixue-dashboard/stock-688400.html
```

---

## 修改已有报告

直接编辑 `_reports/{代码}.md`，重新提交推送即可。

无需手动改 HTML，无需改 CSS，样式由 `_layouts/report.html` 统一控制。

---

## 模板统一

- `_layouts/report.html` — 全站统一模板（渐变标题、金色三问、信息网格、权重标签、裁决框、锚点跳转）
- `_config.yml` — Jekyll 配置（`permalink: /stock-:name.html`）
- `reports.json` — 自动从所有报告生成，无需手动维护

---

## 旧版对比（为什么迁移）

| 维度 | 旧版（37个独立HTML） | 新版（Jekyll Markdown） |
|:-----|:------|:------|
| 新增报告 | 复制模板→改37处数据→易错 | 写Markdown→3步提交 |
| 样式更新 | 改37个文件 | 改1个模板文件 |
| 版本管理 | 混乱 | Git记录清晰 |
| 内容分离 | HTML+CSS+内容混在一起 | 内容纯文本，样式统一 |
| 自动化 | 手动维护reports.json | 自动生成 |

---

*迁移时间：2026-05-31 10:30-10:40 GMT+8*
*迁移数量：37只报告*
*迁移人：小羿*
