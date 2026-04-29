(function () {
  'use strict';

  /* ------------------------------------------------
     LOADER
  ------------------------------------------------ */
  window.addEventListener('load', function () {
    requestAnimationFrame(function () {
      document.getElementById('loader').classList.add('hidden');
    });
  });

  /* ------------------------------------------------
     ENHANCED PARTICLE NETWORK
     More particles, colored connections, mouse interaction
  ------------------------------------------------ */
  var canvas = document.getElementById('bg-canvas');
  var ctx = canvas.getContext('2d');
  var particles = [];
  var supportsHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var PARTICLE_COUNT = 52;
  var CONNECTION_DIST = 132;
  var MOUSE_DIST = 170;
  var paused = false;
  var canvasVisible = true;
  var mouseX = -1000;
  var mouseY = -1000;

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resizeCanvas, 150);
  });
  resizeCanvas();

  function Particle() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = (Math.random() - 0.5) * 0.5;
    this.vy = (Math.random() - 0.5) * 0.5;
    this.radius = Math.random() * 2 + 0.5;
    this.baseRadius = this.radius;
    this.color = Math.random() > 0.5 ? '34, 211, 238' : '244, 114, 182';
  }

  for (var i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  if (supportsHover) {
    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });
  }

  function drawParticles() {
    if (paused) { requestAnimationFrame(drawParticles); return; }
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      var dxM = mouseX - p.x;
      var dyM = mouseY - p.y;
      var distM = Math.sqrt(dxM * dxM + dyM * dyM);
      if (distM > 0 && distM < MOUSE_DIST) {
        var force = (MOUSE_DIST - distM) / MOUSE_DIST;
        p.vx -= (dxM / distM) * force * 0.02;
        p.vy -= (dyM / distM) * force * 0.02;
        p.radius = p.baseRadius + force * 2;
      } else {
        p.radius += (p.baseRadius - p.radius) * 0.05;
      }

      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.99;
      p.vy *= 0.99;

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + p.color + ', 0.6)';
      ctx.fill();

      if (p.radius > p.baseRadius * 1.2) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * 2, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + p.color + ', 0.08)';
        ctx.fill();
      }

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
          var gradient = ctx.createLinearGradient(p.x, p.y, p2.x, p2.y);
          gradient.addColorStop(0, 'rgba(' + p.color + ', ' + (opacity * 0.25) + ')');
          gradient.addColorStop(1, 'rgba(' + p2.color + ', ' + (opacity * 0.25) + ')');
          ctx.strokeStyle = gradient;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(drawParticles);
  }
  drawParticles();

  document.addEventListener('visibilitychange', function () {
    paused = document.hidden || !canvasVisible;
  });

  if ('IntersectionObserver' in window) {
    var heroEl = document.getElementById('hero');
    if (heroEl) {
      var canvasObserver = new IntersectionObserver(function (entries) {
        canvasVisible = entries[0].isIntersecting;
        paused = document.hidden || !canvasVisible;
      }, { threshold: 0 });
      canvasObserver.observe(heroEl);
    }
  }

  /* ------------------------------------------------
     PROJECT CARD GLOW + 3D TILT
  ------------------------------------------------ */
  if (supportsHover) {
    document.querySelectorAll('.project-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', x + 'px');
        card.style.setProperty('--mouse-y', y + 'px');

        var centerX = rect.width / 2;
        var centerY = rect.height / 2;
        var rotateX = ((y - centerY) / centerY) * -2.5;
        var rotateY = ((x - centerX) / centerX) * 2.5;
        card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  /* ------------------------------------------------
     MAGNETIC BUTTON HOVER
  ------------------------------------------------ */
  if (supportsHover) {
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var rect = btn.getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = 'translate(' + (x * 0.08) + 'px, ' + (y * 0.08) + 'px) scale(1.01)';
      });
      btn.addEventListener('mouseleave', function () {
        btn.style.transform = '';
      });
    });
  }

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
     SCROLL REVEAL with staggered delays
  ------------------------------------------------ */
  var reveals = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.getAttribute('data-delay');
          var ms = delay ? parseInt(delay, 10) * 120 : 0;
          setTimeout(function () {
            entry.target.classList.add('visible');
          }, ms);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -60px 0px' });

    reveals.forEach(function (el) { revealObserver.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ------------------------------------------------
     STAT COUNTER ANIMATION with glow effect
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
      var duration = 2000;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 4);
        var current = Math.round(eased * target);
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
     HERO TYPING ANIMATION with glow
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
  var typingPaused = false;

  function typeRole() {
    if (typingPaused) {
      setTimeout(typeRole, 500);
      return;
    }
    var current = roles[roleIndex];
    if (isDeleting) {
      typedEl.textContent = current.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 35;
    } else {
      typedEl.textContent = current.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 70;
    }

    if (!isDeleting && charIndex === current.length) {
      typeSpeed = 2500;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      typeSpeed = 500;
    }

    setTimeout(typeRole, typeSpeed);
  }

  document.addEventListener('visibilitychange', function () {
    typingPaused = document.hidden;
  });

  typeRole();

  /* ------------------------------------------------
     TERMINAL TYPING with colored output
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
  var tPhase = 'prompt';
  var tCurrentText = '';
  var completedTerminalText = '';

  function buildTerminalText() {
    return completedTerminalText;
  }

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
      setTimeout(typeTerminal, 45);
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
        setTimeout(typeTerminal, 700);
        return;
      }
      setTimeout(typeTerminal, 18);
    }
  }

  setTimeout(typeTerminal, 1400);

  /* ------------------------------------------------
     PARALLAX EFFECT on background orbs
  ------------------------------------------------ */
  var orbs = document.querySelectorAll('.bg-orb');
  var ticking = false;

  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        var scroll = window.scrollY;
        orbs.forEach(function (orb, i) {
          var speed = (i + 1) * 0.05;
          orb.style.transform = 'translateY(' + (scroll * speed) + 'px)';
        });
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

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

  /* ------------------------------------------------
     RIPPLE EFFECT on buttons
  ------------------------------------------------ */
  document.querySelectorAll('.btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var rect = btn.getBoundingClientRect();
      var ripple = document.createElement('span');
      ripple.style.cssText = 'position:absolute;border-radius:50%;background:rgba(255,255,255,.25);transform:scale(0);animation:ripple .6s ease-out;pointer-events:none;';
      var size = Math.max(rect.width, rect.height) * 2;
      ripple.style.width = size + 'px';
      ripple.style.height = size + 'px';
      ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
      ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
      btn.style.position = 'relative';
      btn.style.overflow = 'hidden';
      btn.appendChild(ripple);
      setTimeout(function () { ripple.remove(); }, 600);
    });
  });

  /* ------------------------------------------------
     HERO PARALLAX (subtle depth on scroll)
  ------------------------------------------------ */
  var heroContent = document.querySelector('.hero-content');
  var heroVisual = document.querySelector('.hero-visual');

  window.addEventListener('scroll', function () {
    if (window.scrollY < window.innerHeight) {
      var scroll = window.scrollY;
      if (heroContent) heroContent.style.transform = 'translateY(' + (scroll * 0.08) + 'px)';
      if (heroVisual) heroVisual.style.transform = 'translateY(' + (scroll * 0.15) + 'px)';
    }
  }, { passive: true });

  /* ------------------------------------------------
     SKILL CARD TILT on hover
  ------------------------------------------------ */
  if (supportsHover) {
    document.querySelectorAll('.skill-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var centerX = rect.width / 2;
        var centerY = rect.height / 2;
        var rotateX = ((y - centerY) / centerY) * -1.8;
        var rotateY = ((x - centerX) / centerX) * 1.8;
        card.style.transform = 'perspective(600px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  /* ------------------------------------------------
     VERSION BADGE TOGGLE
  ------------------------------------------------ */
  var versionBadge = document.querySelector('.site-version');
  if (versionBadge) {
    function toggleVersion() { versionBadge.classList.toggle('show-date'); }
    versionBadge.addEventListener('click', toggleVersion);
    versionBadge.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleVersion(); }
    });
  }

})();
