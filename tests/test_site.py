"""Pruebas simples sin librerías externas; ejecutar: python -m unittest discover -s tests -v"""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'content'/'site.json').read_text(encoding='utf8'))

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references=[]
        self.ids=set()
        self.h1_count=0
        self.title_count=0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag == 'h1': self.h1_count += 1
        if tag == 'title': self.title_count += 1
        for prop in ('href', 'src'):
            if attrs.get(prop): self.references.append((tag,prop,attrs[prop]))

class SiteTests(unittest.TestCase):
    def test_number_of_pages(self):
        count=2+sum(len(s['items']) for s in DATA['sections'])
        pages=list(ROOT.glob('**/index.html'))
        self.assertEqual(len(pages),count)
    def test_page_metadata_and_links(self):
        pages=list(ROOT.glob('**/index.html'))
        for page in pages:
            with self.subTest(page=page.relative_to(ROOT)):
                parser=Parser(); parser.feed(page.read_text(encoding='utf8'))
                self.assertEqual(parser.h1_count,1)
                self.assertEqual(parser.title_count,1)
                for tag,attr,link in parser.references:
                    if link.startswith(('mailto:','tel:','https:','http:','javascript:','data:')):
                        continue
                    parsed=urlparse(link)
                    if parsed.path:
                        candidate = (page.parent/unquote(parsed.path)).resolve()
                        self.assertTrue(candidate.is_relative_to(ROOT), (page,link))
                        if candidate.is_dir(): candidate/= 'index.html'
                        self.assertTrue(candidate.exists(),(page,link,candidate))
                    if parsed.fragment and not parsed.path and not link.startswith('#toolbar'):
                        self.assertIn(parsed.fragment,parser.ids, (page, link))
    def test_all_pages_have_pdf_placeholder(self):
        for section in DATA['sections']:
            for item in section['items']:
                p=ROOT/section['slug']/item['slug']/'index.html'
                content = p.read_text(encoding='utf8')
                override=DATA.get('overrides',{}).get(f"{section['slug']}/{item['slug']}",{})
                if override.get('pdf'):
                    self.assertIn('class="pdf-frame"',content)
                else:
                    self.assertIn('Documento en preparación',content)
    def test_brand_navigation_and_status(self):
        home=(ROOT/'index.html').read_text(encoding='utf8')
        self.assertIn('VISIÓN', home)
        self.assertIn('aria-controls="nav-menu"',home)
        self.assertTrue((ROOT/'.nojekyll').exists())

if __name__=='__main__': unittest.main()
