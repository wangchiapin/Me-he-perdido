import sys,math,json,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
from graph_map import GRAPH
import gen_questions as g
OUT=sys.argv[1]
K=2.3; N=GRAPH['nodes']
P=lambda x,y:(x*K,y*K)
def pts(e):
    a=N[e['a']];b=N[e['b']]
    return [P(a['x'],a['y'])]+[P(*v) for v in e['via']]+[P(b['x'],b['y'])]
segs=[(p[i-1],p[i]) for e in GRAPH['edges'] for p in [pts(e)] for i in range(1,len(p))]
def dseg(px,py,a,b):
    (x1,y1),(x2,y2)=a,b;dx,dy=x2-x1,y2-y1;l2=dx*dx+dy*dy
    t=max(0,min(1,((px-x1)*dx+(py-y1)*dy)/l2));return math.hypot(px-x1-t*dx,py-y1-t*dy)
rb=P(N['rb']['x'],N['rb']['y']);yy=P(N['y1']['x'],N['y1']['y'])
H=30;RW=19
placed=[]
def ok(cx,cy):
    if min(dseg(cx,cy,a,b) for a,b in segs)<RW+H*0.9: return False
    if math.hypot(cx-rb[0],cy-rb[1])<38+H+6: return False
    if math.hypot(cx-yy[0],cy-yy[1])<30+H: return False
    return all(abs(cx-x)>2*H+5 or abs(cy-y)>2*H+5 for x,y in placed)
bl=[]
items=[(e,s) for e in GRAPH['edges'] for s in 'LR' if e[s]]
for e,side in items:
    sg=1 if side=='L' else -1;k=e[side];p=pts(e);best=None
    for off in (RW+H+4,RW+H+12,RW+H+22):
        for i in range(1,len(p)):
            (x1,y1),(x2,y2)=p[i-1],p[i];dx,dy=x2-x1,y2-y1;l=math.hypot(dx,dy);nx,ny=dy/l,-dx/l
            for t in (.5,.4,.6,.3,.7,.22,.78,.15,.85):
                cx,cy=x1+dx*t+nx*sg*off,y1+dy*t+ny*sg*off
                if ok(cx,cy): best=(cx,cy,nx*sg,ny*sg,t,x1+dx*t,y1+dy*t);break
            if best:break
        if best:break
    if best: placed.append(best[:2]);bl.append((k,best))
    else: print('no room',e['id'],side,k)
print(len(bl),'placed')
def pd(p): return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in p)
h=[]
for e in GRAPH['edges']: h.append(f'<path class="edge" d="{pd(pts(e))}"/>')
for e in GRAPH['edges']: h.append(f'<path class="road" d="{pd(pts(e))}"/>')
for key,n in N.items():
    x,y=P(n['x'],n['y'])
    if n.get('kind') not in('rb','y'): h.append(f'<circle cx="{x}" cy="{y}" r="{RW}" fill="var(--road)"/>')
# Y: green island between the two branches
e10=[e for e in GRAPH['edges'] if e['id']=='e10'][0];e11=[e for e in GRAPH['edges'] if e['id']=='e11'][0]
def along(e,frm,dist):
    p=pts(e);p=p if e['a']==frm else p[::-1]
    (x1,y1),(x2,y2)=p[0],p[1];l=math.hypot(x2-x1,y2-y1);return x1+(x2-x1)/l*dist,y1+(y2-y1)/l*dist
def unit(e):
    p=pts(e);p=p if e['a']=='y1' else p[::-1]
    (x1,y1),(x2,y2)=p[0],p[1];l=math.hypot(x2-x1,y2-y1);return ((x2-x1)/l,(y2-y1)/l)
u1=unit(e10);u2=unit(e11);G=RW+5
def perp_in(u,v):
    d=u[0]*v[0]+u[1]*v[1];w=(v[0]-d*u[0],v[1]-d*u[1]);l=math.hypot(*w);return (w[0]/l,w[1]/l)
n1=perp_in(u1,u2);n2=perp_in(u2,u1)
o1=(yy[0]+n1[0]*G,yy[1]+n1[1]*G);o2=(yy[0]+n2[0]*G,yy[1]+n2[1]*G)
# intersection of o1+t*u1 and o2+s*u2
det=u1[0]*(-u2[1])-u1[1]*(-u2[0]);rx,ry=o2[0]-o1[0],o2[1]-o1[1]
t=(rx*(-u2[1])-ry*(-u2[0]))/det
tip=(o1[0]+u1[0]*t,o1[1]+u1[1]*t)
D=t+70
B1=(o1[0]+u1[0]*D,o1[1]+u1[1]*D);B2=(o2[0]+u2[0]*D,o2[1]+u2[1]*D)
h.append(f'<path d="{pd([tip,B1,B2])}Z" fill="#cfdccb" stroke="#8a867c" stroke-width="1" stroke-linejoin="round"/>')
cen=((tip[0]+B1[0]+B2[0])/3,(tip[1]+B1[1]+B2[1])/3)
tri=[tip]
h.append(f'<circle cx="{yy[0]:.1f}" cy="{yy[1]:.1f}" r="{RW+1}" fill="var(--road)"/>')
h.append(f'<circle cx="{cen[0]:.1f}" cy="{cen[1]:.1f}" r="8" fill="#fffefa" stroke="#8a867c"/><text x="{cen[0]:.1f}" y="{cen[1]+3.8:.1f}" text-anchor="middle" font-size="11" font-weight="700">Y</text>')
# roundabout
x,y=rb
h.append(f'<circle cx="{x}" cy="{y}" r="40" fill="var(--road)" stroke="#bdb8aa"/><circle cx="{x}" cy="{y}" r="20" fill="#cfdccb" stroke="#8a867c"/>')
for dx_,dy_,s in (): h.append(f'<circle cx="{x+dx_}" cy="{y+dy_-4}" r="4.4" fill="{s}" stroke="#8a867c" stroke-width=".6"/>')
h.append(f'<text x="{x}" y="{y+3}" text-anchor="middle" font-size="8" font-weight="700" fill="#4b4a46">圓環</text>')
for deg in (40,160,280):
    th=math.radians(deg);px=x+math.cos(th)*30;py=y-math.sin(th)*30;tx=-math.sin(th);ty=-math.cos(th);nx=-ty;ny=tx
    h.append(f'<path d="M{px+tx*5:.1f} {py+ty*5:.1f} L{px-tx*3.5+nx*4:.1f} {py-ty*3.5+ny*4:.1f} L{px-tx*3.5-nx*4:.1f} {py-ty*3.5-ny*4:.1f}Z" fill="#8a867c"/>')
for e in GRAPH['edges']: h.append(f'<path class="mid" d="{pd(pts(e))}"/>')
# crosswalks near every junction end of an edge
def cw(cx,cy,ux,uy):
    nx,ny=-uy,ux
    for o in (0,6,12):
        px,py=cx+ux*o,cy+uy*o
        h.append(f'<path d="M{px-nx*RW*.95:.1f},{py-ny*RW*.95:.1f} L{px+nx*RW*.95:.1f},{py+ny*RW*.95:.1f}" stroke="#f8f6f0" stroke-width="3.4"/>')
for e in GRAPH['edges']:
    p=pts(e)
    for end in (0,1):
        n=N[e['a'] if end==0 else e['b']]
        if n.get('kind')=='y': continue
        (x1,y1),(x2,y2)=(p[0],p[1]) if end==0 else (p[-1],p[-2])
        l=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/l,(y2-y1)/l
        d0={'rb':50}.get(n.get('kind'),26)
        cw(x1+ux*d0,y1+uy*d0,ux,uy)
# y arms crosswalk
for e in (e10,e11,[e for e in GRAPH['edges'] if e['id']=='e12'][0]):
    p=pts(e);p=p if e['a']=='y1' else p[::-1]
    (x1,y1),(x2,y2)=p[0],p[1];l=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/l,(y2-y1)/l
    cw(x1+ux*(30 if e['id']!='e12' else 28),y1+uy*(30 if e['id']!='e12' else 28),ux,uy)
# trees on the road verge
import random;random.seed(7)
for e in GRAPH['edges']:
    p=pts(e)
    for i in range(1,len(p)):
        (x1,y1),(x2,y2)=p[i-1],p[i];dx,dy=x2-x1,y2-y1;l=math.hypot(dx,dy);nx,ny=dy/l,-dx/l
        for t in (.28,.72):
            for sg in (1,-1):
                if random.random()<.5: continue
                tx,ty=x1+dx*t+nx*sg*(RW+7),y1+dy*t+ny*sg*(RW+7)
                if all(math.hypot(tx-cx,ty-cy)>H+4 if False else (abs(tx-cx)>H+3 or abs(ty-cy)>H+3) for cx,cy in placed) and math.hypot(tx-rb[0],ty-rb[1])>48:
                    h.append(f'<g transform="translate({tx:.1f},{ty:.1f})"><circle r="5" fill="#a9bfa7" stroke="#8a867c" stroke-width=".6"/><circle cx="-1.2" cy="-1.2" r="1.7" fill="#bccdb9"/></g>')
for k,b in bl:
    cx,cy=b[:2]
    h.append(f'<g class="bld"><rect x="{cx-H:.1f}" y="{cy-H:.1f}" width="{2*H}" height="{2*H}" rx="9"/><g transform="translate({cx:.1f},{cy-26:.1f}) scale(.75)">@@{k}@@</g><text class="bn sm" x="{cx:.1f}" y="{cy+22:.1f}" text-anchor="middle">{g.B[k]["tw"]}</text></g>')
xs=[x for x,_ in placed]+[p[0] for s in segs for p in s];ys=[y for _,y in placed]+[p[1] for s in segs for p in s]
vx,vy=min(xs)-H-16,min(ys)-H-16;vw,vh=max(xs)-vx+H+16,max(ys)-vy+H+16
art=open(os.path.join(os.path.dirname(__file__),'..','art.js')).read()
sc=0.85
html=f'''<!doctype html><meta charset=utf-8><style>
:root{{--road:#e7e3d9}}body{{margin:0;background:#f6f4ee;font-family:"Noto Sans TC",sans-serif}}
.edge{{stroke:#cfcabd;stroke-width:{2*RW+3};stroke-linecap:round;stroke-linejoin:round;fill:none}}
.road{{stroke:var(--road);stroke-width:{2*RW};stroke-linecap:round;stroke-linejoin:round;fill:none}}
.mid{{stroke:#d0cbbd;stroke-width:1;stroke-dasharray:5 6;fill:none}}
.bld rect{{fill:#fffefa;stroke:#d3cec0;stroke-width:1.2}}
.bn{{font-size:15px;font-weight:600;fill:#2b2b2b}}.bn.sm{{font-size:13px}}
</style><svg id=m viewBox="{vx:.0f} {vy:.0f} {vw:.0f} {vh:.0f}" width="{vw*sc:.0f}" height="{vh*sc:.0f}"></svg><script>{art}
const body={json.dumps(''.join(h))};
m.innerHTML=body.replace(/@@(\\w+)@@/g,(_,k)=>BA[k]?BA[k]():'');</script>'''
open(OUT+'.html','w').write(html);open(OUT+'.dim','w').write(f'{int(vw*sc)} {int(vh*sc)}')
