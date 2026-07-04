/* ============================================================
   LANDING.JS — Church Festival Landing Page
   ============================================================ */

'use strict';

/* ---- Stars Generator ---- */
(function generateStars() {
  const layer = document.getElementById('starsLayer');
  if (!layer) return;

  const count = window.innerWidth < 600 ? 120 : 250;
  const fragment = document.createDocumentFragment();

  for (let i = 0; i < count; i++) {
    const star = document.createElement('div');
    star.className = 'star';

    const size   = Math.random() * 2.8 + 0.5;
    const x      = Math.random() * 100;
    const y      = Math.random() * 75;          // keep stars in upper 75%
    const dur    = (Math.random() * 4 + 2).toFixed(2);
    const delay  = (Math.random() * 6).toFixed(2);
    const op     = (Math.random() * 0.6 + 0.3).toFixed(2);

    star.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${x}%;
      top: ${y}%;
      --dur: ${dur}s;
      --delay: -${delay}s;
      --op: ${op};
      opacity: ${op};
    `;

    // Occasional bright / coloured star
    if (Math.random() < 0.06) {
      const colours = ['#fff9c4', '#c8e6ff', '#ffe0e0', '#e8ffe0'];
      star.style.background = colours[Math.floor(Math.random() * colours.length)];
      star.style.width  = `${size + 1.5}px`;
      star.style.height = `${size + 1.5}px`;
      star.style.boxShadow = `0 0 ${Math.round(size * 3)}px rgba(255,255,200,0.7)`;
    }

    fragment.appendChild(star);
  }

  layer.appendChild(fragment);
})();


/* ---- Day / Night Toggle ---- */
(function setupDayNight() {
  const btn    = document.getElementById('dayNightToggle');
  const icon   = btn ? btn.querySelector('.toggle-icon') : null;
  const body   = document.body;

  if (!btn) return;

  let isDay = false;

  btn.addEventListener('click', () => {
    isDay = !isDay;

    body.classList.toggle('night-mode',  !isDay);
    body.classList.toggle('day-mode',     isDay);

    if (icon) icon.textContent = isDay ? '🌙' : '☀️';
    btn.setAttribute('title', isDay ? 'تبديل لليل' : 'تبديل للنهار');
  });
})();


/* ---- Mouse Parallax ---- */
(function setupParallax() {
  const sky    = document.getElementById('sky');
  const scene  = document.getElementById('scene');
  const moon   = document.getElementById('moon');
  const sun    = document.getElementById('sun');
  const card   = document.getElementById('glassCard');
  const c1     = document.getElementById('cloud1');
  const c2     = document.getElementById('cloud2');
  const c3     = document.getElementById('cloud3');

  if (!sky) return;

  let mouseX = 0, mouseY = 0;
  let curX   = 0, curY   = 0;
  let raf;

  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth  - 0.5) * 2;  // -1 → 1
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;  // -1 → 1
  });

  // Smooth lerp loop
  function tick() {
    curX += (mouseX - curX) * 0.06;
    curY += (mouseY - curY) * 0.06;

    if (sky)   sky.style.transform   = `translate(${curX * 10}px, ${curY * 6}px)`;
    if (scene) scene.style.transform = `translate(${curX * -5}px, ${curY * -3}px)`;
    if (moon)  moon.style.transform  = `translate(${curX * 18}px, ${curY * 10}px)`;
    if (sun)   sun.style.transform   = `translate(${curX * 18}px, ${curY * 10}px)`;
    if (card)  card.style.transform  = `perspective(1200px) rotateY(${curX * 3}deg) rotateX(${-curY * 2}deg)`;
    if (c1)    c1.style.transform    = `translateX(${curX * -25}px)`;
    if (c2)    c2.style.transform    = `translateX(${curX * -15}px)`;
    if (c3)    c3.style.transform    = `translateX(${curX * 20}px)`;

    raf = requestAnimationFrame(tick);
  }

  raf = requestAnimationFrame(tick);

  // Touch support
  document.addEventListener('touchmove', (e) => {
    if (!e.touches.length) return;
    const t = e.touches[0];
    mouseX = (t.clientX / window.innerWidth  - 0.5) * 2;
    mouseY = (t.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  // Pause when tab hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(raf);
    else raf = requestAnimationFrame(tick);
  });
})();


/* ---- Church Window Random Blinking (extra layer) ---- */
(function setupWindowBlink() {
  const windows = document.querySelectorAll('.arch-glass.window-glow, .tw-glass');
  if (!windows.length) return;

  windows.forEach((win) => {
    // Randomize CSS animation delay slightly so they don't sync
    const offset = (Math.random() * 6).toFixed(2);
    win.style.animationDelay = `-${offset}s`;
  });
})();


/* ---- Start Button ---- */
(function setupStartBtn() {
  const btn = document.getElementById('startBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    btn.querySelector('.btn-text').textContent = 'جاري التحميل…';
    btn.style.pointerEvents = 'none';

    // Simulate navigation — replace with your actual route
    setTimeout(() => {
      // window.location.href = '/dashboard';
      btn.querySelector('.btn-text').textContent = 'ابدأ الآن';
      btn.style.pointerEvents = '';
    }, 2000);
  });
})();


/* ---- Reduce Motion Respect ---- */
(function respectReducedMotion() {
  const mq = window.matchMedia('(prefers-reduced-motion: reduce)');

  function apply(reduced) {
    document.documentElement.style.setProperty(
      '--anim-play', reduced ? 'paused' : 'running'
    );
    if (reduced) {
      document.querySelectorAll('.star, .cloud, .moon, .rose-petal')
        .forEach(el => { el.style.animationPlayState = 'paused'; });
    }
  }

  apply(mq.matches);
  mq.addEventListener('change', e => apply(e.matches));
})();