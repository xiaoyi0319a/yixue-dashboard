/* ============================================================
   一日主帅 · 盘局剧场（羿学天天看 hero）
   设计参考：《大神Okami》水墨白描 × 皮影分层舞台 × 电影分镜运镜
   数据：data/pipeline_latest.json（palace_table/four_slots）+ 页面DOM
        （卦象诗/时辰判语/大势判语——零数据管道新增）
   降级：数据缺失→整剧场隐藏，经典布局兜底；caption缺失→该幕只演不写字
   ============================================================ */
(function () {
    'use strict';

    /* ---------- 八神线条像（stroke白描，currentColor着色） ---------- */
    var DEITIES = {
        '值符': { color: '#e6be6e', svg:
            '<symbol id="dy-zhifu" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M30,20 L36,8 L43,17 L50,6 L57,17 L64,8 L70,20"/>' +         /* 冕旒三峰 */
            '<path d="M30,20 L70,20"/>' +                                          /* 冕梁 */
            '<circle cx="50" cy="30" r="8"/>' +                                   /* 首 */
            '<path d="M50,38 L30,88 L70,88 Z"/>' +                                 /* 袍身 */
            '<path d="M50,44 L34,62 M50,44 L66,62"/>' +                           /* 广袖 */
            '<path d="M37,58 L63,58"/>' +                                          /* 束带 */
            '<rect x="45" y="46" width="10" height="30" rx="1.5"/>' +              /* 圭 */
            '<path d="M50,76 L50,88"/>' +
            '</g></symbol>' },
        '螣蛇': { color: '#c07ee0', svg:
            '<symbol id="dy-tengshe" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M18,82 C30,64 14,54 30,44 C46,34 40,18 60,20 C76,22 70,38 84,42"/>' + /* 蛇身S */
            '<path d="M84,42 L94,38 L88,48 Z"/>' +                                 /* 蛇首三角 */
            '<path d="M94,40 L98,36 M94,42 L99,43"/>' +                           /* 信子 */
            '<path d="M30,44 C34,52 26,58 24,64"/>' +                             /* 腹线 */
            '</g></symbol>' },
        '太阴': { color: '#9db4d4', svg:
            '<symbol id="dy-taiyin" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M30,84 C26,44 38,22 50,22 C62,22 74,44 70,84"/>' +           /* 兜帽 */
            '<path d="M38,84 C36,54 44,38 50,38 C56,38 64,54 62,84"/>' +           /* 内影 */
            '<path d="M42,70 Q50,62 58,70"/>' +                                   /* 敛手 */
            '<path d="M70,30 a10,10 0 1,0 8,14 a8,8 0 1,1 -8,-14"/>' +            /* 月牙 */
            '</g></symbol>' },
        '六合': { color: '#7fd4b0', svg:
            '<symbol id="dy-liuhe" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="26" cy="50" r="9"/>' + '<circle cx="74" cy="50" r="9"/>' + /* 两端环 */
            '<path d="M35,50 C44,34 56,66 65,50"/>' +                             /* 交缠一 */
            '<path d="M35,50 C44,66 56,34 65,50"/>' +                             /* 交缠二 */
            '</g></symbol>' },
        '白虎': { color: '#ff6a55', svg:
            '<symbol id="dy-baihu" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M22,64 C20,48 42,42 58,46 C74,50 80,58 78,66"/>' +           /* 虎身 */
            '<circle cx="76" cy="50" r="10"/>' +                                  /* 虎头 */
            '<path d="M68,42 L66,34 L73,40 M78,41 L82,33 L85,41"/>' +             /* 耳 */
            '<path d="M22,62 C12,56 14,42 26,38"/>' +                             /* 尾 */
            '<path d="M36,66 L34,86 M50,68 L50,88 M64,68 L66,86"/>' +             /* 腿 */
            '<path d="M40,52 l4,6 M52,50 l4,6 M64,52 l3,5"/>' +                   /* 纹 */
            '<path d="M86,46 L97,42 M86,52 L96,53"/>' +                           /* 衔刀 */
            '</g></symbol>' },
        '玄武': { color: '#4a6fd4', svg:
            '<symbol id="dy-xuanwu" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<ellipse cx="44" cy="68" rx="20" ry="12"/>' +                         /* 龟甲 */
            '<circle cx="70" cy="58" r="6"/>' +                                   /* 龟首 */
            '<path d="M62,62 L66,60"/>' +
            '<path d="M32,78 L30,86 M44,80 L44,88 M56,78 L58,86"/>' +             /* 龟足 */
            '<path d="M30,60 C38,44 60,42 70,52 C78,60 72,66 84,66 L92,62"/>' +   /* 蛇绕 */
            '<path d="M92,62 L97,58"/>' +
            '</g></symbol>' },
        '九地': { color: '#d4a017', svg:
            '<symbol id="dy-jiudi" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M16,78 Q32,56 48,78"/>' +                                   /* 三重叠山 */
            '<path d="M34,82 Q50,60 66,82"/>' +
            '<path d="M52,74 Q68,52 84,74"/>' +
            '<path d="M12,86 L88,86"/>' +                                         /* 地线 */
            '<path d="M22,90 L26,90 M42,90 L46,90 M62,90 L66,90 M78,90 L82,90"/>' +
            '</g></symbol>' },
        '九天': { color: '#6ec6ff', svg:
            '<symbol id="dy-jiutian" viewBox="0 0 100 100">' +
            '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="50" cy="34" r="6"/>' +                                   /* 首 */
            '<path d="M50,40 L50,62"/>' +                                         /* 身 */
            '<path d="M50,46 C32,42 22,30 18,16 M44,20 l-8,-4 M36,28 l-9,-2"/>' + /* 左翼+翎 */
            '<path d="M50,46 C68,42 78,30 82,16 M56,20 l8,-4 M64,28 l9,-2"/>' +   /* 右翼+翎 */
            '<path d="M50,62 C46,72 54,78 50,90"/>' +                            /* 飘带 */
            '<path d="M40,92 C46,88 54,88 60,92"/>' +
            '</g></symbol>' }
    };

    /* 门楼剪影（八门复用，按门色着色） */
    var GATE =
        '<symbol id="dy-gate" viewBox="0 0 100 100">' +
        '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
        '<path d="M22,38 L50,22 L78,38"/>' + '<path d="M26,38 L74,38"/>' +       /* 楼顶 */
        '<path d="M30,38 L30,86 M70,38 L70,86"/>' +                           /* 柱 */
        '<path d="M30,48 L70,48 M30,58 L70,58"/>' +                           /* 梁 */
        '<path d="M18,86 L82,86"/>' +
        '</g></symbol>';

    /* 洛书位 → 舞台坐标（1200×675，轻透视：后小前大） */
    var LUOSHU_POS = {
        '巽四': { x: 340, y: 200, s: 0.82 }, '离九': { x: 600, y: 175, s: 0.86 }, '坤二': { x: 860, y: 200, s: 0.82 },
        '震三': { x: 310, y: 360, s: 1.0 }, '中五': { x: 600, y: 340, s: 0.9 }, '兑七': { x: 890, y: 360, s: 1.0 },
        '艮八': { x: 355, y: 520, s: 1.18 }, '坎一': { x: 600, y: 540, s: 1.22 }, '乾六': { x: 845, y: 520, s: 1.18 }
    };
    var PALACE_ALIAS = { '巽四': '巽四', '巽4': '巽四', '四': '巽四', '4': '巽四', '离九': '离九', '离9': '离九', '九': '离九', '9': '离九', '坤二': '坤二', '坤2': '坤二', '二': '坤二', '2': '坤二', '震三': '震三', '震3': '震三', '三': '震三', '3': '震三', '中五': '中五', '中5': '中五', '五': '中五', '5': '中五', '兑七': '兑七', '兑7': '兑七', '七': '兑七', '7': '兑七', '艮八': '艮八', '艮8': '艮八', '八': '艮八', '8': '艮八', '坎一': '坎一', '坎1': '坎一', '一': '坎一', '1': '坎一', '乾六': '乾六', '乾6': '乾六', '六': '乾六', '6': '乾六' };
    var DOOR_COLOR = { '休门': '#3aa0ff', '生门': '#d4a017', '伤门': '#2fbf71', '杜门': '#57c785', '景门': '#ff5a3c', '死门': '#8a7a4a', '惊门': '#e8e8f0', '开门': '#e8e8f0' };
    var GRADE_HEAT = { '强多': 3, '偏多': 2, '中多': 2, '偏强': 3, '微偏强': 1, '略偏多': 1.5, '中性偏强': 1, '无方向': 0, '中性': 0, '中性偏弱': -1, '微偏弱': -1, '略偏空': -1.5, '偏弱': -2, '偏空': -2, '中空': -2, '强空': -3 };

    function palaceKey(name) {
        if (!name) return null;
        var m = String(name).match(/[巽离坤震中兑艮坎乾一二三四五六七八九]+/);
        var k = m ? m[0] : name;
        return PALACE_ALIAS[k] || null;
    }
    function el(tag, attrs, parent) {
        var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (var a in attrs) e.setAttribute(a, attrs[a]);
        if (parent) parent.appendChild(e); return e;
    }

    /* ---------- 字幕采集：从 {{QIMEN_CONTENT}} 的DOM里取，零管道 ---------- */
    function harvest() {
        var poem = [];
        var ph = document.querySelector('.qimen-hexagram p');
        if (ph) {
            var html = ph.innerHTML;
            poem = html.split(/<br\s*\/?>/i).map(function (s) {
                var d = document.createElement('div'); d.innerHTML = s; return d.textContent.trim();
            }).filter(Boolean);
        }
        var slots = [];
        document.querySelectorAll('.time-slot').forEach(function (slot) {
            var t = slot.querySelector('.time-range');
            var v = slot.querySelector('.time-verdict');
            slots.push({ time: t ? t.textContent.trim() : '', text: v ? v.textContent.trim() : '' });
        });
        var closing = '';
        var vp = document.querySelector('.qimen-verdict p');
        if (vp) {
            var txt = vp.textContent.trim();
            var parts = txt.split(/(?<=。)/);
            closing = parts.slice(-2).join('').trim() || txt;
        }
        return { poem: poem, slots: slots, closing: closing };
    }

    /* ---------- 主流程 ---------- */
    fetch('data/pipeline_latest.json', { cache: 'no-store' }).then(function (r) {
        if (!r.ok) throw 0; return r.json();
    }).then(function (d) {
        var pt = d && d.palace_table;
        if (!pt || !pt.length) throw 0;
        build(pt, d.four_slots || [], harvest(), d);
    }).catch(function () {
        var t = document.getElementById('theater');
        if (t) t.style.display = 'none';   /* 兜底：隐藏剧场，经典布局不受影响 */
    });

    function build(palaces, slots, cap, meta) {
        var host = document.getElementById('theater');
        if (!host) return;
        host.innerHTML = '';
        var W = 1200, H = 675;

        /* 角色清单注入 */
        var defs = el('defs', {}, host);
        for (var k in DEITIES) defs.innerHTML += DEITIES[k].svg;
        defs.innerHTML += GATE;

        var root = el('svg', { viewBox: '0 0 ' + W + ' ' + H, preserveAspectRatio: 'xMidYMid slice', 'class': 'stage' }, host);
        root.setAttribute('width', '100%'); root.setAttribute('height', '100%');

        /* 夜空（按日期播种的星点，日不同图） */
        var seed = (meta.date || '20261110').replace(/-/g, '');
        var s = parseInt(seed, 10) || 1;
        function rnd() { s = (s * 9301 + 49297) % 233280; return s / 233280; }
        var sky = el('g', {}, root);
        for (var i = 0; i < 90; i++) {
            el('circle', { cx: rnd() * W, cy: rnd() * H * 0.72, r: (rnd() * 1.3 + 0.3).toFixed(2), fill: '#9db4d4', opacity: (rnd() * 0.5 + 0.08).toFixed(2) }, sky);
        }
        /* 底光 */
        el('ellipse', { cx: 600, cy: 430, rx: 460, ry: 240, fill: 'url(#tglow)' }, root);
        var g = el('radialGradient', { id: 'tglow' }, defs);
        el('stop', { offset: '0%', 'stop-color': '#16264a', 'stop-opacity': 0.85 }, g);
        el('stop', { offset: '100%', 'stop-color': '#16264a', 'stop-opacity': 0 }, g);

        /* 九宫连线 */
        var net = el('g', { stroke: '#3a5480', 'stroke-width': 1, opacity: 0.35 }, root);
        var keys = Object.keys(LUOSHU_POS);
        var center = LUOSHU_POS['中五'];
        keys.forEach(function (a) {
            if (a === '中五') return;
            el('line', { x1: center.x, y1: center.y, x2: LUOSHU_POS[a].x, y2: LUOSHU_POS[a].y }, net);
        });
        keys.forEach(function (a, i) {
            for (var j = i + 1; j < keys.length; j++) {
                var b = keys[j];
                if (a === '中五' || b === '中五') continue;
                var pa = LUOSHU_POS[a], pb = LUOSHU_POS[b];
                var dx = Math.abs(pa.x - pb.x), dy = Math.abs(pa.y - pb.y);
                if (dx <= 280 && dy <= 180 && !(dx > 260 && dy > 160))
                    el('line', { x1: pa.x, y1: pa.y, x2: pb.x, y2: pb.y }, net);
            }
        });

        /* 幕布层（四幕冷暖光） */
        var warmL = el('ellipse', { cx: 600, cy: 400, rx: 620, ry: 330, fill: '#e6a53a', opacity: 0 }, root);
        var coldL = el('ellipse', { cx: 600, cy: 400, rx: 620, ry: 330, fill: '#2a4fd4', opacity: 0 }, root);
        var darkL = el('rect', { x: 0, y: 0, width: W, height: H, fill: '#02040a', opacity: 0 }, root);

        /* 各宫：门楼 + 神将 */
        var actors = {};
        palaces.forEach(function (p) {
            var key = palaceKey(p.palace); if (!key) return;
            var pos = LUOSHU_POS[key];
            var gP = el('g', { transform: 'translate(' + pos.x + ',' + pos.y + ') scale(' + pos.s + ')' }, root);
            var dc = DOOR_COLOR[p.door] || '#8899aa';
            /* 门楼 */
            var gate = el('g', { color: dc, opacity: 0.35 }, gP);
            el('use', { href: '#dy-gate', x: -40, y: -58, width: 80, height: 80 }, gate);
            /* 神将 */
            var deity = DEITIES[p.god] ? p.god : null;
            var fig = el('g', { color: deity ? DEITIES[deity].color : '#8899aa', opacity: 0.13, 'class': 'dy-fig' }, gP);
            if (deity) el('use', { href: '#dy-' + ({ '值符': 'zhifu', '螣蛇': 'tengshe', '太阴': 'taiyin', '六合': 'liuhe', '白虎': 'baihu', '玄武': 'xuanwu', '九地': 'jiudi', '九天': 'jiutian' })[deity], x: -36, y: -52, width: 72, height: 72 }, fig);
            /* 星光 */
            var spark = el('path', { d: 'M0,-7 L2,-2 L7,0 L2,2 L0,7 L-2,2 L-7,0 L-2,-2 Z', fill: '#c9d8f0', opacity: 0.25, transform: 'translate(26,-46)' }, gP);
            actors[key] = { g: gP, gate: gate, fig: fig, spark: spark, god: p.god, door: p.door, star: p.star, pos: pos };
        });

        /* 值符 = 今日主帅 */
        var zhifuKey = null;
        palaces.forEach(function (p) { if (p.god === '值符') zhifuKey = palaceKey(p.palace); });
        var zhifu = zhifuKey ? actors[zhifuKey] : null;
        var halo = null;
        if (zhifu) {
            zhifu.fig.setAttribute('opacity', 1);
            zhifu.gate.setAttribute('opacity', 0.8);
            zhifu.spark.setAttribute('opacity', 0.9);
            halo = el('circle', { cx: 0, cy: -12, r: 52, fill: 'none', stroke: '#e6be6e', 'stroke-width': 1.6, 'stroke-dasharray': '6 5', opacity: 0.8 }, zhifu.g);
        }

        /* 字幕条 */
        var capG = el('g', { 'class': 'cap' }, root);
        var capBg = el('rect', { x: 120, y: 566, width: 960, height: 72, rx: 10, fill: '#050a16', opacity: 0.72 }, capG);
        var capTitle = el('text', { x: 600, y: 592, 'text-anchor': 'middle', fill: '#c9a86a', 'font-size': 15, 'letter-spacing': 4, opacity: 0 }, capG);
        var capText = el('text', { x: 600, y: 620, 'text-anchor': 'middle', fill: '#e8f1ff', 'font-size': 21, opacity: 0 }, capG);
        capTitle.style.fontFamily = capText.style.fontFamily = '"Noto Serif SC","Songti SC","SimSun",serif';

        /* 控制台 */
        var ctl = document.createElement('div');
        ctl.className = 'theater-ctl';
        ctl.innerHTML = '<button class="tc-btn" id="tc-play">▶ 重演</button>' +
            '<span class="tc-dots" id="tc-dots"></span>' +
            '<a class="tc-skip" href="#qimen-text">跳过看文字版 ↓</a>';
        host.appendChild(ctl);
        var dotsBox = ctl.querySelector('#tc-dots');

        /* 分幕编排 */
        var scenes = [];
        scenes.push({ t: '今日盘局 · ' + (meta.dun || '') + ' ' + (meta.ganzhi || ''), lines: cap.poem, dur: 4200, per: 1900, type: 'poem' });
        scenes.push({ t: '主帅登场', lines: [zhifu ? (zhifuKey + '宫 · ' + (zhifu.star || '') + ' · ' + (zhifu.door || '')) : ''], dur: 2600, type: 'show' });
        var slotN = Math.min(4, cap.slots.length);
        for (var si = 0; si < slotN; si++) {
            var sl = cap.slots[si];
            var grade = slots[si] && slots[si].grade || '';
            scenes.push({ t: '第' + '一二三四'[si] + '幕 · ' + sl.time, lines: [sl.text], dur: 5200, type: 'act', heat: GRADE_HEAT[grade] || 0, idx: si });
        }
        scenes.push({ t: '终幕 · 收子', lines: [cap.closing], dur: 5200, type: 'final' });

        /* 点控 */
        var dots = [];
        scenes.forEach(function (sc, i) {
            var d = document.createElement('button');
            d.className = 'tc-dot'; d.textContent = i === 0 ? '诗' : (i === 1 ? '令' : (i === scenes.length - 1 ? '终' : '一二三四'[i - 2]));
            d.onclick = function () { playFrom(i); };
            dotsBox.appendChild(d); dots.push(d);
        });

        /* 动画引擎 */
        var raf = null, start = 0, sceneIdx = 0, lineIdx = 0, lineShown = 0, playing = false;
        function setCaption(title, text, tOp, cOp) {
            capTitle.textContent = title || '';
            capText.textContent = text || '';
            capTitle.setAttribute('opacity', tOp);
            capText.setAttribute('opacity', cOp);
        }
        function applySceneFx(sc, localMs) {
            var p = Math.min(1, localMs / 900);
            if (sc.type === 'act') {
                var h = sc.heat || 0;
                warmL.setAttribute('opacity', (Math.max(0, h) * 0.12 * p).toFixed(3));
                coldL.setAttribute('opacity', (Math.max(0, -h) * 0.13 * p).toFixed(3));
                /* 主演闪烁：暖幕亮九天/六合/生门侧，冷幕亮白虎/玄武/死门侧 */
                for (var k2 in actors) {
                    var a = actors[k2];
                    if (!a.god || a === zhifu) continue;
                    var side = (a.god === '九天' || a.god === '六合' || a.god === '值符') ? 1 : (a.god === '白虎' || a.god === '玄武') ? -1 : 0;
                    var boost = (side !== 0 && Math.sign(h) === side) ? Math.abs(h) : 0;
                    var idle = 0.13;
                    var pulse = boost ? (Math.sin(localMs / 260) * 0.5 + 0.5) * boost : 0;
                    a.fig.setAttribute('opacity', Math.min(0.95, idle + pulse * 0.75).toFixed(3));
                }
            } else if (sc.type === 'show') {
                warmL.setAttribute('opacity', 0); coldL.setAttribute('opacity', 0);
            } else if (sc.type === 'final') {
                warmL.setAttribute('opacity', 0.05); coldL.setAttribute('opacity', 0.05);
                for (var k3 in actors) actors[k3].fig.setAttribute('opacity', 0.22);
                if (zhifu) zhifu.fig.setAttribute('opacity', 1);
            } else if (sc.type === 'poem') {
                warmL.setAttribute('opacity', 0); coldL.setAttribute('opacity', 0);
            }
        }
        function frame(now) {
            if (!playing) return;
            var el2 = now - start;
            var sc = scenes[sceneIdx];
            if (!sc) { playing = false; return; }
            if (sc.type === 'poem' && sc.lines.length > 1) {
                var li = Math.floor(el2 / sc.per);
                if (li !== lineIdx || el2 - lineShown > sc.per) {
                    lineIdx = li; lineShown = el2;
                    if (li < sc.lines.length) setCaption(sc.t + '（' + (li + 1) + '/' + sc.lines.length + '）', sc.lines[li], 0.9, 1);
                }
            } else {
                setCaption(sc.t, sc.lines[0] || '', 0.9, 1);
            }
            applySceneFx(sc, el2);
            /* 值符呼吸 */
            if (halo) { var sc2 = 1 + Math.sin(now / 640) * 0.04; halo.setAttribute('transform', 'scale(' + sc2 + ')'); }
            /* 场景推进 */
            if (el2 > sc.dur) {
                sceneIdx++;
                if (sceneIdx >= scenes.length) { finish(); return; }
                start = now; lineIdx = -1;
                dots.forEach(function (d, i) { d.classList.toggle('on', i === sceneIdx); });
            }
            raf = requestAnimationFrame(frame);
        }
        function finish() {
            playing = false;
            setCaption(scenes[scenes.length - 1].t, scenes[scenes.length - 1].lines[0] || '', 0.9, 1);
            ctl.querySelector('#tc-play').textContent = '↻ 重演';
        }
        function playFrom(i) {
            if (raf) cancelAnimationFrame(raf);
            sceneIdx = i; playing = true; start = performance.now(); lineIdx = -1;
            ctl.querySelector('#tc-play').textContent = '❚❚ 播放中';
            dots.forEach(function (d, j) { d.classList.toggle('on', j === i); });
            raf = requestAnimationFrame(frame);
        }
        ctl.querySelector('#tc-play').onclick = function () { playFrom(0); };

        /* 文字版折叠提示（页面下方就是完整文字版） */
        host.setAttribute('data-ready', '1');
        playFrom(0);
    }
})();
