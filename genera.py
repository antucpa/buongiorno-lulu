"""Buongiorno Lulù — quotidiano A4. Solo Python stdlib + reportlab + PyMuPDF."""
import os, re, json, html, random, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import fitz

ROOT=os.path.dirname(os.path.abspath(__file__))
now=datetime.now(ZoneInfo('Europe/Rome')); day=now.strftime('%Y-%m-%d')
week=['lunedì','martedì','mercoledì','giovedì','venerdì','sabato','domenica']
months=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
longdate=f'{week[now.weekday()].upper()} {now.day} {months[now.month-1].upper()} {now.year}'

FONTDIR=os.environ.get('LULU_FONTS','/usr/share/fonts/truetype/liberation')
for nm,fn in [('Serif','LiberationSerif-Regular.ttf'),('SerifB','LiberationSerif-Bold.ttf'),('SerifI','LiberationSerif-Italic.ttf'),('Sans','LiberationSans-Regular.ttf'),('SansB','LiberationSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(nm,os.path.join(FONTDIR,fn)))

def clean(s):
    s=re.sub(r'<[^>]+>',' ',s or '')
    return re.sub(r'\s+',' ',html.unescape(s)).strip()

def news(query):
    url='https://news.google.com/rss/search?q='+quote(query)+'&hl=it&gl=IT&ceid=IT:it'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 BuongiornoLulu/1.0'})
        with urllib.request.urlopen(req,timeout=20) as f: data=f.read()
        root=ET.fromstring(data)
        for el in root.findall('./channel/item'):
            title=clean(el.findtext('title')); link=(el.findtext('link') or '').strip()
            source=clean(el.findtext('source'))
            description=clean(el.findtext('description'))
            if title and link:
                # Google News spesso ripete il titolo nella descrizione: non inventare riassunti.
                if description.lower().startswith(title.lower()[:45]): description=''
                title=re.sub(r'\s+-\s+[^-]{2,55}$','',title).strip()
                return {'title':title,'source':source,'url':link,'description':description[:380]}
    except Exception as exc: print('Feed non disponibile',query,exc)
    return {'title':'Notizia non disponibile','source':'','url':'','description':'La fonte non è raggiungibile al momento della pubblicazione.'}

items={
 'italia':news('Italia notizia primo piano oggi when:1d'),
 'mondo':news('notizie esteri mondo internazionale oggi when:1d'),
 'buona':news('buone notizie ricerca scientifica medicina scoperta when:7d'),
 'marche':news('Macerata Marche notizie oggi when:3d'),
 'cultura':news('teatro cultura libri cinema Italia when:3d'),
}

POEMS=[('San Martino','Giosuè Carducci',"""La nebbia a gl’irti colli
piovigginando sale,
e sotto il maestrale
urla e biancheggia il mar;

ma per le vie del borgo
dal ribollir de’ tini
va l’aspro odor de i vini
l’anime a rallegrar.

Gira su’ ceppi accesi
lo spiedo scoppiettando:
sta il cacciator fischiando
su l’uscio a rimirar

tra le rossastre nubi
stormi d’uccelli neri,
com’esuli pensieri,
nel vespero migrar."""),('A Zacinto','Ugo Foscolo',"""Né più mai toccherò le sacre sponde
ove il mio corpo fanciulletto giacque,
Zacinto mia, che te specchi nell’onde
del greco mar da cui vergine nacque

Venere, e fea quelle isole feconde
col suo primo sorriso, onde non tacque
le tue limpide nubi e le tue fronde
l’inclito verso di colui che l’acque

cantò fatali, ed il diverso esiglio
per cui bello di fama e di sventura
baciò la sua petrosa Itaca Ulisse.

Tu non altro che il canto avrai del figlio,
o materna mia terra; a noi prescrisse
il fato illacrimata sepoltura.""")]
PSY=[('L’effetto alone','Una qualità che ci colpisce può condizionare il giudizio complessivo su una persona. Ricordarlo aiuta a non scambiare la prima impressione per una conoscenza completa.'),('Il bias di conferma','Cerchiamo e ricordiamo più facilmente le informazioni che sostengono ciò che già pensiamo. Confrontarci con dati contrari rende più accurati i nostri giudizi.'),('La memoria ricostruttiva','Ricordare non equivale a rivedere una registrazione: ogni ricordo viene ricostruito e può cambiare nei dettagli, anche senza che ce ne accorgiamo.'),('L’attenzione selettiva','La mente non può elaborare tutto contemporaneamente. Per questo selezioniamo alcuni stimoli e ne trascuriamo altri, talvolta anche importanti.')]
poem=POEMS[now.toordinal()%len(POEMS)]; psych=PSY[now.toordinal()%len(PSY)]

# Sudoku deterministico, con soluzione unica verificata.
rng=random.Random(day)
base=lambda r,c:(r*3+r//3+c)%9+1
rows=[g*3+r for g in rng.sample(range(3),3) for r in rng.sample(range(3),3)]
cols=[g*3+c for g in rng.sample(range(3),3) for c in rng.sample(range(3),3)]
nums=rng.sample(range(1,10),9)
solution=[nums[base(r,c)-1] for r in rows for c in cols]
puzzle=solution[:]
def solutions(g,cap=2):
    found=0
    def options(i):
        r,c=divmod(i,9)
        used=set(g[r*9:r*9+9])|set(g[c::9])|{g[(r//3*3+rr)*9+c//3*3+cc] for rr in range(3) for cc in range(3)}
        return [v for v in range(1,10) if v not in used]
    def go():
        nonlocal found
        if found>=cap:return
        cand=[(options(i),i) for i,v in enumerate(g) if v==0]
        if not cand:found+=1;return
        opts,i=min(cand,key=lambda x:len(x[0]))
        for n in opts:
            g[i]=n;go();g[i]=0
            if found>=cap:return
    go();return found
for i in rng.sample(range(81),81):
    old=puzzle[i];puzzle[i]=0
    if solutions(puzzle[:])!=1:puzzle[i]=old
    if puzzle.count(0)>=43:break

W,H=A4; M=32; CW=W-2*M; gap=20; half=(CW-gap)/2
ink=HexColor('#25221e'); burg=HexColor('#702c34'); muted=HexColor('#5c5650'); pale=HexColor('#f5f0e8')
c=canvas.Canvas(os.path.join(ROOT,'giornale.pdf'),pagesize=A4)
c.setFillColor(HexColor('#fffdfa'));c.rect(0,0,W,H,fill=1,stroke=0)
def line(x,y,x2,y2=None,col=ink,width=.5):
    c.setStrokeColor(col);c.setLineWidth(width);c.line(x,y,x2,y if y2 is None else y2)
def text(x,y,s,size=9,font='Serif',color=ink):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)
def centered(y,s,size=9,font='SerifB',color=ink):
    c.setFillColor(color);c.setFont(font,size);c.drawCentredString(W/2,y,s)
def paragraph(x,top,width,body,size=9.0,leading=10.8,font='Serif',max_height=None,color=ink):
    st=ParagraphStyle('lulu',fontName=font,fontSize=size,leading=leading,textColor=color)
    body=html.escape(body).replace('\n','<br/>')
    p=Paragraph(body,st);_,h=p.wrap(width,500)
    if max_height is not None and h>max_height:
        words=body.split()
        while words:
            words=words[:-1];p=Paragraph(' '.join(words)+'…',st);_,h=p.wrap(width,500)
            if h<=max_height:break
    p.drawOn(c,x,top-h);return top-h
def label(x,y,s):text(x,y,s.upper(),8.1,'SerifB',burg)
def story(x,top,width,k,small=False):
    item=items[k]
    title_size=12.4 if small else 14.4
    body_size=8.5 if small else 9.0
    title_bottom=paragraph(x,top,width,item['title'],title_size,title_size+1.0,'SerifB',max_height=45 if not small else 42)
    body=item['description'] or ('Fonte: '+item['source']+'. Consulta l’articolo originale per l’approfondimento.')
    body_bottom=paragraph(x,title_bottom-5,width,body,body_size,body_size+1.8,max_height=68 if not small else 75)
    return body_bottom

# Testata e data
line(M,H-30,W-M,H-30,burg,1.1)
centered(H-46,'IL QUOTIDIANO CHE SI LEGGE CON IL CAFFÈ',8.6,'SerifB',muted)
centered(H-95,'Buongiorno Lulù',43,'SerifB')
line(M,H-108,W-M,H-108,burg,1.5);line(M,H-111,W-M,H-111,burg,.4)
text(M,H-126,'ANNO I  ·  EDIZIONE QUOTIDIANA',8,'SerifB',muted)
centered(H-126,longdate,9.4)
c.setFont('SerifI',8);c.setFillColor(muted);c.drawRightString(W-M,H-126,'Edizione del mattino')
line(M,H-134,W-M,H-134)
centered(H-153,'DUE FATTI PER CAPIRE LA GIORNATA',9,'SerifB',burg)
x1=M;x2=M+half+gap
label(x1,H-171,'PRIMO PIANO · ITALIA');label(x2,H-171,'PRIMO PIANO · MONDO')
story(x1,H-179,half,'italia');story(x2,H-179,half,'mondo')
line(W/2,H-164,W/2,H-303,HexColor('#c7bdb1'),.5)
Y=H-316;line(M,Y,W-M,Y,burg,1.0)
label(M,Y-14,'LE ALTRE STORIE CHE MERITANO LA PRIMA PAGINA')
# Parte centrale: due storie e poesia in colonna, Sudoku sotto le storie
G=14;tw=(CW-2*G)/3; xs=[M,M+tw+G,M+2*(tw+G)];T=Y-27
label(xs[0],T,'LA BUONA NOTIZIA');label(xs[1],T,'VOCI DAL TERRITORIO')
story(xs[0],T-7,tw,'buona',True);story(xs[1],T-7,tw,'marche',True)
# Poesia completa, compatta in riquadro
px=xs[2]-5;pw=tw+10;poem_top=T+9;poem_h=213
c.setFillColor(pale);c.roundRect(px,poem_top-poem_h,pw,poem_h,5,fill=1,stroke=0)
label(xs[2]+3,T,'LA POESIA DEL GIORNO')
text(xs[2]+3,T-19,poem[0],14.3,'SerifB');text(xs[2]+3,T-31,poem[1],8.7,'SerifI',muted)
verses=poem[2].splitlines(); yy=T-43
for v in verses:
    if v: text(xs[2]+3,yy,v,8.2,'SerifI')
    yy-=8.4 if v else 3.2
# Sudoku
sx=xs[1]+5;sy=T-125;cell=9.2
label(xs[0],T-130,'IL SUDOKU DEL CAFFÈ')
text(xs[0],T-144,'Livello medio · Soluzione online',8,'SerifI',muted)
paragraph(xs[0],T-152,tw-12,'Ogni riga, colonna e riquadro contiene i numeri da 1 a 9.',8.1,9.8)
for r in range(9):
    for co in range(9):
        n=puzzle[r*9+co]
        if n:text(sx+co*cell+3,sy-r*cell-7,str(n),8,'SerifB')
for i in range(10):
    c.setLineWidth(1.25 if i%3==0 else .3);c.setStrokeColor(ink)
    c.line(sx+i*cell,sy,sx+i*cell,sy-9*cell)
    c.line(sx,sy-i*cell,sx+9*cell,sy-i*cell)
# Terza fascia
B=H-566;line(M,B,W-M,B,burg,.9)
label(M,B-14,'IL TACCUINO DI LULÙ')
paragraph(M,B-21,CW*.57,'Una domanda da portare con sé: che cosa abbiamo imparato oggi che ieri non sapevamo?',9.1,11.1,max_height=34)
line(M+CW*.62,B-18,M+CW*.62,B-62,HexColor('#c7bdb1'),.5)
paragraph(M+CW*.66,B-21,CW*.34,'Un invito: leggere con curiosità, discutere con rispetto, cambiare idea quando servono nuovi fatti.',8.8,10.4,max_height=43)
B2=H-640;line(M,B2,W-M,B2,burg,.65)
label(M,B2-14,'CULTURA, IDEE, SCOPERTE')
story(M,B2-22,half,'cultura',True)
paragraph(x2,B2-22,half,'La lettura del giorno: scegliere una notizia, cercarne la fonte originale e distinguere i fatti dalle opinioni. È un piccolo esercizio di libertà.',9.2,11.2,max_height=65)
# Psicologia prima delle fonti
P=H-727;line(M,P,W-M,P,burg,1.0)
label(M,P-15,'LA MENTE IN POCHE RIGHE')
text(M,P-30,psych[0],10.4,'SansB')
paragraph(M,P-35,CW,psych[1],8.8,10.2,'Sans',max_height=28)
# Fonti sempre ultime
F=49;line(M,F,W-M,F,HexColor('#b5a99a'),.5)
sources=' · '.join(dict.fromkeys([x['source'] for x in items.values() if x['source']]))
paragraph(M,F-5,CW,'FONTI: '+(sources or 'Feed non disponibili: controllare i link sul sito'),7.1,8.2,max_height=18,color=muted)
text(M,14,'Notizie: titoli e brevi estratti da feed pubblici · Poesia integrale di pubblico dominio',7.1,'SerifI',muted)
c.showPage();c.save()
# JPEG direttamente stampabile dalla Canon; A4 150 dpi (1240 x 1754)
pdf=fitz.open(os.path.join(ROOT,'giornale.pdf'))
pix=pdf[0].get_pixmap(matrix=fitz.Matrix(150/72,150/72),alpha=False)
pix.save(os.path.join(ROOT,'giornale.jpg'),jpg_quality=85)
with open(os.path.join(ROOT,'edizione.json'),'w',encoding='utf8') as f:
    json.dump({'data':day,'generata_alle':now.isoformat(),'notizie':items,'sudoku':puzzle,'soluzione_sudoku':solution},f,ensure_ascii=False,indent=2)
links=''.join('<li><b>'+html.escape(k.capitalize())+'</b>: <a href="'+html.escape(v['url'],quote=True)+'">'+html.escape(v['title'])+'</a> ('+html.escape(v['source'])+')</li>' for k,v in items.items() if v['url'])
page=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Buongiorno Lulù — {day}</title><style>body{{font-family:Georgia,serif;background:#eee8de;color:#25221e;max-width:850px;margin:20px auto;padding:16px}}h1,p{{text-align:center}}img{{display:block;width:100%;box-shadow:0 3px 14px #aaa}}a{{color:#702c34}}</style></head><body><h1>Buongiorno Lulù</h1><p>{longdate}</p><a href="giornale.jpg"><img src="giornale.jpg" alt="Giornale del giorno A4"></a><p><a href="giornale.pdf">Scarica il giornale PDF</a> · <a href="giornale.jpg">JPEG per la Canon</a></p><h2>Fonti delle notizie</h2><ul>{links}</ul><p>La selezione dei titoli è automatica: consultare sempre gli articoli originali per il contesto e le verifiche.</p></body></html>'''
with open(os.path.join(ROOT,'index.html'),'w',encoding='utf8') as f:f.write(page)
print('Edizione generata:',day,os.path.getsize(os.path.join(ROOT,'giornale.jpg')),'byte')
