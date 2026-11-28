import json
from playwright.sync_api import sync_playwright

URLS = {'before':'http://127.0.0.1:63404/','after':'http://127.0.0.1:8765/'}
rows = Array = None

def reset(page):
    page.evaluate("""()=>{document.getElementById('probeDialog')?.close();document.getElementById('probeDialog')?.remove();window.scrollTo(0,600);}""")

def wheel(page, selector, steps=8):
    box=page.evaluate("""(s)=>{const b=document.querySelector('#probeDialog '+s).getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}}""", selector)
    page.mouse.move(box['x'],box['y'])
    page.evaluate('window.scrollTo(0,600)')
    before=page.evaluate('Math.round(window.scrollY)')
    for _ in range(steps):
        page.mouse.wheel(0,220);page.wait_for_timeout(40)
    return before,page.evaluate('Math.round(window.scrollY)')

def build(page, kind):
    page.evaluate("""(kind)=>{
      const tall=Array.from({length:40},(_,i)=>`<p style="margin:0;height:28px">row ${i}</p>`).join('');
      const short='<p>short</p>';
      let inner;
      if(kind==='nested'){
        inner=`<div class="editor__picker-menu" style="position:static"><div class="editor__picker-options">${tall}</div></div>`+
              Array.from({length:10},(_,i)=>`<p style="height:40px">tail ${i}</p>`).join('');
      } else inner = kind==='tall' ? tall : short;
      const d=document.createElement('dialog');d.className='editor';d.id='probeDialog';
      d.innerHTML=`<div class="editor__head" style="height:52px">HEADER</div><div class="editor__content">${inner}</div>`;
      document.body.appendChild(d);d.showModal();
    }""",kind)

with sync_playwright() as p:
    b=p.chromium.launch()
    for name,url in URLS.items():
        page=b.new_page(viewport={'width':1200,'height':700})
        page.goto(url,wait_until='domcontentloaded');page.wait_for_timeout(250)
        page.evaluate("document.body.style.minHeight='4000px'")
        for kind in ('tall','short','nested'):
            reset(page);build(page,kind)
            target = '.editor__picker-options' if kind=='nested' else '.editor__content'
            doc_before,doc_after=wheel(page,target,steps=10 if kind=='nested' else 8)
            state=page.evaluate("""(target)=>{
              const s=document.querySelector('#probeDialog '+target);
              const c=document.querySelector('#probeDialog .editor__content');
              const d=document.getElementById('probeDialog');
              return {targetOverscroll:getComputedStyle(s).overscrollBehaviorY,
                      contentOverscroll:getComputedStyle(c).overscrollBehaviorY,
                      dialogOverscroll:getComputedStyle(d).overscrollBehaviorY,
                      rootOverflow:getComputedStyle(document.documentElement).overflowY,
                      targetScroll:s.scrollTop, contentScroll:c.scrollTop,
                      targetRange:s.scrollHeight-s.clientHeight,
                      contentRange:c.scrollHeight-c.clientHeight};
            }""",target)
            print(json.dumps({'side':name,'case':kind,'doc':[doc_before,doc_after],**state}))
        page.close()
    b.close()
