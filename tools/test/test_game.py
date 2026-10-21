import json, sys, os
from playwright.sync_api import sync_playwright
URL = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html'))
SH = '/tmp/shots'
fails = []
def chk(c, m):
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'photos/' not in m.text and 'Failed to load resource' not in m.text else None)
    pg.goto(URL)
    pg.screenshot(path=SH + '/start.png', full_page=True)
    # empty name refused
    pg.click('.lv >> nth=0')
    chk(pg.evaluate("document.querySelector('#s-start').classList.contains('on')"), 'empty name refused')
    pg.fill('#name', 'Ana')
    # map choice chips
    chk(pg.locator('#c-map .chip').count() == 10, '10 map chips (random + 9)')
    # all questions via act()
    qs = pg.evaluate("__askdir.DATA.questions")
    chk(len(qs) == 324, '324 questions')
    bad = 0
    for q in qs:
        pg.evaluate("q=>__askdir.loadSpecific(q)", q)
        for a in q['actions']: pg.evaluate("a=>__askdir.act(a)", a)
        pg.evaluate("__askdir.submit()")
        if pg.evaluate("__askdir.S.correct") != 1: bad += 1
    chk(bad == 0, 'all %d routes answered correctly via act() (bad=%d)' % (len(qs), bad))
    # wrong crossing
    q = next(q for q in qs if q['crosses'])
    pg.evaluate("q=>__askdir.loadSpecific(q)", q)
    for a in q['actions']:
        if a != 'C': pg.evaluate("a=>__askdir.act(a)", a)
    pg.evaluate("__askdir.submit()")
    chk(pg.evaluate("__askdir.S.correct") == 0, 'missing crossing is wrong')
    chk('cruzaste' in pg.inner_text('#feedback'), 'badCross message shown')
    pg.screenshot(path=SH + '/wrongcross.png', full_page=True)
    # closed road: walking into it is refused; dead ends exist
    qn = next(q for q in qs if q['map']=='night')
    pg.evaluate("q=>__askdir.loadSpecific(q)", qn)
    pg.evaluate("q=>{const S=__askdir.S;S.pos={x:0,y:1,d:1};}", qn)
    pg.evaluate("__askdir.act('S')")
    chk(pg.evaluate("[__askdir.S.pos.x,__askdir.S.pos.y,__askdir.S.actions.length]") == [0,1,0], 'cannot walk along a closed road')
    # roundabout: S/L/R refused on it, exit buttons work, wrong use refused
    qr = next(q for q in qs if q['map']=='rb')
    pg.evaluate("q=>__askdir.loadSpecific(q)", qr)
    pg.evaluate("__askdir.act('1')")
    chk(pg.evaluate("__askdir.S.actions.length") == 0, 'exit button refused outside roundabout')
    for a in qr['actions'][:1]: pg.evaluate("a=>__askdir.act(a)", a)
    pg.evaluate("__askdir.act('L')")
    chk(pg.evaluate("__askdir.S.actions.join('')") == qr['actions'][:1], 'turning refused inside roundabout')
    chk(pg.evaluate("document.querySelector('#exits').classList.contains('off')") is False, 'exit buttons enabled in roundabout')
    # level 1 cannot cross
    q1 = next(q for q in qs if q['level'] == 1)
    pg.evaluate("q=>__askdir.loadSpecific(q)", q1)
    pg.evaluate("__askdir.act('C')")
    chk(pg.evaluate("__askdir.S.actions.length") == 0, 'level 1 ignores cross')
    # replay ends at correct square
    pg.evaluate("q=>__askdir.loadSpecific(q)", q)
    pg.evaluate("__askdir.act('L')"); pg.evaluate("__askdir.submit()")
    pg.evaluate("__askdir.replay()"); pg.wait_for_timeout(7000)
    chk(pg.evaluate("[__askdir.S.pos.x,__askdir.S.pos.y,__askdir.S.pos.d]") == q['end'], 'replay ends at correct square')
    pg.screenshot(path=SH + '/replay.png', full_page=True)
    # listen-only + parts
    pg.evaluate("__askdir.S.showText=false;__askdir.S.partMode=true")
    pg.evaluate("q=>__askdir.loadSpecific(q)", q)
    chk('🎧' in pg.inner_text('#zh'), 'listen-only placeholder')
    chk(pg.is_visible('#btn-npart'), 'next-part button visible')
    n = len(q['parts'])
    for _ in range(n - 1): pg.click('#btn-npart')
    chk(not pg.is_visible('#btn-npart'), 'next-part hidden at last part')
    pg.evaluate("__askdir.submit()")
    chk('🎧' not in pg.inner_text('#zh'), 'text revealed after answering')
    chk(pg.inner_text('#zh').replace('\n','') == ''.join(x['tw'] for x in q['parts']), 'full text after answer')
    pg.evaluate("__askdir.S.showText=true;__askdir.S.partMode=false")
    # map filter + full game
    pg.evaluate("__askdir.S.map='night'")
    pg.evaluate("__askdir.startGame(3)")
    chk(pg.evaluate("__askdir.S.qs.every(q=>q.map==='night')") and pg.evaluate("__askdir.S.qs.length")==8, 'map filter, 8 questions')
    # photo onerror removes figure
    for i in range(8):
        qq = pg.evaluate("__askdir.S.q")
        for a in qq['actions']: pg.evaluate("a=>__askdir.act(a)", a)
        pg.evaluate("__askdir.submit()")
        if i == 0:
            pg.wait_for_timeout(300)
            chk(pg.locator('.photo').count() == 0, 'missing photo removed')
            pg.screenshot(path=SH + '/ok.png', full_page=True)
        pg.evaluate("__askdir.nextQuestion()")
    pg.wait_for_timeout(300)
    chk(pg.inner_text('#r-score') == '80', 'perfect round = 80')
    pg.screenshot(path=SH + '/result.png', full_page=True)
    lb = pg.evaluate("localStorage.getItem('askdir_lb')")
    chk('Ana' in (lb or ''), 'local leaderboard saved')
    # screenshots of a level-2 question with pinyin
    pg.evaluate("__askdir.S.pinyin=true")
    q2 = next(q for q in qs if q['level'] == 2 and q['crosses'])
    pg.evaluate("q=>__askdir.loadSpecific(q)", q2)
    for a in q2['actions'][:3]: pg.evaluate("a=>__askdir.act(a)", a)
    pg.screenshot(path=SH + '/l2.png', full_page=True)
    pg.click('#btn-vocab'); pg.screenshot(path=SH + '/vocab.png', full_page=True)
    for mp in ['street','station','night','campus','hospital','metro','rb','y','mix']:
        qq = next(q for q in qs if q['map']==mp and q['level']==(5 if mp in ('rb','y','mix') else 2))
        pg.evaluate("q=>__askdir.loadSpecific(q)", qq)
        pg.locator('.mapwrap').screenshot(path=SH + '/road_%s.png' % mp)
    chk(not errs, 'no console errors %s' % errs[:3])
    b.close()
print('FAILS:', len(fails)); sys.exit(1 if fails else 0)
