// 本地运行奇门排盘 - V3.99
// 用法: node run_qimen_local.js [YYYY-MM-DD] [HH:MM]
// 默认: 今天 09:30

const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

// 解析命令行参数
const targetDate = process.argv[2] || new Date().toISOString().split('T')[0];
const targetTime = process.argv[3] || '09:30';

const htmlPath = path.join(__dirname, 'qimen.html');
const html = fs.readFileSync(htmlPath, 'utf8');

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  url: "http://localhost"
});

const { document } = dom.window;

// 禁用自动设置当前时间的 useNow 函数
dom.window.useNow = function() {};

// 设置日期时间
document.getElementById('date').value = targetDate;
document.getElementById('time').value = targetTime;

dom.window.qiPan();

let data = dom.window.currentPanData || dom.window.qimenPanData;

if (!data) {
  console.error('错误：无法获取排盘数据');
  process.exit(1);
}

// 简洁输出（无调试信息）
console.log('=== 奇门遁甲排盘 ===');
console.log('日期:', targetDate);
console.log('时间:', targetTime, `(${data.sizhu.hour.ganZhi})`);
console.log('节气:', data.jieQi ? data.jieQi.name : '未知');
console.log('局数:', data.juInfo ? (data.juInfo.type + data.juInfo.ju + '局') : '未知');
console.log('旬首:', data.zhiFuInfo ? data.zhiFuInfo.xunShou : '未知');
console.log('值符:', data.zhiFuInfo ? data.zhiFuInfo.zhiFuXing : '未知');
console.log('值符落宫:', data.zhiFuInfo ? data.zhiFuInfo.zhiFuGong : '未知');
console.log('值使:', data.zhiFuInfo ? data.zhiFuInfo.zhiShiMen : '未知');
console.log('马星:', data.maXing || '未知');
console.log('');
console.log('【四柱八字】');
console.log('年柱:', data.sizhu.year.ganZhi);
console.log('月柱:', data.sizhu.month.ganZhi);
console.log('日柱:', data.sizhu.day.ganZhi, `(日干:${data.sizhu.day.gan})`);
console.log('时柱:', data.sizhu.hour.ganZhi, `(时干:${data.sizhu.hour.gan})`);
console.log('');

const gongNames = {1: '坎一', 2: '坤二', 3: '震三', 4: '巽四', 5: '中五', 6: '乾六', 7: '兑七', 8: '艮八', 9: '离九'};
const gongOrder = [4, 9, 2, 3, 5, 7, 8, 1, 6];

console.log('【九宫格】');
gongOrder.forEach(gongNum => {
    const tp = data.tianPan && data.tianPan[gongNum] ? data.tianPan[gongNum] : {};
    const star = tp.star || '';
    const tpGan = tp.gan || '';
    const dpGan = data.diPan && data.diPan[gongNum] ? data.diPan[gongNum] : '';
    const shen = data.baShen && data.baShen[gongNum] ? data.baShen[gongNum] : '';
    const men = data.baMen && data.baMen[gongNum] ? data.baMen[gongNum] : '';
    const yg = (data.yinGan && data.yinGan[gongNum]) || (data.yinGan && data.yinGan[String(gongNum)]) || '';
    const isZhiFu = (data.zhiFuInfo && gongNum === data.zhiFuInfo.zhiFuGong) ? ' [值符]' : '';
    
    console.log(`[${gongNames[gongNum]}${isZhiFu}] 神:${shen} 星:${star} 天:${tpGan} 地:${dpGan} 门:${men} 隐:${yg}`);
});

console.log('');
console.log('【交易用神位置】');
const dayGan = data.sizhu.day.gan;
const hourGan = data.sizhu.hour.gan;

gongOrder.forEach(gongNum => {
    const tp = data.tianPan && data.tianPan[gongNum] ? data.tianPan[gongNum] : {};
    const tpGan = tp.gan || '';
    const men = data.baMen && data.baMen[gongNum] ? data.baMen[gongNum] : '';
    const shen = data.baShen && data.baShen[gongNum] ? data.baShen[gongNum] : '';
    
    if (tpGan === dayGan) console.log(`日干(${dayGan})在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    if (tpGan === hourGan) console.log(`时干(${hourGan})在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    if (tpGan === '乙') console.log(`乙奇(买盘)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    if (tpGan === '庚') console.log(`庚金(卖盘)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    if (tpGan === '戊') console.log(`甲子戊(本金)在 ${gongNames[gongNum]} - 神:${shen} 门:${men}`);
    if (men === '生门') console.log(`生门(利润)在 ${gongNames[gongNum]} - 神:${shen} 天:${tpGan}`);
    if (men === '景门') console.log(`景门(情绪/成交)在 ${gongNames[gongNum]} - 神:${shen} 天:${tpGan}`);
});

// 保存JSON
const outDir = path.join(__dirname, '..', 'memory', '奇门预测');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
const outFile = path.join(outDir, `qimen_data_${targetDate.replace(/-/g, '')}.json`);
fs.writeFileSync(outFile, JSON.stringify(data, null, 2));
console.log('');
console.log('数据已保存到', outFile);
