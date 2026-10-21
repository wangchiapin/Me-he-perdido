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
    closed=[],
    blocks=[['bank', 'conv', 'post'],
            ['pharmacy', 'park', 'cafe'],
            ['bakery', 'book', 'bus']]),
 'station': dict(
    tw='車站前', cn='车站前', es='Frente a la estación', en='Station Front',
    closed=[(1, 0, 1, 1), (2, 0, 2, 1)],      # the road in front of the station is a plaza
    blocks=[['train', 'hotel', 'restaurant'],
            ['bus', 'market', 'bank'],
            ['post', 'breakfast', 'book']]),
 'night': dict(
    tw='夜市', cn='夜市', es='Mercado nocturno', en='Night Market',
    closed=[(0, 1, 1, 1), (2, 2, 2, 3), (2, 3, 3, 3)],   # narrow alleys and dead ends
    blocks=[['temple', 'snack', 'fruit'],
            ['drink', 'nightmkt', 'pharmacy'],
            ['mrt', 'conv', 'police']]),
 'campus': dict(
    tw='校園附近', cn='校园附近', es='Cerca de la escuela', en='Near the School',
    closed=[(1, 1, 1, 2), (1, 2, 2, 2)],      # the playground blocks two roads
    blocks=[['school', 'library', 'park'],
            ['book', 'cafe', 'bento'],
            ['bus', 'conv', 'noodle']]),
 'hospital': dict(
    tw='醫院附近', cn='医院附近', es='Cerca del hospital', en='Near the Hospital',
    closed=[(1, 0, 1, 1), (2, 0, 3, 0)],      # a dead-end lane
    blocks=[['hospital', 'pharmacy', 'clinic'],
            ['bus', 'park', 'breakfast'],
            ['bank', 'conv', 'post']]),
 'metro': dict(
    tw='捷運站出口', cn='捷运站出口', es='Salida del metro', en='MRT Exit',
    closed=[(0, 2, 1, 2), (2, 0, 2, 1), (1, 2, 1, 3)],
    blocks=[['mrt', 'cafe', 'drink'],
            ['conv', 'dept', 'cinema'],
            ['bank', 'laundry', 'salon']]),
}

for _m in MAPS.values():
    _m.setdefault('rb', []); _m.setdefault('ynodes', [])
BASIC = ('street', 'station', 'night', 'campus', 'hospital', 'metro')

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
ORD2 = {
    1: dict(tw='第一個', cn='第一个', py='dì yī ge', es='la primera', en='the first'),
    2: dict(tw='第二個', cn='第二个', py='dì èr ge', es='la segunda', en='the second'),
    3: dict(tw='第三個', cn='第三个', py='dì sān ge', es='la tercera', en='the third'),
    4: dict(tw='第四個', cn='第四个', py='dì sì ge', es='la cuarta', en='the fourth'),
}
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

def is_open(mp, x, y, d):
    """is there a road from (x,y) heading d?"""
    nx, ny = x + DX[d], y + DY[d]
    if not in_map(nx, ny):
        return False
    for (a, b, c, e) in MAPS[mp]['closed']:
        if {(a, b), (c, e)} == {(x, y), (nx, ny)}:
            return False
    return True

def degree(mp, x, y):
    return sum(1 for d in range(4) if is_open(mp, x, y, d))

def straight_through(mp, x, y, d):
    """arriving at (x,y) heading d: a plain stretch of road (no junction, no bend, no end)?"""
    return degree(mp, x, y) == 2 and is_open(mp, x, y, d)

class Sim:
    def __init__(s, mp, x, y, d):
        s.mp, s.x, s.y, s.d = mp, x, y, d
        s.actions, s.path, s.crosses = '', [(x, y)], []
        s.last = None            # (x,y,d) of the last travelled edge
        s.last_len = 0           # edges walked by the last S

    def at_rb(s):
        return (s.x, s.y) in MAPS[s.mp]['rb']

    def at_y_from_stem(s):
        return (s.x, s.y) in MAPS[s.mp]['ynodes'] and not is_open(s.mp, s.x, s.y, s.d)

    def exits(s):
        e = (s.d + 2) % 4
        return [(e - i) % 4 for i in (1, 2, 3) if is_open(s.mp, s.x, s.y, (e - i) % 4)]    # counter-clockwise

    def roundabout(s, k):
        ex = s.exits()
        if not s.at_rb() or k > len(ex):
            return False
        s.d = ex[k - 1]
        s.move(record=False)
        s.actions += str(k)
        return True

    def move(s, record=True):
        """S: walk to the next stop (junction, bend or dead end); plain straight road is passed over."""
        if not is_open(s.mp, s.x, s.y, s.d):
            return False
        n = 0
        while True:
            s.last = (s.x, s.y, s.d)
            s.x, s.y = s.x + DX[s.d], s.y + DY[s.d]
            s.path.append((s.x, s.y))
            n += 1
            if not straight_through(s.mp, s.x, s.y, s.d):
                break
        s.last_len = n
        if record:
            s.actions += 'S'
        return True

    def turn(s, t):
        s.d = (s.d + (1 if t == 'R' else 3)) % 4
        s.actions += t

    def cross(s):
        if not is_open(s.mp, s.x, s.y, s.d) or degree(s.mp, s.x, s.y) < 3:
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
            if k in ('turn', 'round', 'fork'):
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
    if k == 'torb':
        return dict(kind=k, tw=ptw + '直走到圓環', cn=pcn + '直走到圆环', py=ppy + 'zhí zǒu dào yuán huán',
                    es=pes + 'sigue recto hasta la rotonda', en=pen + 'go straight to the roundabout')
    if k == 'round':
        o = ORD2[st['k']]
        return dict(kind=k, tw=ptw + '從' + o['tw'] + '出口出去', cn=pcn + '从' + o['cn'] + '出口出去',
                    py=ppy + 'cóng ' + o['py'] + ' chū kǒu chū qù',
                    es=pes + 'sal por ' + o['es'] + ' salida', en=pen + 'take ' + o['en'] + ' exit')
    if k == 'toy':
        return dict(kind=k, tw=ptw + '直走到Y字路口', cn=pcn + '直走到Y字路口', py=ppy + 'zhí zǒu dào Y zì lù kǒu',
                    es=pes + 'sigue recto hasta la bifurcación en Y', en=pen + 'go straight to the Y-junction')
    if k == 'fork':
        s_ = {'L': ('靠左', '靠左', 'kào zuǒ', 've por la izquierda', 'keep left'), 'R': ('靠右', '靠右', 'kào yòu', 've por la derecha', 'keep right')}[st['t']]
        return dict(kind=k, tw=ptw + s_[0] + '走', cn=pcn + s_[1] + '走', py=ppy + s_[2] + ' zǒu', es=pes + s_[3], en=pen + s_[4])
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
        if c['kind'] in ('go1', 'go', 'pass', 'torb', 'toy'):
            moved = True
        if c['kind'] in ('turn', 'pass', 'round', 'fork') and moved:
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
MAX_MOVES = {1: 4, 2: 5, 3: 6, 4: 8, 5: 6}

def try_build(level, mp, rng):
    pat = rng.choice(PATTERNS[level])
    x, y, d = rng.randrange(W), rng.randrange(H), rng.randrange(4)
    if (x, y) in MAPS[mp]['rb']:
        return None
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
                if not sim.move() or degree(mp, sim.x, sim.y) < 3:
                    return None
            total += n
            steps.append(dict(kind='go', n=n, next=(len(steps) > 0 and n == 1 and rng.random() < 0.5)))
        elif kind == 'turn':
            t = rng.choice('LR')
            sim.turn(t)
            steps.append(dict(kind='turn', t=t))
        elif kind in ('torb', 'toy'):
            if not sim.move() or sim.last_len != 1:
                return None
            if kind == 'torb' and not sim.at_rb():
                return None
            if kind == 'toy' and not sim.at_y_from_stem():
                return None
            total += 1
            steps.append(dict(kind=kind))
        elif kind == 'round':
            if prev != 'torb':
                return None
            k = rng.choice([1, 2, 3])
            if not sim.roundabout(k):
                return None
            total += 1
            steps.append(dict(kind='round', k=k))
        elif kind == 'fork':
            if prev != 'toy':
                return None
            t_ = rng.choice('LR')
            sim.turn(t_)
            if not sim.move() or degree(mp, sim.x, sim.y) < 2:
                return None
            total += 1
            steps.append(dict(kind='fork', t=t_))
        elif kind == 'cross':
            if prev != 'go' or not sim.cross():
                return None
            steps.append(dict(kind='cross'))
        elif kind == 'pass':
            side = rng.choice('LR')
            cands, cx, cy, k = [], sim.x, sim.y, 0
            while is_open(mp, cx, cy, sim.d):
                f = flank(mp, cx, cy, sim.d)
                nx, ny = cx + DX[sim.d], cy + DY[sim.d]
                if not straight_through(mp, nx, ny, sim.d):       # a place where the walker stops
                    k += 1
                    if f[side] and k <= 4:
                        cands.append((k, nx, ny, f[side][0], f['L' if side == 'R' else 'R']))
                else:
                    pass
                cx, cy = nx, ny
            if not cands:
                return None
            k, tx, ty, bkey, opp = rng.choice(cands)
            for _ in range(k):
                sim.move()
            if (sim.x, sim.y) != (tx, ty):
                return None
            total += k
            okey = opp[0] if (opp and opp[0] and rng.random() < 0.55) else None
            turn = rng.choice('LR')
            sim.turn(turn)
            named += [bkey] + ([okey] if okey else [])
            steps.append(dict(kind='pass', side=side, b=bkey, opp=okey, turn=turn))
        if kind in ('go1', 'go', 'turn', 'pass', 'fork', 'cross') and (sim.at_rb() or sim.at_y_from_stem()):
            if not (kind == 'turn' and False):
                return None
        prev = kind if kind not in ('go1',) else 'go'
    if pat[-1] not in ('go', 'go1') or sim.last is None:
        return None
    if total < 2 or total > MAX_MOVES[level]:
        return None
    if (sim.x, sim.y) == (start[0], start[1]):
        return None
    if sim.last_len != 1:
        return None          # the destination must be beside a single block of road
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

# ---------- level 5: the non-grid real-street map ----------
import graph_engine as GE
GPATTERNS = [
    ['go1', 'turn', 'go1'], ['go1', 'turn', 'go1'], ['turn', 'go1', 'turn', 'go1'], ['go1', 'turn', 'go1', 'turn', 'go1'],
    ['torb', 'round', 'go1'], ['torb', 'round', 'go1'], ['go1', 'torb', 'round', 'go1'], ['torb', 'round', 'turn', 'go1'],
    ['turn', 'torb', 'round', 'go1'], ['toy', 'fork', 'go1'], ['go1', 'toy', 'fork', 'go1'], ['turn', 'toy', 'fork', 'go1'],
    ['pass', 'go'], ['go', 'turn', 'go'], ['go', 'pass', 'go'], ['turn', 'pass', 'go'],
    ['go', 'cross', 'go'], ['go', 'cross', 'go', 'turn', 'go'], ['go', 'turn', 'go', 'cross', 'go'],
]

def try_build_graph(rng):
    pat = rng.choice(GPATTERNS)
    n = rng.choice([k for k, v in GE.NODES.items() if v['kind'] != 'rb'])
    e = rng.choice(GE.INC[n])
    sim = GE.GSim(n, e)
    steps, named, total, prev = [], [], 0, None
    for kind in pat:
        if kind == 'go1':
            if not sim.move(): return None
            steps.append(dict(kind='go1')); total += 1
        elif kind == 'go':
            k = rng.choice([1, 1, 2])
            for _ in range(k):
                if not sim.move() or GE.deg(sim.node) < 3: return None
            total += k
            steps.append(dict(kind='go', n=k, next=(len(steps) > 0 and k == 1 and rng.random() < 0.5)))
        elif kind == 'turn':
            t = rng.choice('LR')
            if not sim.turn(t): return None
            steps.append(dict(kind='turn', t=t))
        elif kind in ('torb', 'toy'):
            if not sim.move(): return None
            if kind == 'torb' and not sim.at_rb(): return None
            if kind == 'toy' and not sim.at_y_from_stem(): return None
            total += 1; steps.append(dict(kind=kind))
        elif kind == 'round':
            if prev != 'torb': return None
            k = rng.choice([1, 2, 3, 4])
            if not sim.roundabout(k): return None
            total += 1; steps.append(dict(kind='round', k=k))
        elif kind == 'fork':
            if prev != 'toy': return None
            t = rng.choice('LR')
            if not sim.turn(t) or not sim.move(): return None
            total += 1; steps.append(dict(kind='fork', t=t))
        elif kind == 'cross':
            if prev != 'go' or not sim.cross(): return None
            steps.append(dict(kind='cross'))
        elif kind == 'pass':
            side = rng.choice('LR'); k = rng.choice([1, 1, 2])
            for _ in range(k):
                if not sim.move(): return None
            ed, frm = sim.last
            fl = GE.flank(ed, frm)
            bkey = fl[0] if side == 'L' else fl[1]
            if not bkey: return None
            opp = fl[1] if side == 'L' else fl[0]
            t = rng.choice('LR')
            if not sim.turn(t): return None
            okey = opp if (opp and rng.random() < 0.55) else None
            total += k; named += [bkey] + ([okey] if okey else [])
            steps.append(dict(kind='pass', side=side, b=bkey, opp=okey, turn=t))
        if kind in ('go1', 'go', 'turn', 'pass', 'fork', 'cross') and (sim.at_rb() or sim.at_y_from_stem()):
            return None
        prev = kind if kind != 'go1' else 'go'
    if pat[-1] not in ('go', 'go1') or sim.last is None: return None
    if total < 2 or total > MAX_MOVES[5] or sim.node == n: return None
    ed, frm = sim.last
    fl = GE.flank(ed, frm)
    sides = [s_ for s_, v in zip('LR', fl) if v]
    if not sides: return None
    side = rng.choice(sides)
    tkey = fl[0] if side == 'L' else fl[1]
    other = fl[1] if side == 'L' else fl[0]
    extra = ('opp', other) if (other and rng.random() < 0.5) else None
    if tkey in named or (extra and extra[1] in named): return None
    cons = assign_connectors(steps, 5)
    clauses = [render_step(st, cons[i], 5, rng) for i, st in enumerate(steps)]
    parts = make_parts(clauses, final_clause(tkey, side, extra))
    return dict(level=5, map='real', graph=True, start=[n, e], end=[sim.node, sim.via], actions=sim.actions,
                path=[[round(x, 1), round(y, 1)] for x, y in sim.path], crosses=sim.crosses,
                target=tkey, side=side, parts=parts)

def graph_map_data():
    svg, bpos, vb, cwd = GE.build_drawing()
    return dict(tw=GRAPH_TW['tw'], cn=GRAPH_TW['cn'], es=GRAPH_TW['es'], en=GRAPH_TW['en'], graph=True,
                blocks=[], closed=[], rb=[], ynodes=[], svg=svg, bpos=bpos, vb=vb, cwd=cwd,
                nodes={k: [round(v['p'][0], 1), round(v['p'][1], 1), v['kind'], v['stem']] for k, v in GE.NODES.items()},
                edges={k: dict(a=v['a'], b=v['b'], pts=[[round(x, 1), round(y, 1)] for x, y in v['pts']], L=v['L'], R=v['R']) for k, v in GE.EDGES.items()})

from graph_map import GRAPH as _G
GRAPH_TW = dict(tw=_G['tw'], cn=_G['cn'], es=_G['es'], en=_G['en'])

def main(per=12, per5=72, seed=20261020):
    rng = random.Random(seed)
    out = []
    GE.build_drawing()          # drops building slots that have no room (so the sentences never name them)
    for level in (1, 2, 3, 4, 5):
        for mp in (('real',) if level == 5 else BASIC):
            seen, made, tries, want = set(), 0, 0, (per5 if level == 5 else per)
            while made < want and tries < 60000:
                tries += 1
                q = try_build_graph(rng) if level == 5 else try_build(level, mp, rng)
                if not q:
                    continue
                key = ''.join(p['tw'] for p in q['parts'])
                if key in seen:
                    continue
                seen.add(key)
                made += 1
                q['id'] = '%s-L%d-%02d' % (mp, level, made)
                out.append(q)
            if made < want:
                print('WARN: only %d for %s L%d' % (made, mp, level), file=sys.stderr)
    return out

if __name__ == '__main__':
    qs = main()
    data = dict(buildings={k: dict(tw=v['tw'], cn=v['cn'], py=v['py'], es=v['es'], en=v['en']) for k, v in B.items()},
                maps={k: dict(tw=v['tw'], cn=v['cn'], es=v['es'], en=v['en'], blocks=v['blocks'], closed=[list(c) for c in v['closed']], rb=[list(c) for c in v['rb']], ynodes=[list(c) for c in v['ynodes']]) for k, v in MAPS.items()},
                questions=qs)
    data['maps']['real'] = graph_map_data()
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print('questions:', len(qs))
    if '--show' in sys.argv:
        for q in qs[::17][:14]:
            print(q['id'], q['actions'], q['target'], q['side'], q['crosses'])
            for p in q['parts']:
                print('   ', p['tw'], '|', p['es'])
