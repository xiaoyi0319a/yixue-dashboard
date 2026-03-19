#!/usr/bin/env python3
"""
预期差详细页全自动生成器
使用方法: python3 auto_update_gaps.py data/2026-03-20.json

功能：
1. 读取JSON数据
2. 自动生成清单和详细页HTML
3. 自动替换index.html中的对应区域
4. 保存更新后的index.html
"""

import json
import sys
import re
from datetime import datetime

# 模板配置
TEMPLATES = {
    "list_item": '''                        <div class="gap-item" onclick="showDetail('{id}')">
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
''',
    
    "detail_page": '''        <!-- 详情页：{id} -->
        <div id="detail-{id}" class="detail-page">
            <span class="back-btn" onclick="backToMain()">← 返回清单</span>
            
            <div class="header">
                <h1>{icon} {title}</h1>
                <p>相关标的：{stocks}</p>
                <p style="color:#ef4444;font-size:12px;margin-top:8px;">⚠️ 不是买卖依据，不要轻信！买者自负！</p>
            </div>

            <div class="detail-section">
                <h3>🌎 隔夜美股信号</h3>
{us_signal_items}
            </div>

            <div class="detail-section">
                <h3>📊 当前市场共识</h3>
                <ul>
{consensus_items}
                </ul>
            </div>

            <div class="detail-section">
                <h3>📋 实际信息</h3>
                <ul>
{facts_items}
                </ul>
            </div>

            <div class="detail-section">
                <h3>🔍 预期差分析</h3>
                <table style="width:100%;border-collapse:collapse;margin-top:12px;">
                    <tr style="background:rgba(56,189,248,0.1);">
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">维度</th>
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">市场假设</th>
                        <th style="padding:10px;text-align:left;border:1px solid rgba(148,163,184,0.2);">实际情况</th>
                    </tr>
{analysis_rows}
                </table>
            </div>

            <div class="detail-section">
                <h3>🎯 预期差大小：<span style="color:{color};">{stars}</span></h3>
                <ul>
{conclusion_items}
                </ul>
            </div>

            <div class="detail-section">
                <h3>📝 候选股池筛选</h3>
                <ul>
{candidate_pool_items}
                </ul>
            </div>

            <div class="detail-section">
                <h3>✅ 验证节点</h3>
                <ul>
{validation_items}
                </ul>
            </div>

            <div class="detail-section">
                <h3>📈 最终推荐（按预期差强度排序）</h3>
                <ul>
{stocks_detail_items}
                </ul>
                <p style="color:#94a3b8;font-size:12px;margin-top:12px;">⚠️ 个股仅供参考，不构成投资建议</p>
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

def generate_stocks_detail_items(stocks_detail_list):
    """生成个股详情列表"""
    items = []
    for stock in stocks_detail_list:
        stars = stock.get('stars', '')
        logic = stock.get('logic', '')
        items.append(f'                    <li style="margin-bottom:16px;"><strong>{stock["name"]} ({stock["code"]})</strong> <span style="color:#fbbf24;">{stars}</span><br/><span style="color:#94a3b8;font-size:13px;margin-left:20px;display:block;margin-top:6px;">{logic}</span></li>')
    return '\n'.join(items)

def generate_candidate_pool_items(candidate_pool_list):
    """生成候选股池表格"""
    items = []
    for stock in candidate_pool_list:
        status = stock.get('status', '')
        reason = stock.get('reason', '')
        # 根据状态设置颜色
        if '✅' in status:
            color = '#22c55e'
        elif '⚠️' in status:
            color = '#fbbf24'
        elif '❌' in status:
            color = '#ef4444'
        else:
            color = '#94a3b8'
        items.append(f'                    <li style="margin-bottom:16px;"><strong>{stock["name"]} ({stock["code"]})</strong> <span style="color:{color};font-weight:bold;">{status}</span><br/><span style="color:#94a3b8;font-size:13px;margin-left:20px;display:block;margin-top:6px;">{reason}</span></li>')
    return '\n'.join(items)

def generate_us_signal_items(us_signal):
    """生成美股信号展示"""
    if not us_signal:
        return '                <p style="color:#64748b;">暂无美股信号关联</p>'
    
    indicator = us_signal.get('indicator', '')
    ticker = us_signal.get('ticker', '')
    change = us_signal.get('change', '')
    price = us_signal.get('price', '')
    trigger = us_signal.get('trigger', '')
    update_time = us_signal.get('update_time', '')
    mapping_logic = us_signal.get('mapping_logic', '')
    
    # 判断涨跌颜色
    change_color = '#22c55e' if '+' in change else '#ef4444'
    
    html = f'''                <div style="background:rgba(56,189,248,0.1);padding:12px;border-radius:8px;margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="font-weight:bold;">{indicator} ({ticker})</span>
                        <span style="color:{change_color};font-weight:bold;">{change}</span>
                    </div>
                    <div style="color:#64748b;font-size:13px;margin-bottom:8px;">
                        价格: {price} | 更新时间: {update_time}
                    </div>
                    <div style="color:#e2e8f0;font-size:14px;margin-bottom:8px;">
                        <strong>触发事件:</strong> {trigger}
                    </div>
                    <div style="color:#fbbf24;font-size:13px;">
                        <strong>→ 映射逻辑:</strong> {mapping_logic}
                    </div>
                </div>'''
    return html

def get_size_color(size):
    """根据预期差大小返回颜色"""
    colors = {
        "large": "#f87171",
        "medium": "#fbbf24",
        "small": "#22c55e"
    }
    return colors.get(size, "#fbbf24")

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

def generate_detail_page(gap):
    """生成单个详细页HTML"""
    return TEMPLATES["detail_page"].format(
        id=gap['id'],
        icon=gap.get('icon', '📊'),
        title=gap['title'],
        stocks=gap['stocks'],
        consensus_items=generate_consensus_items(gap['consensus']),
        facts_items=generate_facts_items(gap['facts']),
        analysis_rows=generate_analysis_rows(gap['analysis']),
        color=get_size_color(gap['size']),
        stars=gap['stars'],
        conclusion_items=generate_conclusion_items(gap['conclusion']),
        validation_items=generate_validation_items(gap['validation']),
        us_signal_items=generate_us_signal_items(gap.get('us_signal')),
        candidate_pool_items=generate_candidate_pool_items(gap.get('candidate_pool', [])),
        stocks_detail_items=generate_stocks_detail_items(gap.get('stocks_detail', []))
    )

def update_index_html(json_file, index_file='index.html'):
    """更新index.html文件"""
    
    # 读取JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    gaps = data.get('gaps', [])
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    print(f"📅 处理日期: {date}")
    print(f"📊 预期差数量: {len(gaps)}")
    
    # 生成清单HTML
    list_html = ''.join([generate_list_item(gap) for gap in gaps])
    
    # 生成详细页HTML
    detail_html = '\n'.join([generate_detail_page(gap) for gap in gaps])
    
    # 读取index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换清单区域
    list_pattern = r'(<!-- GAP_LIST_START -->.*?<!-- 预期差清单开始 - 自动生成区域 -->).*?(<!-- GAP_LIST_END -->)'
    list_replacement = r'\1\n' + list_html + r'                        \2'
    content = re.sub(list_pattern, list_replacement, content, flags=re.DOTALL)
    
    # 替换详细页区域
    detail_pattern = r'(<!-- GAP_DETAIL_PAGES_START -->.*?<!-- 预期差详细页开始 - 自动生成区域 -->).*?(<!-- GAP_DETAIL_PAGES_END -->)'
    detail_replacement = r'\1\n' + detail_html + r'        \2'
    content = re.sub(detail_pattern, detail_replacement, content, flags=re.DOTALL)
    
    # 保存更新后的index.html
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已更新: {index_file}")
    print(f"📝 生成的清单条目: {len(gaps)} 个")
    print(f"📄 生成的详细页: {len(gaps)} 个")
    
    return True

def preview_changes(json_file):
    """预览生成的HTML（不保存）"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    gaps = data.get('gaps', [])
    
    print("=" * 60)
    print("📋 清单预览")
    print("=" * 60)
    for gap in gaps:
        print(f"\n🎯 {gap['title']}")
        print(f"   标的: {gap['stocks']}")
        print(f"   星级: {gap['stars']}")
    
    print("\n" + "=" * 60)
    print("📄 详细页预览（第一个）")
    print("=" * 60)
    if gaps:
        print(generate_detail_page(gaps[0])[:1000] + "...")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  预览模式: python3 auto_update_gaps.py data/2026-03-20.json --preview")
        print("  更新模式: python3 auto_update_gaps.py data/2026-03-20.json")
        print("\n提示: 先使用预览模式检查，确认无误后再更新")
        return
    
    json_file = sys.argv[1]
    preview_mode = '--preview' in sys.argv
    
    try:
        if preview_mode:
            print("🔍 预览模式 - 不会修改index.html\n")
            preview_changes(json_file)
        else:
            print("🚀 更新模式 - 将自动更新index.html\n")
            update_index_html(json_file)
            print("\n💡 提示: 运行以下命令推送到GitHub:")
            print("   git add index.html")
            print(f"   git commit -m \"更新: {datetime.now().strftime('%Y-%m-%d')} 预期差清单\"")
            print("   git push origin main")
    
    except FileNotFoundError as e:
        print(f"❌ 错误: 找不到文件 - {e}")
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON格式错误 - {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
