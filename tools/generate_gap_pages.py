#!/usr/bin/env python3
"""
预期差详细页生成器
使用方法: python3 generate_gap_pages.py
"""

import json
from datetime import datetime

# 模板配置
TEMPLATES = {
    "header": '''        <!-- 详情页：{id} -->
        <div id="detail-{id}" class="detail-page">
            <span class="back-btn" onclick="backToMain()">← 返回清单</span>
            
            <div class="header">
                <h1>{icon} {title}</h1>
                <p>相关标的：{stocks}</p>
                <p style="color:#ef4444;font-size:12px;margin-top:8px;">⚠️ 不是买卖依据，不要轻信！买者自负！</p>
            </div>
''',
    
    "consensus": '''            <div class="detail-section">
                <h3>📊 当前市场共识</h3>
                <ul>
{items}
                </ul>
            </div>
''',
    
    "facts": '''            <div class="detail-section">
                <h3>📋 实际信息</h3>
                <ul>
{items}
                </ul>
            </div>
''',
    
    "analysis": '''            <div class="detail-section">
                <h3>🔍 预期差分析</h3>
                <table style="width:100%;border-collapse:collapse;margin-top:12px;">
                    <tr style="background:rgba(56,189,248,0.1);">
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">维度</th>
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">市场假设</th>
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">实际情况</th>
                    </tr>
{rows}
                </table>
            </div>
''',
    
    "conclusion": '''            <div class="detail-section">
                <h3>🎯 预期差大小：<span style="color:{color};">{stars}</span></h3>
                <ul>
{items}
                </ul>
            </div>
''',
    
    "validation": '''            <div class="detail-section">
                <h3>✅ 验证节点</h3>
                <ul>
{items}
                </ul>
            </div>
        </div>
''',
    
    "list_item": '''                    <div class="gap-item" onclick="showDetail('{id}')">
                        <div class="gap-header">
                            <div>
                                <span class="gap-title">{title}</span>
                                <div class="gap-stocks">{stocks}</div>
                            </div>
                            <span class="gap-size {size}">预期差：{stars}</span>
                        </div>
                        <div style="margin-top:8px;">
                            <span class="tag {tag_class}">{tag}</span>
                            <span style="color:#64748b;font-size:12px;">{summary}</span>
                            <span class="gap-arrow" style="float:right;">→</span>
                        </div>
                    </div>
'''
}

def generate_consensus_items(consensus_list):
    """生成市场共识列表"""
    return '\n'.join([f'                    <li>{item}</li>' for item in consensus_list])

def generate_facts_items(facts_list):
    """生成实际信息列表"""
    items = []
    for fact in facts_list:
        if isinstance(fact, dict):
            items.append(f'                    <li><strong>{fact["time"]}</strong>：{fact["content"]}</li>')
        else:
            items.append(f'                    <li>{fact}</li>')
    return '\n'.join(items)

def generate_analysis_rows(analysis_list):
    """生成预期差分析表格行"""
    rows = []
    for item in analysis_list:
        row = f'''                    <tr>
                        <td style="padding:10px;border:1px solid rgba(148,163,184,0.2);"><strong>{item['dimension']}</strong></td>
                        <td style="padding:10px;border:1px solid rgba(148,163,184,0.2);">{item['market']}</td>
                        <td style="padding:10px;border:1px solid rgba(148,163,184,0.2);">{item['reality']}</td>
                    </tr>'''
        rows.append(row)
    return '\n'.join(rows)

def generate_conclusion_items(conclusion_list):
    """生成结论列表"""
    return '\n'.join([f'                    <li>{item}</li>' for item in conclusion_list])

def generate_validation_items(validation_list):
    """生成验证节点列表"""
    return '\n'.join([f'                    <li>{item}</li>' for item in validation_list])

def get_size_color(size):
    """根据预期差大小返回颜色"""
    colors = {
        "large": "#f87171",   # 红色
        "medium": "#fbbf24",  # 黄色
        "small": "#22c55e"    # 绿色
    }
    return colors.get(size, "#fbbf24")

def generate_detail_page(gap):
    """生成单个详细页HTML"""
    parts = []
    
    # Header
    parts.append(TEMPLATES["header"].format(
        id=gap['id'],
        icon=gap.get('icon', '📊'),
        title=gap['title'],
        stocks=gap['stocks']
    ))
    
    # 市场共识
    parts.append(TEMPLATES["consensus"].format(
        items=generate_consensus_items(gap['consensus'])
    ))
    
    # 实际信息
    parts.append(TEMPLATES["facts"].format(
        items=generate_facts_items(gap['facts'])
    ))
    
    # 预期差分析
    parts.append(TEMPLATES["analysis"].format(
        rows=generate_analysis_rows(gap['analysis'])
    ))
    
    # 结论
    parts.append(TEMPLATES["conclusion"].format(
        color=get_size_color(gap['size']),
        stars=gap['stars'],
        items=generate_conclusion_items(gap['conclusion'])
    ))
    
    # 验证节点
    parts.append(TEMPLATES["validation"].format(
        items=generate_validation_items(gap['validation'])
    ))
    
    return '\n'.join(parts)

def generate_list_item(gap):
    """生成清单中的条目HTML"""
    return TEMPLATES["list_item"].format(
        id=gap['id'],
        title=gap['title'],
        stocks=gap['stocks'],
        size=gap['size'],
        stars=gap['stars'],
        tag=gap['tag'],
        tag_class=gap.get('tag_class', ''),
        summary=gap.get('summary', '')
    )

def main():
    """主函数 - 示例数据"""
    
    # 示例：今日预期差数据
    today_gaps = [
        {
            "id": "Hormuz",
            "title": "霍尔木兹海峡封锁规模",
            "stocks": "石油、航运、军工",
            "size": "large",
            "stars": "⭐⭐⭐⭐⭐",
            "tag": "地缘政治",
            "tag_class": "policy",
            "summary": "市场认知：短期事件 → 真实：可能持续数周",
            "icon": "🛢️",
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
            "conclusion": [
                "若封锁持续数周，油价可能冲击120-150美元",
                "全球通胀压力骤增，央行政策空间被压缩",
                "航运、军工、黄金同步受益"
            ],
            "validation": [
                "每日：霍尔木兹海峡通航情况",
                "每周：伊以冲突进展",
                "持续关注：国际油价走势"
            ]
        }
    ]
    
    # 生成详细页HTML
    print("=== 生成的详细页HTML ===")
    for gap in today_gaps:
        print(generate_detail_page(gap))
        print("\n" + "="*50 + "\n")
    
    # 生成清单条目HTML
    print("=== 生成的清单条目HTML ===")
    for gap in today_gaps:
        print(generate_list_item(gap))

if __name__ == "__main__":
    main()
