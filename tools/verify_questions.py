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
def use(mp):                       # check one road-graph map at a time
    global G, GN, GE, INC
    G = maps[mp]; GN, GE = G['nodes'], G['edges']
    INC = {n: [e for e, v in GE.items() if n in (v['a'], v['b'])] for n in GN}
use('real')
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
    if GN[n][2] == 'm':
        mm = G['mid'][n]; fwd = (via == mm['ea'])
        bl, br = (mm['L'], mm['R']) if fwd else (mm['R'], mm['L'])
    else:
        bl, br = _fl(*last)
    if (bl if q['side'] == 'L' else br) != q['target']: return 'target not on stated side'
    return None
def bk(k): return k.split('_')[0]      # 'conv_2' = a second shop of the same kind on the big map

def check_plan(q):
    """level 6: replay the actions against the sentence's own plan (traffic lights, junctions, the k-th shop of a kind)"""
    GM_ = G['mid']
    n, face = q['start']; via = None; h = _ob(n, face); acts = list(q['actions']); i = 0
    lastedge = None
    def step():                       # one 直走: returns False if impossible
        nonlocal n, via, h, face, lastedge
        if face is None: return False
        frm = n; p = _p(face, frm); e = face; n = _oth(e, frm); via = e; h = _b(p[-2], p[-1]); face = None; lastedge = (e, frm)
        c = [(abs(_ad(h, _ob(n, x))), x) for x in INC[n] if x != e and abs(_ad(h, _ob(n, x))) <= 25]
        if c: face = min(c)[1]
        return True
    def beside_(): 
        if GN[n][2] != 'm': return (None, None)
        mm = GM_[n]; fwd = (via == mm['ea'])
        return (mm['L'], mm['R']) if fwd else (mm['R'], mm['L'])
    def pair_():                      # (left, right) buildings next to the stop we stand at / the stretch we just walked
        return beside_() if GN[n][2] == 'm' else _fl(*lastedge)
    def eat(ch):
        nonlocal i
        if i >= len(acts) or acts[i] != ch: return False
        i += 1; return True
    for st in q['plan']:
        k = st['kind']
        if k == 'turn':
            a = st['t']
            if not eat(a): return 'plan: expected turn ' + a
            c = [e for e in INC[n] if (20 < _ad(h, _ob(n, e)) < 160 if a == 'R' else -160 < _ad(h, _ob(n, e)) < -20)]
            if len(c) != 1: return 'plan: bad turn'
            face = c[0]; h = _ob(n, face)
        elif k == 'go1':
            if not eat('S') or not step(): return 'plan: go1'
        elif k in ('go', 'golight'):
            c = 0; first = None; cur = []
            while c < st['n']:
                if not eat('S') or not step(): return 'plan: %s runs out of road' % k
                cur.append(pair_())
                if GN[n][2] == 'm': continue
                if first is None: first = cur
                cur = []
                if len(INC[n]) < 3: return 'plan: %s counted a corner' % k
                if k == 'go' or G['lights'].count(n): c += 1
            if k == 'golight' and n not in G['lights']: return 'plan: golight does not end at a light'
            if st.get('via') and not any(st['via'] in g_ for g_ in first): return 'plan: the 經過 building is not passed before the first junction'
        elif k == 'pass':
            for _ in range(st['k']):
                grp = []
                while True:
                    if not eat('S') or not step(): return 'plan: pass runs out of road'
                    grp.append(pair_())
                    if GN[n][2] != 'm': break
            si = 0 if st['side'] == 'L' else 1
            if not any((st['b'] in g_) if st.get('see') else (g_[si] == st['b']) for g_ in grp): return 'plan: the passed building is not on the stretch'
            if st['turn'] == 'C':
                if not eat('C') or face is None or len(INC[n]) < 3: return 'plan: bad crossing'
            else:
                a = st['turn']
                if not eat(a): return 'plan: expected turn ' + a
                c_ = [e for e in INC[n] if (20 < _ad(h, _ob(n, e)) < 160 if a == 'R' else -160 < _ad(h, _ob(n, e)) < -20)]
                if len(c_) != 1: return 'plan: bad turn after pass'
                face = c_[0]; h = _ob(n, face)
        elif k == 'shop':
            if not eat('S') or not step() or GN[n][2] != 'm': return 'plan: shop'
        elif k == 'gostore':
            c = 0
            while c < st['n']:
                if not eat('S') or not step(): return 'plan: gostore runs out of road'
                if GN[n][2] == 'm':
                    hit = [x for x in beside_() if x and bk(x) == st['b']]
                    if len(hit) == 2: return 'plan: kind on both sides'
                    if hit: c += 1
            if st['key'] not in beside_(): return 'plan: gostore key not beside the stop'
        else:
            return 'plan: unknown step ' + k
    if i != len(acts): return 'plan: actions left over'
    return None

def check_gplan(q):
    """grid maps: replay the actions against the sentence's own plan (junction counts, traffic lights, 經過 / 看到 buildings, 到底)"""
    m = q['map']; x, y, d = q['start']; acts = list(q['actions']); i = 0
    lights = {tuple(p_) for p_ in q.get('lights', [])}
    blocks = q['blocks']
    def flk(px, py, pd):
        mx, my = px + DX[pd] / 2.0, py + DY[pd] / 2.0; out = []
        for sd in ((pd + 3) % 4, (pd + 1) % 4):
            bx, by = int(round(mx + 0.5 * DX[sd] - 0.5)), int(round(my + 0.5 * DY[sd] - 0.5))
            out.append(blocks[by][bx] if (0 <= bx < 3 and 0 <= by < 3) else None)
        return tuple(out)
    def walk():
        nonlocal x, y
        if not is_open(m, x, y, d): return None
        fl = []
        while True:
            fl.append(flk(x, y, d)); x, y = x + DX[d], y + DY[d]
            if not (deg(m, x, y) == 2 and is_open(m, x, y, d)): break
        return fl
    def eat(ch):
        nonlocal i
        if i >= len(acts) or acts[i] != ch: return False
        i += 1; return True
    def turn(a):
        nonlocal d
        if not eat(a): return False
        d = (d + (1 if a == 'R' else 3)) % 4; return True
    for st in q['plan']:
        k = st['kind']
        if k == 'turn':
            if not turn(st['t']): return 'gplan: expected turn'
        elif k == 'go1':
            if not eat('S') or walk() is None: return 'gplan: go1'
        elif k in ('go', 'golight'):
            c = 0; first = None
            while c < st['n']:
                if not eat('S'): return 'gplan: %s: no walk' % k
                fl = walk()
                if fl is None or deg(m, x, y) < 3: return 'gplan: %s: not a junction' % k
                if first is None: first = fl
                if k == 'go' or (x, y) in lights: c += 1
            if k == 'golight' and (x, y) not in lights: return 'gplan: golight does not end at a light'
            if st.get('via') and not any(st['via'] in g_ for g_ in first): return 'gplan: the 經過 building is not beside the first stretch'
        elif k == 'end':
            n_ = 0
            while is_open(m, x, y, d):
                if not eat('S') or walk() is None: return 'gplan: end'
                n_ += 1
            if n_ < 1: return 'gplan: end walks nowhere'
        elif k == 'pass':
            for _ in range(st['k']):
                if not eat('S'): return 'gplan: pass: no walk'
                fl = walk()
                if fl is None: return 'gplan: pass'
            si = 0 if st['side'] == 'L' else 1
            if not any((st['b'] in g_) if st.get('see') else (g_[si] == st['b']) for g_ in fl): return 'gplan: the passed building is not on the last stretch'
            if st['turn'] == 'C':
                if not eat('C') or not is_open(m, x, y, d) or deg(m, x, y) < 3: return 'gplan: bad crossing'
            elif not turn(st['turn']): return 'gplan: turn after pass'
        else:
            return 'gplan: unknown step ' + k
    if i != len(acts): return 'gplan: actions left over'
    return None

for q in Q:
    if not q.get('graph') and q.get('plan'):
        r = check_gplan(q)
        if r: errs.append((q['id'], r))
    if q.get('plan'):                                   # the words in the sentence match the plan
        full_ = ''.join(p['tw'] for p in q['parts']); pl = q['plan']
        for word, cnt in (('紅綠燈', sum(1 for s_ in pl if s_['kind'] == 'golight')), ('經過', sum(1 for s_ in pl if s_.get('via'))),
                          ('看到', sum(1 for s_ in pl if s_.get('see'))), ('間', sum(1 for s_ in pl if s_['kind'] == 'gostore' and s_['n'] >= 2)),
                          ('過了', sum(1 for s_ in pl if s_['kind'] == 'pass' and not s_.get('see')))):
            if full_.count(word) != cnt: errs.append((q['id'], 'text/plan mismatch for ' + word))
        if full_.count('到底') != sum(1 for s_ in pl if s_['kind'] == 'end'): errs.append((q['id'], 'text/plan mismatch for 到底'))
    if q.get('graph'):
        use(q['map'])
        r = check_graph(q) or (check_plan(q) if q.get('plan') else None)
        if r: errs.append((q['id'], r))
        full_ = ''.join(p['tw'] for p in q['parts'])
        if q['map'] == 'big' and ('過馬路' in full_ or q['crosses']): errs.append((q['id'], 'the big map has no crossings'))
        if q['map'] == 'big' and not q.get('plan'): errs.append((q['id'], 'big-map question without a plan'))
        if ('經過' in full_ or '看到' in full_) and not q.get('plan'): errs.append((q['id'], '經過 / 看到 sentence without a plan'))
for mp_, mv in maps.items():
    if not mv.get('graph'): continue
    use(mp_)
    for e_, v in GE.items():
        for sd in ('L', 'R', 'L2', 'R2'):
            if v[sd] and bk(v[sd]) not in B: errs.append((e_, 'unknown building'))
    GBS = [v[s_] for v in GE.values() for s_ in ('L', 'R', 'L2', 'R2') if v[s_]] + [b_ for mm in G['mid'].values() for b_ in (mm['L'], mm['R']) if b_]
    if len(GBS) != len(set(GBS)): errs.append((mp_, 'duplicate building on the graph map'))
    if set(G['bpos']) != set(GBS): errs.append((mp_, 'building positions do not match the roads'))
    if mp_ == 'big':
        degs = {n_: len(INC[n_]) for n_ in GN if GN[n_][2] == 'n'}
        if any(n_ not in degs or degs[n_] < 3 for n_ in G['lights']): errs.append((mp_, 'a traffic light on a corner'))
        if not (3 <= len(G['lights']) < len(degs)): errs.append((mp_, 'traffic lights should be on some, not all, nodes'))

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
        if not (0 <= bx < 3 and 0 <= by < 3) or (q.get('blocks') or maps[q['map']]['blocks'])[by][bx] != q['target']:
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
# every question's own layout: the same nine buildings as the map, the star building unmoved
ANCH = {'station': 'train', 'night': 'temple', 'campus': 'school', 'hospital': 'hospital', 'metro': 'mrt'}
for q in Q:
    if not q.get('graph'):
        base = maps[q['map']]['blocks']
        lay = q.get('blocks')
        if not lay: errs.append((q['id'], 'basic-map question without its own layout')); continue
        if sorted(k for r in lay for k in r) != sorted(k for r in base for k in r): errs.append((q['id'], 'layout changes the set of buildings'))
        a = ANCH.get(q['map'])
        if a and any(base[y][x] == a and lay[y][x] != a for y in range(3) for x in range(3)): errs.append((q['id'], 'star building moved'))
# the four levels (1: grid, no counting / 2: grid + counting, lights, buildings / 3: road graphs / 4: everything)
for q in Q:
    L, gq_ = q['level'], bool(q.get('graph')); tx_ = ''.join(p['tw'] for p in q['parts'])
    if L not in (1, 2, 3, 4): errs.append((q['id'], 'level out of range')); continue
    if L in (1, 2) and gq_: errs.append((q['id'], 'road-graph question in level %d' % L))
    if L == 3 and not gq_: errs.append((q['id'], 'grid question in level 3'))
    if not isinstance(q.get('diff'), int): errs.append((q['id'], 'missing difficulty'))
    if L == 1:
        for w_ in ('過了', '看到', '經過', '紅綠燈', '過馬路', '個路口', '第'):
            if w_ in tx_: errs.append((q['id'], 'level 1 sentence uses ' + w_))
        if q.get('lights') or q['crosses']: errs.append((q['id'], 'level 1 has lights / crossings'))
    if not gq_ and L in (2, 4):
        if 'lights' not in q: errs.append((q['id'], 'grid question without traffic lights list'))
        for lx_, ly_ in q.get('lights', []):
            if deg(q['map'], lx_, ly_) < 3: errs.append((q['id'], 'traffic light on a corner'))
    if L == 2 and not any(k_ in tx_ for k_ in ('路口', '紅綠燈', '過了', '看到', '經過')): errs.append((q['id'], 'level 2 sentence with no counting / mark'))
    if not gq_ and '圓環' in tx_: errs.append((q['id'], 'roundabout on a grid map'))
by, bym = {}, {}
for q in Q:
    by[q['level']] = by.get(q['level'], 0) + 1
    bym[q['map']] = bym.get(q['map'], 0) + 1
print('per level:', by, '| per map:', bym)
print('with plan:', sum(1 for q in Q if q.get('plan')), '| with lights:', sum(1 for q in Q if q.get('lights')), '| 經過:', sum('經過' in ''.join(p['tw'] for p in q['parts']) for q in Q), '| 看到:', sum('看到' in ''.join(p['tw'] for p in q['parts']) for q in Q))
print('with crossing:', sum(1 for q in Q if q['crosses']), '| ERRORS:', len(errs))
for e in errs[:30]: print(' ', e)
sys.exit(1 if errs else 0)
