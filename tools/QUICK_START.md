# 🚀 预期差详细页快速生成指南 V2

## 一键自动更新流程（30秒搞定）

### 第一步：准备数据

复制模板并填写当天数据：
```bash
cp data/template.json data/2026-03-21.json
# 编辑 data/2026-03-21.json，填写5个预期差
```

### 第二步：预览检查（推荐）

```bash
python3 tools/auto_update_gaps.py data/2026-03-21.json --preview
```

### 第三步：一键更新

```bash
python3 tools/auto_update_gaps.py data/2026-03-21.json
```

这一步会自动：
- ✅ 生成清单条目HTML
- ✅ 生成详细页HTML
- ✅ 自动替换index.html中的对应区域
- ✅ 保存更新后的index.html

### 第四步：推送更新

```bash
git add index.html
git commit -m "更新: 2026-03-21 预期差清单"
git push origin main
```

---

## 关键字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 唯一标识，英文无空格 | `Hormuz`、`hk`、`storage2` |
| `title` | 预期差标题 | `霍尔木兹海峡封锁规模` |
| `stocks` | 相关标的 | `石油、航运、军工` |
| `size` | 大小 | `large`（大）、`medium`（中）、`small`（小）|
| `stars` | 星级 | `⭐⭐⭐⭐⭐` |
| `tag` | 标签文字 | `地缘政治` |
| `tag_class` | 标签样式 | `policy`（红）、`highlight`（黄）、空（灰）|
| `summary` | 一句话描述 | `市场认知：短期事件 → 真实：可能持续数周` |
| `icon` | 标题图标 | `🛢️`、`🇭🇰`、`💾` |

---

## 图标速查表

| 类型 | 图标 |
|------|------|
| 能源/石油 | 🛢️ |
| 港股 | 🇭🇰 |
| 芯片/存储 | 💾 |
| 电池/新能源 | 🔋 |
| 航天/卫星 | 🚀 |
| 金融/银行 | 🏦 |
| 宏观/经济 | 📉 |
| 政策/监管 | 📜 |
| AI/科技 | 🤖 |
| 黄金/防御 | 🥇 |

---

## 工作原理

index.html 中包含标记注释：

```html
<!-- GAP_LIST_START -->  <!-- 预期差清单开始 - 自动生成区域 -->
  <!-- 这里的内容会被自动替换 -->
<!-- GAP_LIST_END -->    <!-- 预期差清单结束 - 自动生成区域 -->

<!-- GAP_DETAIL_PAGES_START -->  <!-- 预期差详细页开始 - 自动生成区域 -->
  <!-- 这里的内容会被自动替换 -->
<!-- GAP_DETAIL_PAGES_END -->    <!-- 预期差详细页结束 - 自动生成区域 -->
```

脚本会读取JSON数据，生成HTML，然后自动替换这两个标记区域之间的内容。

---

## 完整文件结构

```
yixue-dashboard/
├── index.html              # 主页面（自动更新）
├── data/
│   ├── template.json       # 数据模板
│   └── 2026-03-20.json     # 每日数据（示例）
├── tools/
│   ├── auto_update_gaps.py # 一键更新脚本 ⭐
│   └── QUICK_START.md      # 本文件
└── templates/
    └── gap-detail-template.html # HTML模板参考
```

---

## 故障排除

### 如果更新后页面显示异常

1. 检查JSON格式是否正确（可以用在线JSON验证器）
2. 重新运行预览模式，查看生成的HTML
3. 手动查看index.html，确认标记注释是否完整

### 如果需要回滚

```bash
git checkout HEAD~1 index.html  # 回滚到上一个版本
git checkout HEAD index.html    # 恢复当前版本
```

---

*系统版本: V2.0 - 一键自动更新*
