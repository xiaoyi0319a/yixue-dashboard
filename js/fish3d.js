/* ============================================================
   3D金鱼 · 卦象文字底下游（老师23:06指令）
   程序化文种金鱼：渐变球身+顶点波动飘带尾鳍+眼/须，正交像素坐标
   巡航：卦象卷轴卡下1/3水域内航点巡游（修复打转=航点制+边缘回中）
   降级：WebGL不可用→移除canvas，页面无损
   ============================================================ */
(function () {
    'use strict';
    function ready(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
    ready(init);

    function init() {
        if (typeof THREE === 'undefined') return;
        var W = window.innerWidth, H = window.innerHeight;

        var cv = document.createElement('canvas');
        cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:60;pointer-events:none;';
        var renderer;
        try {
            renderer = new THREE.WebGLRenderer({ canvas: cv, alpha: true, antialias: true });
        } catch (e) { return; }
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.setSize(W, H);
        document.body.appendChild(cv);

        var scene = new THREE.Scene();
        var cam = new THREE.OrthographicCamera(-W / 2, W / 2, H / 2, -H / 2, -200, 300);
        cam.position.z = 100;

        scene.add(new THREE.AmbientLight(0xffffff, 0.55));
        var key = new THREE.DirectionalLight(0xfff3dd, 1.05); key.position.set(60, 90, 120); scene.add(key);
        var rim = new THREE.DirectionalLight(0xa371f7, 0.5); rim.position.set(-80, -40, 60); scene.add(rim);

        /* 纯色材质路线：纹理在部分GPU/driver上alpha不可靠，纯色+半透明最稳 */
        var bodyMat = new THREE.MeshStandardMaterial({ color: 0xff9c3f, roughness: 0.38, metalness: 0.1, emissive: 0x35130a, emissiveIntensity: 0.5 });
        var finMat = new THREE.MeshBasicMaterial({ color: 0xffb054, transparent: true, opacity: 0.32, side: THREE.DoubleSide, depthWrite: false });
        var finMatLight = new THREE.MeshBasicMaterial({ color: 0xffc372, transparent: true, opacity: 0.25, side: THREE.DoubleSide, depthWrite: false });

        /* ---- 金鱼模型（面向+x，体长约118px） ---- */
        var fish = new THREE.Group();

        var bodyGeo = new THREE.SphereGeometry(34, 28, 20);
        (function taper() {          /* 头钝圆、尾柄收窄 */
            var p = bodyGeo.attributes.position;
            for (var i = 0; i < p.count; i++) {
                var x = p.getX(i);
                var k = 1;
                if (x > 8) k = 1 - (x - 8) / 26 * 0.28;        /* 头部略收 */
                if (x < -12) k = 1 - (-12 - x) / 22 * 0.55;     /* 尾柄收窄 */
                p.setY(i, p.getY(i) * k);
                p.setZ(i, p.getZ(i) * k);
            }
            bodyGeo.computeVertexNormals();
        })();
        var body = new THREE.Mesh(bodyGeo, bodyMat);
        body.scale.set(1.42, 1, 0.82);
        fish.add(body);

        /* 背鳍/腹鳍/胸鳍：波动飘带平面 */
        function fin(w, h, segX, segY, op) {
            var g = new THREE.PlaneGeometry(w, h, segX, segY);
            g.translate(-w / 2, 0, 0);      /* 锚在右侧 */
            var m = new THREE.Mesh(g, (op > 0.8) ? finMat : finMatLight);
            m.userData.base = g.attributes.position.array.slice();
            return m;
        }
        var tail = fin(86, 74, 14, 10, 0.92); tail.position.set(-44, 0, 0); tail.rotation.set(0, 0.18, -0.12); fish.add(tail);
        var dorsal = fin(40, 22, 8, 4, 0.8); dorsal.position.set(2, 26, 0); dorsal.rotation.z = 0.5; dorsal.rotation.y = 0.1; fish.add(dorsal);
        var anal = fin(30, 16, 6, 4, 0.75); anal.position.set(-16, -26, 0); anal.rotation.z = -2.6; fish.add(anal);
        var pecL = fin(26, 13, 6, 3, 0.8); pecL.position.set(16, -8, 14); pecL.rotation.set(0.5, 0.5, -0.7); fish.add(pecL);
        var pecR = fin(26, 13, 6, 3, 0.8); pecR.position.set(16, -8, -14); pecR.rotation.set(-0.5, -0.5, -0.7); fish.add(pecR);

        /* 眼 */
        var eyeMat = new THREE.MeshStandardMaterial({ color: 0x1a0d02, roughness: 0.25 });
        var eyeG = new THREE.SphereGeometry(3.6, 12, 10);
        var eL = new THREE.Mesh(eyeG, eyeMat); eL.position.set(28, 6, 15); fish.add(eL);
        var eR = new THREE.Mesh(eyeG, eyeMat); eR.position.set(28, 6, -15); fish.add(eR);
        var glint = new THREE.MeshBasicMaterial({ color: 0xfff6e0 });
        var gL = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 6), glint); gL.position.set(29.5, 7.3, 17); fish.add(gL);
        var gR = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 6), glint); gR.position.set(29.5, 7.3, -13); fish.add(gR);
        /* 腮红 */
        var cheekMat = new THREE.MeshBasicMaterial({ color: 0xff7a45, transparent: true, opacity: 0.28 });
        var cL = new THREE.Mesh(new THREE.SphereGeometry(6, 10, 8), cheekMat); cL.position.set(36, -2, 13); cL.scale.set(0.8, 0.6, 0.4); fish.add(cL);
        var cR = new THREE.Mesh(new THREE.SphereGeometry(6, 10, 8), cheekMat); cR.position.set(36, -2, -13); cR.scale.set(0.8, 0.6, 0.4); fish.add(cR);
        /* 须（两根细线，摆动） */
        var whMat = new THREE.LineBasicMaterial({ color: 0xffd68c, transparent: true, opacity: 0.85 });
        function whisker(z) {
            var g = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(46, -4, z), new THREE.Vector3(60, -8, z * 1.25), new THREE.Vector3(70, -12, z * 1.4)
            ]);
            var l = new THREE.Line(g, whMat);
            l.userData.z = z;
            fish.add(l);
            return l;
        }
        var wh1 = whisker(6), wh2 = whisker(-6);

        fish.scale.setScalar(0.92);
        scene.add(fish);

        /* ---- 巡游：卦象卷轴卡下1/3水域 ---- */
        var st = { x: W * 0.5, y: H * 0.4, tx: W * 0.6, ty: H * 0.4, face: 1, phase: Math.random() * 6.28, visible: true, lastTurn: 0 };

        function region() {
            var el = document.querySelector('.scroll-wrap') || document.querySelector('.qimen-hexagram');
            var r = el ? el.getBoundingClientRect() : null;
            if (!r || r.width < 40) {
                return { x0: W * 0.15, x1: W * 0.85, y0: H * 0.18, y1: H * 0.72, ok: true };
            }
            /* 卡片离开视口→隐藏。巡游水域=卷轴卡左下半区（竖排文字右侧起排，左下空白，正是"卦象文字底下"） */
            if (r.bottom < -120 || r.top > H + 120) return { ok: false };
            return {
                x0: r.left + 26, x1: r.left + r.width * 0.44,
                y0: r.top + r.height * 0.32, y1: r.top + r.height * 0.9,
                ok: true
            };
        }
        function pickTarget(R) {
            st.tx = R.x0 + Math.random() * (R.x1 - R.x0);
            st.ty = R.y0 + Math.random() * (R.y1 - R.y0);
        }
        pickTarget(region());

        /* 尾巴/鳍波动 */
        function wave(mesh, amp, freq, phase, axis) {
            var pos = mesh.geometry.attributes.position;
            var base = mesh.userData.base;
            var n = pos.count;
            for (var i = 0; i < n; i++) {
                var bx = base[i * 3], by = base[i * 3 + 1];
                var p = -bx / 86;                       /* 0锚点→1尾端 */
                var s = Math.sin(st.phase * freq + phase + p * 4.2) * amp * p;
                if (axis === 'z') pos.setZ(i, s);
                else pos.setY(i, by + s * 0.6);
            }
            pos.needsUpdate = true;
        }

        var last = 0;
        function loop(ts) {
            requestAnimationFrame(loop);
            var dt = Math.min(0.05, (ts - last) / 1000 || 0.016);
            last = ts;
            st.phase += dt * 5.4;
            var R = region();
            if (!R.ok) { fish.visible = false; return; }
            fish.visible = true;
            if (st.x < R.x0 - 60 || st.x > R.x1 + 60 || st.y < R.y0 - 60 || st.y > R.y1 + 60) pickTarget(R);
            var dx = st.tx - st.x, dy = st.ty - st.y;
            var dist = Math.hypot(dx, dy);
            if (dist < 26) pickTarget(R);
            var sp = 46 + Math.sin(st.phase * 0.23) * 12;
            var wantAng = Math.atan2(dy, dx);
            var cur = Math.atan2(Math.sin(st.ang || 0), Math.cos(st.ang || 0));
            var turn = wantAng - cur;
            turn = Math.atan2(Math.sin(turn), Math.cos(turn));
            st.ang = cur + turn * Math.min(1, dt * 2.2);
            st.x += Math.cos(st.ang) * sp * dt;
            st.y += Math.sin(st.ang) * sp * dt;
            /* 面向：右转不翻，左转翻肚180° */
            var fr = Math.cos(st.ang) >= 0;
            st.face += ((fr ? 0 : Math.PI) - st.face) * Math.min(1, dt * 3.2);

            fish.position.set(st.x - W / 2, H / 2 - st.y, Math.sin(st.phase * 0.31) * 6);
            fish.rotation.set(0, st.face, Math.sin(st.ang) * 0.12);
            /* 游动摆尾：左转时z摆镜像 */
            var mirror = Math.abs(st.face) > Math.PI / 2 ? -1 : 1;
            /* 正交前视：z向波动不可见，尾鳍用Y向扇形摆（正弦相位沿尾展开） */
            wave(tail, 15 * mirror, 1.0, 0, 'y');
            wave(dorsal, 4 * mirror, 1.0, 1.2, 'y');
            wave(anal, 4 * mirror, 1.0, 2.1, 'y');
            pecL.rotation.y = 0.5 + Math.sin(st.phase * 1.6) * 0.35;
            pecR.rotation.y = -0.5 - Math.sin(st.phase * 1.6) * 0.35;
            var wob = Math.sin(st.phase * 0.8) * 2.2;
            wh1.rotation.z = wob * 0.01; wh2.rotation.z = wob * 0.01;
            body.rotation.z = Math.sin(st.phase * 1.0) * 0.05 * mirror;
            body.rotation.y = Math.sin(st.phase * 0.5) * 0.04;

            renderer.render(scene, cam);
        }
        requestAnimationFrame(loop);

        window.addEventListener('resize', function () {
            W = window.innerWidth; H = window.innerHeight;
            renderer.setSize(W, H);
            cam.left = -W / 2; cam.right = W / 2; cam.top = H / 2; cam.bottom = -H / 2;
            cam.updateProjectionMatrix();
        });
    }
})();
