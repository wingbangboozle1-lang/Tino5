"""Structural and privacy checks only; not an automated fact checker."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
root=Path('public-safe')
allowed={'www.sco.ca.gov','boe.ca.gov','www.boe.ca.gov','www.irs.gov','www.insurance.ca.gov','www.bls.gov','selfhelp.courts.ca.gov','www.ftb.ca.gov'}
errors=[]; rows=0; links=0
class Check(HTMLParser):
 def __init__(self,path):
  super().__init__();self.path=path;self.inrow=False;self.rowlinks=[];self.head=False
 def handle_starttag(self,t,attrs):
  global links
  a=dict(attrs)
  if t=='thead':self.head=True
  if t=='tr':self.inrow=True;self.rowlinks=[]
  if t in ('script','iframe','form'):errors.append(f'{self.path}: forbidden {t}')
  for k in ('href','src'):
   if k not in a:continue
   v=a[k];links+=1
   if v.startswith('https:'):
    if urlparse(v).hostname not in allowed:errors.append('Unexpected external host '+v)
    if self.inrow:self.rowlinks.append(v)
   elif not (self.path.parent/v.split('#')[0]).exists():errors.append('Broken local link '+v)
 def handle_endtag(self,t):
  global rows
  if t=='tr':
   if not self.head:
    rows+=1
    if not self.rowlinks:errors.append(f'{self.path}: row without official source')
   self.inrow=False
  if t=='thead':self.head=False
for p in root.rglob('*'):
 if p.is_dir():continue
 if p.suffix not in ('.html','.css'):errors.append('Unexpected artifact '+str(p))
 if p.is_symlink():errors.append('Symlink in public artifact')
 text=p.read_text()
 # Private fingerprints supplied in the brief; do not emit matches in logs.
 forbidden=[r'\b(?:95014|94122|550537|539743|114248|112008)\b',r'550,537|539,743|114,248|112,008',r'3,100,000|1,800,000|7,150',r'Cupertino|Outer Sunset',r'[\w.+-]+@[\w.-]+\.[a-z]{2,}',r'\b\d{3}-\d{2}-\d{4}\b']
 if any(re.search(x,text,re.I) for x in forbidden):errors.append(f'{p}: private fingerprint pattern')
 for m in re.finditer(r'\$([\d,]+)(?![\d,])',text):
  if int(m[1].replace(',',''))%10:errors.append(f'{p}: unrounded money')
 if p.suffix=='.html':Check(p).feed(text)
assert len(list(root.glob('*.html')))==9
assert len(re.findall(r'<tr>',(root/'projections.html').read_text()))==56
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: 9 pages; {rows} source-linked rows; {links} links; local targets resolve; privacy patterns clean; money rounded. Structural checks only, not semantic certification.')
