# CLAUDE.md — nirbhays/portfolio

## Repository Purpose

Source code for **Nirbhay Singh's professional portfolio website**, live at [cloudtoai.in](https://cloudtoai.in). Single-page application built with vanilla HTML/CSS/JS, deployed via Netlify.

## Owner Profile

| Attribute | Value |
|---|---|
| Name | Nirbhay Singh |
| Role | Cloud & AI Architect @ Bosch Polska |
| Location | Warsaw, Poland |
| Experience | 11+ years multi-cloud (GCP, AWS, Azure) |
| Specialties | MLOps, GenAI, FinOps, Kubernetes, Terraform, Platform Engineering |
| Education | MTech — Birla Institute of Technology |
| Website | cloudtoai.in |

## File Map

| File | What it contains |
|---|---|
| `index.html` | All page content and structure (sections listed below) |
| `styles.css` | All styling — responsive, dark theme, animations |
| `script.js` | Canvas particle network, typing animation, scroll reveal, sticky nav |
| `netlify.toml` | Deployment config: security headers, caching, 404 redirect |
| `assets/logos/` | Company logos: Bosch, Deloitte, IBM, McAfee, PTC |
| `assets/portfolio_headshot_professional.jpg` | Profile photo |
| `assets/resume.pdf` | Downloadable resume |

## Section Map (`index.html`)

| Section | HTML ID | Lines (approx) | What to update |
|---|---|---|---|
| Hero | `#hero` | ~83–151 | Job title, tagline, terminal animation text |
| About | `#about` | ~154–203 | Bio text, current role, location, focus areas |
| Skills | `#skills` | ~206–329 | Technology tags (cloud, DevOps, MLOps, GenAI tools) |
| Experience | `#experience` | ~332–472 | Job titles, companies, date ranges, bullet points |
| Projects | `#projects` | ~475–785 | Project cards: name, tagline, description, metrics, tech tags, GitHub link |
| Writing | `#writing` | ~786–832 | Medium article links |
| Certifications | `#certifications` | ~833–935 | Cert names, providers, validity dates |
| Education | `#education` | ~936–977 | Degree, institution |
| Contact | `#contact` | ~978–end | Email, LinkedIn, GitHub, Medium cards (no form) |

## Deployment

**Netlify** — auto-deploys on every push to `main`.

```
Push to main → Netlify webhook → Rebuild → Live on cloudtoai.in
```

Build settings in `netlify.toml`:
- Publish directory: `.` (root — no build step)
- Security headers on all routes
- 1-year cache for `assets/*`
- 1-week cache for CSS/JS
- All unmatched routes redirect to `index.html`

To deploy manually: just `git push origin main`.

## How to Update Content

### Updating current job title or role
Edit the `#about` section and `#hero` section in `index.html`. Also update `#experience` with new dates and bullet points.

### Adding a new project
Copy an existing `<article class="project-card reveal">` block in the `#projects` section. Update:
- GitHub link
- Project name (`<h3>`)
- Tagline (`.project-tagline`)
- Description (`.project-desc`)
- Metrics (`.project-metrics`)
- Tech tags (`.project-tech`)

### Adding/updating certifications
Find the relevant `<div class="certs-group reveal">` in `#certifications`. Copy a `<div class="cert-card">` and update the cert name and validity date. Badge classes: `gcp`, `aws`, `k8s`, `tf`, `ms`.

### Adding a Medium article
Find `#writing` section. Add a new article card with the Medium URL, title, and short description.

### Updating resume
Replace `assets/resume.pdf` — same filename, git push. The download link in `#hero` auto-picks it up.

### Updating profile photo
Replace `assets/portfolio_headshot_professional.jpg` — same filename, git push.

## Local Development

```bash
git clone https://github.com/nirbhays/portfolio.git
cd portfolio
python -m http.server 8080
# Open http://localhost:8080
```

No npm, no build tooling — pure static files.

## Key Things to Keep Updated as Career Progresses

1. **Current role** in `#hero` typed-text animation and `#about`
2. **New certifications** (GCP DevOps Engineer, PMLE) when earned — update `#certifications`
3. **New projects** — ShieldIaC, TokenMeter, InfraCents, AgentLoom, Airlock, DataMint, ModelLedger, TuneForge currently listed; add new open-source work
4. **Work experience** — when leaving Bosch for new role, update `#experience`
5. **Writing** — add Medium article links after each new post
6. **Resume PDF** — keep in sync with LinkedIn and actual applications

## Certifications Currently Displayed

**Google Cloud:** Professional ML Engineer (valid Dec 2027), Professional Cloud DevOps Engineer (valid Dec 2027), Professional Cloud Architect (valid Jun 2026), Generative AI Leader (valid Aug 2028), Associate Cloud Engineer

**AWS:** Solutions Architect Professional, Solutions Architect Associate

**Other:** CKAD (valid Sep 2026), Terraform Associate, MCSA

All badges verifiable at: https://www.credly.com/users/nirbhaysingh
