# 問路小達人「分享成績」＋ ?ref=share 來訪追蹤 測試：python3 tools/test/test_share.py
import os, sys, json
from playwright.sync_api import sync_playwright

URL = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'index.html'))
fails = 0
def check(c, msg):
    global fails
    print(('  ok  ' if c else '  FAIL'), msg)
    if not c: fails += 1

APP = "export function initializeApp(c,n){return {c,n}}"
FS = '''
const DB=(window.__db=window.__db||{});
const op=(k,p,d)=>(window.__ops=window.__ops||[]).push({k,p,d});
export function getFirestore(app){return {app}}
export const collection=(db,...p)=>({db,path:p.join('/')});
export const doc=(db,...p)=>({db,path:p.join('/')});
export const serverTimestamp=()=>'SERVER_TS';
export async function setDoc(r,d){ op('set',r.path,d); DB[r.path]=JSON.parse(JSON.stringify(d)); }
export async function addDoc(c,d){op('add',c.path,d);return {id:'P'+(window.__ops.length)}}
export async function updateDoc(r,d){op('update',r.path,d)}
export const getDoc=async(r)=>({exists:()=>r.path in DB,data:()=>DB[r.path]});
export const getDocs=async(q)=>({docs:[],size:0,forEach(){}});
export const query=(...a)=>a,where=()=>0,orderBy=()=>0,limit=(n)=>n,onSnapshot=()=>()=>{},deleteDoc=async()=>{},increment=()=>0,runTransaction=async()=>{},writeBatch=()=>({}),Timestamp={now:()=>({}),fromDate:()=>({}),fromMillis:(m)=>({ms:m})},arrayUnion=()=>0,startAfter=()=>0,getCountFromServer=async()=>({data:()=>({count:0})}),documentId=()=>'id',enableIndexedDbPersistence=async()=>{};
'''
AUTH = """const a={currentUser:null,authStateReady:async()=>{}};
export const getAuth=()=>a,GoogleAuthProvider=class{};
export const signInAnonymously=async()=>{a.currentUser={uid:(window.__uid||'UID1'),isAnonymous:true};return {user:a.currentUser}};
export const onAuthStateChanged=(x,cb)=>{setTimeout(()=>cb(a.currentUser),0);return()=>{}};
export const signInWithPopup=async()=>{},signOut=async()=>{},signInWithCredential=async()=>{},setPersistence=async()=>{},browserLocalPersistence={};"""
def route(r):
    u = r.request.url
    if u.startswith('file:'): return r.continue_()
    if 'gstatic.com/firebasejs' in u:
        body = APP if 'firebase-app' in u else FS if 'firestore' in u else AUTH if 'auth' in u else ''
        return r.fulfill(status=200, content_type='application/javascript', body=body)
    r.abort()

STUB = """(()=>{ window.__shared=[]; window.__copied=[]; window.__mode='share'; window.__shareDelay=0;
  Object.defineProperty(navigator,'share',{configurable:true,get(){ return (window.__mode==='copy'||window.__mode==='fail') ? undefined : async d=>{ window.__shared.push(d);
    if(window.__mode==='abort'){ const e=new Error('x'); e.name='AbortError'; throw e; }
    if(window.__mode==='boom'){ throw new Error('boom'); }
    if(window.__shareDelay) await new Promise(r=>setTimeout(r,window.__shareDelay)); } }});
  Object.defineProperty(navigator,'clipboard',{configurable:true,value:{ writeText: async t=>{ if(window.__mode==='fail') throw new Error('no'); window.__copied.push(t); } }});
  document.execCommand=()=>false;
  window.SpeechSynthesisUtterance=function(t){this.text=t;};
  Object.defineProperty(window,'speechSynthesis',{value:{getVoices:()=>[{lang:'zh-TW',name:'fake'}],speak(){},cancel(){},addEventListener(){}},configurable:true});
})();"""

URL_SHARE = 'https://wangchiapin.github.io/Me-he-perdido/?ref=share'

def open_page(p, query='', lang='es', script='trad'):
    b = p.chromium.launch(args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    ctx.add_init_script(STUB)
    ctx.add_init_script("try{localStorage.setItem('hanziGames.settings',%s)}catch(e){}" % json.dumps(json.dumps({'v': 1, 'script': script, 'lang': lang, 'phon': 'pinyin', 'rate': 'normal'})))
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    ctx.route('**/*', route)
    pg.goto(URL + query); pg.wait_for_timeout(1500)
    return b, pg, errs

def result(pg, correct, name='Ana'):
    pg.evaluate("(n)=>{ document.querySelector('#name').value=n; __askdir.startGame(1); }", name); pg.wait_for_timeout(300)
    pg.evaluate("(c)=>{ __askdir.S.correct=c; __askdir.S.totalMs=42000; __askdir.finish(); }", correct); pg.wait_for_timeout(600)

with sync_playwright() as p:
    # 1) 西文
    b, pg, errs = open_page(p, lang='es')
    result(pg, 7)
    check(pg.evaluate("document.querySelector('#s-result').classList.contains('on')"), '到結果頁')
    check(pg.is_visible('#r-share'), '分數 > 0：顯示分享鈕')
    txt = pg.inner_text('#r-share')
    check('分享成績' in txt and 'Compartir resultado' in txt, '鈕上有「分享成績」與西文小字：%r' % txt)
    ids = pg.evaluate("[...document.querySelectorAll('#s-result button')].map(b=>b.id)")
    check(ids.index('r-again') < ids.index('r-share') < ids.index('r-home'), '順序：再玩一次 → 分享 → 換關卡：%s' % ids)
    check(pg.evaluate("document.getElementById('r-share').classList.contains('btn-restart') || document.getElementById('r-share').id==='btn-restart'") is False, '不用 btn-restart')
    check(pg.evaluate("getComputedStyle(document.getElementById('r-share')).borderTopWidth") == '2px', '空心外框 2px')
    check(pg.evaluate("getComputedStyle(document.getElementById('r-share')).backgroundColor") == 'rgb(255, 255, 255)', '白底')
    pg.click('#r-share'); pg.wait_for_timeout(300)
    sh = pg.evaluate("window.__shared")
    check(len(sh) == 1 and sh[0]['url'] == URL_SHARE, '分享網址是公開頁＋?ref=share：%s' % [s.get('url') for s in sh])
    check('70' in sh[0]['text'] and 'Ana' in sh[0]['text'] and 'Pregunta el camino' in sh[0]['text'], '西文句子含暱稱、分數、遊戲名：%s' % sh[0]['text'])
    check('問路小達人' in sh[0]['title'], '標題含中文遊戲名：%s' % sh[0]['title'])
    check(pg.inner_text('#r-share') == txt, '分享成功後按鈕文字不變')
    pg.evaluate("window.__mode='abort'"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check('複製失敗' not in pg.inner_text('#r-share') and '已複製' not in pg.inner_text('#r-share') and pg.evaluate("window.__copied.length") == 0, '玩家關掉選單：不顯示失敗、不複製')
    pg.evaluate("window.__mode='boom'"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check(pg.evaluate("window.__copied.length") == 1 and URL_SHARE in pg.evaluate("window.__copied[0]"), '分享出錯：改複製（含連結）')
    check('已複製' in pg.inner_text('#r-share') and 'Copiado' in pg.inner_text('#r-share'), '顯示「已複製 Copiado」')
    pg.wait_for_timeout(2500)
    check(pg.inner_text('#r-share') == txt, '2.2 秒後文字還原')
    pg.evaluate("window.__mode='copy'; window.__copied.length=0"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check(pg.evaluate("window.__copied.length") == 1, '不支援分享選單：複製')
    pg.wait_for_timeout(2500)
    pg.evaluate("window.__mode='fail'"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check('複製失敗' in pg.inner_text('#r-share') and 'No se pudo copiar' in pg.inner_text('#r-share'), '複製也失敗：顯示「複製失敗」')
    pg.wait_for_timeout(2500)
    pg.evaluate("window.__mode='share'; window.__shared.length=0; window.__shareDelay=600")
    pg.evaluate("for(let i=0;i<3;i++) document.getElementById('r-share').click()"); pg.wait_for_timeout(900)
    check(pg.evaluate("window.__shared.length") == 1, '連點三下只送一次：%d' % pg.evaluate("window.__shared.length"))
    check(not errs, '沒有網頁錯誤 %s' % errs)
    b.close()

    # 2) 英文
    b, pg, errs = open_page(p, lang='en')
    result(pg, 4)
    pg.click('#r-share'); pg.wait_for_timeout(300)
    t = pg.evaluate("window.__shared[0].text")
    check('40' in t and '4 of' in t and 'points' in t, '英文句子：%s' % t)
    check('Share result' in pg.inner_text('#r-share'), '英文小字 Share result')
    b.close()

    # 3) 只有中文：簡體／繁體
    b, pg, errs = open_page(p, lang='zh', script='simp')
    result(pg, 8)
    check('分享成绩' in pg.inner_text('#r-share'), '簡體鈕：分享成绩：%r' % pg.inner_text('#r-share'))
    pg.click('#r-share'); pg.wait_for_timeout(300)
    t = pg.evaluate("window.__shared[0].text")
    check('答对' in t and '问路小达人' in t and '答對' not in t, '簡體句子：%s' % t)
    pg.evaluate("window.__mode='boom'"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check('已复制' in pg.inner_text('#r-share'), '簡體：已复制：%r' % pg.inner_text('#r-share'))
    pg.wait_for_timeout(2500)
    pg.evaluate("window.__mode='fail'"); pg.click('#r-share'); pg.wait_for_timeout(300)
    check('复制失败' in pg.inner_text('#r-share'), '簡體：复制失败：%r' % pg.inner_text('#r-share'))
    b.close()
    b, pg, errs = open_page(p, lang='zh', script='trad')
    result(pg, 8)
    pg.click('#r-share'); pg.wait_for_timeout(300)
    t = pg.evaluate("window.__shared[0].text")
    check('答對 8/' in t and '問路小達人' in t and '80 分' in t, '繁體句子：%s' % t)
    b.close()

    # 4) 0 分不顯示
    b, pg, errs = open_page(p, lang='es')
    result(pg, 0)
    check(pg.evaluate("document.querySelector('#s-result').classList.contains('on')") and not pg.is_visible('#r-share'), '0 分：不顯示分享鈕')
    pg.evaluate("document.getElementById('r-share').click()"); pg.wait_for_timeout(200)
    check(pg.evaluate("window.__shared.length") == 0, '0 分：強行點也不分享')
    result(pg, 3)
    check(pg.is_visible('#r-share'), '下一局拿到分數：分享鈕又出現')
    b.close()

    # 5) ?ref=share 追蹤
    def ops(pg): return pg.evaluate("window.__ops||[]")
    b, pg, errs = open_page(p, query='?ref=share')
    pg.wait_for_timeout(1500)
    v = [o for o in ops(pg) if o['p'].startswith('visits/')]
    check(len(v) == 1 and v[0]['d'].get('ref') == 'share', '打開 ?ref=share：visit 帶 ref=share：%s' % [o['d'] for o in v])
    result(pg, 5); pg.wait_for_timeout(500)
    pl = [o for o in ops(pg) if o['p'] == 'plays']
    check(len(pl) >= 1 and pl[0]['d'].get('ref') == 'share', '開始玩：play 帶 ref=share：%s' % [o['d'] for o in pl])
    b.close()
    b, pg, errs = open_page(p)
    pg.wait_for_timeout(1500)
    v = [o for o in ops(pg) if o['p'].startswith('visits/')]
    check(len(v) == 1 and 'ref' not in v[0]['d'], '沒帶 ref：visit 沒有 ref 欄位')
    b.close()
    for bad, want in [('?ref=SHARE', 'share'), ('?ref=a%20b', None), ('?ref=' + 'x' * 17, None), ('?ref=%3Cb%3E', None)]:
        b, pg, errs = open_page(p, query=bad)
        pg.wait_for_timeout(1500)
        v = [o for o in ops(pg) if o['p'].startswith('visits/')]
        check(len(v) == 1 and v[0]['d'].get('ref') == want, '記號 %s → %s：%s' % (bad, want, [o['d'].get('ref') for o in v]))
        b.close()

print('FAILS', fails); sys.exit(1 if fails else 0)
