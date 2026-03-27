#!/bin/bash

# 创建简化版报告页面的函数
create_report() {
    code=$1
    name=$2
    rating=$3
    score=$4
    logic=$5
    
    filename="20260327-${code}-${name}.html"
    
    cat > "$filename" << HTML
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${name}(${code}) | 深度研报 | 2026-03-27</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --border: #30363d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-yellow: #d29922;
            --accent-purple: #a371f7;
            --accent-cyan: #39c5cf;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.8;
        }
        .nav {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
        }
        .nav a {
            color: var(--accent-blue);
            text-decoration: none;
            font-size: 14px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 32px 24px;
        }
        .header {
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
        }
        .header h1 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        .header .code {
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 16px;
        }
        .rating {
            display: inline-block;
            padding: 6px 20px;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 600;
        }
        .rating.s {
            background: rgba(63, 185, 80, 0.15);
            color: var(--accent-green);
        }
        .rating.a {
            background: rgba(210, 153, 34, 0.15);
            color: var(--accent-yellow);
        }
        .section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .section h2 {
            font-size: 16px;
            color: var(--accent-cyan);
            margin-bottom: 16px;
        }
        .section p {
            color: var(--text-secondary);
            line-height: 1.8;
        }
        .score-box {
            text-align: center;
            padding: 24px;
        }
        .score-box .number {
            font-size: 48px;
            font-weight: 700;
            color: var(--accent-blue);
        }
        .score-box .label {
            color: var(--text-secondary);
            margin-top: 8px;
        }
        .back-link {
            display: inline-block;
            margin-top: 32px;
            padding: 12px 24px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--accent-blue);
            text-decoration: none;
        }
        .notice {
            background: var(--bg-secondary);
            border-left: 3px solid var(--accent-yellow);
            padding: 16px 20px;
            margin: 24px 0;
            font-size: 13px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="nav">
        <a href="../index.html">← 返回仪表盘</a>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>${name}</h1>
            <div class="code">${code}</div>
            <div class="rating ${rating}">${rating}级 | ${score}分</div>
        </div>
        
        <div class="section">
            <h2>🎯 核心预期差</h2>
            <p>${logic}</p>
        </div>
        
        <div class="notice">
            <strong>📋 详细研报</strong><br>
            本页面为简化版报告，完整深度研报包含：产业链分析、财务数据、风险评估、验证节点等详细内容。
            <br><br>
            请查阅：<a href="../directions/20260327-0${direction}.html" style="color: var(--accent-blue);">方向详细页</a> 获取完整分析。
        </div>
        
        <a href="../index.html" class="back-link">← 返回仪表盘</a>
    </div>
</body>
</html>
HTML
}

# ASIC方向 (direction=1)
create_report "688521" "芯原股份" "s" "8.4" "国内IP授权龙头，2025年新签订单59.6亿（+103%），AI算力订单占比超73%，2026年预计扭亏为盈。市场仍按传统IP授权业务估值，未充分反映ASIC定制业务爆发。" 1
create_report "688220" "翱捷科技" "a" "7.8" "Cat.1bis蜂窝物联网领域市占率接近50%，ASIC在手订单充足，2025年亏损收窄42.38%，预计2026-2027年扭亏。" 1
create_report "688691" "灿芯股份" "a" "7.2" "中芯国际N+1/N+2制程核心配套商，阿里/字节AI芯片代工链核心，在手订单9亿元。" 1
create_report "688262" "国芯科技" "a" "7.0" "国产嵌入式CPU龙头，RISC-V技术领先，比亚迪/奇瑞/吉利供应商，车规级芯片放量。" 1
create_report "300613" "富瀚微" "a" "6.5" "视频编解码SoC芯片龙头，智慧物联+智慧车行双轮驱动，车载芯片（DVR/ISP）放量。" 1

# HBM方向 (direction=2)
create_report "000021" "深科技" "a" "7.8" "国内唯一HBM封测能力，封装良率98%，长鑫存储/长江存储核心封测伙伴，2025年Q1净利润同比+46.91%。" 2
create_report "300475" "香农芯创" "a" "7.4" "SK海力士HBM国内独家代理，分销协议稳定，2025年Q1营收同比增长243%，存货增值确定性强。" 2
create_report "001309" "德明利" "a" "7.2" "存储模组小盘弹性标的，企业级SSD突破（2024年同比+666%），涨价周期毛利率修复空间大。" 2
create_report "688008" "澜起科技" "a" "7.0" "DDR5接口芯片（RCD/DB）寡头，全球市占率领先，AI服务器刚需，2025年Q1净利润+135%。" 2
create_report "301308" "江波龙" "a" "6.5" "企业级存储龙头，2024年企业存储业务同比+666%，Lexar品牌全球知名。" 2

# 磷化铟方向 (direction=3)
create_report "002428" "云南锗业" "s" "8.4" "国内唯一量产磷化铟衬底A股公司，市占率80%，2025年Q1净利润同比+188.73%扭亏为盈。" 3
create_report "600206" "有研新材" "a" "7.8" "央企背景，6英寸磷化铟衬底良率60%，与中际旭创合作推进国产替代，成本优势显著。" 3
create_report "688048" "长光华芯" "a" "7.6" "100G EML年产能500万颗，与中际旭创签订3年6亿元订单，2025年H1扭亏。" 3
create_report "002281" "光迅科技" "a" "7.2" "唯一覆盖光芯片-器件-模块全产业链，IDM产线2025年投产，全球光器件TOP5。" 3
create_report "688498" "源杰科技" "a" "6.8" "磷化铟激光器芯片IDM龙头，50G EML通过英伟达认证（国内首家），毛利率60%+。" 3

echo "15只标的报告页面创建完成！"
