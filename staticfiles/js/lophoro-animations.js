/* ═══════════════════════════════════════════════════════════
   Lophoro IMS — UI Animations & Interactions
   ═══════════════════════════════════════════════════════════ */

/* ── NProgress page loader ───────────────────────────────── */
if (typeof NProgress !== 'undefined') {
  NProgress.configure({ color: '#914D22', showSpinner: false, speed: 300, minimum: 0.08 });
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (a && a.href && !a.href.startsWith('#') && !a.target && !e.ctrlKey && !e.metaKey) {
      NProgress.start();
    }
  });
  window.addEventListener('pageshow', () => NProgress.done());
}

/* ── Scroll progress bar ─────────────────────────────────── */
(function initScrollProgress() {
  const bar = document.createElement('div');
  bar.id = 'scroll-progress-bar';
  bar.style.cssText = `
    position:fixed; top:0; left:0; height:3px; width:0%;
    background:linear-gradient(90deg,#3D1A0A,#914D22,#EDD9C0);
    z-index:9999; transition:width .1s linear;
    border-radius:0 2px 2px 0;
    box-shadow:0 0 8px rgba(145,77,34,0.6);
    pointer-events:none;
  `;
  document.body.appendChild(bar);

  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const total    = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = total > 0 ? (scrolled / total * 100) + '%' : '0%';
  }, { passive: true });
})();

/* ═══════════════════════════════════════════════════════════
   DOM-ready block
   ═══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {

  /* ── AOS ──────────────────────────────────────────────── */
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 520, easing: 'cubic-bezier(0.4,0,0.2,1)', once: true, offset: 40 });
  }

  /* ── Chart.js global defaults ─────────────────────────── */
  if (typeof Chart !== 'undefined') {
    Chart.defaults.font.family = "'Montserrat', sans-serif";
    Chart.defaults.font.size   = 11;
    Chart.defaults.color       = '#9B7B65';
    Chart.defaults.plugins.legend.labels.boxWidth  = 10;
    Chart.defaults.plugins.legend.labels.padding   = 16;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
  }

  /* ── Sidebar collapse ─────────────────────────────────── */
  const sidebar     = document.getElementById('sidebar');
  const toggleBtn   = document.getElementById('sidebarToggle');
  const mainContent = document.querySelector('.main-content');

  if (sidebar && toggleBtn) {
    const KEY = 'lophoro_sidebar_collapsed';
    if (localStorage.getItem(KEY) === 'true') {
      sidebar.classList.add('collapsed');
      mainContent?.classList.add('sidebar-collapsed');
    }
    toggleBtn.addEventListener('click', () => {
      const collapsed = sidebar.classList.toggle('collapsed');
      mainContent?.classList.toggle('sidebar-collapsed', collapsed);
      localStorage.setItem(KEY, collapsed);
    });
  }

  /* Mobile sidebar */
  const mobileBtn  = document.getElementById('mobileMenuToggle');
  const closeBtn   = document.getElementById('mobileMenuClose');
  const overlay    = document.getElementById('sidebarOverlay');

  function openMobileSidebar() {
    sidebar?.classList.add('mobile-open');
    overlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileSidebar() {
    sidebar?.classList.remove('mobile-open');
    overlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  mobileBtn?.addEventListener('click', openMobileSidebar);
  closeBtn?.addEventListener('click', closeMobileSidebar);
  overlay?.addEventListener('click', closeMobileSidebar);

  /* Close sidebar on nav link tap (mobile) */
  if (window.innerWidth <= 768) {
    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', closeMobileSidebar);
    });
  }

  /* ── Active nav detection ─────────────────────────────── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach((link) => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    }
  });

  /* ── Counter animation ────────────────────────────────── */
  const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

  function animateCounter(el) {
    const target   = parseFloat(el.dataset.counter);
    const duration = parseInt(el.dataset.duration || '1400', 10);
    const prefix   = el.dataset.prefix || '';
    const suffix   = el.dataset.suffix || '';
    const decimals = el.dataset.decimals ? parseInt(el.dataset.decimals, 10) : 0;
    const start    = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      el.textContent = prefix + (easeOutExpo(progress) * target).toFixed(decimals) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  new IntersectionObserver((entries, obs) => {
    entries.forEach((e) => {
      if (e.isIntersecting && !e.target.dataset.counted) {
        e.target.dataset.counted = 'true';
        animateCounter(e.target);
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.4 }).observe.bind(
    new IntersectionObserver(() => {})
  );

  // Simpler version that works correctly
  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = 'true';
        animateCounter(entry.target);
        counterObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('[data-counter]').forEach((el) => counterObs.observe(el));

  /* ── 3D Tilt on stat/panel cards ─────────────────────── */
  document.querySelectorAll('.stat-card').forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect    = card.getBoundingClientRect();
      const x       = e.clientX - rect.left;
      const y       = e.clientY - rect.top;
      const rotX    = ((y / rect.height) - 0.5) * -12;
      const rotY    = ((x / rect.width)  - 0.5) *  12;
      card.style.transform = `perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px) scale(1.02)`;
      card.style.transition = 'transform 0.1s ease';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform  = '';
      card.style.transition = 'transform 0.4s cubic-bezier(0.34,1.56,0.64,1)';
    });
  });

  /* ── Subtle tilt on panel cards ──────────────────────── */
  document.querySelectorAll('.panel-card').forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const rotX = ((e.clientY - rect.top)  / rect.height - 0.5) * -4;
      const rotY = ((e.clientX - rect.left) / rect.width  - 0.5) *  4;
      card.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-2px)`;
      card.style.transition = 'transform 0.12s ease';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform  = '';
      card.style.transition = 'transform 0.5s cubic-bezier(0.34,1.56,0.64,1)';
    });
  });

  /* ── Staggered reveal for grid items ─────────────────── */
  function staggerReveal(selector, delayMs = 90) {
    const items = document.querySelectorAll(selector);
    if (!items.length) return;

    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = Array.from(items).indexOf(entry.target);
          setTimeout(() => {
            entry.target.style.opacity    = '1';
            entry.target.style.transform  = 'translateY(0)';
          }, idx * delayMs);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    items.forEach((el) => {
      el.style.opacity    = '0';
      el.style.transform  = 'translateY(18px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s cubic-bezier(0.34,1.56,0.64,1)';
      obs.observe(el);
    });
  }

  staggerReveal('.stat-card',    100);
  staggerReveal('.eoq-card',      80);
  staggerReveal('.quick-action-btn', 70);

  /* ── Hero card floating shimmer ──────────────────────── */
  const hero = document.querySelector('.hero-card');
  if (hero) {
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width  * 100).toFixed(1);
      const y = ((e.clientY - rect.top)  / rect.height * 100).toFixed(1);
      hero.style.setProperty('--mouse-x', x + '%');
      hero.style.setProperty('--mouse-y', y + '%');
    });
  }

  /* ── Toast auto-dismiss ───────────────────────────────── */
  function dismissToast(toast) {
    toast.style.animation = 'toastSlideOut 0.35s ease forwards';
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }

  document.querySelectorAll('.toast').forEach((toast) => {
    setTimeout(() => dismissToast(toast), 4000);
    toast.querySelector('.toast-close')?.addEventListener('click', () => dismissToast(toast));
  });

  /* ── Button ripple ────────────────────────────────────── */
  document.querySelectorAll('.btn-primary, .btn-secondary').forEach((btn) => {
    btn.addEventListener('click', function (e) {
      const ripple = document.createElement('span');
      ripple.className = 'btn-ripple';
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      Object.assign(ripple.style, {
        width:  size + 'px',
        height: size + 'px',
        left:   (e.clientX - rect.left - size / 2) + 'px',
        top:    (e.clientY - rect.top  - size / 2) + 'px',
      });
      this.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    });
  });

  /* ── Magnetic button pull ─────────────────────────────── */
  document.querySelectorAll('.btn-primary').forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const dx = (e.clientX - rect.left - rect.width  / 2) * 0.25;
      const dy = (e.clientY - rect.top  - rect.height / 2) * 0.25;
      btn.style.transform = `translate(${dx}px, ${dy}px) translateY(-2px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });

  /* ── Dropdown menus ───────────────────────────────────── */
  document.querySelectorAll('[data-dropdown]').forEach((trigger) => {
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const menu = document.getElementById(trigger.dataset.dropdown);
      menu?.classList.toggle('open');
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-menu.open').forEach((m) => m.classList.remove('open'));
  });

  /* ── Data table row stagger ───────────────────────────── */
  document.querySelectorAll('.data-table tbody tr, .table-card tbody tr').forEach((tr, i) => {
    tr.style.animationDelay = `${i * 35}ms`;
  });

  /* ── Typewriter effect on hero subtitle ──────────────── */
  const heroSub = document.querySelector('.hero-sub');
  if (heroSub) {
    const text = heroSub.textContent.trim();
    heroSub.textContent = '';
    heroSub.style.opacity = '1';
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        heroSub.textContent += text[i++];
      } else {
        clearInterval(interval);
      }
    }, 18);
  }

});

/* ── Injected keyframes ───────────────────────────────────── */
(function injectStyles() {
  if (document.getElementById('lophoro-keyframes')) return;
  const s = document.createElement('style');
  s.id = 'lophoro-keyframes';
  s.textContent = `
    @keyframes toastSlideOut { to { opacity:0; transform:translateX(110%); } }

    .btn-ripple {
      position:absolute; border-radius:50%; pointer-events:none;
      background:rgba(255,255,255,0.28);
      transform:scale(0); animation:rippleAnim 0.55s ease-out forwards;
    }
    @keyframes rippleAnim { to { transform:scale(2.8); opacity:0; } }

    .hero-card {
      --mouse-x: 50%; --mouse-y: 50%;
    }
    .hero-card::after {
      background: radial-gradient(
        circle at var(--mouse-x) var(--mouse-y),
        rgba(237,217,192,0.08) 0%,
        transparent 60%
      );
    }
  `;
  document.head.appendChild(s);
})();

/* ── Shared Chart.js helpers (used by templates) ─────────── */
window.LophoroChart = {

  /* Brand colours */
  colors: {
    primary:  '#3D1A0A',
    accent:   '#914D22',
    cream:    '#EDD9C0',
    muted:    '#9B7B65',
    grid:     'rgba(226,205,184,0.45)',
    success:  '#2E7D52',
    warning:  '#B45309',
    danger:   '#991B1B',
  },

  /* Gradient fill for bar charts */
  barGradient(ctx, chartArea, alpha1 = 1, alpha2 = 0.65) {
    if (!chartArea) return 'rgba(145,77,34,0.8)';
    const g = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    g.addColorStop(0, `rgba(61,26,10,${alpha2})`);
    g.addColorStop(1, `rgba(145,77,34,${alpha1})`);
    return g;
  },

  /* Gradient fill for line area charts */
  areaGradient(ctx, chartArea) {
    if (!chartArea) return 'rgba(145,77,34,0.1)';
    const g = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
    g.addColorStop(0,   'rgba(145,77,34,0.32)');
    g.addColorStop(0.6, 'rgba(145,77,34,0.08)');
    g.addColorStop(1,   'rgba(145,77,34,0)');
    return g;
  },

  /* Shared scale options */
  scales(opts = {}) {
    return {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#9B7B65',
          font: { size: 11, weight: '600', family: "'Montserrat', sans-serif" },
          padding: 8,
          ...(opts.yTicks || {}),
        },
        grid: { color: 'rgba(226,205,184,0.45)', drawBorder: false },
        border: { display: false },
        ...(opts.y || {}),
      },
      x: {
        ticks: {
          color: '#9B7B65',
          font: { size: 11, weight: '600', family: "'Montserrat', sans-serif" },
          maxRotation: 30,
          ...(opts.xTicks || {}),
        },
        grid: { display: false },
        border: { display: false },
        ...(opts.x || {}),
      },
    };
  },

  /* Shared tooltip */
  tooltip(labelCallback) {
    return {
      backgroundColor: '#2A0F05',
      titleColor: '#EDD9C0',
      bodyColor: '#C4A882',
      padding: { x: 14, y: 10 },
      cornerRadius: 10,
      borderColor: 'rgba(237,217,192,0.12)',
      borderWidth: 1,
      titleFont: { family: "'Montserrat', sans-serif", size: 12, weight: '700' },
      bodyFont:  { family: "'Montserrat', sans-serif", size: 12, weight: '500' },
      displayColors: false,
      callbacks: labelCallback ? { label: labelCallback } : {},
    };
  },

  /* Shared animation */
  animation: {
    duration: 900,
    easing: 'easeOutQuart',
  },
};
