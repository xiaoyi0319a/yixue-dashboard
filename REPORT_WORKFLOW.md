# 报告库新增流程（Jekyll版）

> 2026-05-31 迁移完成 | 37只报告已全部 Markdown 化

---

## 新增报告（4步）

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

### 2. 更新 `reports.json`

**⚠️ 必须手动更新**，不是自动生成。

在 `reports.json` 的**数组开头**插入新条目（按日期降序排列）：

```json
{
  "code": "688488",
  "name": "艾迪药业",
  "date": "2026-09-01",
  "file": "/yixue-dashboard/stock-688488.html",
  "tags": [
    "抗HIV创新药",
    "Biotech商业化拐点",
    "国产替代",
    "7个一类新药",
    "中价值"
  ]
}
```

**注意**：
- `date` 必须与报告 YAML 中的 `date` 一致
- `file` 格式：`/yixue-dashboard/stock-{代码}.html`
- `tags` 选 3-5 个核心标签，最后一个放价值等级（高价值/中价值/低价值/无价值）
- 插入位置：数组**最前面**（最新日期置顶）

### 3. 提交推送

```bash
cd /root/.openclaw/workspace/yixue-dashboard
git add _reports/688488.md reports.json
git commit -m "新增报告：艾迪药业 688488"
git push
```

### 4. 自动生效

GitHub Pages 会在 1-2 分钟内自动构建，新报告访问地址：

```
https://xiaoyi0319a.github.io/yixue-dashboard/stock-688488.html
```

**验证**：推送后打开首页 `https://xiaoyi0319a.github.io/yixue-dashboard/`，确认新报告出现在列表中。

---

## 修改已有报告

直接编辑 `_reports/{代码}.md`，重新提交推送即可。

无需手动改 HTML，无需改 CSS，样式由 `_layouts/report.html` 统一控制。

---

## 模板统一

- `_layouts/report.html` — 全站统一模板（渐变标题、金色三问、信息网格、权重标签、裁决框、锚点跳转）
- `_config.yml` — Jekyll 配置（`permalink: /stock-:name.html`）
- `reports.json` — **需手动维护**（新增报告时插入条目，见 Step 2），首页列表数据源

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
