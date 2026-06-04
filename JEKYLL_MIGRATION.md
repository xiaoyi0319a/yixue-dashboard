# 报告库Jekyll迁移完整记录

> 迁移日期：2026-05-31
> 迁移人：小羿
> 涉及报告：37只

---

## 一、迁移背景

### 原有问题
1. **样式碎片化** — 37份报告各自独立HTML，CSS各写各的，排版不一致
2. **复制粘贴地狱** — 新增报告要复制模板、手动改所有数据，易错
3. **内容混在样式里** — 数据和HTML标签缠在一起，改一句话要翻几百行
4. **版本管理混乱** — 全局修改（如加新section）要改37遍

### 方案选择（C：Markdown + Jekyll）
- GitHub Pages原生支持Jekyll
- 报告内容用Markdown写，模板统一控制样式
- 新增报告只需写Markdown→push→自动渲染
- 老链接URL保持不变

---

## 二、迁移过程

### Step 1：搭建Jekyll架构
| 文件 | 作用 |
|:-----|:-----|
| `_config.yml` | Jekyll配置，启用`_reports/`集合，permalink规则 |
| `_layouts/report.html` | 全站统一模板（渐变标题、大白话三问、信息网格、权重标签、裁决框） |
| `_reports/` | Markdown报告存放目录 |
| `reports.json` | 自动从Jekyll集合生成，无需手动维护 |

### Step 2：批量迁移36只报告（脚本化）
```bash
# 提取HTML中的元数据和body内容
# 生成Markdown文件（YAML frontmatter + HTML内容）
# 删除原HTML文件
```

**迁移结果**：
- 29只成功自动迁移
- 7只因标题格式不同需手动处理
- 总计37只全部完成

### Step 3：修复两大问题

#### 问题1：HTML被当作代码块显示（黄色高亮）
**现象**：页面显示原始HTML标签而非渲染后的内容
**根因**：frontmatter后的HTML内容有8空格缩进，Jekyll的Markdown处理器把缩进HTML当作代码块
**修复**：
```bash
# 去除所有frontmatter后的前导缩进
for file in _reports/*.md; do
    sed -i 's/^        //' "$file"  # 去除8空格缩进
done
```

#### 问题2：部分报告卡片无标签
**现象**：reports.html中部分卡片不显示概念标签
**根因**：`reports.json`的`tags`来自`subtitle`字段按`·`拆分，10只报告的`subtitle`在迁移时为空
**修复**：补充10只报告的subtitle：
- 000899 赣能股份：电力 · 火电 · 资产注入 · 算电协同
- 300163 先锋新材：建筑节能 · 新材料 · 并购重组
- 300176 鸿特科技：汽车零部件 · 压铸 · 新能源
- 300204 舒泰神：创新药 · 生物医药 · 重组蛋白
- 300234 开尔新材：新材料 · 珐琅板 · 绿色建筑
- 300266 兴源环境：环保 · 水处理 · 生态修复
- 300300 海峡创新：智慧城市 · 数字医疗 · 台湾概念
- 300478 杭州高新：新材料 · 电缆料 · 并购重组
- 300807 天迈科技：车联网 · 智能公交 · 无人驾驶
- 301057 汇隆新材：新材料 · 纤维 · 色母粒

---

## 三、新增报告流程（3步）

### 1. 创建Markdown文件
在 `_reports/` 目录下新建文件，命名：`{股票代码}.md`

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

**YAML字段说明**：
| 字段 | 必填 | 说明 |
|:-----|:----:|:-----|
| `code` | ✅ | 6位股票代码 |
| `title` | ✅ | 公司名称 |
| `subtitle` | ✅ | 概念标签（用`·`分隔），决定reports.json中的tags |
| `date` | ✅ | 分析日期（YYYY-MM-DD） |
| `version` | ✅ | 分析版本（如V4.3） |
| `analyst` | ✅ | 分析师 |
| `data_date` | 可选 | 数据截止日期 |

**⚠️ 关键规则**：
- `subtitle` 不能为空，否则reports.json中tags为空数组，卡片不显示标签
- 内容使用HTML标签（`<div class="section">`等），不要用缩进（会被当作代码块）
- 内容紧贴frontmatter，不要空行后缩进

### 2. 提交推送
```bash
cd /root/.openclaw/workspace/yixue-dashboard
git add _reports/688400.md
git commit -m "新增报告：凌云光 688400"
git push
```

### 3. 自动生效
GitHub Pages会在1-2分钟内自动构建，新报告访问地址：
```
https://xiaoyi0319a.github.io/yixue-dashboard/stock-688400.html
```

---

## 四、修改已有报告

直接编辑 `_reports/{代码}.md`，重新提交推送即可。

**无需**：改HTML、改CSS、改reports.json
**样式由** `_layouts/report.html` **统一控制**

---

## 五、模板统一

| 模板文件 | 作用 |
|:---------|:-----|
| `_layouts/report.html` | 单页报告模板（渐变标题、大白话三问区块、信息网格、权重标签、裁决框、锚点跳转） |
| `_config.yml` | Jekyll配置（permalink: `/stock-:name.html`） |
| `reports.json` | 自动生成，从所有报告的YAML frontmatter提取元数据 |

---

## 六、新旧对比

| 维度 | 旧版（37个独立HTML） | 新版（Jekyll Markdown） |
|:-----|:------|:------|
| 新增报告 | 复制模板→改37处数据→易错 | 写Markdown→3步提交 |
| 样式更新 | 改37个文件 | 改1个模板文件 |
| 版本管理 | 混乱 | Git记录清晰 |
| 内容分离 | HTML+CSS+内容混在一起 | 内容纯文本，样式统一 |
| 自动化 | 手动维护reports.json | 自动生成 |
| URL兼容性 | — | 完全保持原URL |

---

## 七、验证清单（新增/修改报告后）

- [ ] Markdown文件命名正确（`{代码}.md`）
- [ ] YAML frontmatter格式正确（`---`开头结尾）
- [ ] `subtitle` 不为空（用`·`分隔标签）
- [ ] 内容无缩进（紧贴frontmatter，不要用空格/制表符开头）
- [ ] `git push` 成功
- [ ] 等待1-2分钟后访问 `stock-{代码}.html` 验证
- [ ] 检查reports.json是否正确包含新报告
- [ ] 检查reports.html卡片是否正确显示标签

---

*文档版本：V1.0*
*创建日期：2026-05-31*
*维护人：小羿*
