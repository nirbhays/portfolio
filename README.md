# Nirbhay Singh — Professional Portfolio

Personal portfolio website for **Nirbhay Singh**, Cloud & AI Architect with 11+ years of experience across AWS, GCP, and Azure.

**Live at:** [cloudtoai.in](https://cloudtoai.in)

## Overview

A single-page portfolio built with vanilla HTML, CSS, and JavaScript — no frameworks, no build step. Deployed on Netlify with automatic deploys on push to `main`.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML5, CSS3, JavaScript (ES6+) |
| Fonts | Google Fonts (Space Grotesk, Inter, JetBrains Mono) |
| Hosting | Netlify (auto-deploy on push) |
| Assets | PNG/JPG logos, PDF resume |
| Animation | Canvas API (particle network background) |

## Repository Structure

```
portfolio/
├── index.html          # All content — single HTML file
├── styles.css          # All styling
├── script.js           # Interactivity: particles, typing, scroll reveal, nav
├── netlify.toml        # Netlify config: headers, caching, 404 redirect
└── assets/
    ├── logos/          # Company logos (Bosch, Deloitte, IBM, McAfee, PTC)
    │   ├── bosch.png
    │   ├── deloitte.png
    │   ├── ibm.png
    │   ├── mcafee.png
    │   └── ptc.png
    ├── portfolio_headshot_professional.jpg  # Profile photo
    └── resume.pdf      # Downloadable resume
```

## Sections

| Section | ID | Description |
|---|---|---|
| Hero | `#hero` | Name, title, CTA buttons, animated terminal |
| About | `#about` | Bio, location, role, focus areas |
| Skills | `#skills` | Cloud, DevOps, MLOps, GenAI technology grid |
| Experience | `#experience` | Work history with company logos |
| Projects | `#projects` | Featured open source (ShieldIaC, TokenMeter, etc.) |
| Writing | `#writing` | Medium articles |
| Certifications | `#certifications` | GCP, AWS, Kubernetes, Terraform credentials |
| Education | `#education` | MTech from BITS |
| Contact | `#contact` | Links and contact form |

## Running Locally

No build process required:

```bash
git clone https://github.com/nirbhays/portfolio.git
cd portfolio

# Option 1: Python simple server
python -m http.server 8080

# Option 2: VS Code Live Server extension
# Right-click index.html → Open with Live Server

# Option 3: Node http-server
npx http-server .
```

Open `http://localhost:8080` in your browser.

## Deployment

Hosted on **Netlify** with automatic deployments:

1. Push to `main` branch
2. Netlify auto-builds and deploys (typically under 1 minute)
3. Live at `https://cloudtoai.in`

Custom headers in `netlify.toml`:
- Security headers (X-Frame-Options, CSP)
- Long-cache for `/assets/*` (1 year)
- Medium cache for CSS/JS (1 week)
- Catch-all redirect to `index.html` for SPA-like behavior

## Featured Projects on the Site

- **ShieldIaC** — AI-powered IaC security scanner (100+ rules, 9 compliance frameworks)
- **TokenMeter** — Open-source LLM cost tracker
- Additional projects linked to GitHub

## Key External Links

- GitHub: [github.com/nirbhays](https://github.com/nirbhays)
- Medium: [medium.com/@nirbhaysingh1](https://medium.com/@nirbhaysingh1)
- Credly: [credly.com/users/nirbhaysingh](https://www.credly.com/users/nirbhaysingh)
- LinkedIn: linked from contact section
