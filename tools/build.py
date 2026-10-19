# -*- coding: utf-8 -*-
"""Rebuild the single-file game: tools/template.html + questions.json -> index.html
Run from inside the tools/ folder:  python3 gen_questions.py && python3 verify_questions.py && python3 build.py
"""
import json
tpl = open('template.html', encoding='utf-8').read()
data = open('questions.json', encoding='utf-8').read()
json.loads(data)  # sanity check
assert '/*__DATA__*/{}' in tpl
out = tpl.replace('/*__DATA__*/{}', data)
open('../index.html', 'w', encoding='utf-8').write(out)
print('built ../index.html', len(out) // 1024, 'KB')
