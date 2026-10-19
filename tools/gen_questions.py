# -*- coding: utf-8 -*-
"""
問路小達人 — question generator.
Builds questions from structured steps so that the sentence (TW/CN/pinyin/ES/EN),
the correct route and the destination always agree. Output: questions.json
"""
import json, random, sys

DX = [0, 1, 0, -1]      # N E S W
DY = [-1, 0, 1, 0]
W = H = 4               # intersections per side (3x3 blocks)

# ---------- vocabulary ----------
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
}

# ---------- tiny phrase helper ----------
class P:
    def __init__(s, tw, cn, py, es, en):
        s.tw, s.cn, s.py, s.es, s.en = tw, cn, py, es, en

def cap(s):
    return s[0].upper() + s[1:] if s else s

def join_clauses(cl):
    """join clauses of one sentence -> (tw, cn, py, es, en) without final stop"""
    return (
        '，'.join(c.tw for c in cl),
        '，'.join(c.cn for c in cl),
        ', '.join(c.py for c in cl),
        ', '.join(c.es for c in cl),
        ', '.join(c.en for c in cl),
    )

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
    4: dict(tw='第四個路口', cn='第四个路口', py='dì sì ge lù kǒu', es='la cuarta intersección', en='the fourth intersection'),
    'next': dict(tw='下一個路口', cn='下一个路口', py='xià yí ge lù kǒu', es='la siguiente intersección', en='the next intersection'),
}

# ---------- geometry ----------
def block_at(mp, bx, by):
    if 0 <= bx < W - 1 and 0 <= by < H - 1:
        return MAPS[mp]['blocks'][by][bx]
    return None

def flank(mp, x, y, d):
    """buildings on each side of the segment leaving (x,y) heading d -> dict L/R -> (key, (bx,by)) or None"""
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

# ---------- simulation of structured steps ----------
class Sim:
    def __init__(s, mp, x, y, d):
        s.mp, s.x, s.y, s.d = mp, x, y, d
        s.actions, s.path = '', [(x, y)]
        s.last = None            # (x,y,d) of last travelled segment start

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

# ---------- sentence construction ----------
def clause_go(first, n, level, rng, used_next):
    """a 'go' clause"""
    if level == 1:
        pre = ('先', 'xiān', 'Primero', 'First') if first else ('再', 'zài', 'luego', 'then')
        return P(pre[0] + '直走', pre[0] + '直走', pre[1] + ' zhí zǒu',
                 (pre[2] + ' sigue recto'), (pre[3] + ' go straight'))
    key = 'next' if (used_next and n == 1) else n
    o = ORD[key]
    pre_tw = '' if first else '再'
    pre_py = '' if first else 'zài '
    es = ('' if first else 'luego ') + 'sigue recto hasta ' + o['es']
    en = ('' if first else 'then ') + 'go straight to ' + o['en']
    return P(pre_tw + '直走到' + o['tw'], pre_tw + '直走到' + o['cn'],
             pre_py + 'zhí zǒu dào ' + o['py'], es, en)

def clause_turn(t, ctx, level):
    tr = TURN[t]
    if level == 1:
        pre = ('先', 'xiān', 'Primero', 'First') if ctx == 'first' else ('再', 'zài', 'luego', 'then')
        return P(pre[0] + tr['tw'], pre[0] + tr['cn'], pre[1] + ' ' + tr['py'],
                 pre[2] + ' ' + tr['es'], pre[3] + ' ' + tr['en'])
    if ctx == 'first':
        return P('先' + tr['tw'], '先' + tr['cn'], 'xiān ' + tr['py'], 'primero ' + tr['es'], 'first ' + tr['en'])
    if ctx == 'cross':
        return P('再' + tr['tw'], '再' + tr['cn'], 'zài ' + tr['py'], 'luego ' + tr['es'], 'then ' + tr['en'])
    return P(tr['tw'], tr['cn'], tr['py'], tr['es'], tr['en'])

def clause_cross():
    return P('過馬路', '过马路', 'guò mǎ lù', 'cruza la calle', 'cross the street')

def clause_pass(first, side, bkey, okey, turn):
    b = B[bkey]
    h = HAND[side]
    pre_tw = '' if first else '再'
    pre_py = '' if first else 'zài '
    pre_es = '' if first else 'luego '
    pre_en = '' if first else 'then '
    tw = pre_tw + '一直走，' + h['tw'] + '是' + b['tw']
    cn = pre_tw + '一直走，' + h['cn'] + '是' + b['cn']
    py = pre_py + 'yì zhí zǒu, ' + h['py'] + ' shì ' + b['py']
    es = pre_es + 'sigue recto, a tu ' + h['es'] + ' está ' + b['es_art']
    en = pre_en + 'keep going straight, ' + b['en_art'] + ' is on your ' + h['en']
    if okey:
        o = B[okey]
        tw += '，對面是' + o['tw']
        cn += '，对面是' + o['cn']
        py += ', duì miàn shì ' + o['py']
        es += ', enfrente está ' + o['es_art']
        en += ', across the street is ' + o['en_art']
    t = TURN[turn]
    tw += '，過了' + b['tw'] + '就' + t['tw']
    cn += '，过了' + b['cn'] + '就' + t['cn']
    py += ', guò le ' + b['py'] + ' jiù ' + t['py']
    es += ', y después de pasar ' + b['es_art'] + ' ' + t['es']
    en += ', and after you pass ' + b['en_art'] + ', ' + t['en']
    return P(tw, cn, py, es, en)

def final_sentence(tkey, side, extra):
    """extra: None | ('opp', key) | ('next', key)"""
    t = B[tkey]
    h = HAND[side]
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
    return P(tw, cn, py, es, en)

def cap_py(s):
    return cap(s)

# ---------- patterns per level ----------
PATTERNS = {
    1: [['go1', 'turn', 'go1'], ['go1', 'turn', 'go1'], ['turn', 'go1', 'turn', 'go1'],
        ['go1', 'go1', 'turn', 'go1'], ['go1', 'turn', 'go1', 'turn', 'go1']],
    2: [['go', 'turn', 'go'], ['go', 'cross', 'go', 'turn', 'go'], ['turn', 'go', 'turn', 'go'],
        ['go', 'turn', 'go', 'cross', 'go'], ['go', 'cross', 'go']],
    3: [['pass', 'go'], ['pass', 'go'], ['turn', 'pass', 'go'], ['go', 'turn', 'go'], ['go', 'cross', 'go']],
    4: [['go', 'turn', 'pass', 'go'], ['pass', 'go', 'cross', 'go'], ['turn', 'go', 'cross', 'go', 'turn', 'go'],
        ['go', 'turn', 'go', 'pass', 'go'], ['pass', 'go', 'turn', 'go']],
}

def try_build(level, mp, rng):
    pat = rng.choice(PATTERNS[level])
    x, y, d = rng.randrange(W), rng.randrange(H), rng.randrange(4)
    sim = Sim(mp, x, y, d)
    start = (x, y, d)
    clauses = []
    named = []                     # buildings mentioned (must stay distinct)
    ctx_prev = 'first'
    first = True
    total_moves = 0
    for i, kind in enumerate(pat):
        if kind == 'go1':
            if not sim.move():
                return None
            clauses.append(clause_go(first, 1, 1, rng, False))
            total_moves += 1
        elif kind == 'go':
            n = rng.choice([1, 2, 2, 3])
            for _ in range(n):
                if not sim.move():
                    return None
            total_moves += n
            used_next = (not first) and rng.random() < 0.5
            clauses.append(clause_go(first, n, level, rng, used_next))
        elif kind == 'turn':
            t = rng.choice('LR')
            sim.turn(t)
            clauses.append(clause_turn(t, 'first' if first else ctx_prev, level))
        elif kind == 'cross':
            # straight through the intersection: no position change, just narrative
            if ctx_prev not in ('go',):
                return None
            clauses.append(clause_cross())
        elif kind == 'pass':
            side = rng.choice('LR')
            # scan ahead along heading for a building on that side
            cands = []
            cx, cy = sim.x, sim.y
            k = 0
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
            total_moves += k
            okey = None
            if opp and opp[0] and rng.random() < 0.55:
                okey = opp[0]
            turn = rng.choice('LR')
            sim.turn(turn)
            named += [bkey] + ([okey] if okey else [])
            clauses.append(clause_pass(first, side, bkey, okey, turn))
        ctx_prev = kind if kind in ('go', 'go1', 'cross', 'pass', 'turn') else kind
        if kind == 'go1':
            ctx_prev = 'go'
        first = False
    if pat[-1] not in ('go', 'go1') or sim.last is None:
        return None
    if total_moves < 2 or total_moves > {1: 4, 2: 5, 3: 6, 4: 8}[level]:
        return None
    if (sim.x, sim.y) == (start[0], start[1]):
        return None
    # destination clause
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
            nbrs = []
            for sgn in (1, -1):
                k = block_at(mp, bx + sgn * DX[ld], by + sgn * DY[ld])
                if k:
                    nbrs.append(k)
            if nbrs:
                extra = ('next', rng.choice(nbrs))
    if tkey in named:
        return None
    if extra and extra[1] in named:
        return None
    # assemble text
    tw1, cn1, py1, es1, en1 = join_clauses(clauses)
    fin = final_sentence(tkey, side, extra)
    text = dict(
        tw=tw1 + '。' + fin.tw + '。',
        cn=cn1 + '。' + fin.cn + '。',
        py=cap(py1) + '. ' + cap(fin.py) + '.',
        es=cap(es1) + '. ' + cap(fin.es) + '.',
        en=cap(en1) + '. ' + cap(fin.en) + '.',
    )
    # build the node path as the list of visited nodes (consecutive duplicates removed)
    return dict(
        level=level, map=mp,
        start=list(start), end=[sim.x, sim.y, sim.d],
        actions=sim.actions, path=[list(p) for p in sim.path],
        target=tkey, side=side,
        **text,
    )

def main(per=10, seed=20261020):
    rng = random.Random(seed)
    out = []
    for level in (1, 2, 3, 4):
        for mp in MAPS:
            seen, made, tries = set(), 0, 0
            while made < per and tries < 20000:
                tries += 1
                q = try_build(level, mp, rng)
                if not q or q['tw'] in seen:
                    continue
                seen.add(q['tw'])
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
    for q in qs[:2] + qs[10:12] + qs[20:22] + qs[30:32] + qs[60:62] + qs[90:92]:
        print(q['id'], q['actions'], q['target'], q['side'])
        print('  ', q['tw'])
        print('  ', q['py'])
        print('  ', q['es'])
        print('  ', q['en'])
