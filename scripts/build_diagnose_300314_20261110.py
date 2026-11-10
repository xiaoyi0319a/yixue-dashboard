#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""戴维医疗300314 首诊 JSON 组装（2026-11-10 10:25快照）"""
import json, os, copy

CODE = "300314"
DATE = "2026-11-10"
OUT_DIR = "/root/.openclaw/workspace/yixue-dashboard/data"
ARCH_DIR = "/root/.openclaw/workspace/memory/个股诊断档案/300314"
os.makedirs(ARCH_DIR, exist_ok=True)

d = {
  "stock": "300314 戴维医疗",
  "date": DATE,
  "generated": "首诊·小羿按个股诊断工作流V1.3-patch9执行（数据截至2026-11-10 10:25盘中）",
  "version": "立体矩阵V0.1 · 诊断V1.3-patch9 · 看板V2",

  "diagnose_meta": {
    "snapshot_time": "2026-11-10 10:25",
    "snapshot_price": 14.71,
    "snapshot_pct": 3.74,
    "close": 14.71,
    "change_pct": 3.74,
    "market_cap": "42.4亿",
    "pe_ttm": 46.2,
    "pb": 3.29,
    "trigger": "首诊(无历史档案)",
    "followed_qimen_version": "V4.1-patch33",
    "baseline_ref": None,
    "prev_diagnose": None,
    "note": "现价距年内低8.89(+65.5%)，距年内高16.90(-13.0%)；三季报非经常损益3339万占归母43%"
  },

  "matrix_grid": {
    "zones": ["底部区","横盘整理","放量突破","主升","退潮"],
    "grades": ["偏多","偏强","中性偏强","无方向","中性偏弱","偏弱","偏空"],
    "current": { "z": 1, "g": 4, "label": "横盘整理 × 中性偏弱" },
    "cells": {},
    "note": "6-8月一波主升+90%(8.89→16.90)后退潮-32%，10月起缩量平台一个月(13.4-15.7箱体内)，量比0.75，MA20上方多头排列未坏"
  },

  "matrix_L0": {
    "v0": { "value": -1, "grade": "偏弱", "detail": "11-03死叉后第4日，柱体-0.04微绿(250日p38分位，远弱于p80=0.14)，DIF=0.46零上托底——交叉项空×柱体弱×DIF正=弱空" },
    "a_macd": { "value": -1, "detail": "死叉后绿柱延续第4日，近5日bar在-0.02~-0.04窄幅，油门缺失；今日盘中+3.74%若收14.5上方柱体有望收窄" },
    "q_bias": 0,
    "q_detail": "问事盘10:00丁巳时(阴遁9局)：卖方庚落坤二带玄武(暗减隐患)，买方乙奇落乾六带伤门；时干丁落艮八螣蛇+景门=题材情绪缠绕；生门在兑七白虎=兑现带杀气——多空缠斗无明显倾斜",
    "cell": { "key": "1_4 横盘整理×中性偏弱" }
  },

  "matrix_L1": {
    "prototype": {
      "match": "横盘整理·缩量平台姿态(轻量三项当日重算)",
      "score_detail": "价格位置:距低点+59.5%>40%否决底部区|量能:5日/60日=0.75缩量|均线:MA5>MA10>MA20>MA60多头排列，价在所有均线上方",
      "full_detail": "8月一波90%主升后回踩32%至11.46，10月19-23放量反弹(板块+Q3业绩)至14.77，随后缩量整理一个月，今日+3.74%再度逼近箱体上沿15.7。平台整理确认：缩量至60日均量0.75倍+区间振幅收窄。跃迁放量突破条件：放量(量比>2)站上15.7。"
    },
    "gene": {
      "pattern": "模式9 游资情绪驱动型(4/5项匹配)",
      "match_detail": "小市值40.8亿<50亿✓|低关注(研报稀少,QFII重仓概念10-23新增)✓|基本面弱(扣非前三季-20.98%)✓|板块热点刺激(8-17医药涨停潮/10月器械行情)✓|游资主导(8月换手19-27%脉冲)✓——5项全中但第3项需注意：有真实主业(婴儿保育细分龙头)非纯壳，故按70-75%匹配度计",
      "full_detail": "与模式9代表案例(一鸣食品+202%/神奇制药+50%)同构：小市值+题材脉冲+快速起落。差异：戴维医疗有真实细分主业与140国出海收入，非纯情绪标的；8-17的20cm涨停由医药板块整体行情驱动(药明康德新高)，非个股消息。与模式5景气共振仅2/5(细分龙头✓/产品升级✓/下游景气✗/业绩拐点✗[扣非-21%]/国产替代✗)。模式8控股股东变更型不匹配：协议转让公告明示不导致控制权变更，陈氏兄弟仍持61.06%。结构结论：题材脉冲型标的，业绩驱动路径不成立。"
    },
    "report_update": { "type": "none", "trigger": "首诊无历史报告——现场版占位，V4.7全量分析异步补跑", "prev_date": None, "changed_fields": [] },
    "report": {
      "date": "2026-11-10 现场版",
      "standing": "待分析报告（V4.7异步跑）——三季报归母+147%但非经常损益占43%、扣非仍-21%，基本面定调待12步工作流确认",
      "plain_qa": {
        "what": "国内婴儿保育设备细分龙头(2012年创业板上市，市占率国内领先)：婴儿培养箱/辐射保暖台/黄疸治疗/新生儿呼吸急救(NICU整体方案)+微创外科吻合器第二曲线，产品出口140+国。(现场版)",
        "expensive": "现价14.71对应PE-TTM约46倍，高于医疗器械同业中枢；扣非口径PE超60倍。基本面锚11~15元已到区间上沿——当前定价的是题材情绪不是盈利。(现场版)",
        "story": "真故事=NICU国产龙头+出海+育儿补贴人口政策受益+吻合器放量；预期差=三季报归母+147.71%看着炸裂，扣非其实-20.98%，水分在非经常损益约3340万。(现场版)",
        "worst": "证伪信号=Q4扣非继续双位数下滑叠加实控人系减持加码，则情绪退潮后跌回11~13基本面锚区。(现场版)"
      },
      "valuation_split": None,
      "scenarios": [
        { "name": "乐观", "prob": "20%", "range": "17.8~19.9元", "trigger": "放量突破15.7+Q4扣非转正+医药板块持续β" },
        { "name": "基准", "prob": "55%", "range": "13.2~15.7元", "trigger": "缩量平台延续，题材轮动无主线", "most_likely": True },
        { "name": "悲观", "prob": "25%", "range": "11.0~13.0元", "trigger": "情绪退潮+3%减持加速+扣非恶化" }
      ],
      "current_price_note": "现价14.71在基准区间中部、箱体上沿15.7下方一步之遥",
      "weight_ranking": None,
      "catalysts": None,
      "falsify": None,
      "valid_nodes": [
        { "time": "2027-01-07前", "event": "陈再宏3%减持窗口(2026-10-08起)", "verify": "减持进展公告/大宗交易记录", "miss_action": "减持完毕且无新增计划→压制解除；若叠加新转让公告→控制权重估预期升温" },
        { "time": "2027-04年报季", "event": "2026年报+Q4扣非全年验证", "verify": "扣非能否修复至7000万+(前三季4431万)", "miss_action": "扣非继续下滑→回归基本面锚下沿11~13元" },
        { "time": "12个月内不定期", "event": "江浩涛(5%新股东)后续动作", "verify": "是否增持/派驻董事/资产运作", "miss_action": "锁定期内无动作→纯财务投资定性，情绪溢价消退" }
      ]
    }
  },

  "matrix_L2": {
    "active_risks": ["扣非前三季-20.98%真实盈利下滑", "实控人系3%减持进行中(至2027-01-07)+此前10年首次减持即抛8%", "题材脉冲退潮回落风险(8月16.90→10月11.46已演示-32%)", "三季报非经常损益3339万占归母43%"],
    "vetoes": [],
    "extreme_day": False
  },

  "fusion": {
    "direction": "中性偏弱",
    "confidence": "低(死叉第4日未修复+问事盘力量缠斗+题材情绪主导无天时窗口)",
    "form": "缩量平台整理第4周，14~15.7箱体上沿压制，今日+3.74%试上攻",
    "verdict": "v0(-1:死叉+微绿柱+DIF零上)×a_macd(-1:绿柱第4日)×q(0:问事盘多空缠斗)→合成-2档弱侧，C维持家族弱分支——力量结构偏空但底盘未坏，方向中性偏弱"
  },

  "pricing": {
    "target_price": {
      "sources": [
        { "source": "基本面估值", "range": "11~15元", "basis": "2026E归母~1.0亿(前三季7770万+Q4传统旺季)×35-45倍PE/扣非0.65亿×45倍" },
        { "source": "启动特征量度", "range": "17.8~19.9元", "basis": "z=1平台突破1:1量度：上沿15.7+平台高度4.24≈19.9；底部翻倍路径8.89×2=17.78" },
        { "source": "翻倍基因先例", "range": "17~26元", "basis": "模式9案例脉冲中位+126%(神奇制药+50%/一鸣食品+202%,n=2)，自本轮低点11.46起算×1.5~2.3" }
      ],
      "overlap_zone": "17.8~19.9元（技术量度与情绪源交集，+21%~+35%）",
      "divergence_note": "基本面锚11~15已贴近现价14.71，技术/情绪源高出基本面30~70%——典型情绪透支结构，追高即接题材盘",
      "confidence": "低（三源分歧大+基本面锚低于现价）"
    },
    "timing": {
      "timing_window": "问事盘时干丁落艮八螣蛇+景门——情绪缠绕拖延无明确兑现窗口；值符落震三死门——突破时点未定；生门在兑七白虎——若冲高兑现窗口短促宜快出。天时窗口缺席，靠题材脉冲，Q4扣非不转正则情绪退潮回归基本面锚",
      "strength_check": "日干戊落巽四惊门+九天——力量虚惊不实，技术/情绪源目标价打7折看待，有效区约13~15元",
      "tail_risk": "玄武临庚(卖盘)——大股东3%减持窗口至2027-01+后续或继续协议转让；螣蛇——题材证伪/澄清风险；扣非持续下滑的盈利质量风险"
    }
  },

  "verdict": {
    "summary": "婴儿保育设备细分龙头，但这是一只基本面平庸、靠题材脉冲吃饭的票，当下唯一要盯的是14~15.7平台能不能放量突破。量来且Q4扣非修复，可看17.8~19.9情绪技术区；量不来，3%减持窗口压制加情绪退潮，回落看11~15基本面锚。坐标：z=1横盘整理×g=4中性偏弱。",
    "dims_oneliner": {
      "gene": "模式9游资情绪驱动型(约4/5项)——小市值40亿+扣非下滑+医药板块脉冲主导；模式5仅2/5，业绩拐点不成立",
      "state": "一波+90%主升后缩量平台一个月，量比0.75，MA20上方多头排列未坏，箱体上沿15.7压制",
      "report": "现场版：三季报归母+147%但非经常占43%、扣非-21%，基本面账本待V4.7深跑",
      "forecast": "中性偏弱——死叉第4日+问事盘多空缠斗，题材情绪未散但无天时窗口"
    },
    "key_risk": "题材情绪退潮+实控人系3%减持(至2027-01)双击回落——8月16.90到10月11.46已经演示过一次-32%",
    "tracking": "盯Q4扣非修复进度+平台量能是否重回60日均量上方；跌破MA20(13.53)为减仓信号"
  },

  "verification": None,

  "view_gene": {
    "total_lit": 7,
    "total_partial": 0,
    "total_vars": 10,
    "top_pattern": "模式9 游资情绪驱动型",
    "note": "题材脉冲型标的，业绩驱动路径不成立；模式5两项点亮但不构成拐点",
    "patterns": [
      {
        "id": "模式9", "name": "游资情绪驱动型", "top": True,
        "lit_vars": 5, "total_vars": 5,
        "vars": [
          { "status": "lit", "name": "小市值<50亿", "evidence": "总市值40.8亿(11-09)" },
          { "status": "lit", "name": "低关注度", "evidence": "研报覆盖稀少，雪球3.25万关注，QFII重仓概念10-23才新增" },
          { "status": "lit", "name": "基本面弱无拐点", "evidence": "2026H1净利-52.75%，扣非前三季-20.98%" },
          { "status": "lit", "name": "板块热点刺激", "evidence": "8-17医药涨停潮(药明康德新高)20cm涨停；10-19~23器械板块+Q3业绩反弹+27%" },
          { "status": "lit", "name": "游资主导", "evidence": "8月脉冲换手19-47%，脉冲急涨急跌(Aug+90%后-32%)" }
        ]
      },
      {
        "id": "模式5", "name": "景气共振型", "top": False,
        "lit_vars": 2, "total_vars": 5,
        "vars": [
          { "status": "lit", "name": "主业细分龙头", "evidence": "婴儿保育设备国内率先上市，单项冠军培育企业" },
          { "status": "lit", "name": "内生升级", "evidence": "吻合器第二曲线+2026-09新增监护/呼吸设备生产许可" },
          { "status": "none", "name": "下游高景气", "evidence": "医疗器械温和修复非爆发；育儿补贴属长期慢变量" },
          { "status": "none", "name": "业绩拐点", "evidence": "扣非前三季-20.98%，归母高增靠非经常损益" },
          { "status": "none", "name": "国产替代卡位", "evidence": "婴儿保育设备非卡脖子清单" }
        ]
      }
    ]
  },

  "view_state": {
    "current_idx": 1,
    "zones": [
      { "name": "底部区", "range": "距年内低点<15%(8.89，2026-06-29)" },
      { "name": "横盘整理区", "range": "13.4~15.7箱体(10月以来缩量一个月)" },
      { "name": "放量突破区", "range": "放量站上15.7，量比>2" },
      { "name": "主升区", "range": "15.7上方打开至前高16.90/19.9量度位" },
      { "name": "退潮区", "range": "跌破MA20(13.53)回箱体下沿" }
    ],
    "judgment": [
      { "dim": "价格位置", "status": "lit", "value": "距低点+59.5%", "evidence": "8.89(6-29)→14.18(11-09)，>40%否决底部区判法" },
      { "dim": "量能", "status": "lit", "value": "量比0.75", "evidence": "5日均量8.49M/60日均量11.37M，缩量整理符合平台特征" },
      { "dim": "均线结构", "status": "lit", "value": "多头排列", "evidence": "MA5>MA10>MA20>MA60，价在所有均线上方；MA120(11.27)远在下" },
      { "dim": "资金", "status": "part", "value": "主力小额净流入", "evidence": "10-23主力+1715万，11-09+205万，今日盘中+405万——脉冲日大额、日常小额" },
      { "dim": "筹码结构", "status": "part", "value": "实控人系61.06%", "evidence": "陈氏兄弟半月内抛8%(5%协议转让9.60元+3%减持至2027-01)，江浩涛5%新进锁12个月" },
      { "dim": "题材", "status": "lit", "value": "婴童/器械/QFII重仓", "evidence": "走势最相关=医药医疗器械板块β(8月/10月两轮脉冲同步板块)" },
      { "dim": "基本面", "status": "part", "value": "扣非-20.98%", "evidence": "前三季归母7770万(+6.99%)但扣非4431万(-20.98%)，非经常占43%" },
      { "dim": "环境", "status": "lit", "value": "大盘偏多C维持", "evidence": "11-10奇门定级偏多(深水盲区压级后)，医药板块近期活跃" }
    ],
    "transitions": [
      { "from": "横盘整理区", "to": "放量突破区", "conditions": [ { "text": "放量(量比>2)站上15.7", "met": False }, { "text": "Q4扣非修复预期强化", "met": False } ] },
      { "from": "横盘整理区", "to": "退潮区", "conditions": [ { "text": "跌破MA20(13.53)", "met": False }, { "text": "减持加速/题材澄清", "met": False } ] }
    ],
    "note": "缩量平台+多头排列未坏，多空在箱体上沿僵持，方向选择临近"
  },

  "daily_chain": [
    { "name": "① MACD底座", "tag": "v0", "output": "v0=-1 偏弱", "formula": "交叉项(死叉)×柱体(-0.04微绿)×DIF位置(零上)=弱空", "note": "11-03死叉后第4日，DIF0.46零上托底未坏" },
    { "name": "② 柱体油门", "tag": "a_macd", "output": "a_macd=-1", "note": "绿柱第4日，柱体p38分位，油门缺失" },
    { "name": "③ 奇门修正", "tag": "q_bias", "output": "q_bias=0", "note": "问事盘多空缠斗：玄武临庚(暗减)vs乙奇伤门，时干螣蛇景门情绪缠绕" },
    { "name": "④ 合成定级", "tag": "fusion", "output": "中性偏弱(低置信)", "formula": "v0(-1)+a(-1)+q(0)→-2档弱侧", "note": "C维持家族弱分支" },
    { "name": "⑤ 三源目标价", "tag": "pricing", "output": "基本面锚11~15/技术情绪源17.8~19.9", "note": "现价贴基本面锚上沿，情绪源高出30-70%" },
    { "name": "⑥ 对账回填", "tag": "verification", "output": "首诊待回填", "note": "下次点播自动回填本次预判" }
  ],

  "todo_list": [
    "V4.7全量个股分析异步补跑，替换现场版报告(weight_ranking/catalysts/falsify)",
    "陈再宏3%减持进展跟踪(至2027-01-07)",
    "Q4扣非环比验证(2027-04年报)",
    "平台突破确认信号：量比>2且站上15.7；防守信号：跌破MA20(13.53)"
  ],

  "history": [
    { "date": DATE, "v0": -1, "a_macd": -1, "q_bias": 0, "pred": "中性偏弱", "actual": "--", "hit": "待回填", "cell": "1_4" }
  ],

  "prev_diagnose": None,

  "timeline": [
    {
      "date": "2026-09-21",
      "type": "restructure",
      "event": "实控人之一陈再慰协议转让5%股份(9.60元/股，1.38亿)予江浩涛；9-8陈再宏预披露减持3%(10-08~2027-01-07)——陈氏兄弟半月合计拟退出8%，仍控股61.06%不变更控制权",
      "dims": { "gene": "事件时基因未定(首诊前)", "state": "事件前股价12~13元低位区", "forecast": None, "report": None }
    },
    {
      "date": "2026-10-16",
      "type": "restructure",
      "event": "协议转让5%过户完成，江浩涛成5%以上股东承诺12个月不减持",
      "dims": { "gene": "事件时基因未定(首诊前)", "state": "过户完成日股价11.61(阶段低位)", "forecast": None, "report": None }
    },
    {
      "date": "2026-10-23",
      "type": "earnings",
      "event": "2026三季报：前三季归母7770万(+6.99%)，Q3单季5361万(+147.71%)，但扣非前三季4431万(-20.98%)——非经常损益3340万占43%",
      "dims": { "gene": "事件时基因未定(首诊前)", "state": "披露日股价14.63，周涨+26%", "forecast": None, "report": None }
    },
    {
      "date": DATE,
      "type": "diagnose",
      "event": "首诊：横盘整理×中性偏弱｜模式9题材脉冲型｜三源分歧大",
      "dims": { "gene": "模式9 游资情绪驱动型(4/5)", "state": "z=1 横盘整理(缩量平台)", "forecast": "中性偏弱(死叉第4日+问事盘缠斗)", "report": "现场版占位，V4.7异步补跑" }
    }
  ]
}

p_latest = os.path.join(OUT_DIR, f"diagnose_{CODE}.json")
p_dated = os.path.join(OUT_DIR, f"diagnose_{CODE}_20261110.json")
for p in (p_latest, p_dated):
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written:", p_latest, p_dated)

# 索引更新
idx_p = "/root/.openclaw/workspace/memory/个股诊断档案/INDEX.json"
idx = json.load(open(idx_p, encoding="utf-8"))
idx[CODE] = { "name": "戴维医疗", "last_diagnose": DATE, "count": 1, "last_zone": "横盘整理", "last_gene": "模式9 游资情绪驱动型", "last_grade": "中性偏弱" }
json.dump(idx, open(idx_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("INDEX updated")

# 看板总索引
di_p = os.path.join(OUT_DIR, "diagnoses_index.json")
di = json.load(open(di_p, encoding="utf-8")) if os.path.exists(di_p) else { "stocks": [] }
stocks = di.setdefault("stocks", [])
row = next((s for s in stocks if s.get("code") == CODE), None)
if row:
    row.update({ "name": "戴维医疗", "last_date": DATE, "count": row.get("count", 0) + 1,
                 "last_zone": "横盘整理", "last_gene": "模式9 游资情绪驱动型", "last_grade": "中性偏弱" })
    if "20261110" not in row.setdefault("dates", []):
        row["dates"].append("20261110")
else:
    stocks.append({ "code": CODE, "name": "戴维医疗", "last_date": DATE, "count": 1,
                    "dates": ["20261110"], "last_zone": "横盘整理", "last_gene": "模式9 游资情绪驱动型", "last_grade": "中性偏弱" })
json.dump(di, open(di_p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("diagnoses_index updated")
