# -*- coding: utf-8 -*-
"""Independent check of questions.json: re-simulate every route and check text alignment."""
import json, re, sys

DX = [0, 1, 0, -1]; DY = [-1, 0, 1, 0]
data = json.load(open('questions.json', encoding='utf-8'))
maps, B, Q = data['maps'], data['buildings'], data['questions']
W = H = 4
TRAD_ONLY = set('轉馬過經對邊個麵廳銀藥醫學書飲車飯郵攤運診廟區館園場買')
errs = []

def han_count(s):
    return len(re.findall(r'[一-鿿]', s))

def py_count(s):
    toks = re.findall(r"[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+", s)
    return len(toks)

for q in Q:
    x, y, d = q['start']
    path = [[x, y]]
    for a in q['actions']:
        if a == 'L': d = (d + 3) % 4
        elif a == 'R': d = (d + 1) % 4
        else:
            lastseg = (x, y, d)
            x, y = x + DX[d], y + DY[d]
            if not (0 <= x < W and 0 <= y < H):
                errs.append((q['id'], 'walks off map')); break
            path.append([x, y])
    else:
        if [x, y, d] != q['end']: errs.append((q['id'], 'end mismatch'))
        if path != q['path']: errs.append((q['id'], 'path mismatch'))
        if q['actions'][-1] != 'S': errs.append((q['id'], 'last action is not a walk'))
        # target on the stated side of the last segment
        lx, ly, ld = lastseg
        mx, my = lx + DX[ld] / 2.0, ly + DY[ld] / 2.0
        sd = (ld + 3) % 4 if q['side'] == 'L' else (ld + 1) % 4
        bx, by = int(round(mx + 0.5 * DX[sd] - 0.5)), int(round(my + 0.5 * DY[sd] - 0.5))
        if not (0 <= bx < 3 and 0 <= by < 3) or maps[q['map']]['blocks'][by][bx] != q['target']:
            errs.append((q['id'], 'target not on stated side'))
    # text alignment: one pinyin syllable per Han char; no traditional-only chars in CN
    for sent_tw, sent_py in zip(q['tw'].split('。')[:-1], q['py'].split('. ')):
        if han_count(sent_tw) != py_count(sent_py):
            errs.append((q['id'], 'pinyin count %d vs han %d: %s' % (py_count(sent_py), han_count(sent_tw), sent_tw)))
    if any(c in TRAD_ONLY for c in q['cn']):
        errs.append((q['id'], 'traditional char in CN: ' + ''.join(c for c in q['cn'] if c in TRAD_ONLY)))
    for k in ('tw', 'cn', 'py', 'es', 'en'):
        if not q[k].strip(): errs.append((q['id'], 'empty ' + k))

ids = [q['id'] for q in Q]
if len(ids) != len(set(ids)): errs.append(('-', 'duplicate ids'))
by = {}
for q in Q: by.setdefault((q['level']), 0); by[q['level']] += 1
print('questions per level:', by)
print('ERRORS:', len(errs))
for e in errs[:30]: print(' ', e)
sys.exit(1 if errs else 0)
