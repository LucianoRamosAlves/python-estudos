(function () {
   const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
   if (prefersReduced) return;

   const canvas = document.createElement('canvas');
   canvas.className = 'ambient-canvas';
   canvas.setAttribute('aria-hidden', 'true');
   document.body.prepend(canvas);

   const ctx = canvas.getContext('2d', { alpha: true });
   if (!ctx) return;

   const state = {
      width: 0,
      height: 0,
      dpr: 1,
      particles: [],
      rafId: null,
      lastTime: 0
   };

   function createParticle() {
      const palette = [
         '122,98,196',
         '106,61,109',
         '177,114,138',
         '200,168,95'
      ];

      return {
         x: Math.random() * state.width,
         y: Math.random() * state.height,
         vx: (Math.random() - 0.5) * 0.05,
         vy: (Math.random() - 0.5) * 0.05,
         radius: 0.8 + Math.random() * 1.3,
         alpha: 0.02 + Math.random() * 0.09,
         color: palette[Math.floor(Math.random() * palette.length)]
      };
   }

   function resize() {
      state.dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      state.width = window.innerWidth;
      state.height = window.innerHeight;

      canvas.width = Math.floor(state.width * state.dpr);
      canvas.height = Math.floor(state.height * state.dpr);
      canvas.style.width = state.width + 'px';
      canvas.style.height = state.height + 'px';
      ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);

      const count = Math.max(12, Math.min(34, Math.floor((state.width * state.height) / 52000)));
      state.particles = new Array(count).fill(null).map(createParticle);
   }

   function drawParticle(p) {
      ctx.beginPath();
      ctx.fillStyle = 'rgba(' + p.color + ',' + p.alpha + ')';
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();
   }

   function animate(time) {
      if (time - state.lastTime < 41) {
         state.rafId = requestAnimationFrame(animate);
         return;
      }
      state.lastTime = time;

      ctx.clearRect(0, 0, state.width, state.height);

      for (let i = 0; i < state.particles.length; i += 1) {
         const p = state.particles[i];
         p.x += p.vx;
         p.y += p.vy;

         if (p.x < -12) p.x = state.width + 12;
         if (p.x > state.width + 12) p.x = -12;
         if (p.y < -12) p.y = state.height + 12;
         if (p.y > state.height + 12) p.y = -12;

         drawParticle(p);
      }

      state.rafId = requestAnimationFrame(animate);
   }

   function start() {
      if (!state.rafId) {
         state.rafId = requestAnimationFrame(animate);
      }
   }

   function stop() {
      if (state.rafId) {
         cancelAnimationFrame(state.rafId);
         state.rafId = null;
      }
   }

   document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
         stop();
      } else {
         start();
      }
   });

   window.addEventListener('resize', resize);

   resize();
   start();
})();
