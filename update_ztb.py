#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新网站index.html - 涨停板方向整理部分
"""

import re

# 读取原文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新标题日期
content = content.replace(
    '<title>羿学交易智囊团 | 2026-04-21</title>',
    '<title>羿学交易智囊团 | 2026-04-22</title>'
)

# 2. 更新header日期
content = content.replace(
    '2026年4月22日 星期三 | 丙午年 壬辰月 丙寅日',
    '2026年4月23日 星期四 | 丙午年 壬辰月 丁卯日'
)

# 3. 新的涨停板梳理内容
new_ztb = '''<div class="ztb-section">
            <h2>📊 涨停板梳理（51只）</h2>
            <p style="color:#8b9dc3;margin-bottom:20px;font-size:0.95em;">方法论：龙头涨停→产业链拆解→找未启动环节→筛补涨标的 | 数据来源：同花顺涨停聚焦</p>
            
            <div class="ztb-grid">
                <!-- 方向1：光通信/光芯片 -->
                <div class="ztb-card" style="background: rgba(255,107,107,0.05); border: 1px solid rgba(255,107,107,0.3);">
                    <h3 style="color:#ff6b6b;">🔥 方向一：光通信/光芯片/CPO（8只）</h3>
                    <div class="logic">AI算力需求爆发→光模块升级800G/1.6T→上游光芯片/器件供不应求→国产替代加速</div>
                    <div class="chain">产业链：光芯片（长光华芯/三安光电）→ 光器件/光纤（永鼎股份/亨通光电）→ 光模块（先导科技/世维科技）→ CPO封装（光电股份）→ 数据中心分销（深圳华强）</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">长光华芯</span>
                                <span class="stock-code">688048</span>
                                <span class="stock-tag tag-s">龙头</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">20cm涨停，国产高功率激光芯片龙头</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">三安光电</span>
                                <span class="stock-code">600703</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">化合物半导体平台，磷化铟光芯片</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">永鼎股份</span>
                                <span class="stock-code">600105</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光通信全产业链，光芯片+光纤光缆</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">光电股份</span>
                                <span class="stock-code">600184</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光刻机+CPO双概念，军工光电背景</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">亨通光电</span>
                                <span class="stock-code">600487</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光纤光缆龙头，海缆第二曲线</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">深圳华强</span>
                                <span class="stock-code">000062</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">电子元器件分销龙头，数据中心+存储</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">先导科技</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光模块核心器件，叠加机器人概念</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">世维科技</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光模块封装</span>
                        </div>
                    </div>
                </div>
                
                <!-- 方向2：液冷/AI算力 -->
                <div class="ztb-card" style="background: rgba(255,107,107,0.05); border: 1px solid rgba(255,107,107,0.3);">
                    <h3 style="color:#ff6b6b;">🔥 方向二：液冷/AI算力（7只）</h3>
                    <div class="logic">AI服务器功耗突破10kW→液冷从可选项变刚需→英维克暴雷后错杀修复→真实需求仍在</div>
                    <div class="chain">产业链：液冷系统（安诺其/海德股份/冰川环境）→ 服务器（中科曙光）→ 算力租赁（杭氧股份）→ 配套（康盛股份/中持股份）</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">安诺其</span>
                                <span class="stock-code">300067</span>
                                <span class="stock-tag tag-s">龙头</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">20cm涨停，AI服务器+液冷双驱动，弹性最大</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">海德股份</span>
                                <span class="stock-code">000567</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">AI服务器液冷，绑定头部客户</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">冰川环境</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">液冷+核电双概念，设备供应商</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">杭氧股份</span>
                                <span class="stock-code">002430</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">算力租赁+空分设备，钢铁转型黑马</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中科曙光</span>
                                <span class="stock-code">603019</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">国产服务器龙头，智慧政务+算力</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中持股份</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">芯片+AI，技术积累</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">康盛股份</span>
                                <span class="stock-code">002418</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">液冷+家电，家电转型液冷黑马</span>
                        </div>
                    </div>
                </div>
                
                <!-- 方向3：一季报业绩 -->
                <div class="ztb-card">
                    <h3>👀 方向三：一季报业绩大增（7只）</h3>
                    <div class="logic">4月一季报密集披露→业绩超预期→市场重新定价→估值修复</div>
                    <div class="chain">业绩线为4月持续性较强的独立逻辑</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">诚志股份</span>
                                <span class="stock-code">000990</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">电子化学品+一季报增长</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">飞龙股份</span>
                                <span class="stock-code">002536</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">汽车热管理龙头，业绩大增</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">龙蟠科技</span>
                                <span class="stock-code">603906</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">磷酸铁锂+一季报增长</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">东山精密</span>
                                <span class="stock-code">002384</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">PCB+精密制造，业绩大增+AI</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">远东股份</span>
                                <span class="stock-code">600869</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">电缆+新能源，一季报增长</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">史丹利</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">复合肥龙头，业绩增长</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">杭电股份</span>
                                <span class="stock-code">600618</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">一季报增长，电线电缆</span>
                        </div>
                    </div>
                </div>
                
                <!-- 方向4：固态电池/储能 -->
                <div class="ztb-card">
                    <h3>👀 方向四：固态电池/储能/新能源（6只）</h3>
                    <div class="logic">宁德时代超级科技日催化→固态电池技术突破预期→储能装机增长</div>
                    <div class="chain">方向独立，与光通信/液冷不重叠</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">先惠技术</span>
                                <span class="stock-code">688155</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">固态电池设备，技术领先</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">科陆发展</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">储能+智慧能源，海外市场</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">翔丰华</span>
                                <span class="stock-code">300890</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">负极材料，硅基负极+快充</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">冠农科技</span>
                                <span class="stock-code">600251</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">光储+农业，转型黑马</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">水发燃气</span>
                                <span class="stock-code">603318</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">燃气轮机，分布式能源黑马</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">天原股份</span>
                                <span class="stock-code">002386</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">碳酸锂+氯碱，锂盐产能释放</span>
                        </div>
                    </div>
                </div>
                
                <!-- 方向5：重组/并购 -->
                <div class="ztb-card">
                    <h3>👀 方向五：重组/并购（4只）</h3>
                    <div class="logic">政策鼓励并购重组→上海/深圳多地出台支持政策→壳资源/低估值公司重组预期升温</div>
                    <div class="chain">独立逻辑，与市场主线无关</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">京投发展</span>
                                <span class="stock-code">600683</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">拟购资产，地产转型</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">苏州高新</span>
                                <span class="stock-code">600736</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">重组预期，国企改革</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">东呈时代</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">收购，产业整合</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">同益化工</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">重组，化工转型黑马</span>
                        </div>
                    </div>
                </div>
                
                <!-- 方向6：有色金属/新材料 -->
                <div class="ztb-card">
                    <h3>👀 方向六：有色金属/新材料（5只）</h3>
                    <div class="logic">地缘风险+供给约束→锗/稀土/铜等战略资源价格上涨→上游矿企受益</div>
                    <div class="chain">防御性方向，与地缘风险相关</div>
                    <div class="stock-list">
                        <h4>📋 涨停标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">云南锗业</span>
                                <span class="stock-code">002428</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">锗矿龙头，半导体材料，地缘风险受益</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">沃尔核材</span>
                                <span class="stock-code">002130</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">铜连接+核电，铜价上涨受益</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">江苏博云</span>
                                <span class="stock-code">-</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">20cm涨停，改性塑料，国产替代黑马</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">金徽股份</span>
                                <span class="stock-code">603132</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">黄金，避险需求+金价上涨</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中信金属</span>
                                <span class="stock-code">601061</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">稀土+贸易，稀土出口管制受益</span>
                        </div>
                    </div>
                </div>
                
                <!-- 重点关注 -->
                <div class="ztb-card" style="background: rgba(255,193,7,0.05); border: 1px solid rgba(255,193,7,0.3);">
                    <h3 style="color:#ffd700;">⭐ 今日重点（按题材强度排序）</h3>
                    <div class="stock-list">
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">1. 光通信/光芯片</span>
                                <span class="stock-tag tag-s">8只涨停</span>
                            </div>
                            <span style="color:#ffd700;font-size:0.8em">AI算力+国产替代双驱动，最强方向</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">2. 液冷/AI算力</span>
                                <span class="stock-tag tag-a">7只涨停</span>
                            </div>
                            <span style="color:#ffd700;font-size:0.8em">英维克错杀修复+真实需求，强度第二</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">3. 一季报业绩</span>
                                <span class="stock-tag tag-a">7只涨停</span>
                            </div>
                            <span style="color:#ffd700;font-size:0.8em">4月业绩线持续性强，独立逻辑</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">4. 长光华芯</span>
                                <span class="stock-code">688048</span>
                                <span class="stock-tag tag-s">20cm</span>
                            </div>
                            <span style="color:#ffd700;font-size:0.8em">光芯片龙头，国产替代核心标的</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">5. 安诺其</span>
                                <span class="stock-code">300067</span>
                                <span class="stock-tag tag-s">20cm</span>
                            </div>
                            <span style="color:#ffd700;font-size:0.8em">AI服务器+液冷双驱动，弹性最大</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>'''

# 找到旧的ztb-section并替换
pattern = r'<div class="ztb-section">.*?</div>\s*</div>\s*(<div class="verification-section">)'
match = re.search(pattern, content, re.DOTALL)

if match:
    old_ztb = match.group(0)
    # 替换：新内容 + 保留verification-section的开头
    new_content = content.replace(old_ztb, new_ztb + '\n        \n        <div class="verification-section">')
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 网站更新成功！")
    print(f"📊 标题日期已更新：2026-04-22")
    print(f"📊 Header日期已更新：2026-04-23")
    print(f"📊 涨停板梳理已更新：6个方向，37只标的")
else:
    print("❌ 未找到涨停板梳理部分，请检查HTML结构")
