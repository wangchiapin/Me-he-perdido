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
    return len(re.findall(r'[一-鿿]', s)) + s.count('Y')

def py_count(s):
    return len(re.findall(r"[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+", s))

GM = {m: v for m, v in maps.items() if not v.get('graph')}
closed = {m: [({(c[0], c[1]), (c[2], c[3])}) for c in GM[m]['closed']] for m in GM}
def is_open(m, x, y, d):
    nx, ny = x + DX[d], y + DY[d]
    return 0 <= nx < W and 0 <= ny < H and {(x, y), (nx, ny)} not in closed[m]
def deg(m, x, y): return sum(is_open(m, x, y, d) for d in range(4))

# every grid map: connected, no isolated node
for m in GM:
    seen, stack = {(0, 0)}, [(0, 0)]
    while stack:
        x, y = stack.pop()
        for d in range(4):
            if is_open(m, x, y, d):
                p = (x + DX[d], y + DY[d])
                if p not in seen: seen.add(p); stack.append(p)
    if len(seen) != W * H: errs.append((m, 'road map not connected'))


import math
G = maps['real']; GN, GE = G['nodes'], G['edges']
INC = {n: [e for e, v in GE.items() if n in (v['a'], v['b'])] for n in GN}
def _p(e, frm): p = GE[e]['pts']; return p if GE[e]['a'] == frm else p[::-1]
def _oth(e, n): return GE[e]['b'] if GE[e]['a'] == n else GE[e]['a']
def _b(p, q): return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
def _ad(a, b):
    d = (b - a + 180) % 360 - 180
    return 180 if d == -180 else d
def _ob(n, e): p = _p(e, n); return _b(p[0], p[1])
def _fl(e, frm): return (GE[e]['L'], GE[e]['R']) if GE[e]['a'] == frm else (GE[e]['R'], GE[e]['L'])
def check_graph(q):
    n, face = q['start']; via = None; h = _ob(n, face)
    path = [GN[n][:2]]; crosses = []; last = None; ys = 0
    def walk(e):
        nonlocal n, via, h, face, last, ys
        frm = n; p = _p(e, frm); path.extend(p[1:]); n = _oth(e, frm); via = e; last = (e, frm)
        h = _b(p[-2], p[-1]); face = None
        if GN[n][2] == 'y' and via == GN[n][3]: ys += 1
        if GN[n][2] != 'rb':
            c = [(abs(_ad(h, _ob(n, x))), x) for x in INC[n] if x != e and abs(_ad(h, _ob(n, x))) <= 25]
            if c: face = min(c)[1]
    for a in q['actions']:
        if a == 'S':
            if face is None or GN[n][2] == 'rb': return 'S with no road ahead'
            walk(face)
        elif a in 'LR':
            if GN[n][2] == 'rb': return 'turn inside roundabout'
            c = [e for e in INC[n] if (20 < _ad(h, _ob(n, e)) < 160 if a == 'R' else -160 < _ad(h, _ob(n, e)) < -20)]
            if len(c) != 1: return 'ambiguous or missing turn'
            face = c[0]; h = _ob(n, face)
        elif a == 'C':
            if face is None or GN[n][2] == 'rb' or len(INC[n]) < 3: return 'bad crossing'
            crosses.append([n, face])
        else:
            if GN[n][2] != 'rb': return 'exit outside roundabout'
            eb = _ob(n, via); ex = sorted([e for e in INC[n] if e != via], key=lambda e: (eb - _ob(n, e)) % 360)
            if int(a) > len(ex): return 'no such exit'
            walk(ex[int(a) - 1])
    if [n, via] != q['end']: return 'end mismatch'
    if [[round(x, 1), round(y, 1)] for x, y in path] != q['path'] and path != q['path']: return 'path mismatch'
    if crosses != q['crosses']: return 'crosses mismatch'
    if q['actions'][-1] != 'S': return 'last action is not a walk'
    full_ = ''.join(p['tw'] for p in q['parts'])
    nr = sum(a in '1234' for a in q['actions'])
    if full_.count('圓環') != nr or full_.count('出口出去') != nr: return 'roundabout text mismatch'
    if full_.count('Y字路口') != ys or full_.count('靠左') + full_.count('靠右') != ys: return 'Y text mismatch'
    if full_.count('過馬路') != len(crosses): return 'crossing text mismatch'
    for m in re.finditer('C', q['actions']):
        if q['actions'][m.end():m.end() + 1] != 'S': return 'crossing not followed by a walk'
    bl, br = _fl(*last)
    if (bl if q['side'] == 'L' else br) != q['target']: return 'target not on stated side'
    return None
for q in Q:
    if q.get('graph'):
        r = check_graph(q)
        if r: errs.append((q['id'], r))
for e_, v in GE.items():
    for sd in 'LR':
        if v[sd] and v[sd] not in B: errs.append((e_, 'unknown building'))
GBS = [v[s_] for v in GE.values() for s_ in 'LR' if v[s_]]
if len(GBS) != len(set(GBS)): errs.append(('real', 'duplicate building on the graph map'))
if set(G['bpos']) != set(GBS): errs.append(('real', 'building positions do not match the roads'))

for q in Q:
    m = q['map']
    gq = bool(q.get('graph'))
    x, y, d = (0, 0, 0) if gq else q['start']
    path, crosses, lastseg, lastlen, bad = [[x, y]], [], None, 0, gq
    rbs = ys = 0
    for a in ('' if gq else q['actions']):
        if a == 'L': d = (d + 3) % 4
        elif a == 'R': d = (d + 1) % 4
        elif a in '123':
            ex = [(((d + 2) % 4) - i) % 4 for i in (1, 2, 3) if is_open(m, x, y, (((d + 2) % 4) - i) % 4)]
            if [x, y] not in maps[m]['rb'] or int(a) > len(ex):
                errs.append((q['id'], 'bad roundabout exit')); bad = True; break
            d = ex[int(a) - 1]; rbs += 1
            n = 0
            while True:
                lastseg = (x, y, d)
                x, y = x + DX[d], y + DY[d]
                path.append([x, y]); n += 1
                if not (deg(m, x, y) == 2 and is_open(m, x, y, d)): break
            lastlen = n
        elif a == 'C':
            if not is_open(m, x, y, d) or deg(m, x, y) < 3:
                errs.append((q['id'], 'crosses where there is no street to cross / no road ahead')); bad = True; break
            crosses.append([x, y, d])
        else:
            if not is_open(m, x, y, d):
                errs.append((q['id'], 'walks along a closed road')); bad = True; break
            n = 0
            while True:
                lastseg = (x, y, d)
                x, y = x + DX[d], y + DY[d]
                path.append([x, y]); n += 1
                if not (deg(m, x, y) == 2 and is_open(m, x, y, d)): break
            lastlen = n
            if [x, y] in maps[m]['ynodes'] and not is_open(m, x, y, d): ys += 1
    if not bad:
        full_ = ''.join(p['tw'] for p in q['parts'])
        if full_.count('圓環') != sum(a in '123' for a in q['actions']): errs.append((q['id'], 'roundabout text/action mismatch'))
        if full_.count('出口出去') != sum(a in '123' for a in q['actions']): errs.append((q['id'], 'exit text mismatch'))
        if full_.count('Y字路口') != ys: errs.append((q['id'], 'Y-junction text mismatch'))
        if full_.count('靠左') + full_.count('靠右') != ys: errs.append((q['id'], 'fork text mismatch'))
        if [x, y, d] != q['end']: errs.append((q['id'], 'end mismatch'))
        if path != q['path']: errs.append((q['id'], 'path mismatch'))
        if crosses != q['crosses']: errs.append((q['id'], 'crosses mismatch'))
        if q['actions'][-1] != 'S': errs.append((q['id'], 'last action is not a walk'))
        if lastlen != 1: errs.append((q['id'], 'last walk is longer than one block'))
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
