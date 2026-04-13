#!/usr/bin/env python3
"""
Premium Resume Generator for Nirbhay Singh
───────────────────────────────────────────
Generates 6 visually-rich, ATS-friendly PDF resumes with:
  - Profile photo (circular crop)
  - Colored sidebar with contact links, skills, education
  - Icon circles for social links with clickable hyperlinks
  - Metric highlight cards
  - Clean modern typography
  - Tailored content per target role
"""

import os, math
from fpdf import FPDF
from PIL import Image, ImageDraw

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = SCRIPT_DIR
PHOTO_SRC   = os.path.join(SCRIPT_DIR, "..", "assets", "portfolio_headshot_professional.jpg")
PHOTO_CIRCLE = os.path.join(SCRIPT_DIR, "_headshot_circle.png")

# ── Prepare circular headshot ───────────────────────────────────
def make_circular_headshot():
    """Crop the headshot into a circle with transparent background."""
    if os.path.exists(PHOTO_CIRCLE):
        return PHOTO_CIRCLE
    img = Image.open(PHOTO_SRC).convert("RGBA")
    # Make it square first
    sz = min(img.size)
    left = (img.width - sz) // 2
    top  = (img.height - sz) // 2
    img = img.crop((left, top, left + sz, top + sz))
    img = img.resize((400, 400), Image.LANCZOS)
    # Create circular mask
    mask = Image.new("L", (400, 400), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 400, 400), fill=255)
    # Apply mask
    out = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    out.save(PHOTO_CIRCLE, "PNG")
    return PHOTO_CIRCLE


# ── Colour constants ────────────────────────────────────────────
WHITE       = (255, 255, 255)
DARK        = (26, 32, 44)
SIDEBAR_BG  = (30, 41, 59)
LIGHT_TEXT  = (203, 213, 225)
MUTED       = (100, 116, 139)
BODY_BG     = (255, 255, 255)
CARD_BG     = (241, 245, 249)
DIVIDER     = (226, 232, 240)

# ── Personal data ───────────────────────────────────────────────
P = {
    "name": "Nirbhay Singh",
    "email": "nirbhaysingh1@live.com",
    "linkedin": "linkedin.com/in/nirbhaysingh1",
    "linkedin_url": "https://www.linkedin.com/in/nirbhaysingh1/",
    "github": "github.com/nirbhays",
    "github_url": "https://github.com/nirbhays",
    "blog": "medium.com/@nirbhaysingh1",
    "blog_url": "https://medium.com/@nirbhaysingh1",
    "credly": "credly.com/users/nirbhaysingh",
    "credly_url": "https://www.credly.com/users/nirbhaysingh/badges",
    "website": "cloudtoai.in",
    "website_url": "https://cloudtoai.in",
    "location": "Warsaw, Poland",
}


# ════════════════════════════════════════════════════════════════
# Premium PDF Builder with Sidebar Layout
# ════════════════════════════════════════════════════════════════

class PremiumResume(FPDF):
    SIDEBAR_W = 62       # mm
    MAIN_X    = 66       # sidebar + 4mm gutter
    MAIN_W    = 128      # 210 - 66 - 16 right margin
    PAGE_H    = 297
    PAGE_W    = 210

    def __init__(self, accent=(37, 99, 235), accent_light=(219, 234, 254)):
        super().__init__("P", "mm", "A4")
        self.accent = accent
        self.accent_light = accent_light
        self.sidebar_items_y = 0
        self.set_auto_page_break(auto=False)

    # ── low-level helpers ───────────────────────────────────────

    def _fill(self, rgb):
        self.set_fill_color(*rgb)

    def _text_color(self, rgb):
        self.set_text_color(*rgb)

    def _draw_color(self, rgb):
        self.set_draw_color(*rgb)

    def _sidebar_bg(self):
        """Draw the sidebar background for the current page."""
        self._fill(SIDEBAR_BG)
        self.rect(0, 0, self.SIDEBAR_W, self.PAGE_H, "F")

    def _ensure_space(self, needed=25):
        if self.get_y() + needed > 282:
            self.add_page()
            self._sidebar_bg()
            self.set_y(10)

    # ── icon circle helper ──────────────────────────────────────

    def _icon_circle(self, x, y, r, label, color):
        """Draw a small filled circle with a 1-2 char label inside."""
        self._fill(color)
        # Draw circle using arc
        self.ellipse(x - r, y - r, r * 2, r * 2, "F")
        self.set_font("Helvetica", "B", 6)
        self._text_color(WHITE)
        tw = self.get_string_width(label)
        self.set_xy(x - tw / 2, y - 2)
        self.cell(tw, 4, label, align="C")

    # ── SIDEBAR SECTIONS ────────────────────────────────────────

    def _sidebar_contact(self, y_start):
        """Render contact links in the sidebar with icon circles."""
        x_icon = 10
        x_text = 18
        w_text = self.SIDEBAR_W - x_text - 3
        y = y_start

        links = [
            ("@",  P["email"],     f"mailto:{P['email']}"),
            ("in", P["linkedin"],  P["linkedin_url"]),
            ("GH", P["github"],    P["github_url"]),
            ("M",  P["blog"],      P["blog_url"]),
            ("W",  P["website"],   P["website_url"]),
            ("C",  P["credly"],    P["credly_url"]),
        ]

        # Section header
        self.set_xy(6, y)
        self.set_font("Helvetica", "B", 8)
        self._text_color(self.accent_light)
        self.cell(self.SIDEBAR_W - 12, 5, "CONTACT", new_x="LMARGIN", new_y="NEXT")
        y += 7
        # Underline
        self._draw_color(self.accent)
        self.set_line_width(0.5)
        self.line(6, y - 1, self.SIDEBAR_W - 6, y - 1)
        self.set_line_width(0.2)

        for icon_label, display, url in links:
            self._icon_circle(x_icon, y + 2, 3, icon_label, self.accent)
            self.set_font("Helvetica", "", 6.5)
            self._text_color(LIGHT_TEXT)
            self.set_xy(x_text, y - 0.5)
            self.cell(w_text, 4.5, display, link=url)
            y += 7

        # Location (no link)
        self._icon_circle(x_icon, y + 2, 3, "L", (100, 116, 139))
        self.set_font("Helvetica", "", 6.5)
        self._text_color(LIGHT_TEXT)
        self.set_xy(x_text, y - 0.5)
        self.cell(w_text, 4.5, P["location"])
        y += 9
        return y

    def _sidebar_skills(self, y_start, skills_dict):
        """Render skills with category headers and items in the sidebar."""
        y = y_start
        # Section header
        self.set_xy(6, y)
        self.set_font("Helvetica", "B", 8)
        self._text_color(self.accent_light)
        self.cell(self.SIDEBAR_W - 12, 5, "CORE SKILLS", new_x="LMARGIN", new_y="NEXT")
        y += 6
        self._draw_color(self.accent)
        self.set_line_width(0.5)
        self.line(6, y, self.SIDEBAR_W - 6, y)
        self.set_line_width(0.2)
        y += 2

        for cat, items in skills_dict.items():
            if y > 270:
                break
            self.set_xy(6, y)
            self.set_font("Helvetica", "B", 6.5)
            self._text_color(self.accent)
            cat_display = cat.upper()
            self.cell(self.SIDEBAR_W - 12, 4, cat_display)
            y += 4.5

            self.set_xy(6, y)
            self.set_font("Helvetica", "", 6)
            self._text_color(LIGHT_TEXT)
            # Wrap items text
            self.multi_cell(self.SIDEBAR_W - 12, 3.5, items)
            y = self.get_y() + 2

        return y

    def _sidebar_education(self, y_start):
        """Render education in sidebar."""
        y = y_start
        if y > 265:
            return y
        self.set_xy(6, y)
        self.set_font("Helvetica", "B", 8)
        self._text_color(self.accent_light)
        self.cell(self.SIDEBAR_W - 12, 5, "EDUCATION")
        y += 6
        self._draw_color(self.accent)
        self.set_line_width(0.5)
        self.line(6, y, self.SIDEBAR_W - 6, y)
        self.set_line_width(0.2)
        y += 3

        self.set_xy(6, y)
        self.set_font("Helvetica", "B", 7)
        self._text_color(WHITE)
        self.cell(self.SIDEBAR_W - 12, 4, "MTech (Master of Technology)")
        y += 4.5
        self.set_xy(6, y)
        self.set_font("Helvetica", "", 6.5)
        self._text_color(LIGHT_TEXT)
        self.cell(self.SIDEBAR_W - 12, 4, "Birla Institute of Technology")
        y += 6

        return y

    def _sidebar_languages(self, y_start):
        """Render languages in sidebar."""
        y = y_start
        if y > 275:
            return y
        self.set_xy(6, y)
        self.set_font("Helvetica", "B", 8)
        self._text_color(self.accent_light)
        self.cell(self.SIDEBAR_W - 12, 5, "LANGUAGES")
        y += 6
        self._draw_color(self.accent)
        self.set_line_width(0.5)
        self.line(6, y, self.SIDEBAR_W - 6, y)
        self.set_line_width(0.2)
        y += 3

        for lang, level in [("English", "Professional"), ("Hindi", "Native")]:
            self.set_xy(6, y)
            self.set_font("Helvetica", "B", 7)
            self._text_color(WHITE)
            self.cell(25, 3.5, lang)
            self.set_font("Helvetica", "", 6)
            self._text_color(LIGHT_TEXT)
            self.cell(25, 3.5, level)
            y += 5

        return y

    # ── MAIN AREA SECTIONS ──────────────────────────────────────

    def _main_section_header(self, title):
        """Render a section header in the main content area."""
        self._ensure_space(15)
        y = self.get_y() + 1
        # Accent block before title
        self._fill(self.accent)
        self.rect(self.MAIN_X, y + 0.5, 3, 5.5, "F")
        # Title text
        self.set_xy(self.MAIN_X + 5, y)
        self.set_font("Helvetica", "B", 10)
        self._text_color(self.accent)
        self.cell(self.MAIN_W - 5, 6.5, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y2 = self.get_y()
        # Thin line under
        self._draw_color(DIVIDER)
        self.set_line_width(0.4)
        self.line(self.MAIN_X, y2, self.MAIN_X + self.MAIN_W, y2)
        self.set_line_width(0.2)
        self.set_y(y2 + 2.5)

    def main_summary(self, text):
        self._main_section_header("Professional Summary")
        self.set_xy(self.MAIN_X, self.get_y())
        self.set_font("Helvetica", "", 8.5)
        self._text_color(DARK)
        self.multi_cell(self.MAIN_W, 4.2, text, new_x="LMARGIN", new_y="NEXT")
        self.set_y(self.get_y() + 2)

    def main_metrics(self, metrics):
        """metrics: list of (value, label) tuples, max 4-5."""
        y = self.get_y()
        n = len(metrics)
        gap = 2
        card_w = (self.MAIN_W - (n - 1) * gap) / n
        x = self.MAIN_X

        for val, label in metrics:
            # Card background with top accent border
            self._fill(self.accent)
            self.rect(x, y, card_w, 1.5, "F")  # accent top stripe
            self._fill(self.accent_light)
            self.rect(x, y + 1.5, card_w, 14, "F")
            # Value
            self.set_font("Helvetica", "B", 13)
            self._text_color(self.accent)
            self.set_xy(x, y + 2.5)
            self.cell(card_w, 6, val, align="C")
            # Label
            self.set_font("Helvetica", "", 5.5)
            self._text_color(MUTED)
            self.set_xy(x, y + 9)
            self.cell(card_w, 5, label, align="C")
            x += card_w + gap

        self.set_y(y + 19)

    def main_highlights(self, items):
        self._main_section_header("Key Achievements")
        for item in items:
            self._ensure_space(10)
            y = self.get_y()
            # Accent arrow/chevron marker
            self._fill(self.accent)
            self.ellipse(self.MAIN_X + 1.5, y + 1.2, 2, 2, "F")
            # White check inside
            self.set_font("Helvetica", "B", 5)
            self._text_color(WHITE)
            self.set_xy(self.MAIN_X + 1.5, y + 0.3)
            self.cell(2, 3, ">", align="C")
            # Text
            self.set_xy(self.MAIN_X + 5.5, y)
            self.set_font("Helvetica", "", 7.5)
            self._text_color(DARK)
            self.multi_cell(self.MAIN_W - 6, 3.8, item, new_x="LMARGIN", new_y="NEXT")
            self.set_y(self.get_y() + 0.5)
        self.set_y(self.get_y() + 1.5)

    def main_experience(self, jobs):
        self._main_section_header("Professional Experience")
        for job in jobs:
            self._ensure_space(26)
            y = self.get_y()

            # ── Timeline dot ────────────────────────────────────
            self._fill(self.accent)
            self.ellipse(self.MAIN_X, y + 1.5, 3.5, 3.5, "F")
            # Small inner white dot for ring effect
            self._fill(WHITE)
            self.ellipse(self.MAIN_X + 0.8, y + 2.3, 1.9, 1.9, "F")

            # ── Duration pill (right-aligned, rendered first to reserve space)
            self.set_font("Helvetica", "B", 6.5)
            dur_text = job["duration"]
            dur_tw = self.get_string_width(dur_text) + 6
            dur_x = self.MAIN_X + self.MAIN_W - dur_tw
            # Pill background
            self._fill(self.accent_light)
            self.rect(dur_x, y + 0.5, dur_tw, 5, "F")
            self._text_color(self.accent)
            self.set_xy(dur_x, y + 0.5)
            self.cell(dur_tw, 5, dur_text, align="C")

            # ── Job title (limited width so it doesn't hit the pill)
            title_max_w = self.MAIN_W - dur_tw - 10
            self.set_xy(self.MAIN_X + 6, y)
            self.set_font("Helvetica", "B", 9)
            self._text_color(DARK)
            self.cell(title_max_w, 5.5, job["title"])

            y += 7

            # ── Company name (bold, prominent, with accent bar)
            self.set_xy(self.MAIN_X + 6, y)
            # Small accent bar before company name
            self._fill(self.accent)
            self.rect(self.MAIN_X + 6, y + 1, 1.5, 3.5, "F")
            self.set_xy(self.MAIN_X + 9.5, y)
            self.set_font("Helvetica", "B", 8.5)
            self._text_color(self.accent)
            self.cell(0, 5, job["company"], new_x="END")

            # Location (lighter, after company)
            if job.get("location"):
                self.set_font("Helvetica", "", 7.5)
                self._text_color(MUTED)
                self.cell(0, 5, f"   {job['location']}")

            y += 7
            self.set_y(y)

            # ── Bullet points
            self.set_font("Helvetica", "", 7.5)
            for b in job["bullets"]:
                self._ensure_space(8)
                by = self.get_y()
                # Accent bullet marker
                self._fill(self.accent)
                self.ellipse(self.MAIN_X + 8, by + 1.2, 1.5, 1.5, "F")
                self.set_xy(self.MAIN_X + 11, by)
                self._text_color(DARK)
                self.multi_cell(self.MAIN_W - 13, 3.8, b, new_x="LMARGIN", new_y="NEXT")

            self.set_y(self.get_y() + 3.5)

    def main_projects(self, projs):
        self._main_section_header("Open-Source Projects")
        for p in projs:
            self._ensure_space(22)
            y_card_start = self.get_y()

            # ── Render content first to measure height, then draw background
            # Project name
            self.set_xy(self.MAIN_X + 4, y_card_start + 2)
            self.set_font("Helvetica", "B", 8.5)
            self._text_color(DARK)
            self.cell(self.MAIN_W - 8, 4.5, p["name"])

            # URL as hyperlink (with icon)
            self.set_xy(self.MAIN_X + 4, y_card_start + 7)
            self.set_font("Helvetica", "", 6.5)
            self._text_color(self.accent)
            link_url = p.get("link", f"https://{p['url']}")
            self.cell(self.MAIN_W - 8, 3.5, f">> {p['url']}", link=link_url)

            # Description
            self.set_xy(self.MAIN_X + 4, y_card_start + 11.5)
            self.set_font("Helvetica", "", 7.5)
            self._text_color(DARK)
            self.multi_cell(self.MAIN_W - 8, 3.5, p["desc"], new_x="LMARGIN", new_y="NEXT")

            # Tech stack
            ty = self.get_y() + 0.5
            self.set_xy(self.MAIN_X + 4, ty)
            self.set_font("Helvetica", "B", 6)
            self._text_color(MUTED)
            self.cell(self.MAIN_W - 8, 3.5, f"STACK: {p['techs']}")
            y_card_end = ty + 5

            # ── Now draw the card background BEHIND the content
            card_h = y_card_end - y_card_start
            # Draw card bg (using lower z-order trick: draw on page)
            # Since fpdf draws in order, we re-draw: fill rect then re-render text
            # Instead: use a left accent bar + bottom border approach
            self._fill(CARD_BG)
            self.rect(self.MAIN_X, y_card_start, self.MAIN_W, card_h, "F")
            # Left accent bar
            self._fill(self.accent)
            self.rect(self.MAIN_X, y_card_start, 2, card_h, "F")

            # ── Re-render content on top of background
            # Project name
            self.set_xy(self.MAIN_X + 5, y_card_start + 2)
            self.set_font("Helvetica", "B", 8.5)
            self._text_color(DARK)
            self.cell(self.MAIN_W - 10, 4.5, p["name"])

            # URL
            self.set_xy(self.MAIN_X + 5, y_card_start + 7)
            self.set_font("Helvetica", "", 6.5)
            self._text_color(self.accent)
            self.cell(self.MAIN_W - 10, 3.5, f">> {p['url']}", link=link_url)

            # Description
            self.set_xy(self.MAIN_X + 5, y_card_start + 11.5)
            self.set_font("Helvetica", "", 7.5)
            self._text_color(DARK)
            self.multi_cell(self.MAIN_W - 10, 3.5, p["desc"], new_x="LMARGIN", new_y="NEXT")

            # Tech stack
            ty2 = self.get_y() + 0.5
            self.set_xy(self.MAIN_X + 5, ty2)
            self.set_font("Helvetica", "B", 6)
            self._text_color(MUTED)
            self.cell(self.MAIN_W - 10, 3.5, f"STACK: {p['techs']}")

            self.set_y(y_card_end + 2)

    def main_certifications(self, certs):
        self._main_section_header("Certifications & Credentials")
        y = self.get_y()
        col_w = (self.MAIN_W - 4) / 2
        col = 0
        y_pos = y
        y_after_col0 = y

        for cert in certs:
            if col == 0:
                x = self.MAIN_X
            else:
                x = self.MAIN_X + col_w + 4

            self._ensure_space(8)

            # Cert badge: small filled diamond/square + bold provider + cert name
            self.set_xy(x, y_pos)
            # Accent diamond marker
            self._fill(self.accent)
            self.rect(x + 0.5, y_pos + 1.2, 2, 2, "F")

            # Parse provider from cert text for highlighting
            self.set_xy(x + 4.5, y_pos)
            self.set_font("Helvetica", "B", 7)
            self._text_color(self.accent)

            # Determine provider prefix
            provider = ""
            cert_name = cert
            for prefix in ["Google ", "AWS ", "CKAD ", "HashiCorp ", "MCSA "]:
                if cert.startswith(prefix):
                    provider = prefix.strip()
                    cert_name = cert[len(prefix):]
                    break

            if provider:
                pw = self.get_string_width(provider + " ")
                self.cell(pw, 4, provider, new_x="END")
                self.set_font("Helvetica", "", 6.5)
                self._text_color(DARK)
                self.multi_cell(col_w - 4.5 - pw, 3.5, cert_name, new_x="LMARGIN", new_y="NEXT")
            else:
                self.set_font("Helvetica", "", 7)
                self._text_color(DARK)
                self.multi_cell(col_w - 4.5, 3.5, cert, new_x="LMARGIN", new_y="NEXT")

            y_after = self.get_y() + 0.5

            if col == 0:
                y_after_col0 = y_after
                col = 1
            else:
                y_pos = max(y_after, y_after_col0) + 0.5
                col = 0

        if col == 1:
            y_pos = max(self.get_y(), y_after_col0) + 0.5
        self.set_y(y_pos + 2)

    def main_articles(self, articles):
        self._main_section_header("Technical Writing & Thought Leadership")
        for art in articles:
            self._ensure_space(10)
            y = self.get_y()
            self._fill(self.accent)
            self.ellipse(self.MAIN_X + 1, y + 0.8, 2, 2, "F")
            self.set_xy(self.MAIN_X + 5, y)
            self.set_font("Helvetica", "", 7.5)
            self._text_color(DARK)
            self.multi_cell(self.MAIN_W - 5, 3.8, art["title"], new_x="LMARGIN", new_y="NEXT")
            self.set_xy(self.MAIN_X + 5, self.get_y())
            self.set_font("Helvetica", "I", 6.5)
            self._text_color(MUTED)
            self.multi_cell(self.MAIN_W - 5, 3.5, art["desc"], new_x="LMARGIN", new_y="NEXT")
            if art.get("link"):
                self.set_xy(self.MAIN_X + 5, self.get_y())
                self.set_font("Helvetica", "", 6)
                self._text_color(self.accent)
                self.cell(self.MAIN_W - 5, 3, art["link"], link=art["link"])
                self.set_y(self.get_y() + 3.5)
        self.set_y(self.get_y() + 2)

    # ── BUILD THE FULL RESUME ───────────────────────────────────

    def build(self, title, subtitle, summary, metrics, highlights,
              sidebar_skills, experience, projects, certifications,
              articles=None):
        """Construct the full resume."""

        # ── PAGE 1 ──────────────────────────────────────────────
        self.add_page()
        self._sidebar_bg()

        # Accent band behind photo area
        self._fill(tuple(max(0, c - 10) for c in SIDEBAR_BG))
        self.rect(0, 0, self.SIDEBAR_W, 56, "F")

        # Profile photo in sidebar (slightly larger)
        photo = make_circular_headshot()
        photo_size = 30
        photo_x = (self.SIDEBAR_W - photo_size) / 2
        self.image(photo, photo_x, 8, photo_size, photo_size)

        # Accent ring around photo area
        self._draw_color(self.accent)
        self.set_line_width(0.8)
        self.ellipse(photo_x - 1, 7, photo_size + 2, photo_size + 2, "D")
        self.set_line_width(0.2)

        # Name in sidebar
        self.set_xy(3, 41)
        self.set_font("Helvetica", "B", 11)
        self._text_color(WHITE)
        self.cell(self.SIDEBAR_W - 6, 6, P["name"], align="C")

        # Title line(s) in sidebar
        self.set_xy(3, 48)
        self.set_font("Helvetica", "", 6.5)
        self._text_color(self.accent)
        self.multi_cell(self.SIDEBAR_W - 6, 3.5, subtitle, align="C")

        y = self.get_y() + 3
        # Contact
        y = self._sidebar_contact(y)
        # Skills
        y = self._sidebar_skills(y, sidebar_skills)
        # Education
        y = self._sidebar_education(y)
        # Languages
        y = self._sidebar_languages(y)

        # ── Main content area (page 1) ──────────────────────────

        # Title bar at top of main area (gradient-like with two tones)
        main_bar_w = self.PAGE_W - self.SIDEBAR_W
        self._fill(self.accent)
        self.rect(self.SIDEBAR_W, 0, main_bar_w, 24, "F")
        # Subtle darker strip at bottom of title bar
        darker = tuple(max(0, c - 25) for c in self.accent)
        self._fill(darker)
        self.rect(self.SIDEBAR_W, 22, main_bar_w, 2, "F")

        # Name in title bar
        self.set_xy(self.MAIN_X, 4)
        self.set_font("Helvetica", "B", 17)
        self._text_color(WHITE)
        self.cell(self.MAIN_W, 8, P["name"], new_x="LMARGIN", new_y="NEXT")

        # Role title in title bar
        self.set_xy(self.MAIN_X, 13)
        self.set_font("Helvetica", "", 8)
        # Slightly transparent white effect
        self._text_color((230, 240, 255))
        self.cell(self.MAIN_W, 5, title)

        self.set_y(28)

        # Metrics cards
        self.main_metrics(metrics)

        # Summary
        self.main_summary(summary)

        # Key highlights
        self.main_highlights(highlights)

        # Experience (may flow to page 2)
        self.main_experience(experience)

        # Projects
        self.main_projects(projects)

        # Certifications
        self.main_certifications(certifications)

        # Articles
        if articles:
            self.main_articles(articles)

    def save(self, filename):
        path = os.path.join(OUTPUT_DIR, filename)
        self.output(path)
        print(f"  -> {filename}")


# ════════════════════════════════════════════════════════════════
# RESUME DATA — Each resume gets unique content tuning
# ════════════════════════════════════════════════════════════════

def build_ml_ai_resume():
    pdf = PremiumResume(
        accent=(124, 58, 237),        # purple
        accent_light=(237, 233, 254),
    )
    pdf.build(
        title="Cloud & AI Architect  |  ML/AI & Generative AI Specialist",
        subtitle="Machine Learning | GenAI | LLMOps\nMLOps | Vertex AI | SageMaker",
        summary=(
            "Cloud & AI Architect with 11+ years architecting production-grade ML/AI systems across AWS, GCP, and Azure. "
            "Currently leading Generative AI and LLM integration at Bosch Europe -- designing enterprise search, "
            "document intelligence, and Agentic AI automation platforms adopted across multiple business units. "
            "Deep hands-on expertise in Vertex AI, SageMaker, RAG architectures, prompt engineering, and MLOps "
            "pipeline design. Built open-source AI cost intelligence tools (TokenMeter) achieving 60% LLM spend "
            "reduction. Google-certified Professional Machine Learning Engineer and Generative AI Leader with "
            "a strong track record of translating ML research into production-ready enterprise systems."
        ),
        metrics=[
            ("11+", "Years Experience"),
            ("14+", "Certifications"),
            ("EUR 4M+", "Cloud Savings"),
            ("1,000+", "Containers Orchestrated"),
            ("60%", "AI Cost Reduction"),
        ],
        highlights=[
            "Architected LLM-powered enterprise search platform serving 15+ Bosch Europe business units using Vertex AI, RAG, and Agentic AI",
            "Designed end-to-end MLOps pipelines: training, evaluation, registry, deployment, monitoring with automated retraining and A/B testing",
            "Built TokenMeter (open-source) -- LLM cost intelligence tracking tokens across OpenAI, Anthropic, Google with smart routing saving 60%",
            "Deployed production ML serving on GKE, EKS, AKS with canary deployments, model versioning, and real-time inference at scale",
            "Created ShieldIaC -- AI-powered security scanner using GPT-4.1 for intelligent fix suggestions across 9 compliance frameworks",
        ],
        sidebar_skills={
            "AI / ML / GenAI": "Vertex AI, SageMaker, LLMs (GPT-4, Claude, Gemini), RAG, Prompt Engineering, Agentic AI, LangChain, Vector DBs",
            "MLOps & LLMOps": "Model Registry, Feature Store, ML Pipelines, A/B Testing, Model Monitoring, Data Drift Detection",
            "Data & Analytics": "BigQuery, Redshift, EMR, Spark, Enterprise Search, Data Pipelines, ETL",
            "Cloud": "GCP, AWS, Azure, Multi-Cloud Architecture",
            "Infrastructure": "Terraform, Kubernetes, Docker, CI/CD, GitOps",
            "Languages": "Python, Bash, SQL, YAML, HCL",
        },
        experience=[
            {
                "title": "Cloud & AI Architect",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Spearheaded GenAI adoption across Bosch Europe: integrated LLMs and Agentic AI into enterprise search, deploying on Vertex AI, BigQuery, and Cloud Run",
                    "Designed RAG-based document intelligence platform processing 500K+ documents with semantic search across 15+ business units",
                    "Established LLMOps framework: prompt versioning, evaluation pipelines, cost tracking, and guardrails for production deployments",
                    "Led strategic AI partnership between Google Cloud, AWS, and Bosch Poland -- defined AI/ML architecture standards",
                    "Implemented FinOps for AI/ML workloads, contributing to EUR 4M+ total cloud savings through GPU scheduling and preemptible instances",
                ],
            },
            {
                "title": "Senior DevOps Consultant (ML Platform)",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Deployed production ML serving on GKE and EKS with auto-scaling, canary deployments, and real-time inference",
                    "Built ML monitoring: performance tracking, data drift detection, and automated alerting with Prometheus and Grafana",
                    "Automated ML infrastructure with Terraform IaC, reducing deployment time from days to hours (50%+ improvement)",
                ],
            },
            {
                "title": "Senior DevOps Engineer / Data & AI Architect",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Built data & AI platforms on SageMaker, EMR, and Redshift for model training, batch inference, and Fortune 500 analytics",
                    "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS for distributed ML training",
                    "Reduced ML infrastructure costs by $45,000 through Spot Instance optimisation and GPU right-sizing",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Designed fault-tolerant AWS architectures (EC2, RDS, S3, VPC) supporting data ingestion pipelines and early ML workloads",
                    "Led cloud migration of 11,000+ server infrastructure, enabling data teams to adopt cloud-native ML and analytics tooling",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "Infrastructure operations, P1/P2 incident response, and root cause analysis for production enterprise systems",
                ],
            },
        ],
        projects=[
            {
                "name": "TokenMeter -- Cost Intelligence Layer for LLM Apps",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "One-line Python integration tracking cost, latency, and tokens across OpenAI, Anthropic, Google. Smart routing saves up to 60% on AI spend. <5ms overhead.",
                "techs": "Python, OpenAI API, Anthropic API, Google AI, Smart Routing, PyPI",
            },
            {
                "name": "ShieldIaC -- AI-Powered IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "100+ security rules, 9 compliance frameworks (CIS, SOC2, HIPAA, PCI-DSS, NIST). GPT-4.1 fix suggestions for Terraform and CloudFormation misconfigurations.",
                "techs": "Python, Terraform, CloudFormation, GPT-4.1, GitHub Actions",
            },
            {
                "name": "InfraCents -- Terraform Cost Estimates on Every PR",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "Open-source GitHub App posting real-time AWS+GCP cost estimates directly on pull requests. Zero configuration -- parses Terraform changes and queries live pricing APIs.",
                "techs": "Python, Next.js, Terraform, GitHub App, AWS/GCP Pricing APIs",
            },
        ],
        certifications=[
            "Google Professional Machine Learning Engineer (Valid Dec 2027)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "Google Associate Cloud Engineer (Aug 2023)",
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
            "HashiCorp Terraform Associate",
            "MCSA - Microsoft Certified Solutions Associate (Apr 2015)",
        ],
        articles=[
            {
                "title": '"Our AI Bill Was $4,800 Last Month -- Nobody Knew Why" | "How I Built an AI-Powered IaC Security Scanner"',
                "desc": "Published on Medium -- deep dives into LLM cost intelligence (TokenMeter) and AI-powered security scanning (ShieldIaC).",
                "link": "https://medium.com/@nirbhaysingh1",
            },
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_ML_AI_GenAI.pdf")


# ════════════════════════════════════════════════════════════════
# RESUME 2 — Cloud DevOps (Multi-Cloud)
# ════════════════════════════════════════════════════════════════

def build_cloud_devops_resume():
    pdf = PremiumResume(
        accent=(37, 99, 235),          # blue
        accent_light=(219, 234, 254),
    )
    pdf.build(
        title="Cloud & DevOps Architect  |  Multi-Cloud Platform Engineer",
        subtitle="Multi-Cloud | Kubernetes | Terraform\nCI/CD | GitOps | Platform Engineering",
        summary=(
            "Cloud & DevOps Architect with 11+ years designing, automating, and operating production infrastructure "
            "across AWS, GCP, and Azure simultaneously. Expert in Terraform IaC, Kubernetes multi-cluster management "
            "(EKS, GKE, AKS), and GitOps-driven deployment workflows. Proven record of reducing deployment time by "
            "50%+, accelerating CI/CD pipelines by 30x, and orchestrating 1,000+ container workloads. Delivered "
            "EUR 4M+ in cloud cost savings through FinOps governance at Bosch Europe. Currently architecting "
            "multi-cloud strategy and platform engineering for one of Europe's largest industrial conglomerates."
        ),
        metrics=[
            ("11+", "Years Experience"),
            ("50%+", "Faster Deploys"),
            ("30x", "CI/CD Speedup"),
            ("EUR 4M+", "Cloud Savings"),
            ("14+", "Certifications"),
        ],
        highlights=[
            "Architected multi-cloud platform strategy across GCP and AWS for Bosch Europe -- unified governance, networking, and security across 15+ business units",
            "Automated infrastructure with Terraform IaC (1,500+ resources), achieving 50%+ reduction in deployment time and near-zero configuration drift",
            "Accelerated CI/CD pipeline speed by 30x at Deloitte through parallel execution, caching strategies, and pipeline-as-code architecture redesign",
            "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS with automated scaling, health monitoring, and self-healing",
            "Deployed and managed production Kubernetes clusters across GKE, EKS, AKS, and ECS simultaneously with GitOps (ArgoCD) workflows",
            "Implemented FinOps governance delivering EUR 4M+ in savings through tagging strategies, right-sizing, and reserved capacity planning",
        ],
        sidebar_skills={
            "Cloud Platforms": "AWS, GCP, Azure, VMware, Multi-Cloud Architecture, Landing Zones",
            "IaC & Config": "Terraform (expert), CloudFormation, Ansible, Puppet, HCL, Policy-as-Code",
            "Containers": "Kubernetes (EKS, GKE, AKS), Docker, Helm, Anthos, ECS, Istio",
            "CI/CD & GitOps": "GitHub Actions, Jenkins, ArgoCD, Flux, GitOps, Spinnaker",
            "Observability": "Prometheus, Grafana, ELK Stack, Datadog, CloudWatch",
            "Security": "IAM, Zero-Trust, OPA/Gatekeeper, Secret Mgmt, Compliance",
            "Languages": "Python, Bash, YAML, JSON, HCL, PowerShell, Go",
        },
        experience=[
            {
                "title": "Cloud & AI Architect",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Architected multi-cloud infrastructure strategy across GCP and AWS for Bosch Europe business units -- defined landing zones, networking, identity, and governance",
                    "Led strategic partnership between Google Cloud, AWS, and Bosch Poland -- unified cloud tooling, established architecture review boards, and standardised deployment patterns",
                    "Designed GKE and Cloud Run microservices platforms for enterprise AI workloads with autoscaling, service mesh, and zero-trust security",
                    "Implemented FinOps at enterprise scale, delivering EUR 4M+ in savings through optimisation, tagging governance, and cost-aware architecture reviews",
                    "Mentored 20+ senior developers and architects on multi-cloud strategy, IaC best practices, and Kubernetes operations across global teams",
                ],
            },
            {
                "title": "Senior DevOps Consultant",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Automated infrastructure provisioning with Terraform IaC across AWS, GCP, and Azure -- 50%+ reduction in deployment time, near-zero drift",
                    "Deployed and managed production container platforms across GKE, EKS, AKS, and ECS with GitOps workflows and automated rollbacks",
                    "Built comprehensive observability stack: Prometheus, Grafana, and ELK for metrics, logging, alerting, and distributed tracing",
                    "Developed Python and Bash automation for infrastructure lifecycle management, secret rotation, and compliance scanning",
                ],
            },
            {
                "title": "Senior DevOps Engineer",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Reduced AWS costs by $45,000 and accelerated CI/CD pipeline speed by 30x through architecture redesign, caching, and parallel execution",
                    "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS for distributed batch processing and analytics",
                    "Implemented multi-cloud security controls and networking spanning GCP, AWS, Azure, and OCI with unified IAM and audit logging",
                    "Built data platform infrastructure on EMR, Redshift, and BigQuery with automated ETL pipelines and data governance",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Designed secure, fault-tolerant AWS architectures (EC2, RDS, S3, VPC) with multi-AZ deployments and automated failover",
                    "Built disaster recovery strategies for hybrid cloud and on-premise environments with RTO/RPO guarantees",
                    "Managed 11,000+ server Windows infrastructure with Active Directory, Group Policy, and operations automation",
                    "Led large-scale cloud migration planning and execution using PowerShell, Ansible, and custom migration tooling",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "Infrastructure operations, migrations, and P1/P2 incident response for enterprise production environments",
                ],
            },
        ],
        projects=[
            {
                "name": "ShieldIaC -- AI-Powered IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "Catches security misconfigurations in Terraform and CloudFormation before they reach production. 100+ rules, 9 compliance frameworks (CIS, SOC2, HIPAA, PCI-DSS, NIST), AI-powered fix suggestions via GPT-4.1.",
                "techs": "Python, Terraform, CloudFormation, GPT-4.1, GitHub Actions",
            },
            {
                "name": "InfraCents -- Terraform Cost Estimates on Every PR",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "GitHub App posting real-time AWS+GCP cost estimates on pull requests before merge. Zero config, automatic Terraform parsing, live pricing APIs.",
                "techs": "Python, Next.js, Terraform, GitHub App, AWS/GCP Pricing APIs",
            },
            {
                "name": "TokenMeter -- LLM Cost Intelligence Layer",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "Tracks token usage, cost, and latency across OpenAI, Anthropic, Google. Smart routing saves up to 60% on AI spend. <5ms overhead.",
                "techs": "Python, OpenAI, Anthropic, Google AI, Smart Routing, PyPI",
            },
        ],
        certifications=[
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "Google Associate Cloud Engineer (Aug 2023)",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
            "HashiCorp Terraform Associate",
            "Google Professional ML Engineer (Valid Dec 2027)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "MCSA - Microsoft Certified Solutions Associate (Apr 2015)",
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_Cloud_DevOps.pdf")


# ════════════════════════════════════════════════════════════════
# RESUME 3 — AWS DevOps
# ════════════════════════════════════════════════════════════════

def build_aws_devops_resume():
    pdf = PremiumResume(
        accent=(234, 126, 0),          # AWS orange
        accent_light=(255, 237, 213),
    )
    pdf.build(
        title="AWS DevOps Architect  |  AWS Solutions Architect - Professional",
        subtitle="AWS | EKS | Terraform | CI/CD\nCloudFormation | SageMaker | Cost Optimisation",
        summary=(
            "AWS-certified DevOps Architect (Solutions Architect Professional) with 11+ years designing, "
            "automating, and operating production-grade AWS infrastructure at enterprise scale. Deep expertise "
            "across the full AWS stack: EKS, EC2, RDS, S3, VPC, Batch, Spot Instances, SageMaker, Lambda, and "
            "CloudFormation. Proven record of reducing AWS costs by $45K+, accelerating CI/CD by 30x, orchestrating "
            "1,000+ containers on EKS, and migrating 11,000+ servers to AWS. Currently leading AWS architecture "
            "strategy at Bosch Europe with EUR 4M+ in documented cloud savings."
        ),
        metrics=[
            ("11+", "Years Experience"),
            ("$45K+", "AWS Cost Savings"),
            ("30x", "CI/CD Speedup"),
            ("11,000+", "Servers Migrated"),
            ("14+", "Certifications"),
        ],
        highlights=[
            "AWS Solutions Architect Professional certified with 8+ years of continuous AWS production experience across 4 enterprises",
            "Reduced AWS costs by $45,000 at Deloitte through Spot Instance strategies, Reserved Instances, right-sizing, and pipeline optimisation",
            "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS for distributed analytics and ML workloads",
            "Migrated 11,000+ server on-premise infrastructure to AWS with zero-downtime cutover and automated rollback strategies",
            "Designed fault-tolerant AWS architectures (multi-AZ, cross-region) with 99.99% uptime SLAs across production environments",
            "Built data & AI platforms on SageMaker, EMR, and Redshift serving Fortune 500 analytics workloads",
            "Created InfraCents (open-source): real-time AWS cost estimation on every Terraform pull request",
        ],
        sidebar_skills={
            "AWS Compute": "EC2, EKS, ECS, Lambda, Batch, Spot Instances, ASG, Fargate",
            "AWS Storage & DB": "S3, RDS, Redshift, DynamoDB, EBS, EFS, Glacier, ElastiCache",
            "AWS Networking": "VPC, Route53, CloudFront, ALB/NLB, Transit GW, Direct Connect, PrivateLink",
            "AWS AI/ML & Data": "SageMaker, EMR, Glue, Athena, Kinesis, Redshift, Lake Formation",
            "AWS Security": "IAM, KMS, CloudTrail, GuardDuty, Security Hub, Config, Organizations, SCPs",
            "IaC & CI/CD": "Terraform, CloudFormation, CDK, GitHub Actions, Jenkins, CodePipeline, ArgoCD",
            "Containers": "EKS, ECR, ECS Fargate, Docker, Helm",
            "Observability": "CloudWatch, X-Ray, Prometheus, Grafana, ELK",
            "Languages": "Python, Bash, YAML, JSON, HCL, PowerShell",
        },
        experience=[
            {
                "title": "Cloud & AI Architect (AWS Lead)",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Led strategic AWS partnership for Bosch Poland -- defined AWS architecture standards, landing zone design, and multi-account governance using AWS Organizations and SCPs",
                    "Designed AWS-native AI/ML infrastructure: SageMaker pipelines, EKS model serving, S3 data lake, and Glue ETL for enterprise workloads",
                    "Implemented FinOps governance for 50+ AWS accounts, contributing to EUR 4M+ total savings through Savings Plans, right-sizing, and automated cleanup",
                    "Established AWS Well-Architected reviews as standard practice -- mentored architects on security, reliability, and cost optimisation pillars",
                ],
            },
            {
                "title": "Senior DevOps Consultant",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Automated AWS infrastructure with Terraform (300+ resources), achieving 50%+ reduction in deployment time with near-zero configuration drift",
                    "Deployed and operated production EKS and ECS clusters with auto-scaling, spot integration, and GitOps-driven deployments via ArgoCD",
                    "Built AWS observability: CloudWatch dashboards, custom metrics, Prometheus, and Grafana for real-time infrastructure and application monitoring",
                    "Implemented AWS security best practices: IAM least-privilege, KMS encryption, VPC flow logs, and automated compliance scanning",
                ],
            },
            {
                "title": "Senior DevOps Engineer / Data & AI Architect",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Reduced AWS costs by $45,000 through Spot Instance fleet management, Reserved Instances, Savings Plans, and workload right-sizing",
                    "Accelerated CI/CD pipeline speed by 30x through CodePipeline architecture redesign, parallel stages, and artefact caching",
                    "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS for distributed data processing and ML training",
                    "Built data & AI platforms on EMR, Redshift, and SageMaker -- serving analytics and model training for Fortune 500 clients",
                    "Implemented AWS security controls: IAM policies, KMS encryption, CloudTrail auditing, GuardDuty threat detection, and Config rules",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Designed secure, fault-tolerant AWS architectures (EC2, RDS Multi-AZ, S3, VPC) for production SaaS workloads",
                    "Led migration of 11,000+ server on-premise infrastructure to AWS -- zero-downtime cutover with automated rollback",
                    "Built disaster recovery with cross-region replication, automated failover, and RTO/RPO validation testing",
                    "Managed AWS networking: VPC design, subnets, security groups, NACLs, Transit Gateway for multi-tier applications",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "Infrastructure operations, P1/P2 incident response, and root cause analysis for enterprise production environments",
                ],
            },
        ],
        projects=[
            {
                "name": "InfraCents -- AWS Cost Estimates on Every Terraform PR",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "GitHub App posting real-time AWS cost estimates on Terraform pull requests. Parses TF changes, queries live AWS Pricing API. Zero config, native PR integration.",
                "techs": "Python, Next.js, Terraform, GitHub App, AWS Pricing API",
            },
            {
                "name": "ShieldIaC -- AI-Powered IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "Scans Terraform/CloudFormation for AWS security misconfigs pre-production. 100+ rules, 9 compliance frameworks (CIS AWS Benchmark, SOC2, HIPAA, PCI-DSS), GPT-4.1 fix suggestions.",
                "techs": "Python, Terraform, CloudFormation, GPT-4.1, GitHub Actions",
            },
            {
                "name": "TokenMeter -- LLM Cost Intelligence",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "Tracks token cost and latency across LLM providers. Smart routing saves up to 60% on AI spend with <5ms overhead.",
                "techs": "Python, OpenAI, Anthropic, Google AI, Smart Routing, PyPI",
            },
        ],
        certifications=[
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
            "HashiCorp Terraform Associate",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "Google Professional ML Engineer (Valid Dec 2027)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "Google Associate Cloud Engineer (Aug 2023)",
            "MCSA - Microsoft Certified Solutions Associate (Apr 2015)",
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_AWS_DevOps.pdf")


# ════════════════════════════════════════════════════════════════
# RESUME 4 — GCP DevOps
# ════════════════════════════════════════════════════════════════

def build_gcp_devops_resume():
    pdf = PremiumResume(
        accent=(66, 133, 244),         # Google blue
        accent_light=(219, 234, 254),
    )
    pdf.build(
        title="GCP Cloud Architect & DevOps Engineer  |  5x Google Cloud Certified",
        subtitle="GCP | GKE | Vertex AI | BigQuery\nCloud Build | Anthos | Terraform",
        summary=(
            "5x Google Cloud certified Cloud & DevOps Architect with 11+ years of production experience. "
            "Deep expertise in GKE, Vertex AI, BigQuery, Cloud Run, Cloud Build, and Anthos for enterprise-scale "
            "platform engineering. Currently leading the strategic Google Cloud partnership at Bosch Europe -- "
            "designing GKE platforms, Vertex AI pipelines, and BigQuery analytics adopted across 15+ business units. "
            "Proven ability to architect scalable, secure GCP infrastructure with FinOps governance, delivering "
            "EUR 4M+ in documented cloud savings."
        ),
        metrics=[
            ("5x", "GCP Certified"),
            ("11+", "Years Experience"),
            ("EUR 4M+", "Cloud Savings"),
            ("15+", "Business Units"),
            ("14+", "Total Certs"),
        ],
        highlights=[
            "5x Google Cloud Certified: Professional ML Engineer, Cloud DevOps Engineer, Cloud Architect, Generative AI Leader, Associate Cloud Engineer",
            "Leading strategic Google Cloud partnership for Bosch Poland -- GCP architecture standards, governance, and platform engineering",
            "Designed Vertex AI and GKE-based ML/AI platforms adopted across 15+ Bosch Europe business units for enterprise search and automation",
            "Architected production GKE clusters with Anthos service mesh, Binary Authorization, and Workload Identity for zero-trust security",
            "Built BigQuery analytics pipelines processing petabyte-scale enterprise data with optimised partitioning and materialised views",
            "Deployed Cloud Run microservices for serverless AI inference with auto-scaling, traffic splitting, and canary deployments",
            "Implemented GCP FinOps: committed use discounts, preemptible VMs, BigQuery slot reservations, contributing to EUR 4M+ savings",
        ],
        sidebar_skills={
            "GCP Compute": "GKE, Cloud Run, Compute Engine, Cloud Functions, App Engine, Anthos",
            "GCP AI/ML": "Vertex AI, AutoML, GenAI Studio, BigQuery ML, AI Platform Pipelines",
            "GCP Data": "BigQuery, Cloud Storage, Dataflow, Dataproc, Pub/Sub, Cloud SQL, Firestore",
            "GCP Security": "IAM, Cloud KMS, SCC, Binary Auth, VPC SC, Workload Identity",
            "GCP DevOps": "Cloud Build, Cloud Deploy, Artifact Registry, Config Connector",
            "GCP Networking": "VPC, CLB, Cloud CDN, Cloud DNS, Interconnect, Private Google Access",
            "IaC & CI/CD": "Terraform (GCP), GitHub Actions, Jenkins, ArgoCD, GitOps, Flux",
            "Observability": "Cloud Monitoring, Cloud Logging, Cloud Trace, Prometheus, Grafana",
        },
        experience=[
            {
                "title": "Cloud & AI Architect (GCP Lead)",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Led strategic Google Cloud partnership for Bosch Poland -- defined GCP landing zones, architecture standards, and governance policies",
                    "Designed Vertex AI and BigQuery-powered ML/AI solutions adopted across 15+ Bosch Europe business units for enterprise search and process automation",
                    "Architected production GKE platforms with Anthos service mesh, Workload Identity, Binary Authorization, and namespace-level multi-tenancy",
                    "Built BigQuery analytics pipelines with optimised partitioning, clustering, and materialised views for petabyte-scale data processing",
                    "Deployed Cloud Run microservices for serverless LLM inference with traffic splitting, auto-scaling, and canary rollouts",
                    "Implemented GCP FinOps governance: committed use discounts, preemptible VMs, slot reservations, contributing to EUR 4M+ total savings",
                    "Mentored teams on GCP Well-Architected Framework, GKE operations, Vertex AI best practices, and Cloud Build pipeline design",
                ],
            },
            {
                "title": "Senior DevOps Consultant",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Deployed and managed production GKE clusters with node auto-provisioning, pod auto-scaling, and automated security patching",
                    "Built CI/CD pipelines using Cloud Build and GitHub Actions for GKE deployments with automated testing and canary analysis",
                    "Automated GCP infrastructure with Terraform (GCP provider), achieving 50%+ reduction in deployment time",
                    "Implemented comprehensive observability with Cloud Monitoring, Cloud Logging, Prometheus, and Grafana dashboards",
                ],
            },
            {
                "title": "Senior DevOps Engineer / Data Architect",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Built BigQuery data platforms for enterprise analytics with automated ETL using Dataflow and Cloud Composer",
                    "Implemented multi-cloud security controls spanning GCP, AWS, Azure, and OCI with unified audit logging and IAM",
                    "Orchestrated containerised workloads across GKE and EKS for distributed data processing at scale",
                    "Accelerated CI/CD pipeline speed by 30x through Cloud Build optimisation, caching, and parallel execution",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Designed cloud architectures for production workloads -- established patterns later applied to GCP migrations",
                    "Built disaster recovery strategies with cross-region replication and automated failover testing",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "Infrastructure operations, P1/P2 incident response, and root cause analysis for enterprise production systems",
                ],
            },
        ],
        projects=[
            {
                "name": "InfraCents -- GCP Cost Estimates on Every Terraform PR",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "GitHub App posting real-time GCP cost estimates on Terraform pull requests. Queries live GCP Pricing API, parses Terraform changes automatically. Zero config.",
                "techs": "Python, Next.js, Terraform, GitHub App, GCP Pricing API",
            },
            {
                "name": "ShieldIaC -- AI-Powered IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "Scans Terraform for GCP security misconfigurations pre-production. 100+ rules across CIS GCP Benchmark, SOC2, HIPAA, PCI-DSS, NIST. GPT-4.1 fix suggestions.",
                "techs": "Python, Terraform, GPT-4.1, GitHub Actions",
            },
            {
                "name": "TokenMeter -- LLM Cost Intelligence (Google AI Support)",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "Tracks token cost across Google AI (Gemini), OpenAI, Anthropic. Smart routing matches tasks to optimal models, saving up to 60% on AI spend.",
                "techs": "Python, Google AI, OpenAI, Anthropic, Smart Routing, PyPI",
            },
        ],
        certifications=[
            "Google Professional Machine Learning Engineer (Valid Dec 2027)",
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "Google Associate Cloud Engineer (Aug 2023)",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
            "HashiCorp Terraform Associate",
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "MCSA - Microsoft Certified Solutions Associate (Apr 2015)",
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_GCP_DevOps.pdf")


# ════════════════════════════════════════════════════════════════
# RESUME 5 — FinOps
# ════════════════════════════════════════════════════════════════

def build_finops_resume():
    pdf = PremiumResume(
        accent=(5, 150, 105),          # green
        accent_light=(209, 250, 229),
    )
    pdf.build(
        title="FinOps & Cloud Cost Optimisation Architect  |  EUR 4M+ Documented Savings",
        subtitle="FinOps | Cloud Cost Governance\nSavings Plans | Right-Sizing | AI Cost Mgmt",
        summary=(
            "Cloud & FinOps Architect with 11+ years of experience and EUR 4M+ in documented cloud cost savings "
            "at Bosch Europe. Expert in FinOps governance, cloud cost optimisation across AWS, GCP, and Azure, "
            "and building open-source cost intelligence tools. Created TokenMeter (LLM cost tracker achieving 60% "
            "AI spend reduction) and InfraCents (Terraform cost estimation on every PR). Combines deep cloud "
            "architecture expertise with strategic cost governance -- helping organisations maximise cloud ROI "
            "through data-driven decisions, cultural change, and automated cost controls without sacrificing "
            "performance, security, or innovation velocity."
        ),
        metrics=[
            ("EUR 4M+", "Total Savings"),
            ("$45K", "AWS Savings (Deloitte)"),
            ("60%", "AI Cost Reduction"),
            ("50+", "Accounts Governed"),
            ("14+", "Certifications"),
        ],
        highlights=[
            "Delivered EUR 4M+ in documented cloud savings at Bosch Europe through FinOps governance, optimisation, and cost-aware architecture",
            "Reduced AWS costs by $45,000 at Deloitte through Spot Instance fleet management, Reserved Instances, workload right-sizing, and pipeline efficiency",
            "Built TokenMeter (open-source): LLM cost intelligence layer providing per-feature/per-team breakdowns with smart routing saving 60% on AI spend",
            "Built InfraCents (open-source): GitHub App posting real-time cloud cost estimates (AWS+GCP) on every Terraform PR before merge",
            "Established enterprise FinOps practice: chargeback/showback models, tagging strategies, budget automation, anomaly detection, and executive reporting",
            "Optimised AI/ML workload costs through GPU scheduling, preemptible instances, Spot Instance strategies, and model right-sizing",
            "Led FinOps culture transformation -- trained 50+ engineers on cost-conscious architecture and cloud spending accountability",
        ],
        sidebar_skills={
            "FinOps": "FinOps Framework, Cloud Cost Allocation, Chargeback/Showback, Unit Economics, Cloud Billing APIs",
            "Cost Optimisation": "Spot/Preemptible, Reserved/Committed, Savings Plans, Right-Sizing, Auto-Scaling, Resource Lifecycle",
            "Cloud Billing": "AWS (Cost Explorer, CUR, Budgets), GCP (Billing, BQ export), Azure (Cost Mgmt)",
            "Cost Tooling": "TokenMeter, InfraCents, Infracost, Kubecost, CloudHealth",
            "Infrastructure": "Terraform, Kubernetes, Docker, CI/CD, GitHub Actions, Jenkins",
            "Data & Dashboards": "BigQuery, Redshift, Grafana, Looker, Python, SQL",
            "Governance": "Tagging, Multi-Account, Budget Alerts, Policy-as-Code, OPA",
        },
        experience=[
            {
                "title": "Cloud & AI Architect (FinOps Lead)",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Implemented enterprise FinOps programme at Bosch Europe, delivering EUR 4M+ in documented savings through optimisation, governance, and cost-aware architecture",
                    "Established chargeback/showback models, tagging strategies, and automated budget alerts across 50+ AWS and GCP accounts serving 15+ business units",
                    "Built real-time cost dashboards and anomaly detection systems providing cloud spend visibility to engineering and executive stakeholders",
                    "Defined resource lifecycle policies, right-sizing cadence, and reserved/committed capacity purchasing strategies based on usage analysis",
                    "Led FinOps culture transformation: trained 50+ engineers on cost-conscious architecture, established cost reviews in architecture governance",
                    "Optimised AI/ML workload costs on Vertex AI and GKE through GPU scheduling, preemptible instances, and workload bin-packing strategies",
                ],
            },
            {
                "title": "Senior DevOps Consultant",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Automated infrastructure with Terraform IaC, eliminating resource waste from manual provisioning and reducing deployment overhead by 50%+",
                    "Implemented cost-aware container orchestration across GKE, EKS, and AKS with cluster auto-scaling, pod resource limits, and spot integration",
                    "Built monitoring dashboards correlating infrastructure costs with performance metrics for data-driven optimisation decisions",
                    "Identified and eliminated $100K+ in unused resources through automated cleanup scripts and resource lifecycle policies",
                ],
            },
            {
                "title": "Senior DevOps Engineer / Data & AI Architect",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Reduced AWS costs by $45,000 through Spot Instance fleet management, Reserved Instances, Savings Plans, and workload right-sizing",
                    "Orchestrated 1,000+ containers using AWS Batch with Spot Instances -- maximised cost efficiency for distributed batch processing at 70% compute savings",
                    "Accelerated CI/CD pipeline speed by 30x, reducing build/test compute costs and improving developer productivity",
                    "Implemented cost monitoring, anomaly detection, and budget alerting for multi-cloud environments (AWS, GCP, Azure, OCI)",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Designed cost-optimised AWS architectures: Auto Scaling policies, Spot Instances for non-critical workloads, Reserved Instances for baseline",
                    "Managed 11,000+ server infrastructure -- identified and executed consolidation opportunities saving significant operational costs",
                    "Led cloud migration planning with detailed TCO analysis, cost projection models, and ROI justification for executive stakeholders",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "Infrastructure operations and capacity planning for production environments -- early exposure to cost/capacity optimisation",
                ],
            },
        ],
        projects=[
            {
                "name": "TokenMeter -- Cost Intelligence Layer for LLM Apps",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "One-line integration tracking every token, cost, and latency across OpenAI, Anthropic, Google. Per-feature and per-team breakdowns. Smart routing saves up to 60% by matching task complexity to model capability. <5ms overhead.",
                "techs": "Python, OpenAI API, Anthropic API, Google AI, Smart Routing, PyPI",
            },
            {
                "name": "InfraCents -- Terraform Cost Estimates on Every PR",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "GitHub App posting real-time AWS+GCP cost estimates on Terraform PRs before merge. Engineers see exact cost impact of infrastructure changes. Zero config, live pricing APIs.",
                "techs": "Python, Next.js, Terraform, GitHub App, AWS/GCP Pricing APIs",
            },
            {
                "name": "ShieldIaC -- AI-Powered IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "Prevents costly security incidents by catching IaC misconfigs pre-production. 100+ rules, 9 compliance frameworks, AI fix suggestions.",
                "techs": "Python, Terraform, CloudFormation, GPT-4.1, GitHub Actions",
            },
        ],
        certifications=[
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "Google Professional ML Engineer (Valid Dec 2027)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "HashiCorp Terraform Associate",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
        ],
        articles=[
            {
                "title": '"Our AI Bill Was $4,800 Last Month -- Nobody Knew Why"',
                "desc": "How engineering teams can reclaim control of LLM spend: per-feature cost breakdowns, smart model routing, and the story behind building TokenMeter.",
                "link": "https://medium.com/@nirbhaysingh1",
            },
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_FinOps.pdf")


# ════════════════════════════════════════════════════════════════
# RESUME 6 — SRE
# ════════════════════════════════════════════════════════════════

def build_sre_resume():
    pdf = PremiumResume(
        accent=(220, 38, 38),          # red
        accent_light=(254, 226, 226),
    )
    pdf.build(
        title="Site Reliability Engineer  |  Cloud Infrastructure & Observability Architect",
        subtitle="SRE | Observability | Kubernetes\nIncident Response | Disaster Recovery",
        summary=(
            "Site Reliability Engineer and Cloud Architect with 11+ years ensuring production reliability across "
            "AWS, GCP, and Azure. Expert in observability (Prometheus, Grafana, ELK), Kubernetes operations "
            "(EKS, GKE, AKS), SLO/SLI-driven engineering, incident response, and disaster recovery. Managed "
            "infrastructure serving 11,000+ endpoints at PTC, orchestrated 1,000+ containers at Deloitte, and "
            "currently architects multi-cloud platforms at Bosch Europe. Builds open-source tools for proactive "
            "reliability: security scanning (ShieldIaC) and cost anomaly detection (InfraCents, TokenMeter)."
        ),
        metrics=[
            ("11+", "Years Experience"),
            ("11,000+", "Servers Managed"),
            ("1,000+", "Containers"),
            ("99.99%", "Uptime Target"),
            ("14+", "Certifications"),
        ],
        highlights=[
            "11+ years ensuring production reliability across AWS, GCP, and Azure in enterprise environments (Bosch, McAfee, Deloitte, PTC, IBM)",
            "Built comprehensive observability stacks: Prometheus, Grafana, ELK, CloudWatch -- unified metrics, logging, alerting, and distributed tracing",
            "Managed production Kubernetes clusters (EKS, GKE, AKS) -- orchestrated 1,000+ containers with automated scaling, health monitoring, and self-healing",
            "Designed disaster recovery strategies with cross-region replication, automated failover, and validated RTO/RPO testing",
            "Managed 11,000+ server infrastructure at PTC with Active Directory, high availability, and automated failover -- 99.99% uptime SLA",
            "P1/P2 incident response leadership across entire career: escalation management, root cause analysis, blameless post-mortems",
            "Built ShieldIaC (open-source): proactive IaC security scanning preventing production incidents at the infrastructure-as-code layer",
        ],
        sidebar_skills={
            "Observability": "Prometheus, Grafana, ELK Stack, CloudWatch, Cloud Monitoring, X-Ray, Datadog",
            "SRE Practices": "SLO/SLI/Error Budgets, Incident Response, Post-Mortems, Capacity Planning, Chaos Engineering, Toil Reduction",
            "Kubernetes": "EKS, GKE, AKS, Docker, Helm, Anthos, Istio Service Mesh",
            "Cloud Platforms": "AWS, GCP, Azure, Multi-Cloud, Landing Zones",
            "IaC & Automation": "Terraform, CloudFormation, Ansible, Puppet, Python, Bash, PowerShell",
            "CI/CD & Deploys": "GitHub Actions, Jenkins, ArgoCD, Canary, Blue-Green, Rolling",
            "DR & HA": "Cross-Region Replication, Automated Failover, RTO/RPO, Backup, Multi-AZ",
            "Security": "IAM, Zero-Trust, ShieldIaC, OPA/Gatekeeper, Compliance",
        },
        experience=[
            {
                "title": "Cloud & AI Architect (Platform Reliability)",
                "company": "Robert Bosch (Bosch Polska)",
                "duration": "Dec 2022 - Present",
                "location": "Warsaw, Poland",
                "bullets": [
                    "Architected reliable multi-cloud platforms on GCP and AWS for Bosch Europe with 99.99% uptime targets and automated incident detection",
                    "Designed GKE and Cloud Run platforms with pod disruption budgets, autoscaling, health probes, liveness checks, and automated rollback",
                    "Established observability standards: structured logging, distributed tracing (Cloud Trace), SLO-based alerting, and error budget tracking",
                    "Implemented proactive reliability: FinOps anomaly detection, security scanning (ShieldIaC), and infrastructure drift monitoring",
                    "Mentored 20+ engineers on SRE best practices, incident response processes, blameless post-mortems, and reliability culture",
                    "Defined SLO/SLI framework for platform services -- error budget-driven release management and change velocity governance",
                ],
            },
            {
                "title": "Senior DevOps Consultant (Platform Reliability)",
                "company": "McAfee",
                "duration": "Jun 2021 - Nov 2022",
                "location": "",
                "bullets": [
                    "Built production observability stack: Prometheus metrics, Grafana dashboards, ELK logging, custom alerting rules, and on-call runbooks",
                    "Deployed and operated production Kubernetes clusters across GKE, EKS, AKS, and ECS with automated node patching and security updates",
                    "Automated infrastructure with Terraform, reducing manual toil by 50%+ and eliminating configuration drift as a reliability risk",
                    "Developed incident response runbooks, automated remediation scripts, and escalation procedures for common failure modes",
                ],
            },
            {
                "title": "Senior DevOps Engineer",
                "company": "Deloitte",
                "duration": "Dec 2018 - Jun 2021",
                "location": "",
                "bullets": [
                    "Orchestrated 1,000+ containers using AWS Batch, Spot Instances, and EKS with automated health monitoring, restart policies, and graceful degradation",
                    "Accelerated CI/CD pipeline speed by 30x while implementing reliability gates: automated testing, security scanning, and canary analysis",
                    "Implemented multi-cloud security controls and monitoring spanning GCP, AWS, Azure, and OCI with centralised audit logging",
                    "Reduced AWS infrastructure costs by $45,000 while maintaining SLO compliance through smart resource optimisation",
                ],
            },
            {
                "title": "Senior Cloud Infrastructure Engineer",
                "company": "PTC",
                "duration": "Nov 2015 - Dec 2018",
                "location": "",
                "bullets": [
                    "Managed 11,000+ server Windows infrastructure with Active Directory, high availability clustering, and 99.99% uptime SLA",
                    "Designed disaster recovery: cross-region replication, automated failover, backup validation, and regular DR testing with documented RTO/RPO",
                    "Built fault-tolerant AWS architectures (EC2, RDS Multi-AZ, S3, VPC) for production workloads with multi-AZ deployments",
                    "Led zero-downtime cloud migrations with automated rollback strategies, canary traffic shifting, and comprehensive smoke testing",
                    "Built operations automation using PowerShell and Ansible, reducing MTTR for common incidents by 60%+",
                ],
            },
            {
                "title": "System Engineer",
                "company": "IBM",
                "duration": "Mar 2013 - Jul 2014",
                "location": "",
                "bullets": [
                    "P1/P2 incident response, escalation management, and root cause analysis for enterprise production systems",
                    "Infrastructure operations, change management, and migration planning in high-availability environments",
                ],
            },
        ],
        projects=[
            {
                "name": "ShieldIaC -- Proactive IaC Security Scanner",
                "url": "github.com/nirbhays/shieldiac",
                "link": "https://github.com/nirbhays/shieldiac",
                "desc": "Prevents production security incidents at the IaC layer. Scans Terraform/CloudFormation for misconfigs. 100+ rules, 9 compliance frameworks (CIS, SOC2, HIPAA, PCI-DSS, NIST). GPT-4.1 fix suggestions.",
                "techs": "Python, Terraform, CloudFormation, GPT-4.1, GitHub Actions",
            },
            {
                "name": "InfraCents -- Infrastructure Cost Anomaly Prevention",
                "url": "github.com/nirbhays/infracents",
                "link": "https://github.com/nirbhays/infracents",
                "desc": "Prevents cost-related reliability issues by showing exact infrastructure cost impact of Terraform changes before merge. Catches unintended resource scaling.",
                "techs": "Python, Next.js, Terraform, GitHub App, AWS/GCP Pricing APIs",
            },
            {
                "name": "TokenMeter -- LLM Performance & Cost Monitoring",
                "url": "github.com/nirbhays/tokenmeter",
                "link": "https://github.com/nirbhays/tokenmeter",
                "desc": "Monitors LLM latency, token usage, and costs across providers. Smart routing ensures performance SLOs while reducing spend by 60%. <5ms overhead.",
                "techs": "Python, OpenAI, Anthropic, Google AI, Smart Routing, PyPI",
            },
        ],
        certifications=[
            "Google Professional Cloud DevOps Engineer (Valid Dec 2027)",
            "CKAD - Certified Kubernetes Application Developer (Valid Sep 2026)",
            "Google Professional Cloud Architect (Valid Jun 2026)",
            "AWS Solutions Architect - Professional (Feb 2020)",
            "AWS Solutions Architect - Associate (Jan 2021)",
            "HashiCorp Terraform Associate",
            "Google Professional ML Engineer (Valid Dec 2027)",
            "Google Generative AI Leader (Valid Aug 2028)",
            "MCSA - Microsoft Certified Solutions Associate (Apr 2015)",
        ],
    )
    pdf.save("Nirbhay_Singh_Resume_SRE.pdf")


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating 6 premium resumes for Nirbhay Singh...\n")
    build_ml_ai_resume()
    build_cloud_devops_resume()
    build_aws_devops_resume()
    build_gcp_devops_resume()
    build_finops_resume()
    build_sre_resume()
    # Clean up temp file
    if os.path.exists(PHOTO_CIRCLE):
        os.remove(PHOTO_CIRCLE)
    print("\nAll 6 premium resumes generated successfully!")
