# -*- coding: utf-8 -*-
"""
問路小達人 — question generator.
Questions are built from structured steps, so the sentence (TW / CN / pinyin / ES / EN),
the correct route, the crossings and the destination always agree.
Output: questions.json  (read by verify_questions.py and build.py)

Action codes in `actions`:  S = walk to next intersection, L / R = turn, C = cross the street
"""
import json, random, sys

DX = [0, 1, 0, -1]      # N E S W
DY = [-1, 0, 1, 0]
W = H = 4               # intersections per side (3x3 blocks)

# ---------- vocabulary (Taiwan readings) ----------
B = {
 'bank':     dict(tw='銀行', cn='银行', py='yín háng', es='banco', es_art='el banco', en='bank', en_art='the bank'),
 'conv':     dict(tw='便利商店', cn='便利商店', py='biàn lì shāng diàn', es='tienda de conveniencia', es_art='la tienda de conveniencia', en='convenience store', en_art='the convenience store'),
 'post':     dict(tw='郵局', cn='邮局', py='yóu jú', es='correos', es_art='el correo', en='post office', en_art='the post office'),
 'pharmacy': dict(tw='藥局', cn='药局', py='yào jú', es='farmacia', es_art='la farmacia', en='pharmacy', en_art='the pharmacy'),
 'park':     dict(tw='公園', cn='公园', py='gōng yuán', es='parque', es_art='el parque', en='park', en_art='the park'),
 'cafe':     dict(tw='咖啡店', cn='咖啡店', py='kā fēi diàn', es='cafetería', es_art='la cafetería', en='café', en_art='the café'),
 'bakery':   dict(tw='麵包店', cn='面包店', py='miàn bāo diàn', es='panadería', es_art='la panadería', en='bakery', en_art='the bakery'),
 'book':     dict(tw='書店', cn='书店', py='shū diàn', es='librería', es_art='la librería', en='bookstore', en_art='the bookstore'),
 'bus':      dict(tw='公車站', cn='公车站', py='gōng chē zhàn', es='parada de autobús', es_art='la parada de autobús', en='bus stop', en_art='the bus stop'),
 'train':    dict(tw='火車站', cn='火车站', py='huǒ chē zhàn', es='estación de tren', es_art='la estación de tren', en='train station', en_art='the train station'),
 'hotel':    dict(tw='飯店', cn='饭店', py='fàn diàn', es='hotel', es_art='el hotel', en='hotel', en_art='the hotel'),
 'restaurant': dict(tw='餐廳', cn='餐厅', py='cān tīng', es='restaurante', es_art='el restaurante', en='restaurant', en_art='the restaurant'),
 'market':   dict(tw='超市', cn='超市', py='chāo shì', es='supermercado', es_art='el supermercado', en='supermarket', en_art='the supermarket'),
 'breakfast': dict(tw='早餐店', cn='早餐店', py='zǎo cān diàn', es='desayunería', es_art='la desayunería', en='breakfast shop', en_art='the breakfast shop'),
 'temple':   dict(tw='廟', cn='庙', py='miào', es='templo', es_art='el templo', en='temple', en_art='the temple'),
 'snack':    dict(tw='小吃攤', cn='小吃摊', py='xiǎo chī tān', es='puesto de comida', es_art='el puesto de comida', en='snack stall', en_art='the snack stall'),
 'fruit':    dict(tw='水果攤', cn='水果摊', py='shuǐ guǒ tān', es='puesto de frutas', es_art='el puesto de frutas', en='fruit stand', en_art='the fruit stand'),
 'drink':    dict(tw='飲料店', cn='饮料店', py='yǐn liào diàn', es='tienda de bebidas', es_art='la tienda de bebidas', en='drink shop', en_art='the drink shop'),
 'nightmkt': dict(tw='夜市', cn='夜市', py='yè shì', es='mercado nocturno', es_art='el mercado nocturno', en='night market', en_art='the night market'),
 'mrt':      dict(tw='捷運站', cn='捷运站', py='jié yùn zhàn', es='estación de metro', es_art='la estación de metro', en='MRT station', en_art='the MRT station'),
 'police':   dict(tw='警察局', cn='警察局', py='jǐng chá jú', es='comisaría', es_art='la comisaría', en='police station', en_art='the police station'),
 # --- new ---
 'school':   dict(tw='學校', cn='学校', py='xué xiào', es='escuela', es_art='la escuela', en='school', en_art='the school'),
 'library':  dict(tw='圖書館', cn='图书馆', py='tú shū guǎn', es='biblioteca', es_art='la biblioteca', en='library', en_art='the library'),
 'hospital': dict(tw='醫院', cn='医院', py='yī yuàn', es='hospital', es_art='el hospital', en='hospital', en_art='the hospital'),
 'clinic':   dict(tw='診所', cn='诊所', py='zhěn suǒ', es='clínica', es_art='la clínica', en='clinic', en_art='the clinic'),
 'noodle':   dict(tw='麵店', cn='面店', py='miàn diàn', es='tienda de fideos', es_art='la tienda de fideos', en='noodle shop', en_art='the noodle shop'),
 'bento':    dict(tw='便當店', cn='便当店', py='biàn dāng diàn', es='tienda de loncheras', es_art='la tienda de loncheras', en='lunch-box shop', en_art='the lunch-box shop'),
 'dept':     dict(tw='百貨公司', cn='百货公司', py='bǎi huò gōng sī', es='centro comercial', es_art='el centro comercial', en='department store', en_art='the department store'),
 'cinema':   dict(tw='電影院', cn='电影院', py='diàn yǐng yuàn', es='cine', es_art='el cine', en='cinema', en_art='the cinema'),
 'laundry':  dict(tw='洗衣店', cn='洗衣店', py='xǐ yī diàn', es='lavandería', es_art='la lavandería', en='laundry', en_art='the laundry'),
 'salon':    dict(tw='髮廊', cn='发廊', py='fà láng', es='peluquería', es_art='la peluquería', en='hair salon', en_art='the hair salon'),
}

MAPS = {
 'street': dict(
    tw='便利商店街', cn='便利商店街', es='Calle comercial', en='Shopping Street',
    blocks=[['bank', 'conv', 'post'],
            ['pharmacy', 'park', 'cafe'],
            ['bakery', 'book', 'bus']]),
 'station': dict(
    tw='車站前', cn='车站前', es='Frente a la estación', en='Station Front',
    blocks=[['train', 'hotel', 'restaurant'],
            ['bus', 'market', 'bank'],
            ['post', 'breakfast', 'book']]),
 'night': dict(
    tw='夜市', cn='夜市', es='Mercado nocturno', en='Night Market',
    blocks=[['temple', 'snack', 'fruit'],
            ['drink', 'nightmkt', 'pharmacy'],
            ['mrt', 'conv', 'police']]),
 'campus': dict(
    tw='校園附近', cn='校园附近', es='Cerca de la escuela', en='Near the School',
    blocks=[['school', 'library', 'park'],
            ['book', 'cafe', 'bento'],
            ['bus', 'conv', 'noodle']]),
 'hospital': dict(
    tw='醫院附近', cn='医院附近', es='Cerca del hospital', en='Near the Hospital',
    blocks=[['hospital', 'pharmacy', 'clinic'],
            ['bus', 'park', 'breakfast'],
            ['bank', 'conv', 'post']]),
 'metro': dict(
    tw='捷運站出口', cn='捷运站出口', es='Salida del metro', en='MRT Exit',
    blocks=[['mrt', 'cafe', 'drink'],
            ['conv', 'dept', 'cinema'],
            ['bank', 'laundry', 'salon']]),
}

# ---------- phrase pieces ----------
TURN = {
    'L': dict(tw='左轉', cn='左转', py='zuǒ zhuǎn', es='gira a la izquierda', en='turn left'),
    'R': dict(tw='右轉', cn='右转', py='yòu zhuǎn', es='gira a la derecha', en='turn right'),
}
HAND = {
    'L': dict(tw='左手邊', cn='左手边', py='zuǒ shǒu biān', es='izquierda', en='left'),
    'R': dict(tw='右手邊', cn='右手边', py='yòu shǒu biān', es='derecha', en='right'),
}
ORD = {
    1: dict(tw='第一個路口', cn='第一个路口', py='dì yī ge lù kǒu', es='la primera intersección', en='the first intersection'),
    2: dict(tw='第二個路口', cn='第二个路口', py='dì èr ge lù kǒu', es='la segunda intersección', en='the second intersection'),
    3: dict(tw='第三個路口', cn='第三个路口', py='dì sān ge lù kǒu', es='la tercera intersección', en='the third intersection'),
    'next': dict(tw='下一個路口', cn='下一个路口', py='xià yí ge lù kǒu', es='la siguiente intersección', en='the next intersection'),
}
# connectors:  (tw, cn, pinyin, es, en)
CON = [
    ('先', '先', 'xiān', 'primero', 'first'),
    ('然後', '然后', 'rán hòu', 'luego', 'then'),
    ('再', '再', 'zài', 'después', 'next'),
    ('最後', '最后', 'zuì hòu', 'por último', 'finally'),
]

def cap(s):
    return s[0].upper() + s[1:] if s else s

# ---------- geometry ----------
def block_at(mp, bx, by):
    if 0 <= bx < W - 1 and 0 <= by < H - 1:
        return MAPS[mp]['blocks'][by][bx]
    return None

def flank(mp, x, y, d):
    """buildings on each side of the segment leaving (x,y) heading d -> {'L': (key,(bx,by)) | None, 'R': ...}"""
    mx, my = x + DX[d] / 2.0, y + DY[d] / 2.0
    out = {}
    for side, sd in (('L', (d + 3) % 4), ('R', (d + 1) % 4)):
        cx, cy = mx + 0.5 * DX[sd], my + 0.5 * DY[sd]
        bx, by = int(round(cx - 0.5)), int(round(cy - 0.5))
        k = block_at(mp, bx, by)
        out[side] = (k, (bx, by)) if k else None
    return out

def in_map(x, y):
    return 0 <= x < W and 0 <= y < H

class Sim:
    def __init__(s, mp, x, y, d):
        s.mp, s.x, s.y, s.d = mp, x, y, d
        s.actions, s.path, s.crosses = '', [(x, y)], []
        s.last = None            # (x,y,d) of last travelled segment

    def move(s):
        nx, ny = s.x + DX[s.d], s.y + DY[s.d]
        if not in_map(nx, ny):
            return False
        s.last = (s.x, s.y, s.d)
        s.x, s.y = nx, ny
        s.actions += 'S'
        s.path.append((nx, ny))
        return True

    def turn(s, t):
        s.d = (s.d + (1 if t == 'R' else 3)) % 4
        s.actions += t

    def cross(s):
        if not in_map(s.x + DX[s.d], s.y + DY[s.d]):
            return False
        s.actions += 'C'
        s.crosses.append([s.x, s.y, s.d])
        return True

# ---------- rendering of steps into clauses ----------
def assign_connectors(steps, level):
    n = len(steps)
    cons, alt = [None] * n, 0
    for i, st in enumerate(steps):
        k = st['kind']
        if k == 'cross':
            continue
        if level == 1:
            if i == 0:
                con = 0
            elif i == n - 1 and n >= 3:
                con = 3
            else:
                con = 1 if alt % 2 == 0 else 2
                alt += 1
        else:
            if k == 'turn':
                con = 0 if i == 0 else None
            elif i == 0:
                con = None
            elif i == n - 1:
                con = 3
            else:
                con = 1 if alt % 2 == 0 else 2
                alt += 1
        cons[i] = con
    return cons

def pre(con):
    if con is None:
        return '', '', '', '', ''
    c = CON[con]
    return c[0], c[1], c[2] + ' ', c[3] + ' ', c[4] + ' '

def render_step(st, con, level, rng):
    k = st['kind']
    ptw, pcn, ppy, pes, pen = pre(con)
    if k == 'go1':
        return dict(kind=k, tw=ptw + '直走', cn=pcn + '直走', py=ppy + 'zhí zǒu',
                    es=pes + 'sigue recto', en=pen + 'go straight')
    if k == 'turn':
        t = TURN[st['t']]
        return dict(kind=k, tw=ptw + t['tw'], cn=pcn + t['cn'], py=ppy + t['py'],
                    es=pes + t['es'], en=pen + t['en'])
    if k == 'go':
        o = ORD['next' if st.get('next') else st['n']]
        return dict(kind=k, tw=ptw + '直走到' + o['tw'], cn=pcn + '直走到' + o['cn'],
                    py=ppy + 'zhí zǒu dào ' + o['py'],
                    es=pes + 'sigue recto hasta ' + o['es'], en=pen + 'go straight to ' + o['en'])
    if k == 'cross':
        return dict(kind=k, tw='過馬路', cn='过马路', py='guò mǎ lù', es='cruza la calle', en='cross the street')
    if k == 'pass':
        b, h, t = B[st['b']], HAND[st['side']], TURN[st['turn']]
        tw = ptw + '一直走，' + h['tw'] + '是' + b['tw']
        cn = pcn + '一直走，' + h['cn'] + '是' + b['cn']
        py = ppy + 'yì zhí zǒu, ' + h['py'] + ' shì ' + b['py']
        es = pes + 'sigue recto, a tu ' + h['es'] + ' está ' + b['es_art']
        en = pen + 'keep going straight, ' + b['en_art'] + ' is on your ' + h['en']
        if st.get('opp'):
            o = B[st['opp']]
            tw += '，對面是' + o['tw']; cn += '，对面是' + o['cn']
            py += ', duì miàn shì ' + o['py']
            es += ', enfrente está ' + o['es_art']
            en += ', across the street is ' + o['en_art']
        tw += '，過了' + b['tw'] + '就' + t['tw']
        cn += '，过了' + b['cn'] + '就' + t['cn']
        py += ', guò le ' + b['py'] + ' jiù ' + t['py']
        es += ', y después de pasar ' + b['es_art'] + ' ' + t['es']
        en += ', and after you pass ' + b['en_art'] + ', ' + t['en']
        return dict(kind=k, tw=tw, cn=cn, py=py, es=es, en=en)
    raise ValueError(k)

def final_clause(tkey, side, extra):
    t, h = B[tkey], HAND[side]
    tw = t['tw'] + '就在你的' + h['tw']
    cn = t['cn'] + '就在你的' + h['cn']
    py = t['py'] + ' jiù zài nǐ de ' + h['py']
    es = t['es_art'] + ' está a tu ' + h['es']
    en = t['en_art'] + ' is on your ' + h['en']
    if extra:
        kind, k = extra
        o = B[k]
        if kind == 'opp':
            tw += '，對面是' + o['tw']; cn += '，对面是' + o['cn']
            py += ', duì miàn shì ' + o['py']
            es += ', y enfrente está ' + o['es_art']
            en += ', and across the street is ' + o['en_art']
        else:
            tw += '，旁邊是' + o['tw']; cn += '，旁边是' + o['cn']
            py += ', páng biān shì ' + o['py']
            es += ', y al lado está ' + o['es_art']
            en += ', and next to it is ' + o['en_art']
    return dict(tw=tw, cn=cn, py=py, es=es, en=en)

def part_from(clauses):
    return dict(
        tw='，'.join(c['tw'] for c in clauses) + '。',
        cn='，'.join(c['cn'] for c in clauses) + '。',
        py=cap(', '.join(c['py'] for c in clauses)) + '.',
        es=cap(', '.join(c['es'] for c in clauses)) + '.',
        en=cap(', '.join(c['en'] for c in clauses)) + '.',
    )

def make_parts(clauses, fin):
    """split the route into listening parts: a part ends after a turn (or a 'pass' clause)
    once it contains some walking; the destination sentence is the last part."""
    parts, cur, moved = [], [], False
    for c in clauses:
        cur.append(c)
        if c['kind'] in ('go1', 'go', 'pass'):
            moved = True
        if c['kind'] in ('turn', 'pass') and moved:
            parts.append(part_from(cur)); cur, moved = [], False
    if cur:
        parts.append(part_from(cur))
    parts.append(part_from([fin]))
    return parts

# ---------- patterns per level ----------
PATTERNS = {
    1: [['go1', 'turn', 'go1'], ['go1', 'turn', 'go1'], ['go1', 'turn', 'go1'],
        ['turn', 'go1', 'turn', 'go1'], ['turn', 'go1', 'turn', 'go1'],
        ['go1', 'turn', 'go1', 'turn', 'go1']],
    2: [['go', 'turn', 'go'], ['go', 'cross', 'go'], ['go', 'cross', 'go', 'turn', 'go'],
        ['turn', 'go', 'turn', 'go'], ['go', 'turn', 'go', 'cross', 'go']],
    3: [['pass', 'go'], ['pass', 'go'], ['turn', 'pass', 'go'], ['go', 'turn', 'go'], ['go', 'cross', 'go']],
    4: [['go', 'turn', 'pass', 'go'], ['pass', 'go', 'cross', 'go'], ['turn', 'go', 'cross', 'go', 'turn', 'go'],
        ['go', 'turn', 'go', 'pass', 'go'], ['pass', 'go', 'turn', 'go']],
}
MAX_MOVES = {1: 4, 2: 5, 3: 6, 4: 8}

def try_build(level, mp, rng):
    pat = rng.choice(PATTERNS[level])
    x, y, d = rng.randrange(W), rng.randrange(H), rng.randrange(4)
    sim = Sim(mp, x, y, d)
    start = (x, y, d)
    steps, named, total = [], [], 0
    prev = None
    for kind in pat:
        if kind == 'go1':
            if not sim.move():
                return None
            steps.append(dict(kind='go1')); total += 1
        elif kind == 'go':
            n = rng.choice([1, 2, 2, 3])
            for _ in range(n):
                if not sim.move():
                    return None
            total += n
            steps.append(dict(kind='go', n=n, next=(len(steps) > 0 and n == 1 and rng.random() < 0.5)))
        elif kind == 'turn':
            t = rng.choice('LR')
            sim.turn(t)
            steps.append(dict(kind='turn', t=t))
        elif kind == 'cross':
            if prev != 'go' or not sim.cross():
                return None
            steps.append(dict(kind='cross'))
        elif kind == 'pass':
            side = rng.choice('LR')
            cands, cx, cy, k = [], sim.x, sim.y, 0
            while in_map(cx + DX[sim.d], cy + DY[sim.d]):
                f = flank(mp, cx, cy, sim.d)
                k += 1
                if f[side]:
                    cands.append((k, f[side][0], f['L' if side == 'R' else 'R']))
                cx, cy = cx + DX[sim.d], cy + DY[sim.d]
            if not cands:
                return None
            k, bkey, opp = rng.choice(cands)
            for _ in range(k):
                sim.move()
            total += k
            okey = opp[0] if (opp and opp[0] and rng.random() < 0.55) else None
            turn = rng.choice('LR')
            sim.turn(turn)
            named += [bkey] + ([okey] if okey else [])
            steps.append(dict(kind='pass', side=side, b=bkey, opp=okey, turn=turn))
        prev = kind if kind != 'go1' else 'go'
    if pat[-1] not in ('go', 'go1') or sim.last is None:
        return None
    if total < 2 or total > MAX_MOVES[level]:
        return None
    if (sim.x, sim.y) == (start[0], start[1]):
        return None
    # destination
    lx, ly, ld = sim.last
    f = flank(mp, lx, ly, ld)
    sides = [s for s in 'LR' if f[s]]
    if not sides:
        return None
    side = rng.choice(sides)
    tkey = f[side][0]
    other = 'L' if side == 'R' else 'R'
    extra = None
    if level >= 3:
        r = rng.random()
        if r < 0.45 and f[other]:
            extra = ('opp', f[other][0])
        elif r < 0.9:
            bx, by = f[side][1]
            nbrs = [k for sgn in (1, -1)
                    for k in [block_at(mp, bx + sgn * DX[ld], by + sgn * DY[ld])] if k]
            if nbrs:
                extra = ('next', rng.choice(nbrs))
    if tkey in named or (extra and extra[1] in named):
        return None
    cons = assign_connectors(steps, level)
    clauses = [render_step(st, cons[i], level, rng) for i, st in enumerate(steps)]
    parts = make_parts(clauses, final_clause(tkey, side, extra))
    return dict(
        level=level, map=mp,
        start=list(start), end=[sim.x, sim.y, sim.d],
        actions=sim.actions, path=[list(p) for p in sim.path], crosses=sim.crosses,
        target=tkey, side=side, parts=parts,
    )

def main(per=12, seed=20261020):
    rng = random.Random(seed)
    out = []
    for level in (1, 2, 3, 4):
        for mp in MAPS:
            seen, made, tries = set(), 0, 0
            while made < per and tries < 30000:
                tries += 1
                q = try_build(level, mp, rng)
                if not q:
                    continue
                key = ''.join(p['tw'] for p in q['parts'])
                if key in seen:
                    continue
                seen.add(key)
                made += 1
                q['id'] = '%s-L%d-%02d' % (mp, level, made)
                out.append(q)
            if made < per:
                print('WARN: only %d for %s L%d' % (made, mp, level), file=sys.stderr)
    return out

if __name__ == '__main__':
    qs = main()
    data = dict(buildings={k: dict(tw=v['tw'], cn=v['cn'], py=v['py'], es=v['es'], en=v['en']) for k, v in B.items()},
                maps={k: dict(tw=v['tw'], cn=v['cn'], es=v['es'], en=v['en'], blocks=v['blocks']) for k, v in MAPS.items()},
                questions=qs)
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print('questions:', len(qs))
    if '--show' in sys.argv:
        for q in qs[::17][:14]:
            print(q['id'], q['actions'], q['target'], q['side'], q['crosses'])
            for p in q['parts']:
                print('   ', p['tw'], '|', p['es'])
