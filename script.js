(function () {
  'use strict';

  var supportsHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ------------------------------------------------
     LOADER
  ------------------------------------------------ */
  window.addEventListener('load', function () {
    requestAnimationFrame(function () {
      document.getElementById('loader').classList.add('hidden');
    });
  });

  /* ------------------------------------------------
     ENHANCED PARTICLE NETWORK + FLOATING SHAPES
  ------------------------------------------------ */
  var canvas = document.getElementById('bg-canvas');
  var ctx = canvas.getContext('2d');
  var particles = [];
  var PARTICLE_COUNT = 100;
  var CONNECTION_DIST = 132;
  var MOUSE_DIST = 220;
  var paused = false;
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

  var particleColors = ['34,211,238', '244,114,182', '167,139,250'];

  function Particle() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = (Math.random() - 0.5) * 0.5;
    this.vy = (Math.random() - 0.5) * 0.5;
    this.radius = Math.random() * 2 + 0.5;
    this.baseRadius = this.radius;
    this.color = particleColors[Math.floor(Math.random() * particleColors.length)];
    this.isStar = Math.random() < 0.2;
    this.ttl = -1;
    this.baseOpacity = 0.6;
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

  var floatingShapes = [];
  var shapeTypes = ['triangle', 'hexagon', 'cross'];

  function FloatingShape() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = (Math.random() - 0.5) * 0.2;
    this.vy = (Math.random() - 0.5) * 0.15;
    this.rotation = Math.random() * Math.PI * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 0.005;
    this.size = 15 + Math.random() * 15;
    this.type = shapeTypes[Math.floor(Math.random() * shapeTypes.length)];
    this.color = particleColors[Math.floor(Math.random() * particleColors.length)];
    this.opacity = 0.03 + Math.random() * 0.04;
  }

  for (var si = 0; si < 10; si++) {
    floatingShapes.push(new FloatingShape());
  }

  function drawShape(shape) {
    ctx.save();
    ctx.translate(shape.x, shape.y);
    ctx.rotate(shape.rotation);
    ctx.strokeStyle = 'rgba(' + shape.color + ',' + shape.opacity + ')';
    ctx.lineWidth = 1;
    ctx.beginPath();

    if (shape.type === 'triangle') {
      for (var i = 0; i < 3; i++) {
        var angle = (i * 2 * Math.PI / 3) - Math.PI / 2;
        var px = Math.cos(angle) * shape.size;
        var py = Math.sin(angle) * shape.size;
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
    } else if (shape.type === 'hexagon') {
      for (var j = 0; j < 6; j++) {
        var ha = (j * Math.PI / 3) - Math.PI / 6;
        var hx = Math.cos(ha) * shape.size;
        var hy = Math.sin(ha) * shape.size;
        if (j === 0) ctx.moveTo(hx, hy); else ctx.lineTo(hx, hy);
      }
      ctx.closePath();
    } else {
      var s = shape.size * 0.4;
      ctx.moveTo(-s, 0); ctx.lineTo(s, 0);
      ctx.moveTo(0, -s); ctx.lineTo(0, s);
    }
    ctx.stroke();
    ctx.restore();
  }

  function drawStar(x, y, r, color, opacity) {
    ctx.beginPath();
    for (var i = 0; i < 4; i++) {
      var angle = (i * Math.PI / 2);
      ctx.moveTo(x, y);
      ctx.lineTo(x + Math.cos(angle) * r * 2, y + Math.sin(angle) * r * 2);
    }
    ctx.strokeStyle = 'rgba(' + color + ',' + opacity + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
  }

  var explosionParticles = [];

  function drawParticles() {
    if (paused) { requestAnimationFrame(drawParticles); return; }
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var scrollFade = window.scrollY > window.innerHeight ? 0.55 : 1;

    for (var si = 0; si < floatingShapes.length; si++) {
      var shape = floatingShapes[si];
      shape.x += shape.vx;
      shape.y += shape.vy;
      shape.rotation += shape.rotationSpeed;
      if (shape.x < -shape.size) shape.x = canvas.width + shape.size;
      if (shape.x > canvas.width + shape.size) shape.x = -shape.size;
      if (shape.y < -shape.size) shape.y = canvas.height + shape.size;
      if (shape.y > canvas.height + shape.size) shape.y = -shape.size;
      drawShape(shape);
    }

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      if (p.ttl > 0) {
        p.ttl--;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.04;
        p.vx *= 0.98;
        p.vy *= 0.98;
        var ttlOpacity = (p.ttl / 50) * 0.8;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + p.color + ',' + ttlOpacity + ')';
        ctx.fill();
        if (p.ttl <= 0) { particles.splice(i, 1); i--; }
        continue;
      }

      var dxM = mouseX - p.x;
      var dyM = mouseY - p.y;
      var distM = Math.sqrt(dxM * dxM + dyM * dyM);
      if (distM > 0 && distM < MOUSE_DIST) {
        var force = (MOUSE_DIST - distM) / MOUSE_DIST;
        if (distM < 120) {
          p.vx += (dxM / distM) * force * 0.008;
          p.vy += (dyM / distM) * force * 0.008;
        } else {
          p.vx -= (dxM / distM) * force * 0.02;
          p.vy -= (dyM / distM) * force * 0.02;
        }
        p.radius = p.baseRadius + force * 2.5;
      } else {
        p.radius += (p.baseRadius - p.radius) * 0.05;
      }

      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.99;
      p.vy *= 0.99;

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      var pOpacity = p.baseOpacity * scrollFade;

      if (p.isStar) {
        drawStar(p.x, p.y, p.radius, p.color, pOpacity);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + p.color + ',' + pOpacity + ')';
        ctx.fill();
      } else {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + p.color + ',' + pOpacity + ')';
        ctx.fill();
      }

      if (p.radius > p.baseRadius * 1.2) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + p.color + ',' + (pOpacity * 0.1) + ')';
        ctx.fill();
      }

      for (var j = i + 1; j < particles.length; j++) {
        var p2 = particles[j];
        if (p2.ttl > 0) continue;
        var dx = p.x - p2.x;
        var dy = p.y - p2.y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DIST) {
          var opacity = 1 - dist / CONNECTION_DIST;
          var nearCursorBoost = 1;
          var midX = (p.x + p2.x) / 2;
          var midY = (p.y + p2.y) / 2;
          var distToCursor = Math.sqrt((midX - mouseX) * (midX - mouseX) + (midY - mouseY) * (midY - mouseY));
          if (distToCursor < MOUSE_DIST) {
            nearCursorBoost = 1 + (1 - distToCursor / MOUSE_DIST) * 1.5;
          }
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          var gradient = ctx.createLinearGradient(p.x, p.y, p2.x, p2.y);
          var lineOpacity = opacity * 0.25 * nearCursorBoost * scrollFade;
          gradient.addColorStop(0, 'rgba(' + p.color + ',' + lineOpacity + ')');
          gradient.addColorStop(1, 'rgba(' + p2.color + ',' + lineOpacity + ')');
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
    paused = document.hidden;
  });

  /* ------------------------------------------------
     CLICK PARTICLE EXPLOSIONS
  ------------------------------------------------ */
  var activeExplosions = 0;
  var sectionColors = {
    hero: '34,211,238',
    about: '34,211,238',
    skills: '96,165,250',
    experience: '244,114,182',
    projects: '244,114,182',
    writing: '167,139,250',
    certifications: '167,139,250',
    education: '96,165,250',
    contact: '34,211,238'
  };

  function getSectionColor() {
    var scrollY = window.scrollY + window.innerHeight / 2;
    var sections = document.querySelectorAll('main .section, .hero');
    var color = '34,211,238';
    sections.forEach(function (s) {
      if (scrollY >= s.offsetTop) {
        color = sectionColors[s.id] || '34,211,238';
      }
    });
    return color;
  }

  document.addEventListener('click', function (e) {
    if (activeExplosions >= 3) return;
    activeExplosions++;
    var color = getSectionColor();
    var count = 15 + Math.floor(Math.random() * 6);
    for (var i = 0; i < count; i++) {
      var angle = (Math.PI * 2 / count) * i + (Math.random() - 0.5) * 0.5;
      var speed = 2 + Math.random() * 4;
      var ep = new Particle();
      ep.x = e.clientX + window.scrollX;
      ep.y = e.clientY;
      ep.vx = Math.cos(angle) * speed;
      ep.vy = Math.sin(angle) * speed;
      ep.radius = 1.5 + Math.random() * 3;
      ep.color = color;
      ep.ttl = 30 + Math.floor(Math.random() * 20);
      ep.isStar = false;
      particles.push(ep);
    }
    setTimeout(function () { activeExplosions--; }, 800);
  });

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
     UNIVERSAL 3D CARD TILT (all other cards)
  ------------------------------------------------ */
  if (supportsHover) {
    var tiltConfigs = [
      { selector: '.article-card', maxTilt: 2.2 },
      { selector: '.contact-card', maxTilt: 2.0 },
      { selector: '.education-card', maxTilt: 2.0 },
      { selector: '.cert-card', maxTilt: 1.5 },
      { selector: '.stat', maxTilt: 1.8 }
    ];

    tiltConfigs.forEach(function (config) {
      document.querySelectorAll(config.selector).forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
          var rect = card.getBoundingClientRect();
          var x = e.clientX - rect.left;
          var y = e.clientY - rect.top;
          var centerX = rect.width / 2;
          var centerY = rect.height / 2;
          var rotateX = ((y - centerY) / centerY) * -config.maxTilt;
          var rotateY = ((x - centerX) / centerX) * config.maxTilt;
          card.style.transform = 'perspective(600px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-3px)';
        });
        card.addEventListener('mouseleave', function () {
          card.style.transform = '';
        });
      });
    });
  }

  /* ------------------------------------------------
     MAGNETIC ELEMENT HOVER (expanded)
  ------------------------------------------------ */
  if (supportsHover) {
    var magneticSelectors = '.btn, .nav-link, .nav-icon, .tag, .tag-sm, .project-links a, .timeline-marker, .contact-card svg';
    document.querySelectorAll(magneticSelectors).forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var rect = el.getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        el.style.transform = 'translate(' + (x * 0.08) + 'px, ' + (y * 0.08) + 'px) scale(1.02)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transform = '';
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
     TEXT SCRAMBLE REVEAL
  ------------------------------------------------ */
  var scrambleChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';

  function scrambleReveal(el) {
    var finalText = el.getAttribute('data-text');
    if (!finalText) return;

    var length = finalText.length;
    var resolved = 0;
    var current = [];
    for (var i = 0; i < length; i++) {
      current.push(scrambleChars[Math.floor(Math.random() * scrambleChars.length)]);
    }
    el.textContent = current.join('');

    var interval = setInterval(function () {
      for (var i = resolved; i < length; i++) {
        current[i] = scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
      }
      if (resolved < length) {
        current[resolved] = finalText[resolved];
        resolved++;
      }
      el.textContent = current.join('');
      if (resolved >= length) {
        clearInterval(interval);
        el.textContent = finalText;
      }
    }, 40);
  }

  if ('IntersectionObserver' in window) {
    var scrambleLabels = document.querySelectorAll('.section-label[data-text]');
    var scrambleObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          scrambleReveal(entry.target);
          scrambleObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    scrambleLabels.forEach(function (el) { scrambleObserver.observe(el); });
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
     HERO CURSOR PARALLAX (mouse-driven depth)
  ------------------------------------------------ */
  var heroContent = document.querySelector('.hero-content');
  var heroVisual = document.querySelector('.hero-visual');
  var heroName = document.querySelector('.hero-name');
  var heroDesc = document.querySelector('.hero-desc');
  var heroStats = document.querySelector('.hero-stats');
  var heroSection = document.getElementById('hero');

  if (supportsHover && heroSection) {
    heroSection.addEventListener('mousemove', function (e) {
      var rect = heroSection.getBoundingClientRect();
      var mx = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      var my = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

      if (heroName) heroName.style.transform = 'translate(' + (mx * -8) + 'px, ' + (my * -5) + 'px)';
      if (heroDesc) heroDesc.style.transform = 'translate(' + (mx * -4) + 'px, ' + (my * -3) + 'px)';
      if (heroStats) heroStats.style.transform = 'translate(' + (mx * -6) + 'px, ' + (my * -4) + 'px)';
      if (heroVisual) heroVisual.style.transform = 'translate(' + (mx * 12) + 'px, ' + (my * 8) + 'px)';
    });

    heroSection.addEventListener('mouseleave', function () {
      if (heroName) heroName.style.transform = '';
      if (heroDesc) heroDesc.style.transform = '';
      if (heroStats) heroStats.style.transform = '';
      if (heroVisual) heroVisual.style.transform = '';
    });
  }

  window.addEventListener('scroll', function () {
    if (window.scrollY < window.innerHeight) {
      var scroll = window.scrollY;
      if (heroContent) heroContent.style.opacity = 1 - scroll / (window.innerHeight * 0.8);
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
     SCROLL-SYNCED TIMELINE GLOW
  ------------------------------------------------ */
  var experienceSection = document.getElementById('experience');
  var timeline = experienceSection ? experienceSection.querySelector('.timeline') : null;

  if (timeline) {
    var timelineAfterStyle = document.createElement('style');
    timelineAfterStyle.id = 'timeline-scroll-style';
    document.head.appendChild(timelineAfterStyle);

    window.addEventListener('scroll', function () {
      var rect = experienceSection.getBoundingClientRect();
      var sectionTop = rect.top;
      var sectionHeight = rect.height;
      var viewH = window.innerHeight;

      var progress = Math.max(0, Math.min(1, (viewH - sectionTop) / (sectionHeight + viewH)));
      var topPercent = progress * 100;

      timelineAfterStyle.textContent =
        '.timeline::after { animation: none !important; top: ' + topPercent + '% !important; opacity: 1 !important; }';
    }, { passive: true });
  }

  /* ------------------------------------------------
     BACKGROUND SCROLL COLOR SHIFT
  ------------------------------------------------ */
  var bgColors = [
    { pos: 0, r: 6, g: 11, b: 24 },
    { pos: 0.2, r: 6, g: 13, b: 30 },
    { pos: 0.4, r: 10, g: 11, b: 24 },
    { pos: 0.6, r: 8, g: 9, b: 30 },
    { pos: 0.8, r: 6, g: 11, b: 28 },
    { pos: 1.0, r: 6, g: 11, b: 24 }
  ];

  function lerpColor(a, b, t) {
    return {
      r: Math.round(a.r + (b.r - a.r) * t),
      g: Math.round(a.g + (b.g - a.g) * t),
      b: Math.round(a.b + (b.b - a.b) * t)
    };
  }

  window.addEventListener('scroll', function () {
    var scrollFraction = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
    scrollFraction = Math.max(0, Math.min(1, scrollFraction));

    var lower = bgColors[0], upper = bgColors[1];
    for (var i = 0; i < bgColors.length - 1; i++) {
      if (scrollFraction >= bgColors[i].pos && scrollFraction <= bgColors[i + 1].pos) {
        lower = bgColors[i];
        upper = bgColors[i + 1];
        break;
      }
    }

    var range = upper.pos - lower.pos;
    var t = range > 0 ? (scrollFraction - lower.pos) / range : 0;
    var c = lerpColor(lower, upper, t);
    document.body.style.background = 'rgb(' + c.r + ',' + c.g + ',' + c.b + ')';
  }, { passive: true });

  /* ------------------------------------------------
     HERO NAME GLITCH EFFECT
  ------------------------------------------------ */
  var heroNameEl = document.querySelector('.hero-name');
  if (heroNameEl) {
    function triggerGlitch() {
      heroNameEl.classList.add('glitch');
      setTimeout(function () {
        heroNameEl.classList.remove('glitch');
      }, 200);
      var nextDelay = 8000 + Math.random() * 4000;
      setTimeout(triggerGlitch, nextDelay);
    }
    setTimeout(triggerGlitch, 5000);
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
