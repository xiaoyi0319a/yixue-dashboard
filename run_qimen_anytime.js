const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('/root/.openclaw/workspace/yixue-dashboard/qimen.html', 'utf8');

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  url: "http://localhost"
});

const { document } = dom.window;

const time = process.argv[2] || '10:30';
document.getElementById('date').value = '2026-06-25';
document.getElementById('time').value = time;

dom.window.qiPan();

let data = dom.window.currentPanData || dom.window.qimenPanData;

if (!data) {
    console.log('错误：无法获取排盘数据');
    process.exit(1);
}

// 保存JSON
const outDir = '/root/.openclaw/workspace/memory/奇门预测/起盘数据';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
const suffix = time.replace(':', '');
fs.writeFileSync(outDir + '/qimen_data_20260625_' + suffix + '.json', JSON.stringify(data, null, 2));
console.log('数据已保存到 ' + outDir + '/qimen_data_20260625_' + suffix + '.json');
