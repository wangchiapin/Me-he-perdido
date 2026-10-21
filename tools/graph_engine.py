# -*- coding: utf-8 -*-
"""Road-graph engine for level 5 (non-grid map): geometry, turn rules, roundabout exits, drawing data."""
import math, random
from graph_map import GRAPH

K = 2.3                 # layout scale
RW = 19                 # half road width
H = 35                  # half building tile
STRAIGHT = 25           # within this many degrees of straight ahead = "straight"
MINTURN, MAXTURN = 20, 160   # a turn is a branch between these angles on that side

NODES = {k: dict(p=(v['x'] * K, v['y'] * K), kind=v.get('kind', 'n'), stem=v.get('stem')) for k, v in GRAPH['nodes'].items()}
EDGES = {}
for e in GRAPH['edges']:
    a, b = NODES[e['a']]['p'], NODES[e['b']]['p']
    EDGES[e['id']] = dict(a=e['a'], b=e['b'], pts=[a] + [(x * K, y * K) for x, y in e['via']] + [b], L=e['L'], R=e['R'])
INC = {n: [e for e, v in EDGES.items() if n in (v['a'], v['b'])] for n in NODES}

def brg(p, q):                      # screen bearing in degrees: 0 = east, 90 = south (clockwise)
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
def adiff(a, b):                    # signed angle from a to b in (-180, 180]; positive = clockwise = a right turn
    d = (b - a + 180) % 360 - 180
    return 180 if d == -180 else d
def other(e, n): return EDGES[e]['b'] if EDGES[e]['a'] == n else EDGES[e]['a']
def opts(e, frm):                   # polyline of edge e starting at node frm
    p = EDGES[e]['pts']; return p if EDGES[e]['a'] == frm else p[::-1]
def out_bearing(n, e): p = opts(e, n); return brg(p[0], p[1])
def arr_heading(e, to): p = opts(e, other(e, to)); return brg(p[-2], p[-1])
def flank(e, frm):                  # (left building, right building) when walking e starting at frm
    v = EDGES[e]; return (v['L'], v['R']) if v['a'] == frm else (v['R'], v['L'])
def deg(n): return len(INC[n])

def turn_cands(n, h, side):
    """branches at node n on the given side of heading h: [(theta, edge)] sorted by closeness"""
    out = []
    for e in INC[n]:
        t = adiff(h, out_bearing(n, e))
        if side == 'R' and MINTURN < t < MAXTURN: out.append((t, e))
        if side == 'L' and -MAXTURN < t < -MINTURN: out.append((-t, e))
    return sorted(out)

def rb_exits(n, entry):             # exits counter-clockwise from the entry arm
    eb = out_bearing(n, entry)
    arms = [e for e in INC[n] if e != entry]
    return sorted(arms, key=lambda e: (eb - out_bearing(n, e)) % 360)

class GSim:
    def __init__(s, n, e):
        s.node, s.face, s.via = n, e, None
        s.h = out_bearing(n, e)
        s.path = [NODES[n]['p']]; s.crosses = []; s.actions = ''
        s.last = None; s.start = (n, e)
    def at_rb(s): return NODES[s.node]['kind'] == 'rb'
    def at_y_from_stem(s): return NODES[s.node]['kind'] == 'y' and s.via == NODES[s.node]['stem']
    def _walk(s, e):
        frm = s.node; p = opts(e, frm)
        s.path += p[1:]; s.node = other(e, frm); s.via = e; s.last = (e, frm)
        s.h = arr_heading(e, s.node); s.face = None
        if NODES[s.node]['kind'] != 'rb':
            c = [(abs(adiff(s.h, out_bearing(s.node, x))), x) for x in INC[s.node] if x != e]
            c = [t for t in c if t[0] <= STRAIGHT]
            if c: s.face = min(c)[1]
    def move(s):
        if s.face is None or s.at_rb(): return False
        s._walk(s.face); s.actions += 'S'; return True
    def turn(s, t):
        if s.at_rb(): return False
        c = turn_cands(s.node, s.h, t)
        if len(c) != 1: return False                     # nothing there, or two roads on that side: ambiguous
        s.face = c[0][1]; s.h = out_bearing(s.node, s.face); s.actions += t; return True
    def cross(s):
        if s.face is None or s.at_rb() or deg(s.node) < 3: return False
        s.crosses.append([s.node, s.face]); s.actions += 'C'; return True
    def roundabout(s, k):
        if not s.at_rb(): return False
        ex = rb_exits(s.node, s.via)
        if k > len(ex): return False
        s._walk(ex[k - 1]); s.actions += str(k); return True

# ---------- drawing ----------
def pd(p): return 'M' + ' L'.join('%.1f,%.1f' % q for q in p)

def build_drawing():
    """returns (svg_base, bpos, viewBox, cwd) ; buildings are drawn by the game from bpos"""
    segs = [(p[i - 1], p[i]) for v in EDGES.values() for p in [v['pts']] for i in range(1, len(p))]
    def dseg(px, py, a, b):
        (x1, y1), (x2, y2) = a, b; dx, dy = x2 - x1, y2 - y1; l2 = dx * dx + dy * dy
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / l2)); return math.hypot(px - x1 - t * dx, py - y1 - t * dy)
    rb = [v['p'] for v in NODES.values() if v['kind'] == 'rb'][0]
    placed = []
    def ok(cx, cy):
        if min(dseg(cx, cy, a, b) for a, b in segs) < RW + H * 0.9: return False
        if math.hypot(cx - rb[0], cy - rb[1]) < 40 + H + 6: return False
        for v in NODES.values():
            if v['kind'] == 'y' and math.hypot(cx - v['p'][0], cy - (v['p'][1] - 55)) < 92 + H * 0.6: return False
        return all(abs(cx - x) > 2 * H + 5 or abs(cy - y) > 2 * H + 5 for x, y in placed)
    bpos = {}
    for eid, v in EDGES.items():
        for side in 'LR':
            k = v[side]
            if not k: continue
            sg = 1 if side == 'L' else -1; p = v['pts']; best = None
            for off in (RW + H + 4, RW + H + 12, RW + H + 22, RW + H + 34):
                for i in range(1, len(p)):
                    (x1, y1), (x2, y2) = p[i - 1], p[i]; dx, dy = x2 - x1, y2 - y1; l = math.hypot(dx, dy); nx, ny = dy / l, -dx / l
                    for t in (.5, .4, .6, .3, .7, .22, .78, .15, .85):
                        cx, cy = x1 + dx * t + nx * sg * off, y1 + dy * t + ny * sg * off
                        if ok(cx, cy): best = (cx, cy); break
                    if best: break
                if best: break
            if not best:
                print('WARN no room for %s on %s' % (k, eid)); v[side] = None; continue
            placed.append(best); bpos[k] = [round(best[0], 1), round(best[1], 1)]
    h = []
    for v in EDGES.values(): h.append('<path d="%s" fill="none" stroke="#cfcabd" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>' % (pd(v['pts']), 2 * RW + 3))
    for v in EDGES.values(): h.append('<path d="%s" fill="none" stroke="#e7e3d9" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>' % (pd(v['pts']), 2 * RW))
    for k, n in NODES.items():
        if n['kind'] == 'n': h.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="#e7e3d9"/>' % (n['p'][0], n['p'][1], RW))
    # Y junction island
    cwd = {}
    for k, n in NODES.items():
        if n['kind'] != 'y': continue
        yy = n['p']; br = [e for e in INC[k] if e != n['stem']]
        def unit(e): b = math.radians(out_bearing(k, e)); return (math.cos(b), math.sin(b))
        u1, u2 = unit(br[0]), unit(br[1]); G = RW + 5
        def perp_in(u, v):
            d = u[0] * v[0] + u[1] * v[1]; w = (v[0] - d * u[0], v[1] - d * u[1]); l = math.hypot(*w); return (w[0] / l, w[1] / l)
        n1, n2 = perp_in(u1, u2), perp_in(u2, u1)
        o1 = (yy[0] + n1[0] * G, yy[1] + n1[1] * G); o2 = (yy[0] + n2[0] * G, yy[1] + n2[1] * G)
        det = u1[0] * (-u2[1]) - u1[1] * (-u2[0]); rx, ry = o2[0] - o1[0], o2[1] - o1[1]
        t = (rx * (-u2[1]) - ry * (-u2[0])) / det
        tip = (o1[0] + u1[0] * t, o1[1] + u1[1] * t); D = t + 70
        B1 = (o1[0] + u1[0] * D, o1[1] + u1[1] * D); B2 = (o2[0] + u2[0] * D, o2[1] + u2[1] * D)
        h.append('<path d="%sZ" fill="#cfdccb" stroke="#8a867c" stroke-width="1" stroke-linejoin="round"/>' % pd([tip, B1, B2]))
        cen = ((tip[0] + B1[0] + B2[0]) / 3, (tip[1] + B1[1] + B2[1]) / 3)
        h.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="#e7e3d9"/>' % (yy[0], yy[1], RW + 1))
        h.append('<circle cx="%.1f" cy="%.1f" r="8" fill="#fffefa" stroke="#8a867c"/><text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="700" fill="#2b2b2b">Y</text>' % (cen[0], cen[1], cen[0], cen[1] + 3.8))
    for k, n in NODES.items():
        if n['kind'] != 'rb': continue
        x, y = n['p']
        h.append('<circle cx="%.1f" cy="%.1f" r="40" fill="#e7e3d9" stroke="#bdb8aa"/><circle cx="%.1f" cy="%.1f" r="22" fill="#cfdccb" stroke="#8a867c"/>' % (x, y, x, y))
        h.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="700" fill="#4b4a46" class="rbl">圓環</text>' % (x, y + 4))
        for deg_ in (40, 160, 280):
            th = math.radians(deg_); px = x + math.cos(th) * 30; py = y - math.sin(th) * 30; tx = -math.sin(th); ty = -math.cos(th); nx, ny = -ty, tx
            h.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#8a867c"/>' % (px + tx * 5, py + ty * 5, px - tx * 3.5 + nx * 4, py - ty * 3.5 + ny * 4, px - tx * 3.5 - nx * 4, py - ty * 3.5 - ny * 4))
    for v in EDGES.values(): h.append('<path d="%s" fill="none" stroke="#d0cbbd" stroke-width="1" stroke-dasharray="5 6"/>' % pd(v['pts']))
    # crosswalks on every arm of every junction
    for k, n in NODES.items():
        if deg(k) < 3: continue
        d0 = {'rb': 52, 'y': 34}.get(n['kind'], 30); cwd[k] = d0
        for e in INC[k]:
            if n['kind'] == 'y' and e != n['stem']: dd = d0 + 6
            else: dd = d0
            p = opts(e, k)
            (x1, y1), (x2, y2) = p[0], p[1]; l = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / l, (y2 - y1) / l; nx, ny = -uy, ux
            for o in (-6, 0, 6):
                px, py = x1 + ux * (dd + o), y1 + uy * (dd + o)
                h.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#f8f6f0" stroke-width="3.4"/>' % (px - nx * RW * .95, py - ny * RW * .95, px + nx * RW * .95, py + ny * RW * .95))
    rnd = random.Random(7)
    for v in EDGES.values():
        p = v['pts']
        for i in range(1, len(p)):
            (x1, y1), (x2, y2) = p[i - 1], p[i]; dx, dy = x2 - x1, y2 - y1; l = math.hypot(dx, dy); nx, ny = dy / l, -dx / l
            for t in (.28, .72):
                for sg in (1, -1):
                    if rnd.random() < .5: continue
                    tx, ty = x1 + dx * t + nx * sg * (RW + 7), y1 + dy * t + ny * sg * (RW + 7)
                    if all(abs(tx - cx) > H + 3 or abs(ty - cy) > H + 3 for cx, cy in placed) and math.hypot(tx - rb[0], ty - rb[1]) > 50 and \
                       min(math.hypot(tx - n['p'][0], ty - n['p'][1]) for n in NODES.values()) > 34:
                        h.append('<g transform="translate(%.1f,%.1f)"><circle r="5" fill="#a9bfa7" stroke="#8a867c" stroke-width=".6"/><circle cx="-1.2" cy="-1.2" r="1.7" fill="#bccdb9"/></g>' % (tx, ty))
    xs = [x for x, _ in placed] + [q[0] for s in segs for q in s]; ys = [y for _, y in placed] + [q[1] for s in segs for q in s]
    vx, vy = min(xs) - H - 14, min(ys) - H - 14
    vb = [round(vx), round(vy), round(max(xs) + H + 14 - vx), round(max(ys) + H + 14 - vy)]
    return ''.join(h), bpos, vb, cwd
