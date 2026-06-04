// 使用jsdom执行qimen.html V3.86排盘逻辑
const { JSDOM } = require('jsdom');
const fs = require('fs');

// 读取qimen.html
const html = fs.readFileSync('/root/.openclaw/workspace/yixue-dashboard/qimen.html', 'utf8');

// 创建jsdom环境
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  url: "http://localhost"
});

const { document } = dom.window;

// 设置日期和时间
const dateInput = document.getElementById('date');
const timeInput = document.getElementById('time');
dateInput.value = '2026-04-24';
timeInput.value = '09:30';

// 调用起盘函数
dom.window.qiPan();

// 获取排盘数据
const data = dom.window.currentPanData;

// 输出结果
console.log('=== 奇门遁甲排盘 ===');
console.log('日期: 2026-04-24');
console.log('时间: 09:30 (丁巳时)');
console.log('节气:', data.jieQi.name);
console.log('局数:', data.juInfo.type + data.juInfo.ju + '局');
console.log('旬首:', data.zhiFuInfo.xunShou);
console.log('值符:', data.zhiFuInfo.zhiFuXing);
console.log('值使:', data.zhiFuInfo.zhiShiMen);
console.log('马星:', data.maXing);
console.log('');
console.log('【四柱八字】');
console.log('年柱:', data.sizhu.year.ganZhi);
console.log('月柱:', data.sizhu.month.ganZhi);
console.log('日柱:', data.sizhu.day.ganZhi, '(日干:', data.sizhu.day.gan + ')');
console.log('时柱:', data.sizhu.hour.ganZhi, '(时干:', data.sizhu.hour.gan + ')');
console.log('');

// 输出九宫格
const gongNames = {1: '坎一', 2: '坤二', 3: '震三', 4: '巽四', 5: '中五', 6: '乾六', 7: '兑七', 8: '艮八', 9: '离九'};
const gongOrder = [4, 9, 2, 3, 5, 7, 8, 1, 6];

console.log('【九宫格】');
gongOrder.forEach(gongNum => {
    const tp = data.tianPan[gongNum] || {};
    const star = tp.star || '';
    const tpGan = tp.gan || '';
    const dpGan = data.diPan[gongNum] || '';
    const shen = data.baShen[gongNum] || '';
    const men = data.baMen[gongNum] || '';
    const yg = data.yinGan[gongNum] || data.yinGan[String(gongNum)] || '';
    const isZhiFu = (gongNum === data.zhiFuInfo.zhiFuGong) ? ' [值符]' : '';
    
    console.log(`[${gongNames[gongNum]}${isZhiFu}] 神:${shen} 星:${star} 天:${tpGan} 地:${dpGan} 门:${men} 隐:${yg}`);
});

console.log('');
console.log('【交易用神位置】');
gongOrder.forEach(gongNum => {
    const tp = data.tianPan[gongNum] || {};
    const tpGan = tp.gan || '';
    const men = data.baMen[gongNum] || '';
    const shen = data.baShen[gongNum] || '';
    
    if (tpGan === data.sizhu.day.gan) {
        console.log(`日干(${data.sizhu.day.gan})在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    }
    if (tpGan === data.sizhu.hour.gan) {
        console.log(`时干(${data.sizhu.hour.gan})在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    }
    if (tpGan === '乙') {
        console.log(`乙奇(买盘)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    }
    if (tpGan === '庚') {
        console.log(`庚金(卖盘)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    }
    if (tpGan === '戊') {
        console.log(`甲子戊(本金)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    }
    if (men === '生门') {
        console.log(`生门(利润)在 ${gongNames[gongNum]} - 神:${shen} 天:${tpGan}`);
    }
    if (men === '景门') {
        console.log(`景门(情绪/成交)在 ${gongNames[gongNum]} - 神:${shen} 天:${tpGan}`);
    }
});

fs.writeFileSync('/tmp/qimen_20260424.json', JSON.stringify(data, null, 2));
console.log('');
console.log('数据已保存到 /tmp/qimen_20260424.json');