# -*- coding: utf-8 -*-
"""Independent check of questions.json: re-simulate every route and check the text."""
import json, re, sys

DX = [0, 1, 0, -1]; DY = [-1, 0, 1, 0]
data = json.load(open('questions.json', encoding='utf-8'))
maps, B, Q = data['maps'], data['buildings'], data['questions']
W = H = 4
TRAD_ONLY = set('轉馬過經對邊個麵廳銀藥醫學書飲車飯郵攤運診廟區館園場買髮當劇圖貨電')
errs = []

def han_count(s):
    return len(re.findall(r'[一-鿿]', s))

def py_count(s):
    return len(re.findall(r"[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+", s))

for q in Q:
    x, y, d = q['start']
    path, crosses, lastseg, bad = [[x, y]], [], None, False
    for a in q['actions']:
        if a == 'L': d = (d + 3) % 4
        elif a == 'R': d = (d + 1) % 4
        elif a == 'C':
            if not (0 <= x + DX[d] < W and 0 <= y + DY[d] < H):
                errs.append((q['id'], 'crosses where there is no road')); bad = True; break
            crosses.append([x, y, d])
        else:
            lastseg = (x, y, d)
            x, y = x + DX[d], y + DY[d]
            if not (0 <= x < W and 0 <= y < H):
                errs.append((q['id'], 'walks off map')); bad = True; break
            path.append([x, y])
    if not bad:
        if [x, y, d] != q['end']: errs.append((q['id'], 'end mismatch'))
        if path != q['path']: errs.append((q['id'], 'path mismatch'))
        if crosses != q['crosses']: errs.append((q['id'], 'crosses mismatch'))
        if q['actions'][-1] != 'S': errs.append((q['id'], 'last action is not a walk'))
        # every crossing must be followed by a walk
        for m in re.finditer('C', q['actions']):
            if q['actions'][m.end():m.end() + 1] != 'S': errs.append((q['id'], 'crossing not followed by a walk'))
        # the sentence mentions 過馬路 exactly as often as the route crosses
        full_tw = ''.join(p['tw'] for p in q['parts'])
        if full_tw.count('過馬路') != len(q['crosses']): errs.append((q['id'], 'text/crossing count mismatch'))
        # target on the stated side of the last segment
        lx, ly, ld = lastseg
        mx, my = lx + DX[ld] / 2.0, ly + DY[ld] / 2.0
        sd = (ld + 3) % 4 if q['side'] == 'L' else (ld + 1) % 4
        bx, by = int(round(mx + 0.5 * DX[sd] - 0.5)), int(round(my + 0.5 * DY[sd] - 0.5))
        if not (0 <= bx < 3 and 0 <= by < 3) or maps[q['map']]['blocks'][by][bx] != q['target']:
            errs.append((q['id'], 'target not on stated side'))
    if len(q['parts']) < 2: errs.append((q['id'], 'needs at least 2 parts'))
    for i, p in enumerate(q['parts']):
        if han_count(p['tw']) != py_count(p['py']):
            errs.append((q['id'], 'part %d pinyin %d vs han %d: %s' % (i, py_count(p['py']), han_count(p['tw']), p['tw'])))
        if any(c in TRAD_ONLY for c in p['cn']):
            errs.append((q['id'], 'traditional char in CN: ' + ''.join(c for c in p['cn'] if c in TRAD_ONLY)))
        if not p['tw'].endswith('。') or not p['py'].endswith('.') or not p['es'].endswith('.') or not p['en'].endswith('.'):
            errs.append((q['id'], 'part %d punctuation' % i))
        for k in ('tw', 'cn', 'py', 'es', 'en'):
            if not p[k].strip(): errs.append((q['id'], 'empty ' + k))

ids = [q['id'] for q in Q]
if len(ids) != len(set(ids)): errs.append(('-', 'duplicate ids'))
for mp in maps:
    keys = [k for r in maps[mp]['blocks'] for k in r]
    if len(keys) != len(set(keys)) or any(k not in B for k in keys): errs.append((mp, 'map buildings not unique / unknown'))
by, bym = {}, {}
for q in Q:
    by[q['level']] = by.get(q['level'], 0) + 1
    bym[q['map']] = bym.get(q['map'], 0) + 1
print('per level:', by, '| per map:', bym)
print('with crossing:', sum(1 for q in Q if q['crosses']), '| ERRORS:', len(errs))
for e in errs[:30]: print(' ', e)
sys.exit(1 if errs else 0)
