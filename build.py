#!/usr/bin/env python3
"""
Build script for B3 Commit AI Handbook
Generates bilingual HTML from markdown sources
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

try:
    import markdown
    from markdown.extensions import codehilite, fenced_code, tables, toc
except ImportError:
    print("Error: markdown library not found. Install with: pip install markdown")
    exit(1)


@dataclass
class Article:
    slug: str
    html: str
    category: str
    date: str
    title: Dict[str, str]
    subtitle: Dict[str, str]
    meta: Dict[str, str]
    sources: Dict[str, str]
    description: Dict[str, str]


def read_manifest() -> Tuple[List[Article], Dict]:
    """Read manifest.json and return articles and categories"""
    with open('articles/manifest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = [Article(**item) for item in data['articles']]
    categories = data['categories']
    return articles, categories


def read_markdown(path: str) -> str:
    """Read markdown file"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_h2_sections(md_content: str) -> List[Tuple[str, str, str]]:
    """Extract H2 sections from markdown. Returns list of (id, title, content) tuples"""
    sections = []
    lines = md_content.split('\n')
    current_section = []
    current_id = None
    current_title = None
    
    for line in lines:
        if line.startswith('## '):
            # Save previous section
            if current_id and current_title:
                sections.append((current_id, current_title, '\n'.join(current_section)))
            
            # Start new section
            title = line[3:].strip()
            # Create ID from title (lowercase, replace spaces with hyphens, remove special chars)
            current_id = re.sub(r'[^\w\s-]', '', title.lower())
            current_id = re.sub(r'[-\s]+', '-', current_id)
            current_title = title
            current_section = [line]
        elif current_id:
            current_section.append(line)
    
    # Add last section
    if current_id and current_title:
        sections.append((current_id, current_title, '\n'.join(current_section)))
    
    return sections


def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML"""
    md = markdown.Markdown(
        extensions=[
            'codehilite',
            'fenced_code',
            'tables',
            'toc',
            'nl2br',
            'sane_lists'
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': False
            }
        }
    )
    html = md.convert(md_content)
    return html


def generate_mobile_menu(articles: List[Article], categories: Dict) -> str:
    """Generate mobile menu HTML from manifest"""
    menu_items = []
    
    # Group articles by category
    articles_by_category = {}
    for article in articles:
        cat = article.category
        if cat not in articles_by_category:
            articles_by_category[cat] = []
        articles_by_category[cat].append(article)
    
    # Generate menu sections
    for cat_key, cat_info in categories.items():
        if cat_key in articles_by_category:
            menu_items.append(f'''        <div class="mobile-menu-section">
            <h3>
                <span class="lang-sv">{cat_info['sv']}</span>
                <span class="lang-en">{cat_info['en']}</span>
            </h3>
            <ul class="mobile-menu-links">''')
            
            for article in articles_by_category[cat_key]:
                menu_items.append(f'''                <li><a href="{article.html}">
                    <span class="lang-sv">{article.title['sv']}</span>
                    <span class="lang-en">{article.title['en']}</span>
                </a></li>''')
            
            menu_items.append('            </ul>\n        </div>')
    
    # Add links section
    menu_items.append('''        <div class="mobile-menu-section">
            <h3>
                <span class="lang-sv">Länkar</span>
                <span class="lang-en">Links</span>
            </h3>
            <ul class="mobile-menu-links">
                <li><a href="https://github.com/b3-commit" target="_blank">GitHub</a></li>
                <li>
                    <a href="#" id="menuThemeToggle">
                        <span id="menuThemeText">
                            <span class="lang-sv">Byt till mörkt läge</span>
                            <span class="lang-en">Switch to dark mode</span>
                        </span>
                    </a>
                </li>
                <li>
                    <a href="#" id="menuLangToggle">
                        <span id="menuLangText">
                            <span class="lang-sv">English</span>
                            <span class="lang-en">Svenska</span>
                        </span>
                    </a>
                </li>
            </ul>
        </div>''')
    
    return '\n'.join(menu_items)


def generate_article_html(article: Article, sv_content: str, en_content: str, all_articles: List[Article], categories: Dict) -> str:
    """Generate complete HTML for an article"""
    
    # Extract H2 sections from both languages (should match)
    sv_sections = extract_h2_sections(sv_content)
    en_sections = extract_h2_sections(en_content)
    
    if len(sv_sections) != len(en_sections):
        print(f"Warning: {article.slug} has mismatched H2 sections (SV: {len(sv_sections)}, EN: {len(en_sections)})")
    
    # Generate article navigation
    nav_items = []
    for i, (section_id, section_title, _) in enumerate(sv_sections):
        nav_items.append(f'<a href="#{section_id}" class="nav-pill">{section_title}</a>')
    
    nav_html = '\n                '.join(nav_items)
    
    # Generate presentation progress items
    progress_items = ['<div class="presentation-progress-item active" data-slide="0">\n            <div class="presentation-progress-dot"></div>\n            <span class="presentation-progress-label">Intro</span>\n        </div>']
    
    for i, (section_id, section_title, _) in enumerate(sv_sections, 1):
        progress_items.append(f'''<div class="presentation-progress-item" data-slide="{i}">
            <div class="presentation-progress-dot"></div>
            <span class="presentation-progress-label">{section_title}</span>
        </div>''')
    
    progress_html = '\n        '.join(progress_items)
    
    # Generate reading progress items (for reading mode, desktop only)
    reading_progress_items = []
    for i, (section_id, section_title, _) in enumerate(sv_sections):
        # Get English title for bilingual support
        en_title = en_sections[i][1] if i < len(en_sections) else section_title
        reading_progress_items.append(f'''<a href="#{section_id}" class="reading-progress-item" data-section="{section_id}">
            <div class="reading-progress-dot"></div>
            <span class="reading-progress-label">
                <span class="lang-sv">{section_title}</span>
                <span class="lang-en">{en_title}</span>
            </span>
        </a>''')
    
    reading_progress_html = '\n        '.join(reading_progress_items)
    
    # Convert markdown to HTML
    sv_html = markdown_to_html(sv_content)
    en_html = markdown_to_html(en_content)
    
    # Wrap bilingual content
    bilingual_content = f'''<div class="lang-sv">{sv_html}</div>
            <div class="lang-en">{en_html}</div>'''
    
    # Generate mobile menu
    mobile_menu = generate_mobile_menu(all_articles, categories)
    
    # Generate presentation slides
    total_slides = len(sv_sections) + 1
    slides = []
    
    # Hero slide
    slides.append(f'''    <section class="presentation-slide hero-slide" data-slide-number="1 / {total_slides}">
        <div class="presentation-slide-content">
            <p class="article-meta">
                <span class="lang-sv">{article.meta['sv']} // {article.date}</span>
                <span class="lang-en">{article.meta['en']} // {article.date}</span>
            </p>
            <h1>{article.title['en']}</h1>
            <p class="subtitle">
                <span class="lang-sv">{article.subtitle['sv']}</span>
                <span class="lang-en">{article.subtitle['en']}</span>
            </p>
        </div>
        <div class="presentation-scroll-hint">
            <span class="lang-sv">Scrolla ner</span>
            <span class="lang-en">Scroll down</span>
            <span>↓</span>
        </div>
    </section>''')
    
    # Content slides
    for slide_num, (section_id, section_title, section_content) in enumerate(sv_sections, 2):
        # Get corresponding English section
        if slide_num - 2 < len(en_sections):
            _, _, en_section_content = en_sections[slide_num - 2]
        else:
            en_section_content = section_content
        
        sv_slide_html = markdown_to_html(section_content)
        en_slide_html = markdown_to_html(en_section_content)
        
        slides.append(f'''    <section class="presentation-slide" data-slide-number="{slide_num} / {total_slides}">
        <div class="presentation-slide-content">
            <div class="lang-sv">{sv_slide_html}</div>
            <div class="lang-en">{en_slide_html}</div>
        </div>
    </section>''')
    
    slides_html = '\n\n'.join(slides)
    
    # Generate JavaScript
    js_code = generate_javascript()
    
    html = f'''<!DOCTYPE html>
<html lang="sv" data-lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.title['en']} - B3 Commit AI Handbook</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Progress Bar -->
    <div class="progress-bar" id="progressBar"></div>

    <!-- Presentation Progress Indicator -->
    <nav class="presentation-progress" id="presentationProgress">
        <div class="presentation-progress-track"></div>
        <div class="presentation-progress-fill" id="progressFill"></div>
        {progress_html}
    </nav>

    <!-- Reading Progress (vertical chapter nav for reading mode) -->
    <nav class="reading-progress" id="readingProgress">
        <div class="reading-progress-track"></div>
        <div class="reading-progress-fill" id="readingProgressFill"></div>
        {reading_progress_html}
    </nav>

    <!-- Menu Overlay -->
    <div class="menu-overlay" id="menuOverlay"></div>

    <!-- Mobile Menu -->
    <nav class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-header">
            <a href="index.html" class="logo">B3 Commit</a>
            <button class="mobile-menu-close" id="menuClose" aria-label="Stäng meny">&times;</button>
        </div>
        <!-- Mobile menu content would be generated from manifest -->
    </nav>

    <header>
        <nav class="nav-container">
            <div class="nav-left">
                <a href="index.html" class="logo">B3 Commit</a>
                <span class="breadcrumb">/ <a href="index.html"><span class="lang-sv">AI Handbook</span><span class="lang-en">AI Handbook</span></a> / <span class="lang-sv">{article.title['sv']}</span><span class="lang-en">{article.title['en']}</span></span>
            </div>
            <div class="nav-right">
                <button class="presentation-toggle" id="presentationToggle" aria-label="Presentation mode">
                    <span class="icon">📽️</span>
                    <span class="lang-sv">Presentation</span>
                    <span class="lang-en">Present</span>
                </button>
                <button class="lang-toggle" id="langToggle" aria-label="Byt språk">
                    <span class="flag lang-sv">🇸🇪</span>
                    <span class="flag lang-en">🇬🇧</span>
                    <span class="lang-sv">SV</span>
                    <span class="lang-en">EN</span>
                </button>
                <button class="theme-toggle" id="themeToggle" aria-label="Växla tema">
                    <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                </button>
                <button class="hamburger" id="hamburger" aria-label="Öppna meny">
                    <span class="hamburger-line"></span>
                    <span class="hamburger-line"></span>
                    <span class="hamburger-line"></span>
                </button>
            </div>
        </nav>
    </header>

    <main>
        <article>
            <header class="article-header" id="intro">
                <p class="article-meta">
                    <span class="lang-sv">{article.meta['sv']} // {article.date}</span>
                    <span class="lang-en">{article.meta['en']} // {article.date}</span>
                </p>
                <h1><span class="lang-sv">{article.title['sv']}</span><span class="lang-en">{article.title['en']}</span></h1>
                <p class="subtitle">
                    <span class="lang-sv">{article.subtitle['sv']}</span>
                    <span class="lang-en">{article.subtitle['en']}</span>
                </p>
            </header>

            <!-- Article Navigation -->
            <nav class="article-nav" id="articleNav">
                {nav_html}
            </nav>

            {bilingual_content}

        </article>
    </main>

    <!-- Presentation Slides -->
{slides_html}

    <footer>
        <div class="footer-content">
            <div class="footer-brand">
                <a href="index.html" class="logo">B3 Commit</a>
                <span class="status-badge">All Systems Operational</span>
            </div>
        </div>
    </footer>

    <script>
{js_code}
    </script>
</body>
</html>'''
    
    return html


def generate_javascript() -> str:
    """Generate complete JavaScript for article pages"""
    return '''        // Theme Toggle
        const themeToggle = document.getElementById('themeToggle');
        const menuThemeToggle = document.getElementById('menuThemeToggle');
        const html = document.documentElement;

        function setTheme(theme) {
            html.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        }

        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });

        if (menuThemeToggle) {
            menuThemeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                const currentTheme = html.getAttribute('data-theme');
                setTheme(currentTheme === 'dark' ? 'light' : 'dark');
            });
        }

        // Language Toggle
        const langToggle = document.getElementById('langToggle');
        const menuLangToggle = document.getElementById('menuLangToggle');

        function setLanguage(lang) {
            html.setAttribute('data-lang', lang);
            html.setAttribute('lang', lang);
            localStorage.setItem('language', lang);
        }

        const savedLang = localStorage.getItem('language') || 'sv';
        setLanguage(savedLang);

        langToggle.addEventListener('click', () => {
            const currentLang = html.getAttribute('data-lang');
            setLanguage(currentLang === 'sv' ? 'en' : 'sv');
        });

        if (menuLangToggle) {
            menuLangToggle.addEventListener('click', (e) => {
                e.preventDefault();
                const currentLang = html.getAttribute('data-lang');
                setLanguage(currentLang === 'sv' ? 'en' : 'sv');
            });
        }

        // Hamburger Menu
        const hamburger = document.getElementById('hamburger');
        const mobileMenu = document.getElementById('mobileMenu');
        const menuOverlay = document.getElementById('menuOverlay');
        const menuClose = document.getElementById('menuClose');

        function openMenu() {
            hamburger.classList.add('active');
            mobileMenu.classList.add('active');
            menuOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('active');
            menuOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        hamburger.addEventListener('click', () => {
            mobileMenu.classList.contains('active') ? closeMenu() : openMenu();
        });

        if (menuOverlay) menuOverlay.addEventListener('click', closeMenu);
        if (menuClose) menuClose.addEventListener('click', closeMenu);

        // Progress Bar
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            const progressBar = document.getElementById('progressBar');
            if (progressBar) progressBar.style.width = scrolled + '%';
        });

        // Presentation Mode
        const presentationToggle = document.getElementById('presentationToggle');
        const presentationProgress = document.getElementById('presentationProgress');
        const progressFill = document.getElementById('progressFill');
        const slides = document.querySelectorAll('.presentation-slide');
        const progressItems = document.querySelectorAll('.presentation-progress-item');

        function setPresentationMode(enabled) {
            html.setAttribute('data-presentation', enabled ? 'true' : 'false');
            localStorage.setItem('presentation', enabled ? 'true' : 'false');
            if (presentationToggle) {
                presentationToggle.classList.toggle('active', enabled);
            }
        }

        // Always start with presentation mode OFF (user must click to enable)
        setPresentationMode(false);

        if (presentationToggle) {
            presentationToggle.addEventListener('click', () => {
                const current = html.getAttribute('data-presentation') === 'true';
                setPresentationMode(!current);
                if (!current) {
                    // Scroll to first slide when enabling
                    slides[0]?.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }

        // Presentation Progress Tracking
        function updatePresentationProgress() {
            if (html.getAttribute('data-presentation') !== 'true') return;

            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            let currentSlide = 0;

            slides.forEach((slide, index) => {
                const slideTop = slide.offsetTop;
                const slideBottom = slideTop + slide.offsetHeight;
                if (scrollTop + windowHeight / 2 >= slideTop && scrollTop + windowHeight / 2 < slideBottom) {
                    currentSlide = index;
                }
            });

            // Update progress items
            progressItems.forEach((item, index) => {
                item.classList.toggle('active', index === currentSlide);
                item.classList.toggle('passed', index < currentSlide);
            });

            // Update progress fill
            if (progressFill && slides.length > 0) {
                const progress = ((currentSlide + 1) / slides.length) * 100;
                progressFill.style.height = progress + '%';
            }
        }

        window.addEventListener('scroll', updatePresentationProgress);
        updatePresentationProgress();

        // Keyboard Navigation for Presentation Mode
        // Note: We query slides fresh each time to include dynamically created continuation slides
        document.addEventListener('keydown', (e) => {
            if (html.getAttribute('data-presentation') !== 'true') return;

            // Query slides fresh to include any dynamically created continuation slides
            const allSlides = document.querySelectorAll('.presentation-slide');
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            let currentSlideIndex = 0;

            allSlides.forEach((slide, index) => {
                const slideTop = slide.offsetTop;
                if (currentScroll + windowHeight / 2 >= slideTop) {
                    currentSlideIndex = index;
                }
            });

            if (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') {
                e.preventDefault();
                if (currentSlideIndex < allSlides.length - 1) {
                    allSlides[currentSlideIndex + 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
                e.preventDefault();
                if (currentSlideIndex > 0) {
                    allSlides[currentSlideIndex - 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } else if (e.key === 'Home') {
                e.preventDefault();
                allSlides[0].scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else if (e.key === 'End') {
                e.preventDefault();
                allSlides[allSlides.length - 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else if (e.key === 'Escape') {
                e.preventDefault();
                setPresentationMode(false);
            }
        });

        // Click on progress items to jump to slide
        progressItems.forEach((item, index) => {
            item.addEventListener('click', () => {
                if (slides[index]) {
                    slides[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // Auto-split overflowing slides into continuation slides
        let slidesSplit = false;
        
        function splitOverflowingSlides() {
            if (slidesSplit) return; // Only run once
            if (html.getAttribute('data-presentation') !== 'true') return;
            
            const maxContentHeight = window.innerHeight - 220; // Account for padding (6rem top + 4rem bottom + buffer)
            const allSlides = Array.from(document.querySelectorAll('.presentation-slide:not(.continuation-slide)'));
            let continuationSlides = [];
            
            allSlides.forEach((slide, originalIndex) => {
                const content = slide.querySelector('.presentation-slide-content');
                if (!content || slide.classList.contains('hero-slide')) return;
                
                // Force layout calculation
                const svDiv = content.querySelector('.lang-sv');
                const enDiv = content.querySelector('.lang-en');
                if (!svDiv || !enDiv) return;
                
                // Check both language versions for overflow
                const svOverflows = svDiv.scrollHeight > maxContentHeight;
                const enOverflows = enDiv.scrollHeight > maxContentHeight;
                
                if (!svOverflows && !enOverflows) return;
                
                // This slide needs splitting
                slide.classList.add('has-continuation');
                
                // Get splittable elements (skip H2 headers)
                const svElements = Array.from(svDiv.children).filter(el => el.tagName !== 'H2');
                const enElements = Array.from(enDiv.children).filter(el => el.tagName !== 'H2');
                
                if (svElements.length <= 1) return;
                
                // Find split point based on cumulative height
                let currentHeight = 0;
                let splitIndex = -1;
                
                // Include H2 height in initial calculation
                const svH2 = svDiv.querySelector('h2');
                if (svH2) currentHeight = svH2.offsetHeight + 40;
                
                for (let i = 0; i < svElements.length; i++) {
                    const el = svElements[i];
                    const style = window.getComputedStyle(el);
                    const marginTop = parseInt(style.marginTop) || 0;
                    const marginBottom = parseInt(style.marginBottom) || 0;
                    currentHeight += el.offsetHeight + marginTop + marginBottom;
                    
                    if (currentHeight > maxContentHeight && i > 0) {
                        splitIndex = i;
                        break;
                    }
                }
                
                if (splitIndex <= 0) return;
                
                // Create continuation slide
                const continuationSlide = document.createElement('section');
                continuationSlide.className = 'presentation-slide continuation-slide';
                continuationSlide.setAttribute('data-original-slide', originalIndex.toString());
                
                const continuationContent = document.createElement('div');
                continuationContent.className = 'presentation-slide-content';
                
                // Create language containers for continuation
                const svContinuation = document.createElement('div');
                svContinuation.className = 'lang-sv';
                const enContinuation = document.createElement('div');
                enContinuation.className = 'lang-en';
                
                // Add continuation label
                const svLabel = document.createElement('span');
                svLabel.className = 'continuation-label';
                svLabel.textContent = '(fortsättning)';
                svContinuation.appendChild(svLabel);
                
                const enLabel = document.createElement('span');
                enLabel.className = 'continuation-label';
                enLabel.textContent = '(continued)';
                enContinuation.appendChild(enLabel);
                
                // Move overflow elements to continuation slide
                for (let i = splitIndex; i < svElements.length; i++) {
                    svContinuation.appendChild(svElements[i].cloneNode(true));
                    svElements[i].remove();
                }
                
                const enSplitIndex = Math.min(splitIndex, enElements.length);
                for (let i = enSplitIndex; i < enElements.length; i++) {
                    enContinuation.appendChild(enElements[i].cloneNode(true));
                    enElements[i].remove();
                }
                
                continuationContent.appendChild(svContinuation);
                continuationContent.appendChild(enContinuation);
                continuationSlide.appendChild(continuationContent);
                
                // Insert continuation slide after original
                slide.insertAdjacentElement('afterend', continuationSlide);
                continuationSlides.push(continuationSlide);
            });
            
            // If we created continuation slides, update numbering
            if (continuationSlides.length > 0) {
                const allSlidesNow = document.querySelectorAll('.presentation-slide');
                const totalSlides = allSlidesNow.length;
                
                allSlidesNow.forEach((slide, index) => {
                    slide.setAttribute('data-slide-number', `${index + 1} / ${totalSlides}`);
                });
                
                slidesSplit = true;
                
                // Recursively check if continuation slides also need splitting
                setTimeout(splitOverflowingSlides, 50);
            } else {
                slidesSplit = true;
            }
        }
        
        // Run split check when presentation mode is toggled
        const originalSetPresentationMode = setPresentationMode;
        setPresentationMode = function(enabled) {
            originalSetPresentationMode(enabled);
            if (enabled && !slidesSplit) {
                // Delay to allow rendering
                requestAnimationFrame(() => {
                    setTimeout(splitOverflowingSlides, 50);
                });
            }
        };

        // Reading Progress (vertical chapter navigation for reading mode)
        const readingProgressItems = document.querySelectorAll('.reading-progress-item');
        const readingProgressFill = document.getElementById('readingProgressFill');
        
        function updateReadingProgress() {
            // Don't update in presentation mode
            if (html.getAttribute('data-presentation') === 'true') return;
            
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const currentLang = html.getAttribute('data-lang') || 'sv';
            
            // Find H2 sections only from the active language
            const sections = document.querySelectorAll(`article .lang-${currentLang} h2[id]`);
            let currentIndex = -1;
            
            sections.forEach((section, index) => {
                const sectionTop = section.offsetTop - 150; // Offset for header
                if (scrollTop >= sectionTop) {
                    currentIndex = index;
                }
            });
            
            // Update reading progress items
            readingProgressItems.forEach((item, index) => {
                item.classList.remove('active', 'passed');
                if (index === currentIndex) {
                    item.classList.add('active');
                } else if (index < currentIndex) {
                    item.classList.add('passed');
                }
            });
            
            // Update progress fill
            if (readingProgressFill && sections.length > 0) {
                const progress = ((currentIndex + 1) / sections.length) * 100;
                readingProgressFill.style.height = Math.max(0, progress) + '%';
            }
        }
        
        // Listen for scroll events
        window.addEventListener('scroll', updateReadingProgress);
        
        // Initial update
        updateReadingProgress();
        
'''


def main():
    """Main build function"""
    print("Building B3 Commit AI Handbook...")
    
    articles, categories = read_manifest()
    
    # Build each article
    for article in articles:
        print(f"Building {article.slug}...")
        
        # Read markdown sources
        sv_path = article.sources['sv']
        en_path = article.sources['en']
        
        if not os.path.exists(sv_path):
            print(f"Warning: {sv_path} not found, skipping...")
            continue
        if not os.path.exists(en_path):
            print(f"Warning: {en_path} not found, skipping...")
            continue
        
        sv_content = read_markdown(sv_path)
        en_content = read_markdown(en_path)
        
        # Generate HTML
        html = generate_article_html(article, sv_content, en_content, articles, categories)
        
        # Write HTML file
        output_path = article.html
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  [OK] Generated {output_path}")
    
    print("\nBuild complete!")


if __name__ == '__main__':
    main()
