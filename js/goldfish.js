/* ============================================================
   背景金鱼 · 羿学天天看（老师22:35指令：紫色款背景游条金鱼）
   文种金鱼侧视：canvas 2D，飘带尾鳍正弦摆动、须、吐泡、柔光
   规则：fixed 背景层(z-index 0)，内容在上；prefers-reduced-motion 只画静态一帧
   ============================================================ */
(function () {
    'use strict';
    var cv = document.createElement('canvas');
    cv.id = 'fishbg';
    cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:60;pointer-events:none;opacity:.86;';
    document.body.insertBefore(cv, document.body.firstChild);
    var style = document.createElement('style');
    style.textContent = '.container,.footer{position:relative;z-index:1}';
    document.head.appendChild(style);

    var ctx = cv.getContext('2d');
    var W = 0, H = 0, DPR = 1;
    function resize() {
        DPR = Math.min(window.devicePixelRatio || 1, 2);
        W = window.innerWidth; H = window.innerHeight;
        cv.width = W * DPR; cv.height = H * DPR;
        ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize);

    /* 状态 */
    var F = {
        x: -160, y: 0, vx: 42, vy: 0, ang: 0, seed: Math.random() * 1000,
        bubbles: [], lastBubble: 0, t: 0
    };

    function bodyPath(c) {
        /* 文种胖金鱼：蛋形身段，腹深背拱 */
        c.beginPath();
        c.moveTo(58, 0);                                    /* 吻端 */
        c.bezierCurveTo(50, -22, 14, -32, -12, -26);      /* 背弧 */
        c.bezierCurveTo(-33, -21, -47, -10, -50, -3);     /* 尾柄上 */
        c.bezierCurveTo(-52, 3, -46, 12, -34, 17);        /* 尾柄下 */
        c.bezierCurveTo(-13, 27, 26, 27, 44, 17);         /* 腹（胖） */
        c.bezierCurveTo(56, 11, 59, 5, 58, 0);
        c.closePath();
    }

    /* 飘带鳍：从锚点展开一条正弦舞动的带状鳍 */
    function ribbon(c, ax, ay, len, wid, phase, hueA, hueB, alpha, dirY) {
        var steps = 14, top = [], bot = [];
        for (var i = 0; i <= steps; i++) {
            var p = i / steps;
            var sway = Math.sin(F.t * 3.1 + phase + p * 3.6) * (3 + 13 * p);
            var x = ax - len * p;
            var y = ay + dirY * wid * Math.sin(p * Math.PI) * 0.35 + sway + dirY * 4 * p;
            var half = wid * (0.5 - 0.32 * p) + Math.sin(p * 9 + phase) * 1.1;
            top.push([x, y - half]);
            bot.push([x, y + half]);
        }
        var g = c.createLinearGradient(ax, ay, ax - len, ay);
        g.addColorStop(0, hueA); g.addColorStop(1, hueB);
        c.beginPath();
        c.moveTo(top[0][0], top[0][1]);
        for (var j = 1; j < top.length; j++) c.lineTo(top[j][0], top[j][1]);
        for (var k = bot.length - 1; k >= 0; k--) c.lineTo(bot[k][0], bot[k][1]);
        c.closePath();
        c.globalAlpha = alpha;
        c.fillStyle = g;
        c.fill();
        /* 鳍脉 */
        c.globalAlpha = alpha * 0.5;
        c.strokeStyle = 'rgba(200,90,20,.6)';
        c.lineWidth = 0.8;
        c.beginPath();
        for (var m = 0; m <= steps; m += 2) {
            var p2 = m / steps;
            var sw2 = Math.sin(F.t * 3.1 + phase + p2 * 3.6) * (3 + 13 * p2);
            var xx = ax - len * p2, yy = ay + dirY * wid * Math.sin(p2 * Math.PI) * 0.35 + sw2 + dirY * 4 * p2;
            c.moveTo(ax, ay); c.lineTo(xx, yy);
        }
        c.stroke();
        c.globalAlpha = 1;
    }

    function drawFish() {
        ctx.save();
        ctx.translate(F.x, F.y);
        ctx.rotate(F.ang);
        ctx.scale(1.26, 1.26);
        /* 柔光 */
        ctx.shadowColor = 'rgba(255,170,60,.45)';
        ctx.shadowBlur = 14;

        /* 尾鳍（后画，层在身体下先画） */
        ribbon(ctx, -45, -1, 78, 31, 0.0, 'rgba(255,140,40,.85)', 'rgba(255,190,90,.15)', 0.8, -1);
        ribbon(ctx, -45, 4, 78, 31, 1.7, 'rgba(255,140,40,.85)', 'rgba(255,190,90,.15)', 0.8, 1);
        ctx.shadowBlur = 0;

        /* 身体 */
        bodyPath(ctx);
        var g = ctx.createLinearGradient(0, -30, 0, 28);
        g.addColorStop(0, '#ff8c2e');
        g.addColorStop(0.45, '#ffb14e');
        g.addColorStop(0.8, '#ffd98f');
        g.addColorStop(1, '#ffe9c4');
        ctx.fillStyle = g;
        ctx.fill();
        /* 背部轮廓线 */
        ctx.strokeStyle = 'rgba(190,84,15,.75)';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(58, 0);
        ctx.bezierCurveTo(50, -22, 14, -32, -12, -26);
        ctx.bezierCurveTo(-33, -21, -47, -10, -50, -3);
        ctx.stroke();
        /* 鳞光 */
        ctx.save();
        bodyPath(ctx);
        ctx.clip();
        ctx.strokeStyle = 'rgba(255,255,255,.14)';
        ctx.lineWidth = 1;
        for (var r = 0; r < 4; r++) {
            ctx.beginPath();
            for (var q = 0; q < 5; q++) {
                var sx = 28 - q * 15, sy = -14 + r * 10;
                ctx.arc(sx, sy, 8, Math.PI * 0.15, Math.PI * 0.85);
            }
            ctx.stroke();
        }
        /* 侧身高光 */
        var hg = ctx.createRadialGradient(18, -4, 2, 18, -4, 33);
        hg.addColorStop(0, 'rgba(255,255,255,.30)');
        hg.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = hg;
        ctx.fillRect(-54, -32, 116, 62);
        ctx.restore();

        /* 背鳍 + 腹鳍（飘带） */
        ctx.shadowColor = 'rgba(255,170,60,.4)'; ctx.shadowBlur = 8;
        ribbon(ctx, 6, -24, 36, 12, 0.9, 'rgba(255,150,50,.8)', 'rgba(255,200,110,.12)', 0.75, -1);
        ribbon(ctx, -8, 19, 46, 11, 2.6, 'rgba(255,150,50,.75)', 'rgba(255,200,110,.10)', 0.7, 1);
        ribbon(ctx, 0, 21, 37, 8, 4.1, 'rgba(255,150,50,.7)', 'rgba(255,200,110,.10)', 0.65, 1);
        ctx.shadowBlur = 0;
        /* 胸鳍扑动 */
        var pec = Math.sin(F.t * 6.2) * 6;
        ctx.save();
        ctx.translate(28, 7);
        ctx.rotate(0.5 + pec * 0.02);
        ctx.fillStyle = 'rgba(255,170,70,.75)';
        ctx.beginPath();
        ctx.ellipse(0, 7, 5, 13, 0.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        /* 眼 */
        ctx.fillStyle = '#2a1503';
        ctx.beginPath(); ctx.arc(35, -9, 3.8, 0, 7); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.9)';
        ctx.beginPath(); ctx.arc(36, -10, 1.3, 0, 7); ctx.fill();
        /* 腮红 */
        ctx.fillStyle = 'rgba(255,110,60,.20)';
        ctx.beginPath(); ctx.arc(44, 5, 7, 0, 7); ctx.fill();
        /* 须（两条，摆动） */
        ctx.strokeStyle = 'rgba(255,214,140,.85)';
        ctx.lineWidth = 1.1;
        for (var w = 0; w < 2; w++) {
            var ph = Math.sin(F.t * 2.4 + w * 1.9) * 5;
            ctx.beginPath();
            ctx.moveTo(55, 4 + w * 2.5);
            ctx.quadraticCurveTo(68, 9 + w * 4 + ph, 78, 15 + w * 6 + ph * 1.4);
            ctx.stroke();
        }
        /* 嘴 */
        ctx.strokeStyle = 'rgba(160,70,20,.8)';
        ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(56, 1, 2.4, -0.9, 0.9); ctx.stroke();
        ctx.restore();
    }

    function step(dt) {
        F.t += dt;
        /* 缓游 + 正弦游弋 + 边界回游 */
        var wob = Math.sin(F.t * 0.55 + F.seed) * 14;
        var wobY = Math.cos(F.t * 0.4 + F.seed * 2) * 18;
        var targetVx = 42 + wob * 0.3;
        var m = 140;
        if (F.x > W - m) targetVx = -Math.abs(targetVx);
        if (F.x < m) targetVx = Math.abs(targetVx);
        var targetVy = (H * 0.62 + wobY * 3 - F.y) * 0.12 + wobY * 0.2;
        if (F.y < H * 0.18) targetVy = Math.abs(targetVy) + 8;
        if (F.y > H * 0.9) targetVy = -Math.abs(targetVy) - 8;
        F.vx += (targetVx - F.vx) * 0.02;
        F.vy += (targetVy - F.vy) * 0.02;
        F.x += F.vx * dt;
        F.y += F.vy * dt;
        var want = Math.atan2(F.vy, F.vx) * (F.vx >= 0 ? 1 : 1);
        /* 鱼头朝速度方向（canvas朝右为正，掉头时身体不翻转——鱼模型侧视单向，用镜像翻转） */
        F.faceRight = F.vx >= 0;
        F.ang += (want - F.ang) * 0.04;
        /* 吐泡 */
        if (F.t - F.lastBubble > 2.2 + Math.random() * 2.5) {
            F.lastBubble = F.t;
            F.bubbles.push({ x: F.x + Math.cos(F.ang) * 58, y: F.y + Math.sin(F.ang) * 58, r: 1.5 + Math.random() * 2.5, vy: -14 - Math.random() * 10, a: 0.7, w: Math.random() * 6.28 });
        }
        for (var i = F.bubbles.length - 1; i >= 0; i--) {
            var b = F.bubbles[i];
            b.y += b.vy * dt; b.x += Math.sin(F.t * 3 + b.w) * 0.35; b.a -= dt * 0.16;
            if (b.a <= 0 || b.y < -10) F.bubbles.splice(i, 1);
        }
    }

    function drawBubbles() {
        ctx.save();
        for (var i = 0; i < F.bubbles.length; i++) {
            var b = F.bubbles[i];
            ctx.strokeStyle = 'rgba(190,225,255,' + (b.a * 0.8).toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.stroke();
            ctx.fillStyle = 'rgba(255,255,255,' + (b.a * 0.25).toFixed(3) + ')';
            ctx.fill();
        }
        ctx.restore();
    }

    var last = 0;
    function loop(ts) {
        var dt = Math.min(0.05, (ts - last) / 1000 || 0.016);
        last = ts;
        step(dt);
        ctx.clearRect(0, 0, W, H);
        ctx.save();
        ctx.translate(F.x, F.y);
        ctx.rotate(F.ang);
        if (!F.faceRight) ctx.scale(1, -1);   /* 掉头时镜像 */
        ctx.translate(-F.x, -F.y);
        drawFish();
        ctx.restore();
        drawBubbles();
        requestAnimationFrame(loop);
    }

    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {
        F.x = W * 0.62; F.y = H * 0.55; F.t = 1.2;
        drawFish();
    } else {
        F.y = H * 0.6;
        requestAnimationFrame(loop);
    }
})();
