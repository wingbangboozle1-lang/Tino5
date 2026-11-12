#!/usr/bin/env python3
"""Check local HTML links and fragments in a static directory, without network access.

External link availability, source authority, accuracy, and privacy are not verified.
Usage: python3 tools-786/check_links.py public-safe
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.duplicates = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in (attrs.get('id'), attrs.get('name') if tag == 'a' else None):
            if name:
                if name in self.ids:
                    self.duplicates.append(name)
                self.ids.add(name)
        for attr in ('href', 'src'):
            if attr in attrs and attrs[attr]:
                self.links.append(attrs[attr])


def check(root):
    root = Path(root).resolve()
    pages = {}
    errors = []
    for path in root.rglob('*.html'):
        page = Page()
        try:
            page.feed(path.read_text(encoding='utf-8'))
            page.close()
        except (UnicodeError, OSError, ValueError) as e:
            errors.append(f'{path.relative_to(root)}: cannot parse: {e}')
            continue
        pages[path.resolve()] = page
        for identifier in page.duplicates:
            errors.append(f'{path.relative_to(root)}: duplicate id/name {identifier!r}')
    if not pages:
        errors.append('No HTML pages found')
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                errors.append(f'{path.relative_to(root)}: root-relative URL cannot be checked in a project Pages site: {link}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(root):
                errors.append(f'{path.relative_to(root)}: link escapes checked directory: {link}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(root)}: missing target: {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(root)}: missing fragment: {link}')
    return len(pages), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    count, errors = check(args.directory)
    for error in errors:
        print('ERROR:', error)
    print(f'{count} HTML pages checked; {len(errors)} errors. External URLs and claim accuracy not checked.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
