#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""华策影视300133 复诊（2026-11-10 涨停日）JSON组装——基于11-09档案整体重写（patch5七块重算）"""
import json, os

CODE = "300133"
DATE = "2026-11-10"
OUT = "/root/.openclaw/workspace/yixue-dashboard/data"
ARCH = "/root/.openclaw/workspace/memory/个股诊断档案/300133"

old = json.load(open(f"{OUT}/diagnose_{CODE}.json", encoding="utf-8"))
old_rep = old["matrix_L1"]["report"]

d = old  # 整体重写
d["date"] = DATE
d["generated"] = "复诊·涨停日诊断（数据截至2026-11-10 10:45盘中，涨停11.64封板）"

d["diagnose_meta"] = {
    "snapshot_time": "2026-11-10 10:45",
    "snapshot_price": 11.64,
    "snapshot_pct": 20.0,
    "close": 11.64,
    "change_pct": 20.0,
    "market_cap": "218亿",
    "pe_ttm": None,
    "pb": None,
    "trigger": "复诊(距上次1天)",
    "followed_qimen_version": "V4.1-patch33",
    "baseline_ref": "20261109",
    "prev_diagnose": {"date": "2026-11-09", "prev_z": 1, "prev_g": 4, "note": "上次z=1横盘整理×g4中性偏弱(9.90放量失守假突破定罪)；本次涨停平反"},
    "note": "20cm涨停11.64封板：收复9.90分水岭+创52周新高(2018年以来)，近5日+25%，传媒指数11月+12.45%"
}

d["matrix_grid"]["current"] = {"z": 2, "g": 0, "label": "放量突破 × 偏多"}
d["matrix_grid"]["note"] = "11-09假突破定罪后次日即被20cm涨停平反：放量(5日量比1.61)收复9.90/10.36/11.04三重关卡，创52周新高，AI漫剧板块共振(文投2连板/掌阅涨停)"

d["matrix_L0"] = {
    "v0": {"value": 1, "grade": "偏多", "detail": "11-04金叉后第5日，柱体+0.09(p65分位)但连续2日收缩(0.141→0.09)，DIF0.476零上——今日20cm将令柱体大幅张开；交叉项多×柱体中上×DIF正=偏多"},
    "a_macd": {"value": 1, "detail": "金叉后红柱延续，今日涨停柱体跳空放大，油门全开(板块β驱动)"},
    "q_bias": 1,
    "q_detail": "问事盘10:00丁巳时：时干丁落艮八景门+螣蛇——情绪/成交极旺但虚；值符死门震三——主线未定型；生门兑七白虎——利润兑现带杀气宜快出；马星亥冲动——波动加剧。资金侧：超大单净买2.3亿、机构占比五成，对冲部分盘虚→q=+1",
    "cell": {"key": "2_0 放量突破×偏多"}
}

d["matrix_L1"]["gene"] = {
    "pattern": "模式2跨界转型(4/6)+模式5景气共振(4/5)",
    "match_detail": "今日触发事件重跑：算力已成第一大收入(23.41%)+预收14.13亿(+55.41%)→模式2第5项'实质客户收入'由待验证转已验证(3/6→4/6)；前三季扣非1.19亿(+41.19%)/Q3单季+181.75%→模式5'业绩拐点'点亮(3/5→4/5)。市值218亿>80亿仍不符弹性项",
    "full_detail": "匹配度双上调的结构含义：本轮不是纯板块脉冲——算力转型兑现(转固+预收)与扣非拐点(Q3+181.75%)两个数据验证点同时落地，'质疑→认可'的分歧消除段开启。风险边界：模式2案例均值+120~180%系小市值(<80亿)样本，218亿体量弹性递减；题材情绪(短剧数据)已两日强势，追高分歧大。"
}
d["matrix_L1"]["prototype"]["match"] = "放量突破·主升前夜姿态(七维全量：涨停异动事件触发)"

# 模块D：分支2状态刷新
rep = dict(old_rep)
rep["standing"] = "假设仍成立且强化——算力第二曲线兑现(预收14.13亿/已成第一大收入)，AI漫剧行业数据(QuestMobile短剧时长净增Top1)验证板块β持续性；新波动：股价20cm后定价已计入强预期"
catalysts = list(rep.get("catalysts") or [])
catalysts.append({"text": "QuestMobile秋季报告：短剧视频使用时长净增133.29亿小时居全网Top1(2026-09)，AI漫剧出海1.5亿月活", "status": "兑现中", "note": "2026-11-10板块共振催化，非公司独有"})
rep["catalysts"] = catalysts
rep["scenarios"] = [
    {"name": "乐观", "prob": "25%", "range": "12.4~13.5元", "trigger": "AI漫剧梯队续命(文投/掌阅连板)+Q4算力收入确认加速"},
    {"name": "基准", "prob": "50%", "range": "10.4~12.2元", "trigger": "情绪脉冲两日内消化，高位宽幅震荡等Q4验证", "most_likely": True},
    {"name": "悲观", "prob": "25%", "range": "9.0~10.4元", "trigger": "板块退潮+获利盘涌出，回补今日跳空缺口"}
]
rep["current_price_note"] = "现价11.64已兑现上轮冻结目标区11.2~11.9，上方进入纯情绪定价区，基本面源支撑在11下方"
d["matrix_L1"]["report"] = rep
d["matrix_L1"]["report_update"] = {"type": "refresh", "trigger": "AI漫剧板块数据催化+20cm涨停异动(非公司公告)", "prev_date": "2026-11-05", "changed_fields": ["standing", "catalysts", "scenarios", "current_price_note"]}

d["matrix_L2"] = {
    "active_risks": ["情绪脉冲两日后回落风险(短剧数据已消化)", "218亿市值超模式2弹性边界(<80亿)", "大盘C维持深水区系统性压制未除", "获利盘：近5日+25%短线客浮盈厚"],
    "vetoes": [],
    "extreme_day": True
}

d["fusion"] = {
    "direction": "偏多",
    "confidence": "中(金叉+红柱+板块β+机构资金共振，但系情绪驱动盘象虚，追高性价比低)",
    "form": "20cm涨停封板创52周新高，跳空缺口10.36-11.64，量能1.61倍",
    "verdict": "v0(+1:金叉红柱)×a(+1:油门全开)×q(+1:情绪资金共振盘虚)=+3偏多——方向明确但属性是板块脉冲，纪律上持筹者可持不追，空仓者不追高等回踩"
}

d["pricing"] = {
    "target_price": {
        "sources": [
            {"source": "基本面估值", "range": "8~11元", "basis": "2027E营收~25亿(算力15+影视10)×PS5倍/归母2.5亿×55倍——现价11.64已在源上方，基本面无支撑"},
            {"source": "启动特征量度", "range": "12.4~13.5元", "basis": "z=2突破1:1量度：11月箱体9.0-11.0高度2元→11+2=13；底部翻倍路径6.22×2=12.44"},
            {"source": "翻倍基因先例", "range": "13.5~18元", "basis": "模式2跨界转型案例涨幅中位约+120%(金富+180%/九州一轨+91%,n=12)，自本轮启动点起算×1.5~2"}
        ],
        "overlap_zone": "13.5元一线窄交集（源2上沿=源3下沿）",
        "divergence_note": "基本面源(8~11)已低于现价——当前定价完全脱离基本面锚，纯情绪+模式先例支撑；13.5上方进入无锚区",
        "confidence": "低-中"
    },
    "timing": {
        "timing_window": "时干丁景门+螣蛇=情绪窗口正开但虚，值符死门=主线未定型——脉冲窗口期看板块梯队(文投/掌阅/慈文连板持续性)，本周内见分晓；生门白虎=冲高兑现宜快不宜拖",
        "strength_check": "日干戊惊门九天追高力量虚+机构净买五成部分对冲——三源技术/情绪目标打8折，有效区约11~14元",
        "tail_risk": "玄武临庚=脉冲后获利盘出货；螣蛇=板块情绪证伪(数据利好两日后反转剧本常见)；大盘深水C维持=系统性回撤放大器"
    }
}

d["verdict"] = {
    "summary": "算力转型兑现叠加AI漫剧行业数据催化，华策20cm涨停创八年新高，'质疑到认可'的分歧消除段开启。但现价已脱离基本面锚，上方是纯情绪定价区，脉冲窗口正开而虚，宜持不宜追。两个剧本：板块梯队续命冲13.5，量退回补缺口看10.4。坐标：z=2放量突破×g=0偏多。",
    "dims_oneliner": {
        "gene": "模式2跨界转型(3/6→4/6)+模式5景气共振(3/5→4/5)——算力第一大收入+扣非拐点两个验证点今日兑现",
        "state": "z：1→2放量突破确认(20cm收复9.90+创52周新高+量比1.61)，假突破一日平反",
        "report": "分支2refresh：QuestMobile短剧数据入催化剂(兑现中)，上轮冻结目标区11.2~11.9今日触及兑现",
        "forecast": "偏多(中置信)：金叉+红柱+板块β共振，但系情绪脉冲，纪律=持不追"
    },
    "key_risk": "情绪脉冲两日后退潮：近5日+25%浮盈盘+218亿超模式弹性边界+大盘深水区，三因素共振回落剧本",
    "tracking": "AI漫剧梯队连板持续性(文投/掌阅/慈文)+今日跳空缺口10.36-11.64是否回补；Q4算力收入确认"
}

d["view_gene"] = {
    "total_lit": 8,
    "total_partial": 2,
    "total_vars": 11,
    "top_pattern": "模式2 跨界转型型",
    "note": "双模式匹配度同上调：算力实质收入+扣非拐点验证，'质疑→认可'分歧消除段",
    "patterns": [
        {"id": "模式2", "name": "跨界转型型", "top": True, "lit_vars": 4, "total_vars": 6, "vars": [
            {"status": "lit", "name": "原主业下滑/瓶颈", "evidence": "长剧主业2024-2025承压，平台预算紧缩"},
            {"status": "lit", "name": "管理层转型意愿", "evidence": "算力独立业务单元+有风/国色双模型备案+1亿AI基金"},
            {"status": "part", "name": "业绩承诺机制", "evidence": "算力自建非并购，无3年承诺条款；预收款14.13亿部分替代"},
            {"status": "lit", "name": "赛道景气度极高", "evidence": "AI算力+AI视频双高景气，QuestMobile短剧时长Top1"},
            {"status": "lit", "name": "实质客户收入", "evidence": "算力已成第一大收入23.41%，服务器转固交付"},
            {"status": "none", "name": "市值<80亿弹性", "evidence": "218亿，超模式边界(历史案例均值<80亿)"}
        ]},
        {"id": "模式5", "name": "景气共振型", "top": False, "lit_vars": 4, "total_vars": 5, "vars": [
            {"status": "lit", "name": "主业龙头", "evidence": "电视剧工业化龙头，内容储备头部"},
            {"status": "lit", "name": "内生升级", "evidence": "全AI动画剧+互动影游+AIGC工作流提效"},
            {"status": "lit", "name": "下游景气", "evidence": "AI漫剧/短剧出海1.5亿月活，行业数据断层领先"},
            {"status": "lit", "name": "业绩拐点", "evidence": "扣非前三季1.19亿+41.19%，Q3单季+181.75%"},
            {"status": "part", "name": "国产替代", "evidence": "传媒非替代逻辑，对应变体=文化出海(付费榜九席中国厂商)"}
        ]}
    ]
}

d["view_state"]["current_idx"] = 2
d["view_state"]["zones"] = [
    {"name": "底部区", "range": "6.22~8.0(2026年4-8月)"},
    {"name": "横盘整理区", "range": "8.6~11.0(9-11月大箱体)"},
    {"name": "放量突破区", "range": "11.04上方，今日11.64创52周新高确认"},
    {"name": "主升区", "range": "站稳11.64后看12.4~13.5量度区"},
    {"name": "退潮区", "range": "回补今日缺口10.36-11.64即脉冲终结"}
]
d["view_state"]["judgment"] = [
    {"dim": "价格位置", "status": "lit", "value": "11.64(20cm)", "evidence": "收复9.90分水岭+创52周新高，8年新高"},
    {"dim": "量能", "status": "lit", "value": "5日量比1.61", "evidence": "今日半日157万手≈昨日172万手全天；超大单+2.3亿，机构占比五成"},
    {"dim": "均线结构", "status": "lit", "value": "多头排列", "evidence": "价>MA5(9.82)>MA10(9.46)>MA20(9.27)>MA60(8.00)，跳空远离"},
    {"dim": "资金", "status": "lit", "value": "超大单+2.3亿", "evidence": "机构净买入占比超五成(同花顺监控)"},
    {"dim": "筹码结构", "status": "part", "value": "近5日+25%", "evidence": "短线浮盈盘厚，获利了结压力随涨幅累积"},
    {"dim": "题材", "status": "lit", "value": "AI漫剧+短剧Top1", "evidence": "QuestMobile短剧时长净增133亿小时断层第一，板块梯队完整"},
    {"dim": "基本面", "status": "lit", "value": "扣非+41.19%", "evidence": "前三季扣非1.19亿，Q3+181.75%；算力第一大收入23.41%"},
    {"dim": "环境", "status": "part", "value": "传媒指数11月+12.45%", "evidence": "大盘C维持深水区未除，系统性压制仍在"}
]
d["view_state"]["transitions"] = [
    {"from": "放量突破区", "to": "主升区", "conditions": [{"text": "站稳11.64三日+板块梯队续命", "met": False}, {"text": "Q4算力收入确认加速", "met": False}]},
    {"from": "放量突破区", "to": "退潮区", "conditions": [{"text": "回补跳空缺口10.36-11.64", "met": False}, {"text": "文投/掌阅连板梯队断板退潮", "met": False}]}
]
d["view_state"]["note"] = "20cm放量突破创52周新高，方向选择向上，持续性系于板块情绪"

d["daily_chain"] = [
    {"name": "① MACD底座", "tag": "v0", "output": "v0=+1 偏多", "formula": "交叉项(11-04金叉)×柱体(+0.09,p65)×DIF(零上)", "note": "今日20cm令柱体跳空放大"},
    {"name": "② 柱体油门", "tag": "a_macd", "output": "a_macd=+1", "note": "红柱延续+涨停跳空，油门全开(板块β)"},
    {"name": "③ 奇门修正", "tag": "q_bias", "output": "q_bias=+1", "note": "景门情绪极旺但螣蛇虚+白虎兑现杀——资金数据(机构五成)对冲部分盘虚"},
    {"name": "④ 合成定级", "tag": "fusion", "output": "偏多(中置信)", "formula": "+1+1+1=+3", "note": "方向明确但属性=板块脉冲"},
    {"name": "⑤ 三源目标价", "tag": "pricing", "output": "基本面源8~11/量度12.4~13.5/先例13.5~18", "note": "现价已脱离基本面锚，13.5窄交集上方无锚"},
    {"name": "⑥ 对账回填", "tag": "verification", "output": "上次(11-09)判中性偏弱，今日+20%涨停——方向未兑现，情绪盘超技术预期", "note": "剧本2(收复9.90重启突破)触发兑现"}
]

d["todo_list"] = [
    "AI漫剧梯队连板持续性跟踪(文投控股/掌阅科技/慈文传媒)",
    "今日跳空缺口10.36-11.64回补监测——回补=脉冲终结信号",
    "Q4算力收入确认进度(年报2027-04)",
    "上轮冻结目标区11.2~11.9已兑现，上移至12.4~13.5观察"
]

# history 追加
hist = d.get("history", [])
hist.append({"date": DATE, "v0": 1, "a_macd": 1, "q_bias": 1, "pred": "偏多", "actual": "--", "hit": "待回填", "cell": "2_0"})
d["history"] = hist

d["prev_diagnose"] = {"date": "2026-11-09", "prev_z": 1, "prev_g": 4, "note": "上次z=1×g4(假突破定罪)；本次涨停平反z=2×g0"}

tl = d.get("timeline", [])
tl.append({"date": DATE, "type": "diagnose", "event": "复诊：放量突破×偏多｜20cm涨停创52周新高｜模式2+模式5匹配度双上调", "dims": {"gene": "模式2(4/6)+模式5(4/5)", "state": "z=2放量突破确认", "forecast": "偏多(中置信，板块脉冲)", "report": "分支2refresh：QuestMobile催化入列"}})
tl.append({"date": DATE, "type": "policy", "event": "AI漫剧板块催化：QuestMobile秋季报告短剧时长净增133.29亿小时居全网Top1；传媒指数11月+12.45%", "dims": {"gene": "模式2+模式5双模式受益", "state": "板块β驱动涨停", "forecast": None, "report": "催化剂兑现中"}})
d["timeline"] = tl

for p in (f"{OUT}/diagnose_{CODE}.json", f"{OUT}/diagnose_{CODE}_20261110.json"):
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written both files")

idx_p = "/root/.openclaw/workspace/memory/个股诊断档案/INDEX.json"
idx = json.load(open(idx_p, encoding="utf-8"))
idx[CODE] = {"name": "华策影视", "last_diagnose": DATE, "count": 8, "last_zone": "放量突破", "last_gene": "模式2跨界转型(4/6)+模式5景气共振(4/5)", "last_grade": "偏多"}
json.dump(idx, open(idx_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

di_p = f"{OUT}/diagnoses_index.json"
di = json.load(open(di_p, encoding="utf-8"))
for s in di["stocks"]:
    if s.get("code") == CODE:
        s.update({"last_date": DATE, "count": 8, "last_zone": "放量突破", "last_gene": "模式2跨界转型(4/6)+模式5景气共振(4/5)", "last_grade": "偏多"})
        if "20261110" not in s["dates"]:
            s["dates"].append("20261110")
json.dump(di, open(di_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("indexes updated")
