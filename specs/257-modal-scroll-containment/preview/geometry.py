import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,url in {'before':'http://127.0.0.1:63404/','after':'http://127.0.0.1:8765/'}.items():
        page=b.new_page(viewport={'width':1200,'height':700})
        page.goto(url,wait_until='domcontentloaded');page.wait_for_timeout(250)
        page.evaluate("document.body.style.minHeight='4000px'; window.scrollTo(0,600)")
        closed=page.evaluate("({W:document.documentElement.clientWidth,S:scrollY})")
        page.evaluate("""()=>{const d=document.createElement('dialog');d.className='editor';d.id='probeDialog';d.innerHTML='<div class="editor__content"><p>short</p></div>';document.body.appendChild(d);d.showModal();}""")
        page.wait_for_timeout(80)
        opened=page.evaluate("""()=>{const d=document.getElementById('probeDialog');const b=d.getBoundingClientRect();return {W:document.documentElement.clientWidth,S:scrollY,x:b.x,y:b.y,w:b.width,h:b.height}}""")
        page.evaluate("document.getElementById('probeDialog').close()")
        page.wait_for_timeout(80)
        restored=page.evaluate("({W:document.documentElement.clientWidth,S:scrollY})")
        print(json.dumps({'side':name,'closed':closed,'opened':opened,'afterClose':restored}))
        page.close()
    b.close()
