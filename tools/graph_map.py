# -*- coding: utf-8 -*-
"""The non-grid neighbourhood used by level 5 (real-street map).
Coordinates are in the same 0..300 drawing space as the grid maps.
Each edge is a road between two real nodes; `via` are bend points; L / R are the buildings on the
left / right of the road when walking a -> b (at most one per side)."""

GRAPH = dict(
    tw='真實街區', cn='真实街区', es='Barrio real', en='Real Neighborhood',
    nodes={
        'rb': dict(x=150, y=125, kind='rb'),     # roundabout
        'n1': dict(x=88,  y=14),
        'n2': dict(x=262, y=22),
        'n3': dict(x=292, y=122),
        'n4': dict(x=246, y=212),
        'n5': dict(x=62,  y=208),
        'y1': dict(x=150, y=262, kind='y'),      # Y fork, stem comes from the south
        'n8': dict(x=150, y=318),
    },
    edges=[
        dict(id='e1',  a='rb', b='n1', via=[(122, 70)],           L='bakery',  R='bank'),
        dict(id='e2',  a='rb', b='n2', via=[],                    L='cafe',    R='park'),
        dict(id='e3',  a='rb', b='n3', via=[],                    L='hospital', R='conv'),
        dict(id='e4',  a='rb', b='n4', via=[],                    L='dept',    R='cinema'),
        dict(id='e5',  a='rb', b='n5', via=[(102, 160)],          L='book',    R='pharmacy'),
        dict(id='e6',  a='n1', b='n5', via=[(38, 50), (14, 130)], L='school',  R='library'),
        dict(id='e7',  a='n1', b='n2', via=[],                    L='post',    R='temple'),
        dict(id='e8',  a='n2', b='n3', via=[(286, 70)],           L='noodle',  R='bento'),
        dict(id='e9',  a='n3', b='n4', via=[],                    L='drink',   R='clinic'),
        dict(id='e10', a='n5', b='y1', via=[],                    L='market',  R='laundry'),
        dict(id='e11', a='n4', b='y1', via=[],                    L='salon',   R='breakfast'),
        dict(id='e12', a='y1', b='n8', via=[],                    L=None,      R=None),
    ],
)
