/* 粒子旋涡星系 · Demo（老师23:41参考图复刻）
   双臂旋涡+银心亮核+紫罗兰色阶+加法混合辉光+慢旋转 */
(function () {
    var W = window.innerWidth, H = window.innerHeight;
    var cv = document.getElementById('gc');
    var renderer;
    try { renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: false }); }
    catch (e) { document.body.innerHTML = 'no webgl'; return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(W, H);
    renderer.setClearColor(0x030304, 1);

    var scene = new THREE.Scene();
    var cam = new THREE.PerspectiveCamera(46, W / H, 0.1, 100);
    cam.position.set(0, 2.7, 7.4);
    cam.lookAt(0, 0, 0);

    var group = new THREE.Group();
    group.rotation.x = 0.18;
    scene.add(group);

    /* 色阶：银心暖白 → 薰衣草紫 → 深紫 */
    /* 圆形柔光点精灵（消除方块感） */
    function dot() {
        var c = document.createElement('canvas'); c.width = c.height = 64;
        var x = c.getContext('2d');
        var g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
        g.addColorStop(0, 'rgba(255,255,255,1)');
        g.addColorStop(0.3, 'rgba(255,255,255,.75)');
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
            var r = Math.pow(Math.random(), 0.62) * R;                 /* 内密外疏 */
            var arm = (i % arms) / arms * Math.PI * 2;
            var ang = arm + r * spin + (Math.random() - 0.5) * scatter * (0.35 + r / R * 1.4);
            v.set(Math.cos(ang) * r, 0, Math.sin(ang) * r);
            /* 盘厚（银心略鼓）+ 弥散 */
            var thick = 0.10 + Math.exp(-r * 2.2) * 0.30;
            v.y = (Math.random() + Math.random() + Math.random() - 1.5) * 2 * thick;
            v.x += (Math.random() - 0.5) * scatter * 0.35;
            v.z += (Math.random() - 0.5) * scatter * 0.35;
            pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
            /* 颜色：半径插值+随机明暗 */
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
        var pts = new THREE.Points(g, m);
        group.add(pts);
        return pts;
    }

    /* 三层：主星盘(细点) / 辉光晕(大点稀疏) / 银心核(极密小点) */
    cloud({ count: 28000, radius: 3.9, arms: 2, spin: 1.5, scatter: 0.78, size: 0.030 });
    cloud({ count: 6500, radius: 3.7, arms: 2, spin: 1.45, scatter: 1.1, size: 0.10 });
    cloud({ count: 6000, radius: 0.7, arms: 1, spin: 0.3, scatter: 0.3, size: 0.026 });

    /* 远景星尘 */
    (function dust() {
        var N = 900, pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
        for (var i = 0; i < N; i++) {
            var r = 8 + Math.random() * 20, th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
            pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
            pos[i * 3 + 1] = r * Math.cos(ph) * 0.6;
            pos[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
            var b = 0.25 + Math.random() * 0.5;
            col[i * 3] = b * 0.9; col[i * 3 + 1] = b * 0.85; col[i * 3 + 2] = b;
        }
        var g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        g.setAttribute('color', new THREE.BufferAttribute(col, 3));
        var m = new THREE.PointsMaterial({ size: 0.06, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
        scene.add(new THREE.Points(g, m));
    })();

    var last = 0;
    (function loop(ts) {
        requestAnimationFrame(loop);
        var dt = Math.min(0.05, (ts - last) / 1000 || 0.016);
        last = ts;
        group.rotation.y += dt * 0.055;
        renderer.render(scene, cam);
    })(0);

    window.addEventListener('resize', function () {
        W = window.innerWidth; H = window.innerHeight;
        cam.aspect = W / H; cam.updateProjectionMatrix();
        renderer.setSize(W, H);
    });
})();
