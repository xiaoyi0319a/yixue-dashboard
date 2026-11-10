/* ============================================================
   星系底 · 卦象卷轴卡（老师23:51指令：星云垫在卦象文字下方，边缘=卡框）
   卡片内嵌WebGL canvas（z0），竖排诗文浮其上（z1），星系调暗慢转
   降级：无scroll-wrap/WebGL→静默跳过，页面无损
   ============================================================ */
(function () {
    'use strict';
    function boot() {
        var card = document.querySelector('.scroll-wrap');
        if (!card || typeof THREE === 'undefined') return;
        if (card.querySelector('.gx-bg')) return;
        try { init(card); } catch (e) {}
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(boot, 60); });
    else setTimeout(boot, 60);

    function init(card) {
        var cv = document.createElement('canvas');
        cv.className = 'gx-bg';
        cv.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:0;opacity:.62;border-radius:inherit;pointer-events:none;';
        card.insertBefore(cv, card.firstChild);
        var st = document.createElement('style');
        st.textContent = '.scroll-wrap .poem-v,.scroll-wrap .seal{position:relative;z-index:1}.scroll-wrap .seal{position:absolute;}';
        document.head.appendChild(st);

        var renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true });
        var DPR = Math.min(window.devicePixelRatio || 1, 2);
        var W = card.clientWidth, H = card.clientHeight;
        renderer.setPixelRatio(DPR);
        renderer.setSize(W, H);
        renderer.setClearColor(0x04050c, 1);

        var scene = new THREE.Scene();
        var cam = new THREE.PerspectiveCamera(46, W / H, 0.1, 100);
        cam.position.set(0, 3.1, 5.4);
        cam.lookAt(0, 0.85, 0);          /* 亮核压到下区，避开上中部文字 */

        var group = new THREE.Group();
        group.rotation.x = 0.22;
        scene.add(group);

        function dot() {
            var c = document.createElement('canvas'); c.width = c.height = 64;
            var x = c.getContext('2d');
            var g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
            g.addColorStop(0, 'rgba(255,255,255,1)');
            g.addColorStop(0.3, 'rgba(255,255,255,.72)');
            g.addColorStop(1, 'rgba(255,255,255,0)');
            x.fillStyle = g; x.fillRect(0, 0, 64, 64);
            return new THREE.CanvasTexture(c);
        }
        var SP = dot();
        var cIn = new THREE.Color('#ffdf9e');
        var cMid = new THREE.Color('#c39bf5');
        var cOut = new THREE.Color('#6a4fd8');

        function cloud(opt) {
            var N = opt.count, pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
            var R = opt.radius, arms = opt.arms || 2, spin = opt.spin, scatter = opt.scatter;
            var v = new THREE.Vector3(), c = new THREE.Color();
            for (var i = 0; i < N; i++) {
                var r = Math.pow(Math.random(), 0.62) * R;
                var arm = (i % arms) / arms * Math.PI * 2;
                var ang = arm + r * spin + (Math.random() - 0.5) * scatter * (0.35 + r / R * 1.4);
                v.set(Math.cos(ang) * r, 0, Math.sin(ang) * r);
                var thick = 0.10 + Math.exp(-r * 2.2) * 0.30;
                v.y = (Math.random() + Math.random() + Math.random() - 1.5) * 2 * thick;
                v.x += (Math.random() - 0.5) * scatter * 0.35;
                v.z += (Math.random() - 0.5) * scatter * 0.35;
                pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
                var t = r / R;
                if (t < 0.28) c.copy(cIn).lerp(cMid, t / 0.28 * 0.55);
                else c.copy(cMid).lerp(cOut, (t - 0.28) / 0.72);
                var br = 0.5 + Math.random() * 0.7;
                col[i * 3] = c.r * br; col[i * 3 + 1] = c.g * br; col[i * 3 + 2] = c.b * br;
            }
            var g = new THREE.BufferGeometry();
            g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            g.setAttribute('color', new THREE.BufferAttribute(col, 3));
            var m = new THREE.PointsMaterial({
                size: opt.size, map: SP, vertexColors: true, transparent: true,
                blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true
            });
            group.add(new THREE.Points(g, m));
        }
        cloud({ count: 24000, radius: 4.0, arms: 2, spin: 1.5, scatter: 0.8, size: 0.030 });
        cloud({ count: 5500, radius: 3.8, arms: 2, spin: 1.45, scatter: 1.15, size: 0.10 });
        cloud({ count: 6000, radius: 0.75, arms: 1, spin: 0.3, scatter: 0.3, size: 0.026 });

        var last = 0;
        (function loop(ts) {
            requestAnimationFrame(loop);
            var dt = Math.min(0.05, (ts - last) / 1000 || 0.016);
            last = ts;
            group.rotation.y += dt * 0.05;
            renderer.render(scene, cam);
        })(0);

        /* 卡片尺寸跟随 */
        var ro = new ResizeObserver(function () {
            W = card.clientWidth; H = card.clientHeight;
            cam.aspect = W / H; cam.updateProjectionMatrix();
            renderer.setSize(W, H);
        });
        ro.observe(card);
    }
})();
