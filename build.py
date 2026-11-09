#!/usr/bin/env python3
"""Generador de sitio estático. Solo biblioteca estándar de Python 3.10+."""
from __future__ import annotations
import json
import html
from pathlib import Path
from datetime import date
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content' / 'site.json').read_text(encoding='utf-8'))
SECTIONS = DATA['sections']
ALL = [(s, p) for s in SECTIONS for p in s['items']]
E = lambda s: html.escape(str(s), quote=True)

# Publicación sin rutas absolutas; compatible con usuario.github.io/nombre-repositorio/
def root_prefix(depth: int) -> str:
    return '../' * depth if depth else './'


def nav_markup(depth: int, active: str = '') -> str:
    pre = root_prefix(depth)
    sections = []
    for section in SECTIONS:
        dropdown = ''.join(f'<li><a href="{pre}{E(section["slug"])}/{E(p["slug"])}/">{E(p["title"])}</a></li>' for p in section['items'])
        is_current = active == section['slug']
        sections.append(f'''<div class="nav-group {'is-current' if is_current else ''}">
          <button class="nav-trigger" type="button" aria-expanded="false" aria-haspopup="true">{E(section['label'])}<svg viewBox="0 0 12 12" aria-hidden="true"><path d="m2.5 4.5 3.5 3.5 3.5-3.5"/></svg></button>
          <ul class="dropdown" aria-label="{E(section['label'])}">{dropdown}</ul>
        </div>''')
    return f'''<header class="site-header" id="top">
      <div class="topline"></div>
      <div class="header-inner container">
        <a class="brand" href="{pre}" aria-label="Visión Venezuela, volver al inicio">
          <span class="brand-symbol" aria-hidden="true"><span>V</span></span>
          <span class="brand-copy"><strong>VISIÓN <span>VENEZUELA</span></strong><small>UNA VISIÓN DE PAÍS</small></span>
        </a>
        <button class="menu-toggle" type="button" aria-label="Abrir menú de navegación" aria-controls="nav-menu" aria-expanded="false"><span></span><span></span><span></span></button>
        <nav class="main-nav" id="nav-menu" aria-label="Navegación principal">
          <a class="nav-link {'is-current' if active == 'inicio' else ''}" href="{pre}">Inicio</a>
          {''.join(sections)}
          <a class="nav-link {'is-current' if active == 'faq' else ''}" href="{pre}faq/">FAQ</a>
        </nav>
      </div>
    </header>'''


def footer(depth: int) -> str:
    pre = root_prefix(depth)
    return f'''<footer class="footer">
      <div class="container footer-top">
        <div class="footer-brand"><span class="footer-kicker">UNA VISIÓN DE PAÍS</span><strong>VISIÓN<br>VENEZUELA<span class="gold-dot">.</span></strong><p>Una plataforma pública para documentar y desarrollar propuestas de país.</p></div>
        <div class="footer-col"><h3>Explorar</h3><a href="{pre}gobierno/ideologia/">Principios</a><a href="{pre}leyes/constitucional/">Leyes</a><a href="{pre}proyectos/infraestructura/">Proyectos</a></div>
        <div class="footer-col"><h3>Documentos</h3><a href="{pre}objetivos/corto-plazo/">Hoja de ruta</a><a href="{pre}faq/">Preguntas frecuentes</a><a href="{pre}">Página principal</a></div>
        <div class="footer-col"><h3>Información</h3><p>Publicación independiente y en desarrollo.</p><p>Los materiales propuestos no son instrumentos jurídicos oficiales.</p></div>
      </div>
      <div class="container footer-bottom"><span>© {date.today().year} VISIÓN VENEZUELA · PROYECTO INDEPENDIENTE</span><a href="#top">VOLVER ARRIBA <span aria-hidden="true">↑</span></a></div>
    </footer>'''


def html_shell(title: str, desc: str, body: str, depth: int, active: str, extras: str='') -> str:
    pre = root_prefix(depth)
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0c2948">
  <meta name="description" content="{E(desc)}">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:type" content="website">
  <title>{E(title)} | Visión Venezuela</title>
  <link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{pre}assets/styles.css">
  <script src="{pre}assets/app.js" defer></script>
  {extras}
</head>
<body>
  <a href="#contenido" class="skip-link">Saltar al contenido</a>
  {nav_markup(depth, active)}
  <main id="contenido">{body}</main>
  {footer(depth)}
</body>
</html>
'''


def main_page():
    pre = './'
    first_pillars = [
        ('01', 'Gobierno', 'Arquitectura del Estado, ministerios y principios de organización pública.', 'gobierno/ministerios/', 'arrow-up-right'),
        ('02', 'Leyes', 'Análisis del marco legal, su depuración y propuestas de actualización.', 'leyes/constitucional/', 'arrow-up-right'),
        ('03', 'Proyectos', 'Infraestructura, capacidades productivas y desarrollo del capital humano.', 'proyectos/infraestructura/', 'arrow-up-right'),
        ('04', 'Objetivos', 'Prioridades organizadas en horizontes de corto, mediano y largo plazo.', 'objetivos/corto-plazo/', 'arrow-up-right')
    ]
    cards = ''.join(f'''<a class="pillar-card" href="{pre}{lnk}"><span class="card-index">{num} / ÁREA</span><span class="pillar-ornament" aria-hidden="true"><i></i><i></i></span><div class="pillar-bottom"><h3>{E(name)}</h3><span class="small-arrow" aria-hidden="true">↗</span></div><p>{E(desc)}</p></a>''' for num, name, desc, lnk, _ in first_pillars)
    body = f'''
    <section class="hero-home"><div class="container hero-home-grid">
      <div class="hero-copy"><div class="eyebrow"><span class="eyebrow-line"></span> PLATAFORMA DE PROPUESTAS · VENEZUELA</div>
        <h1>Una visión de país.<br><span>Un proyecto de futuro.</span></h1>
        <p>Un espacio para presentar y desarrollar propuestas sobre la reconstrucción institucional, jurídica y económica de Venezuela. Ideas organizadas, documentos abiertos y objetivos que puedan examinarse.</p>
        <div class="hero-actions"><a class="button button-primary" href="#ejes">Explorar la propuesta <span aria-hidden="true">↗</span></a><a class="text-link" href="#metodo">Cómo se publican los proyectos <span aria-hidden="true">→</span></a></div>
        <div class="hero-note"><span class="note-rule"></span> DOCUMENTACIÓN EN DESARROLLO · ACCESO PÚBLICO</div>
      </div>
      <div class="hero-graphic" aria-label="Composición visual abstracta de arquitectura institucional">
        <div class="graphic-grid"></div><div class="graphic-diagonal"></div><div class="graphic-circle circle-one"></div><div class="graphic-circle circle-two"></div>
        <div class="graphic-caption">VZ / 001</div>
        <div class="graphic-center"><span>V</span><i></i><small>UNA VISIÓN<br>DE PAÍS</small></div>
        <div class="graphic-bottom"><span>RECONSTRUCCIÓN<br>INSTITUCIONAL</span><span>01 — 04</span></div>
      </div>
    </div></section>
    <section class="micro-strip"><div class="container micro-inner"><span>INSTITUCIONES</span><i></i><span>SEGURIDAD JURÍDICA</span><i></i><span>DESARROLLO</span><i></i><span>PLANIFICACIÓN</span></div></section>
    <section class="section section-pillars" id="ejes"><div class="container"><div class="section-intro"><div><div class="eyebrow muted"><span class="eyebrow-line"></span> EL PROYECTO</div><h2>Cuatro ejes.<br><span>Una misma visión.</span></h2></div><p>El contenido está dividido por áreas para facilitar su consulta, actualización y evaluación. Cada apartado irá incorporando análisis, propuestas y documentos completos.</p></div>
    <div class="pillar-grid">{cards}</div></div></section>
    <section class="editorial-banner"><div class="container editorial-grid"><div class="editorial-mark" aria-hidden="true"><span>VV</span><div class="editorial-lines"></div></div><div class="editorial-content"><div class="eyebrow on-dark"><span class="eyebrow-line"></span> PROPÓSITO</div><h2>Las propuestas merecen ser <em>explicadas,</em> documentadas y examinadas.</h2><p>Este sitio reúne una visión de transformación del país. Los textos se publicarán progresivamente y distinguirán las ideas, los proyectos legislativos y sus fuentes de referencia.</p><a href="{pre}gobierno/ideologia/" class="banner-link">Conocer los principios <span aria-hidden="true">↗</span></a></div></div></section>
    <section class="section section-method" id="metodo"><div class="container"><div class="section-intro"><div><div class="eyebrow muted"><span class="eyebrow-line"></span> CÓMO LEER EL SITIO</div><h2>Del resumen<br><span>al documento.</span></h2></div><p>Cada página está concebida como un expediente público de consulta: primero las ideas centrales, después la documentación, las referencias y su estado de desarrollo.</p></div>
    <div class="method-grid"><div class="method-card"><span class="method-num">01</span><div class="method-icon">≡</div><h3>Resumen ejecutivo</h3><p>Una explicación clara del problema, el enfoque y los resultados previstos.</p></div><div class="method-card"><span class="method-num">02</span><div class="method-icon">▤</div><h3>Documento completo</h3><p>Un lector PDF integrado para consultar la propuesta desarrollada cuando esté disponible.</p></div><div class="method-card"><span class="method-num">03</span><div class="method-icon">▧</div><h3>Referencias visuales</h3><p>Fotografías, planos y otros materiales que ilustren cada proyecto.</p></div></div></div></section>
    <section class="closing-section"><div class="container closing-flex"><div><span class="closing-kicker">EXPLORAR EL CONTENIDO</span><h2>Una agenda abierta<br>al desarrollo de propuestas.</h2></div><a href="{pre}leyes/constitucional/" class="button button-outline">Ver el apartado de leyes <span aria-hidden="true">↗</span></a></div></section>
    '''
    (ROOT / 'index.html').write_text(html_shell('Inicio', DATA['site_description'], body, 0, 'inicio'), encoding='utf-8')


def item_page(section, item):
    key = f"{section['slug']}/{item['slug']}"
    override = DATA.get('overrides', {}).get(key, {})
    title = override.get('title', item['title'])
    intro = override.get('intro', item['intro'])
    summary = override.get('summary', f'Este apartado reunirá el diagnóstico, las propuestas y los documentos de trabajo relacionados con {title.lower()}. El contenido se publicará de manera progresiva y estará acompañado, cuando corresponda, por fuentes y referencias.')
    highlights = override.get('focus', ['Diagnóstico y contexto', 'Propuestas y desarrollo', 'Implementación y seguimiento'])
    pdf = override.get('pdf', '').strip()
    images = override.get('images', [])
    status = override.get('status', 'En preparación')
    updated = override.get('updated', 'Pendiente de publicación')
    pre = '../../'
    if pdf:
        # Nunca se inyecta markup del JSON; las rutas son relativas al sitio.
        clean_pdf = E(pre + pdf.lstrip('/'))
        pdfbox = f'''<div class="pdf-frame"><iframe title="Documento PDF: {E(title)}" src="{clean_pdf}#toolbar=1" loading="lazy"></iframe></div><div class="document-actions"><a class="button button-primary" href="{clean_pdf}" target="_blank" rel="noopener">Abrir documento completo <span aria-hidden="true">↗</span></a><a class="text-link" href="{clean_pdf}" download>Descargar PDF <span aria-hidden="true">↓</span></a></div>'''
    else:
        pdfbox = '''<div class="pdf-empty"><div class="pdf-icon" aria-hidden="true"><svg viewBox="0 0 64 76"><path d="M10 2h31l13 14v58H10z"/><path d="M41 2v16h13"/><path d="M20 34h24M20 44h24M20 54h17"/></svg></div><div><span class="small-cap">DOCUMENTACIÓN</span><h3>Documento en preparación</h3><p>El PDF completo de esta propuesta se incorporará aquí cuando esté disponible.</p></div></div>'''
    tiles = ''.join(f'<div class="focus-row"><span>0{i+1}</span><span>{E(text)}</span><span aria-hidden="true">↗</span></div>' for i, text in enumerate(highlights[:4]))
    if not images:
        images = [{"placeholder": True, "caption": "Espacio reservado para fotografía o referencia visual"}, {"placeholder": True, "caption": "Espacio reservado para plano, imagen o documento visual"}]
    gallery = ''
    for i, im in enumerate(images[:6]):
        if im.get('src'):
            src = E(pre + im['src'].lstrip('/'))
            photo = f'<a href="{src}" target="_blank" rel="noopener" aria-label="Ampliar fotografía {i+1}"><img loading="lazy" alt="{E(im.get("alt", "Imagen de referencia"))}" src="{src}"></a>'
        else:
            photo = f'<div class="image-placeholder"><div class="placeholder-shape" aria-hidden="true"><i></i><i></i><i></i></div><span>IMAGEN / {i+1:02}</span></div>'
        gallery += f'<figure class="gallery-item">{photo}<figcaption>{E(im.get("caption", "Referencia visual"))}</figcaption></figure>'
    body = f'''
      <section class="subhero"><div class="container"><div class="crumbs"><a href="{pre}">Inicio</a><span>/</span><span>{E(section['label'])}</span><span>/</span><strong>{E(title)}</strong></div>
       <div class="subhero-row"><div><div class="eyebrow"><span class="eyebrow-line"></span> {E(section['label'].upper())} / DOCUMENTACIÓN</div><h1>{E(title)}<span class="gold-dot">.</span></h1><p>{E(intro)}</p></div><div class="subhero-index"><span>ÁREA</span><strong>{E(str(SECTIONS.index(section)+1).zfill(2))}</strong><i></i><small>{E(section['label'].upper())}</small></div></div>
      </div></section>
      <section class="body-section"><div class="container content-layout">
       <article class="article-content"><div class="status-line"><span class="status-pill"><span></span> {E(status)}</span><span>ÚLTIMA ACTUALIZACIÓN: {E(updated)}</span></div>
       <section class="article-section" id="resumen"><div class="eyebrow muted"><span class="eyebrow-line"></span> 01 / PRESENTACIÓN</div><h2>Resumen de la propuesta</h2><p class="lead-paragraph">{E(summary)}</p><p class="subtle-para">Este espacio se actualizará con el contenido específico del proyecto. No se incorporarán posiciones ni conclusiones como definitivas mientras no se haya preparado su documentación.</p>
       <div class="focus-list"><span class="small-cap">ESTRUCTURA PREVISTA</span>{tiles}</div></section>
       <section class="article-section" id="documento"><div class="eyebrow muted"><span class="eyebrow-line"></span> 02 / PUBLICACIÓN COMPLETA</div><h2>Documento del proyecto</h2><p>Consulta aquí el texto completo, su fundamentación y las referencias correspondientes.</p>{pdfbox}</section>
       <section class="article-section" id="referencias"><div class="eyebrow muted"><span class="eyebrow-line"></span> 03 / MATERIAL VISUAL</div><h2>Referencias e imágenes</h2><p>Material complementario para ilustrar, contextualizar y documentar el proyecto.</p><div class="gallery-grid">{gallery}</div></section></article>
       <aside class="article-sidebar"><div class="sticky-side"><div class="sidebar-label">EN ESTA PÁGINA</div><a href="#resumen"><span>01</span> Resumen ejecutivo</a><a href="#documento"><span>02</span> Documento PDF</a><a href="#referencias"><span>03</span> Referencias visuales</a><div class="side-divider"></div><span class="sidebar-label">ESTADO</span><p>Contenido en elaboración. La publicación final incorporará sus fuentes y documentos de respaldo.</p><a class="side-link" href="{pre}faq/">Preguntas frecuentes <span aria-hidden="true">↗</span></a></div></aside>
      </div></section>
      <section class="related-section"><div class="container related-inner"><div><div class="eyebrow muted"><span class="eyebrow-line"></span> CONTINUAR EXPLORANDO</div><h2>Más áreas de {E(section['label'].lower())}.</h2></div><div class="related-list">{related_links(section, item, pre)}</div></div></section>
    '''
    folder = ROOT / section['slug'] / item['slug']
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(html_shell(title, intro, body, 2, section['slug']), encoding='utf-8')


def related_links(section, item, pre):
    alternatives = [p for p in section['items'] if p['slug'] != item['slug']][:3]
    if not alternatives:
        alternatives = [s['items'][0] for s in SECTIONS if s['slug'] != section['slug']][:3]
    links = []
    for p in alternatives:
        group = section if p in section['items'] else next(s for s in SECTIONS if p in s['items'])
        links.append(f'<a href="{pre}{E(group["slug"])}/{E(p["slug"])}/">{E(p["title"])} <span aria-hidden="true">↗</span></a>')
    return ''.join(links)


def faq_page():
    pre='../'
    items = ''.join(f'''<details class="faq-item" {'open' if i == 0 else ''}><summary><span class="faq-number">{i+1:02d}</span><span>{E(faq['question'])}</span><span class="faq-plus" aria-hidden="true"></span></summary><p>{E(faq['answer'])}</p></details>''' for i, faq in enumerate(DATA['faq']))
    body = f'''<section class="subhero faq-hero"><div class="container"><div class="crumbs"><a href="{pre}">Inicio</a><span>/</span><strong>FAQ</strong></div><div class="eyebrow"><span class="eyebrow-line"></span> INFORMACIÓN</div><h1>Preguntas frecuentes<span class="gold-dot">.</span></h1><p>Información general sobre el propósito, la documentación y el funcionamiento de esta plataforma.</p></div></section>
      <section class="faq-section"><div class="container faq-layout"><div class="faq-aside"><span class="small-cap">UNA PLATAFORMA ABIERTA</span><h2>Claridad desde el primer documento.</h2><p>Las publicaciones distinguirán las propuestas de sus fuentes y el estado de preparación de cada texto.</p></div><div class="faq-list">{items}</div></div></section>'''
    folder=ROOT/'faq';folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(html_shell('Preguntas frecuentes', 'Respuestas a preguntas sobre Visión Venezuela, sus propuestas y documentos.', body, 1,'faq'), encoding='utf-8')


def main():
    main_page()
    faq_page()
    for section, item in ALL:
        item_page(section, item)
    (ROOT/'.nojekyll').touch(exist_ok=True)
    print(f'Sitio generado: {len(ALL)+2} páginas HTML')

if __name__ == '__main__':
    main()
