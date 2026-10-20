# -*- coding: utf-8 -*-
"""2026-10-20 19:25 老师指令：按v2.2重读今日盘（13行+104格穷举+三层合成重算）
旧JSON问题：palace_table缺4行（景门/九天/九地/天蓬）；matrix_drop仅11条且四害列无计分；
qimen块残留已退役的效能系数制(coef 0.69)与四害双向祖父条款。
重算结果：a_raw=+0.0 → 表2-D=0（新读法多空基本平衡；fusion保留11:04旧读法v=4偏强并记分歧note）
"""
import json

PATH = 'data/pipeline_20261020.json'
d = json.load(open(PATH, encoding='utf-8'))

# ============ 1. palace_table 9→13行 ============
pt = d['palace_table']
new_rows = [
    {"yongshen": "景门（情绪/成交）", "palace": "乾六", "star": "天柱（金·凶）", "door": "景门",
     "god": "九天", "sky_ground": "乙+戊", "month_state": "火休",
     "harms": "景门迫（火克金）", "note": "景门克宫而迫——情绪亢奋带伤，成交放大而质量存疑"},
    {"yongshen": "九天（涨能）", "palace": "乾六", "star": "天柱（金·凶）", "door": "景门",
     "god": "九天", "sky_ground": "乙+戊", "month_state": "—（神盘不论月令）",
     "harms": "无", "note": "九天临乾——涨能当位而带天柱之凶，攻势真实度待数据（轴9覆盖读法）"},
    {"yongshen": "九地（托底）", "palace": "坎一", "star": "天心（金·吉）", "door": "死门",
     "god": "九地", "sky_ground": "戊+癸", "month_state": "—（神盘不论月令）",
     "harms": "无", "note": "九地临坎——托底当位而死门同宫，守势带滞（轴9覆盖读法）"},
    {"yongshen": "天蓬（流入/流出）", "palace": "艮八（空亡）", "star": "天蓬（水·凶）", "door": "惊门",
     "god": "玄武", "sky_ground": "癸+丙", "month_state": "水死",
     "harms": "空亡（艮八寅空）", "note": "天蓬水死于艮土又逢空亡——资金流入通道闭死，玄武主暗流"},
]
# 去重（防重复运行）
exist = {r['yongshen'].split('（')[0] for r in pt}
for r in new_rows:
    if r['yongshen'].split('（')[0] not in exist:
        pt.append(r)
d['palace_table'] = pt

# ============ 2. matrix_drop 全量重出（v2.2穷举） ============
def sig(cell, g, state, dest, note=''):
    s = {'cell': cell, 'g': g, 'state': state, 'dest': dest}
    if note: s['note'] = note
    return s

md = [
    # ---- ●计分 攻多7条 ----
    sig('值符×旺/当令', 'G38', '●', '攻多+2', '天芮土星戌月当令→大势有托'),
    sig('时干×休囚/死·废', 'G33', '●', '攻多+2', '乙木囚于戌月→空方帅弱'),
    sig('时干×四害', 'G34', '●', '攻多+1.5', '帅残（景门迫克宫）→空方帅受创·方向歧义点[空方弱则多方受益]'),
    sig('生门×旺/当令', 'A3', '●', '攻多+2', '戌月土旺当令→利润有根'),
    sig('戊×旺/当令', 'G36', '●', '攻多+2', '戊土当令→资金充沛'),
    sig('开门×旺/当令', 'G41', '●', '攻多+2', '开门金相→通道有气'),
    sig('日干×四喜', 'G78', '●', '攻多+1.5', '丁生己（通气）·价格有根·新判定首跑待口径确认'),
    # ---- ●计分 攻空12条 ----
    sig('值符×四害', 'G49', '●', '攻空+1.5', '门制（杜门木被兑金克）→大势受创'),
    sig('日干×休囚/死·废', 'G31', '●', '攻空+2', '丁火休于戌月→价格身弱'),
    sig('日干×四害', 'G2', '●', '攻空+1.5', '伤门迫（木克坤土）→核心受制'),
    sig('时干×得生/受克', 'A2', '●', '攻空+2', '时干乙木生日干丁火→M4口径攻空（272天实证）'),
    sig('庚×旺/当令', 'G27', '●', '攻空+2', '庚金相于戌月→空方得旺'),
    sig('戊×四害', 'G37', '●', '攻空+1.5', '死门迫（土克坎水）→资金受制'),
    sig('乙奇×休囚/死·废', 'G11', '●', '攻空+2', '乙木囚→买盘乏力'),
    sig('乙奇×四害', 'G1', '●', '攻空+1.5', '景门迫→买盘受制'),
    sig('开门×四害', 'G4', '●', '攻空+1.5', '门迫（金克震木）→通道受阻'),
    sig('景门×休囚/死·废', 'G40', '●', '攻空+2', '景门火休→情绪低迷'),
    sig('景门×四害', 'G50', '●', '攻空+1.5', '景门迫→情绪受创'),
    sig('天蓬×休囚/死·废', 'G46', '●', '攻空+2', '天蓬水死→资金流出'),
    # ---- ●计分 结构2条（值使门行→振幅进结构渠道） ----
    sig('值使×旺/当令', 'G68', '●', '结构+2', '死门土旺→振幅放大·方向随门性'),
    sig('值使×四害', 'G70', '●', '结构+1.5', '死门迫→振幅扭曲·假动作风险'),
    # ---- ◌观察 0分 ----
    sig('庚×得生/受克', 'G15', '◌', '观察追踪表', '庚受离火克→候选格(◌·⊙)未转正'),
    sig('乙奇×得生/受克', 'G12', '◌', '观察追踪表', '乙受乾金克→候选格未转正'),
    sig('开门×空亡', 'G23', '◌', '观察追踪表', '震三卯空→空亡候选'),
    sig('天蓬×空亡', 'G26', '◌', '观察追踪表', '艮八寅空→空亡候选（旧读法漏读·本次补上）'),
    sig('戊×吉格', '—◌', '—◌', '不计分', '戊+癸不编格（10-20实测中性空格纪律）'),
]
d['matrix_drop'] = md

# ============ 3. qimen块三层合成重算 ============
LAYERS = {'值符': '核心', '值使': '核心', '日干': '核心', '时干': '核心',
          '庚': '力量', '乙奇': '力量', '戊': '力量', '生门': '力量', '开门': '力量',
          '景门': '衍生', '九天': '衍生', '九地': '衍生', '天蓬': '衍生'}
COEF = {'核心': 1.5, '力量': 1.0, '衍生': 0.5}
BASE = {'旺/当令': 2, '休囚/死·废': 2, '四害': 1.5, '四喜': 1.5,
        '凶格临宫': 3, '吉格临宫': 3, '空亡': 2, '得生/受克': 2}

ap, am, st = [], [], []
for s in md:
    if s['state'] != '●':
        continue
    cell = s['cell']
    yongshen = cell.split('×')[0]
    col = cell.split('×')[1]
    layer = next((v for k, v in LAYERS.items() if yongshen.startswith(k)), None)
    if layer is None:
        continue
    base = BASE.get(col, 2)
    eff = round(base * COEF[layer], 3)
    item = {'name': f"{s['g']}·{cell}", 'condition': s.get('note', ''),
            'base': base, 'layer': layer, 'layer_coef': COEF[layer],
            'effective': eff, 'cell': cell, 'g': s['g']}
    if '攻多' in s['dest']: ap.append(item)
    elif '攻空' in s['dest']: am.append(item)
    elif '结构' in s['dest']: st.append(item)

def synth(lst):
    sub = {}
    for it in lst:
        sub[it['layer']] = sub.get(it['layer'], 0) + it['effective']
    total = round(sum(sub.get(k, 0) for k in ('核心', '力量', '衍生')), 3)
    return sub, total

ap_sub, ap_t = synth(ap)
am_sub, am_t = synth(am)
st_sub, st_t = synth(st)
a_raw = round(ap_t - am_t + st_t, 3)

def disc(x):
    return 2 if x >= 6 else 1 if x >= 3 else 0 if x >= -2 else -1 if x >= -5 else -2

q = d['qimen']
q['attack_plus'] = round(ap_t, 3)
q['attack_minus'] = round(am_t, 3)
q['structure'] = round(st_t, 3)
q['attack_plus_signals'] = ap
q['attack_minus_signals'] = am
q['structure_signals'] = st
q['a_raw'] = a_raw
q['a_discrete'] = disc(a_raw)
q['a_total'] = q.get('a_macd', 0) + disc(a_raw)
q['r_triggered'] = abs(a_raw) >= 8
# fusion块不联动改写：11:04老师指令重推口径（旧读法a_raw=3→a总1→v=4偏强）保留v_final=4；
# 新读法a_total=0若联动则v=3偏多——差异记入note，明早首跑起以v2.2为准
fused = d.get('fusion', {})
if fused:
    fused['reread_note'] = ('19:25 v2.2重读：qimen_a三层合成a_raw=+4.0旧手算口径→机器重算+0.0→a_total=0。'
                            '若联动v=2.5+0→3偏多；本字段保留11:04老师重推v=4偏强（旧读法），双口径分歧日，'
                            '明早06:30首跑起以v2.2为准')
q['layer_synthesis'] = {
    '攻多': {'核心小计': ap_sub.get('核心', 0), '力量小计': ap_sub.get('力量', 0),
            '衍生小计': ap_sub.get('衍生', 0), '合成': ap_t},
    '攻空': {'核心小计': am_sub.get('核心', 0), '力量小计': am_sub.get('力量', 0),
            '衍生小计': am_sub.get('衍生', 0), '合成': am_t},
    '结构': {'核心小计': st_sub.get('核心', 0), '力量小计': st_sub.get('力量', 0),
            '衍生小计': st_sub.get('衍生', 0), '合成': st_t},
    '公式': 'a_raw=攻多-攻空+结构=1.5×核心+1.0×力量+0.5×衍生（分渠道）',
}
q['reread_note'] = ('19:25老师"重新读一下"指令：v2.2全量重读。旧读法11条(●3+◌8)→新26条(●21+◌4+—◌1)。'
                    '删除：四害双向祖父条款+2(0779c5a已退役)/值符休囚G20(土旺判错)/效能系数coef(V2.8已退役)。'
                    '新增：景门/九天/九地/天蓬4行落宫+四害列门迫7条计分+值使门行G68/G70+四喜通气G78+天蓬空亡G26◌。'
                    'a_raw:旧口径+3(系数制)→新+0.0(三层合成,多空基本平衡)→表2-D=0。'
                    'fusion保留11:04重推v=4偏强(旧读法),新读法联动应v=3偏多,明早首跑以v2.2为准。'
                    '存疑3项：①G34方向(帅残→空方弱→攻多,格名带空字待老师裁)②日干通气G78(丁生己是否算通气)③八神两行主矩阵全灰(口径未立,轴9覆盖)。')

d['rule_version'] = d.get('rule_version', '') + ' | v2.2重读@19:25'

json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'a_raw={a_raw} discrete={disc(a_raw)} a_total={q["a_total"]}')
print(f'攻多={ap_t} {ap_sub} | 攻空={am_t} {am_sub} | 结构={st_t} {st_sub}')
print(f'palace_table={len(d["palace_table"])}行 matrix_drop={len(md)}条 (●{sum(1 for s in md if s["state"]=="●")})')
