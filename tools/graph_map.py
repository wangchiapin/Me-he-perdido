# -*- coding: utf-8 -*-
"""The non-grid neighbourhood used by level 5 (real-street map).
Coordinates are in a 0..300 drawing space (graph_engine scales them).
Every edge is a road between two nodes; `via` are bend points; L / R are the buildings on the
left / right of the road when walking a -> b (at most one per side).
Design rule: the ring road runs (almost) straight through its T junctions, and each arm of the
roundabout joins it from the inside, so a left / right turn is never ambiguous."""

GRAPH = dict(
    tw='真實街區', cn='真实街区', es='Barrio real', en='Real Neighborhood',
    nodes={
        'rb': dict(x=150, y=125, kind='rb'),
        'A': dict(x=95,  y=16),
        'B': dict(x=228, y=24),
        'C': dict(x=288, y=118),
        'D': dict(x=256, y=200),
        'E': dict(x=22,  y=150),
        'y1': dict(x=150, y=262, kind='y', stem='e12'),
        'n8': dict(x=150, y=318),
    },
    edges=[
        dict(id='e1',  a='rb', b='A',  via=[(118, 72)],  L='bakery',   R='bank'),
        dict(id='e2',  a='rb', b='B',  via=[],           L='cafe',     R='park'),
        dict(id='e3',  a='rb', b='C',  via=[],           L='hospital', R='conv'),
        dict(id='e4',  a='rb', b='D',  via=[],           L='dept',     R='cinema'),
        dict(id='e5',  a='rb', b='E',  via=[(88, 142)],  L='book',     R='pharmacy'),
        dict(id='e6',  a='A',  b='B',  via=[(160, 6)],   L='post',     R='temple'),
        dict(id='e7',  a='B',  b='C',  via=[(272, 50)],  L='noodle',   R='bento'),
        dict(id='e8',  a='C',  b='D',  via=[(284, 160)], L='drink',    R='clinic'),
        dict(id='e9',  a='D',  b='y1', via=[(244, 226), (206, 236), (172, 232)], L='salon', R='breakfast'),
        dict(id='e10', a='y1', b='E',  via=[(128, 232), (94, 236), (52, 226), (26, 196)], L='market', R='laundry'),
        dict(id='e11', a='E',  b='A',  via=[(14, 100), (40, 30)], L='school', R='library'),
        dict(id='e12', a='y1', b='n8', via=[],           L=None,       R=None),
    ],
)


# second buildings on the longer roads (placed by graph_engine wherever there is room, in this order)
SECOND_POOL = ['hotel', 'restaurant', 'snack', 'fruit', 'police', 'bus', 'flower', 'optical', 'gym', 'stationery']
SECOND_CANDIDATES = [('e9', 'L'), ('e10', 'R'), ('e11', 'L'), ('e6', 'R'), ('e7', 'L'), ('e8', 'R'), ('e1', 'L'), ('e5', 'R'),
                     ('e2', 'L'), ('e3', 'R'), ('e4', 'L'), ('e9', 'R'), ('e10', 'L'), ('e11', 'R'), ('e6', 'L'), ('e7', 'R'),
                     ('e1', 'R'), ('e5', 'L'), ('e2', 'R'), ('e8', 'L')]


# ---------------- level 6: the big irregular map (no roundabout / Y: those are level 5) ----------------
# Same drawing space as above. `light=True` marks a junction that has a traffic light (random, not every junction).
# Shops with a name ending in _2 / _3 are a second / third shop of the same kind (the game strips the suffix).
_N = dict(
    A1=(40, 40), A2=(175, 22), A3=(310, 50), A4=(445, 28),
    B1=(22, 170), B2=(160, 155), B3=(295, 185), B4=(430, 150), B5=(560, 200),
    C1=(55, 305), C2=(185, 290), C3=(315, 320), C4=(450, 285), C5=(575, 335),
    D1=(135, 430), D2=(320, 445), D3=(470, 415),
)
_LIGHTS = {'B2', 'B3', 'C2', 'C3', 'C4', 'A3', 'D2'}          # random-looking subset (7 of 17 nodes)
_E = [  # (a, b, via)
    ('A1', 'A2', [(105, 20)]), ('A2', 'A3', []), ('A3', 'A4', [(380, 28)]),
    ('A1', 'B1', []), ('A2', 'B2', []), ('A3', 'B3', []), ('A4', 'B4', []),
    ('B1', 'B2', []), ('B2', 'B3', [(228, 172)]), ('B4', 'B5', []),
    ('B1', 'C1', []), ('B2', 'C2', []), ('B3', 'C3', []), ('B4', 'C4', []), ('B5', 'C5', []),
    ('C1', 'C2', []), ('C2', 'C3', []), ('C3', 'C4', [(385, 300)]), ('C4', 'C5', []),
    ('C1', 'D1', []), ('C3', 'D2', []), ('C4', 'D3', []),
    ('D1', 'D2', []), ('D2', 'D3', []),
]
# (left, right) shops of every road when walking a -> b; None = nothing there
_SHOPS = [
    ('bank', 'post'), ('cafe', 'gym'), ('cafe_2', 'temple'),            # f1-f3   top street (two cafés on it)
    ('park', None), ('book', 'flower'), ('hospital', 'pharmacy'), ('school', 'library'),
    ('noodle', 'conv'), ('bento', 'conv_2'), ('dept', 'clinic'),         # f8-f10  middle street (two convenience stores on it)
    ('salon', 'stationery'), ('restaurant', 'hotel'), ('snack', 'pharmacy_2'), ('police', 'bakery'), ('market', 'laundry'),
    ('optical', 'drink'), ('cinema', 'bus'), ('breakfast', 'drink_2'), ('train', 'fruit'),   # f16-f19 lower street (two drink shops)
    ('mrt', None), ('nightmkt', None), ('library_2', None),
    (None, 'bank_2'), ('post_2', None),
]
BIG = dict(
    tw='大街區', cn='大街区', es='Barrio grande', en='Big Neighborhood',
    nodes={k: dict(x=v[0], y=v[1], light=(k in _LIGHTS)) for k, v in _N.items()},
    edges=[dict(id='f%d' % (i + 1), a=a, b=b, via=via, L=_SHOPS[i][0], R=_SHOPS[i][1]) for i, (a, b, via) in enumerate(_E)],
)
BIG_SECOND = []      # (edge, side, shop): second shops on the longer roads, filled in below
