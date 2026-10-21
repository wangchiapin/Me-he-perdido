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
