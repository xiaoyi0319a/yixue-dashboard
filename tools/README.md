# 预期差详细页自动生成系统

## 系统说明
自动根据每日预期差清单生成对应的详细页HTML代码

## 文件结构
```
yixue-dashboard/
├── tools/
│   └── gap-page-generator.js    # 生成器脚本
├── templates/
│   └── gap-detail-template.html # 详细页模板
└── data/
    └── daily-gaps.json          # 每日预期差数据
```

## 使用方法

### 1. 准备数据（JSON格式）

```json
{
  "date": "2026-03-20",
  "gaps": [
    {
      "id": " Hormuz",
      "title": "霍尔木兹海峡封锁规模",
      "stocks": "石油、航运、军工",
      "size": "large",
      "stars": "⭐⭐⭐⭐⭐",
      "tag": "地缘政治",
      "tagClass": "policy",
      "marketView": "短期事件 → 真实：可能持续数周",
      
      "consensus": [
        "霍尔木兹海峡封锁是短期事件，几天内就会恢复",
        "伊朗不敢长期封锁，担心军事报复",
        "油价上涨是情绪性炒作，很快回落"
      ],
      "facts": [
        {"time": "3月19日", "content": "霍尔木兹海峡实质性中断，约30%全球石油运输受影响"},
        {"time": "WTI原油", "content": "涨至98美元/桶，布伦特原油涨至105美元/桶"},
        {"time": "A股反应", "content": "首华燃气、通源石油涨停，油气板块逆势走强"},
        {"time": "持续时间", "content": "伊以冲突持续升级，封锁可能持续数周而非数日"}
      ],
      "analysis": [
        {"dimension": "持续时间", "market": "短期事件，几天恢复", "reality": "伊以冲突升级，可能持续数周"},
        {"dimension": "影响范围", "market": "局部影响，可控", "reality": "30%全球石油运输中断，供给冲击巨大"}
      ],
      "conclusion": "若封锁持续数周，油价可能冲击120-150美元；全球通胀压力骤增",
      "validation": ["每日：霍尔木兹海峡通航情况", "每周：伊以冲突进展", "持续关注：国际油价走势"]
    }
  ]
}
```

### 2. 运行生成器

```bash
node tools/gap-page-generator.js data/daily-gaps.json
```

### 3. 输出

生成 `output/gap-pages-2026-03-20.html`，复制到 index.html 中

## 快速手动生成（今日使用）

如果不想用脚本，可以用以下模板手动填写：

