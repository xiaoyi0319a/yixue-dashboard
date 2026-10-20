# -*- coding: utf-8 -*-
"""2026-10-20 19:57 老师指令：落宫表改9宫制（去用神列·按宫读图·同宫信息叠加）
+ 修结构行渲染bug（cell='值使×' 与前端YL键'值使门'不匹配→结构合成显示0）
9宫数据=今日实盘（阴遁6局·丁卯日乙巳时）"""
import json

NINE = [
    {"palace": "坎一", "gods": ["值使（振幅）", "戊（资金）", "九地（托底）"],
     "star": "天心（金·吉）", "god": "九地", "door": "死门", "sky_ground": "戊+癸",
     "month_state": "土旺", "harms": "死门迫（土克水）",
     "note": "资金入死乡——值使死门振幅带滞，戊癸青龙华盖而受迫，九地托底当位：守势胶着，财力有而难举"},
    {"palace": "坤二", "gods": ["日干丁（价格）"],
     "star": "天英（火·小凶）", "god": "螣蛇", "door": "伤门", "sky_ground": "丁+己壬",
     "month_state": "火休", "harms": "伤门迫（木克土）",
     "note": "价格带伤——丁火休囚而伤门迫，螣蛇主虚惊动荡，价格根基偏弱"},
    {"palace": "震三（空亡）", "gods": ["开门（突破）"],
     "star": "天任（土·大吉）", "god": "白虎", "door": "开门", "sky_ground": "丙+辛",
     "month_state": "金相", "harms": "门迫（金克木）+空亡",
     "note": "通道带伤而虚——开门迫逢空亡，白虎临之，动则有险"},
    {"palace": "巽四", "gods": [],
     "star": "天冲（木）", "god": "六合", "door": "休门", "sky_ground": "辛+庚",
     "month_state": "—", "harms": "—",
     "note": "无主要用神落此宫"},
    {"palace": "中五", "gods": [],
     "star": "—（寄坤二）", "god": "—", "door": "—", "sky_ground": "己",
     "month_state": "—", "harms": "—",
     "note": "中宫寄坤二"},
    {"palace": "乾六", "gods": ["时干乙（时机/空方帅）", "乙奇（买盘）", "景门（情绪/成交）", "九天（涨能）"],
     "star": "天柱（金·凶）", "god": "九天", "door": "景门", "sky_ground": "乙+戊",
     "month_state": "木囚·火休", "harms": "景门迫（火克金）",
     "note": "四角色叠加宫——空方帅与买盘同体（乙），情绪带伤而涨能同临（九天）：帅弱而动象在，攻势真实度待验证"},
    {"palace": "兑七", "gods": ["值符（大势）"],
     "star": "芮禽（土·凶）", "god": "值符", "door": "杜门", "sky_ground": "己壬+乙",
     "month_state": "土旺", "harms": "门制（杜门木被宫克）",
     "note": "大势有格而气机不畅——值符带病星而杜门自闭，壬己混浊宜静守"},
    {"palace": "艮八（空亡）", "gods": ["天蓬（流入/流出）"],
     "star": "天蓬（水·凶）", "god": "玄武", "door": "惊门", "sky_ground": "癸+丙",
     "month_state": "水死", "harms": "空亡（艮八寅空）",
     "note": "流入闭死——天蓬水死于艮土又逢空亡，玄武主暗流：资金明面通道关闭"},
    {"palace": "离九", "gods": ["庚（卖盘）", "生门（利润）"],
     "star": "天辅（木·大吉）", "god": "太阴", "door": "生门", "sky_ground": "庚+丁",
     "month_state": "金相·土旺当令", "harms": "宫克（火克金·庚受创，非四害）",
     "note": "卖压与利润纠缠——庚受离火之克而临生门，卖盘带伤压而不决，太阴暗护其侧"},
]

for f in ['data/pipeline_20261020.json', 'data/pipeline_latest.json']:
    d = json.load(open(f, encoding='utf-8'))
    d['palace_table'] = NINE
    # cell名统一：值使→值使门（前端YL匹配+矩阵行名一致）
    for s in d['matrix_drop']:
        if s['cell'].startswith('值使×'):
            s['cell'] = s['cell'].replace('值使×', '值使门×')
    for key in ('structure_signals', 'attack_plus_signals', 'attack_minus_signals'):
        for s in d['qimen'].get(key, []):
            if s.get('cell', '').startswith('值使×'):
                s['cell'] = s['cell'].replace('值使×', '值使门×')
            if s.get('name', '').startswith('G') and '值使×' in s['name']:
                s['name'] = s['name'].replace('值使×', '值使门×')
    d['qimen']['reread_note'] = d['qimen'].get('reread_note', '') + ' 19:57落宫表改9宫制（老师指令：去用神列·按宫读图·同宫叠加），cell值使→值使门。'
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{f}: 9宫落宫表写入完成，matrix_drop值使门化完成')
