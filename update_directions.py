#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

os.chdir('/root/.openclaw/workspace/yixue-dashboard')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Part 1: lines 0-314 (before us-mapping-section)
# Part 2: new directions section (replaces lines 315-665)
# Part 3: lines 665+ (ztb-section onward)

part1 = lines[:314]  # up to line 314 (0-indexed 313), before us-mapping

new_directions = '''        <div class="directions-section">
            <h2>📰 重要新闻整理方向（6个）</h2>
            <p style="color:#8b9dc3;margin-bottom:20px;font-size:0.95em;">数据来源：同花顺Wind万得陆家嘴早餐 + 同花顺要闻 + 6维度信息差挖掘 + iFinD验证</p>
            <div class="direction-grid">
                <div class="direction-card hot">
                    <span class="tag tag-hot">🔥 重点看</span>
                    <h3>光伏反内卷/供给侧改革</h3>
                    <p>工信部、发改委、市场监管总局、能源局<strong>四部门联合</strong>召开光伏座谈会，部署治理"内卷式"竞争。推进产能调控、兼并重组、价格执法等综合治理。光伏板块长期低迷，供给侧改革预期差显著。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">隆基绿能</span>
                                <span class="stock-code">601012</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">单晶硅片全球龙头，市占率30%+，-0.23%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">通威股份</span>
                                <span class="stock-code">600438</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">硅料+电池片双龙头，成本全球最低，+1.26%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">晶科能源</span>
                                <span class="stock-code">688223</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">组件龙头，海外布局领先，-1.6%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">福斯特</span>
                                <span class="stock-code">603806</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">EVA胶膜全球龙头，市占率50%+，光伏辅材受益</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">德业股份</span>
                                <span class="stock-code">605117</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">逆变器+储能，海外户储龙头，业绩韧性强</span>
                        </div>
                    </div>
                </div>
                
                <div class="direction-card hot">
                    <span class="tag tag-hot">🔥 重点看</span>
                    <h3>油气产业链/能源安全</h3>
                    <p>美伊谈判消息不实，霍尔木兹海峡实际未开放，原油大涨+4.55%。认知滞后24-48h，油气板块相对历史均值折价15-20%。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中国海油</span>
                                <span class="stock-code">600938</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">海上油气龙头，桶油成本$28全球最低，-0.93%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中远海能</span>
                                <span class="stock-code">600026</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">VLCC运力全球第一，中东航线占比高，-2.19%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">杰瑞股份</span>
                                <span class="stock-code">002353</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">压裂设备占国内50%，中东订单增200%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">通源石油</span>
                                <span class="stock-code">300164</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">北美页岩气射孔主力，油价传导1-2周</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">广汇能源</span>
                                <span class="stock-code">600256</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">煤制油+天然气，资源禀赋独特，能源安全受益</span>
                        </div>
                    </div>
                </div>
                
                <div class="direction-card hot">
                    <span class="tag tag-hot">🔥 重点看</span>
                    <h3>国产半导体/芯片替代</h3>
                    <p>英特尔暴跌-4.09%，AMD-1.24%，外部芯片脆弱性暴露。国产替代紧迫性上升，半导体设备相对海外折价40-50%。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">北方华创</span>
                                <span class="stock-code">002371</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">半导体设备平台型龙头，+6.13%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中芯国际</span>
                                <span class="stock-code">688981</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">中国最大晶圆代工厂，14nm及以下先进制程，+0.38%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">中微公司</span>
                                <span class="stock-code">688012</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">刻蚀设备技术达国际一流，5nm制程突破</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">安集科技</span>
                                <span class="stock-code">688019</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">CMP抛光液进入中芯国际供应链</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">拓荆科技</span>
                                <span class="stock-code">688072</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">薄膜沉积设备，PECVD/SACVD，国产替代</span>
                        </div>
                    </div>
                </div>
                
                <div class="direction-card hot">
                    <span class="tag tag-hot">🔥 重点看</span>
                    <h3>液冷/AI算力</h3>
                    <p>AI服务器功耗突破10kW→液冷成刚需。英维克Q1业绩暴雷后市场恐慌，但真实需求仍在，错杀标的修复。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">安诺其</span>
                                <span class="stock-code">300067</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">AI服务器+液冷双驱动，+20%</span>
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
                                <span class="stock-name">高澜股份</span>
                                <span class="stock-code">300499</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">华为/字节液冷供应商，创历史新高</span>
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
                                <span class="stock-name">康盛股份</span>
                                <span class="stock-code">002418</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">液冷+家电，家电转型液冷黑马</span>
                        </div>
                    </div>
                </div>
                
                <div class="direction-card watch">
                    <span class="tag tag-watch">👀 可关注</span>
                    <h3>重组/并购</h3>
                    <p>上海印发产业互联网平台方案，鼓励并购重组。支持产业互联网平台企业并购整合国外品牌、渠道、研发与生产等业务板块。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
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
                                <span class="stock-name">上海钢联</span>
                                <span class="stock-code">300226</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">产业互联网平台龙头，上海本地</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">宝信软件</span>
                                <span class="stock-code">600845</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">工业互联网平台，宝钢旗下</span>
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
                
                <div class="direction-card watch">
                    <span class="tag tag-watch">👀 可关注</span>
                    <h3>固态电池/钠电池</h3>
                    <p>宁德时代举办"超级科技日"，发布钠电、凝聚态、快充等技术产品。市场对钠电池商业化进度有分歧，若超预期存在巨大预期差。</p>
                    <div class="stock-list">
                        <h4>📋 重点标的</h4>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">宁德时代</span>
                                <span class="stock-code">300750</span>
                                <span class="stock-tag tag-s">S</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">发布会主体，钠电/凝聚态/快充三重催化，-2.51%</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">华阳股份</span>
                                <span class="stock-code">600348</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">绑定中科海钠，正负极材料布局</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">美联新材</span>
                                <span class="stock-code">300586</span>
                                <span class="stock-tag tag-a">A</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">普鲁士蓝正极，钠电三大路线之一</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">先惠技术</span>
                                <span class="stock-code">688155</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">固态电池设备，技术领先</span>
                        </div>
                        <div class="stock-item">
                            <div class="stock-info">
                                <span class="stock-name">万顺新材</span>
                                <span class="stock-code">300057</span>
                                <span class="stock-tag tag-horse">黑马</span>
                            </div>
                            <span style="color:#8b9dc3;font-size:0.8em">铝箔（钠电集流体用铝不用铜），位置极低</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
'''

part3 = lines[665:]  # ztb-section onward

# Write new file
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(part1)
    f.write(new_directions)
    f.writelines(part3)

print("✅ 网站更新成功！")
print("📊 已移除：隔夜美股映射方向")
print("📊 已更新：重要新闻整理方向（6个方向，30只标的）")
