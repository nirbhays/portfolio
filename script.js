/* ========================================================
   NIRBHAY SINGH — PORTFOLIO JS
   Particle network, typing, scroll reveals, counters, nav
   ======================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------
     LOADER
  ------------------------------------------------ */
  window.addEventListener('load', function () {
    setTimeout(function () {
      document.getElementById('loader').classList.add('hidden');
    }, 1400);
  });

  /* ------------------------------------------------
     PARTICLE NETWORK BACKGROUND
     Lightweight canvas drawing connected nodes
  ------------------------------------------------ */
  var canvas = document.getElementById('bg-canvas');
  var ctx = canvas.getContext('2d');
  var particles = [];
  var PARTICLE_COUNT = 60;
  var CONNECTION_DIST = 150;
  var paused = false;

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  function Particle() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.radius = Math.random() * 1.5 + 0.5;
  }

  for (var i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  function drawParticles() {
    if (paused) { requestAnimationFrame(drawParticles); return; }
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(6, 214, 160, 0.5)';
      ctx.fill();

      for (var j = i + 1; j < particles.length; j++) {
        var p2 = particles[j];
        var dx = p.x - p2.x;
        var dy = p.y - p2.y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DIST) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          var opacity = 1 - dist / CONNECTION_DIST;
          ctx.strokeStyle = 'rgba(79, 143, 255, ' + (opacity * 0.15) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(drawParticles);
  }
  drawParticles();

  // Pause when tab is hidden
  document.addEventListener('visibilitychange', function () {
    paused = document.hidden;
  });

  /* ------------------------------------------------
     PROJECT CARD GLOW (mouse follow)
  ------------------------------------------------ */
  document.querySelectorAll('.project-card').forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      var rect = card.getBoundingClientRect();
      card.style.setProperty('--mouse-x', (e.clientX - rect.left) + 'px');
      card.style.setProperty('--mouse-y', (e.clientY - rect.top) + 'px');
    });
  });

  /* ------------------------------------------------
     SCROLL PROGRESS BAR
  ------------------------------------------------ */
  var progressBar = document.querySelector('.scroll-progress');

  function updateProgress() {
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = pct + '%';
  }

  /* ------------------------------------------------
     NAV SCROLL EFFECT + ACTIVE LINK
  ------------------------------------------------ */
  var nav = document.getElementById('nav');
  var navLinks = document.querySelectorAll('.nav-link');
  var sections = document.querySelectorAll('main .section, .hero');

  function updateNav() {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }

    // Active link
    var current = '';
    sections.forEach(function (section) {
      var top = section.offsetTop - 150;
      if (window.scrollY >= top) {
        current = section.getAttribute('id') || '';
      }
    });
    navLinks.forEach(function (link) {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) {
        link.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', function () {
    updateProgress();
    updateNav();
  }, { passive: true });

  /* ------------------------------------------------
     MOBILE NAV TOGGLE
  ------------------------------------------------ */
  var navToggle = document.getElementById('nav-toggle');
  var navLinksEl = document.getElementById('nav-links');
  var navEnd = document.querySelector('.nav-end');

  navToggle.addEventListener('click', function () {
    var isOpen = navToggle.classList.toggle('open');
    navLinksEl.classList.toggle('mobile-open', isOpen);
    if (navEnd) navEnd.classList.toggle('mobile-open', isOpen);
    navToggle.setAttribute('aria-expanded', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on link click
  navLinksEl.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      navToggle.classList.remove('open');
      navLinksEl.classList.remove('mobile-open');
      if (navEnd) navEnd.classList.remove('mobile-open');
      navToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });

  /* ------------------------------------------------
     SCROLL REVEAL (IntersectionObserver)
  ------------------------------------------------ */
  var reveals = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.getAttribute('data-delay');
          var ms = delay ? parseInt(delay, 10) * 100 : 0;
          setTimeout(function () {
            entry.target.classList.add('visible');
          }, ms);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    // Fallback: show everything
    reveals.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ------------------------------------------------
     STAT COUNTER ANIMATION
  ------------------------------------------------ */
  var stats = document.querySelectorAll('.stat');
  var statAnimated = false;

  function animateCounters() {
    if (statAnimated) return;
    statAnimated = true;

    stats.forEach(function (stat) {
      var target = parseInt(stat.getAttribute('data-target'), 10);
      var numEl = stat.querySelector('.stat-number');
      if (!numEl || isNaN(target)) return;

      numEl.textContent = '0';
      var current = 0;
      var duration = 1500;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        current = Math.round(eased * target);
        numEl.textContent = current;
        if (progress < 1) {
          requestAnimationFrame(step);
        }
      }
      requestAnimationFrame(step);
    });
  }

  if ('IntersectionObserver' in window) {
    var statsContainer = document.querySelector('.hero-stats');
    if (statsContainer) {
      var statsObserver = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
          animateCounters();
          statsObserver.disconnect();
        }
      }, { threshold: 0.5 });
      statsObserver.observe(statsContainer);
    }
  } else {
    animateCounters();
  }

  /* ------------------------------------------------
     HERO TYPING ANIMATION
  ------------------------------------------------ */
  var roles = [
    'Cloud & AI Architect',
    'DevOps & MLOps Engineer',
    'Open Source Builder',
    'FinOps Strategist',
    'Platform Engineer'
  ];
  var typedEl = document.getElementById('typed-text');
  var roleIndex = 0;
  var charIndex = 0;
  var isDeleting = false;
  var typeSpeed = 80;

  function typeRole() {
    var current = roles[roleIndex];
    if (isDeleting) {
      typedEl.textContent = current.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 40;
    } else {
      typedEl.textContent = current.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 80;
    }

    if (!isDeleting && charIndex === current.length) {
      typeSpeed = 2000; // pause at end
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      typeSpeed = 400; // pause before typing next
    }

    setTimeout(typeRole, typeSpeed);
  }
  typeRole();

  /* ------------------------------------------------
     TERMINAL TYPING
  ------------------------------------------------ */
  var terminalBody = document.getElementById('terminal-body');
  var terminalLines = [
    { prompt: '$ whoami', response: 'nirbhay — cloud & ai architect' },
    { prompt: '$ cat skills.yaml', response: 'clouds: [aws, gcp, azure]\nfocus: [mlops, llmops, devsecops]\npassion: building resilient systems' },
    { prompt: '$ uptime', response: '11 years, 0 downtime' },
    { prompt: '$ echo $STATUS', response: 'open to collaboration' }
  ];
  var tLineIndex = 0;
  var tCharIndex = 0;
  var tPhase = 'prompt'; // 'prompt' | 'pause' | 'response' | 'wait'
  var tCurrentText = '';

  function typeTerminal() {
    if (tLineIndex >= terminalLines.length) return;

    var line = terminalLines[tLineIndex];

    if (tPhase === 'prompt') {
      tCurrentText += line.prompt[tCharIndex] || '';
      terminalBody.textContent = buildTerminalText() + tCurrentText + '_';
      tCharIndex++;
      if (tCharIndex > line.prompt.length) {
        tPhase = 'pause';
        tCharIndex = 0;
        setTimeout(typeTerminal, 400);
        return;
      }
      setTimeout(typeTerminal, 50);
    } else if (tPhase === 'pause') {
      tCurrentText += '\n';
      tPhase = 'response';
      setTimeout(typeTerminal, 100);
    } else if (tPhase === 'response') {
      tCurrentText += line.response[tCharIndex] || '';
      terminalBody.textContent = buildTerminalText() + tCurrentText + '_';
      tCharIndex++;
      if (tCharIndex > line.response.length) {
        tCurrentText += '\n';
        completedTerminalText += tCurrentText;
        tCurrentText = '';
        tCharIndex = 0;
        tLineIndex++;
        tPhase = 'prompt';
        setTimeout(typeTerminal, 600);
        return;
      }
      setTimeout(typeTerminal, 20);
    }
  }

  var completedTerminalText = '';
  function buildTerminalText() {
    return completedTerminalText;
  }

  // Start terminal after loader
  setTimeout(typeTerminal, 1800);

  /* ------------------------------------------------
     SMOOTH SCROLL for anchor links
  ------------------------------------------------ */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var offset = 80;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

})();
