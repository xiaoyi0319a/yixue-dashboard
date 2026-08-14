const { execSync } = require('child_process');
const fs = require('fs');

const times = [
  '09:30', '09:40', '09:50', '10:00', '10:10', '10:20',
  '10:30', '10:40', '10:50', '11:00', '11:10', '11:20', '11:30',
  '13:00', '13:10', '13:20', '13:30', '13:40', '13:50',
  '14:00', '14:10', '14:20', '14:30', '14:40', '14:50', '15:00'
];

const results = [];

for (const time of times) {
  try {
    const output = execSync(`node run_qimen_local.js 2026-08-10 ${time}`, {
      encoding: 'utf8',
      timeout: 30000
    });
    
    const lines = output.split('\n');
    let juShu = '', zhiFu = '', zhiFuGong = '', zhiShi = '';
    let gengGong = '', yiGong = '', wuGong = '', shengMenGong = '';
    
    for (const line of lines) {
      if (line.includes('局数:')) juShu = line.split('局数:')[1].trim();
      if (line.includes('值符:')) zhiFu = line.split('值符:')[1].trim();
      if (line.includes('值符落宫:')) zhiFuGong = line.split('值符落宫:')[1].trim();
      if (line.includes('值使:')) zhiShi = line.split('值使:')[1].trim();
      if (line.includes('庚金(卖盘)在')) {
        const m = line.match(/庚金\(卖盘\)在\s*(\S+)/);
        if (m) gengGong = m[1];
      }
      if (line.includes('乙奇(买盘)在')) {
        const m = line.match(/乙奇\(买盘\)在\s*(\S+)/);
        if (m) yiGong = m[1];
      }
      if (line.includes('景门(情绪/成交)在')) {
        const m = line.match(/景门\(情绪\/成交\)在\s*(\S+)/);
        if (m) wuGong = m[1];
      }
      if (line.includes('生门(利润)在')) {
        const m = line.match(/生门\(利润\)在\s*(\S+)/);
        if (m) shengMenGong = m[1];
      }
    }
    
    results.push({
      time, juShu, zhiFu, zhiFuGong, zhiShi,
      gengGong, yiGong, wuGong, shengMenGong
    });
    
    console.log(`OK ${time}`);
  } catch (e) {
    console.log(`ERR ${time}: ${e.message}`);
    results.push({ time, error: e.message });
  }
}

fs.writeFileSync('/root/.openclaw/workspace/memory/奇门预测/起盘数据/qimen_daxin_20260810.json', JSON.stringify(results, null, 2));
console.log('Done');
