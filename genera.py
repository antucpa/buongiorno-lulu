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

# I contenuti sono preparati dalla redazione automatica ChatGPT.
# Nessun titolo RSS viene scambiato per un articolo completo.
with open(os.path.join(ROOT,'contenuti.json'),encoding='utf8') as f:
    edition=json.load(f)
if edition.get('data') != day:
    raise RuntimeError('Contenuti non aggiornati a oggi: conservata la precedente edizione.')
items=edition.get('notizie',{})
required={'italia','mondo','buona','marche','cultura'}
if set(items) != required:
    raise ValueError('Servono cinque rubriche complete.')
for key,item in items.items():
    for field in ('title','description','source','url','published_at'):
        if not isinstance(item.get(field),str) or not item[field].strip():
            raise ValueError(f'{key}: campo {field} mancante.')
    if not item['url'].startswith('https://') or 'news.google.com' in item['url']:
        raise ValueError(f'{key}: serve il link alla fonte originale.')
    minimum=50 if key in ('italia','mondo') else 32
    if len(item['description'].split()) < minimum:
        raise ValueError(f'{key}: testo troppo breve.')
    age=(now.date()-datetime.strptime(item['published_at'],'%Y-%m-%d').date()).days
    if age < 0 or age > (7 if key in ('buona','cultura') else 3 if key=='marche' else 1):
        raise ValueError(f'{key}: fonte non recente.')
    if any(s in item['description'].lower() for s in ('consulta l’articolo','notizia non disponibile','fonte non raggiungibile')):
        raise ValueError(f'{key}: testo segnaposto vietato.')


    if item.get('ambito') not in ({'macerata'} if key=='marche' else {'nazionale','internazionale'}):
        raise ValueError(f'{key}: ammessa una sola notizia locale, quella di Macerata.')
meteo=edition.get('meteo',{})
if meteo.get('data')!=day or meteo.get('localita')!='Macerata':
    raise ValueError('Servono le previsioni odierne per Macerata.')
for field in ('condizioni','source','url'):
    if not isinstance(meteo.get(field),str) or not meteo[field].strip():
        raise ValueError(f'Meteo: campo {field} mancante.')
if not meteo['url'].startswith('https://'):
    raise ValueError('Meteo: collegamento alla fonte non valido.')
for field in ('min_c','max_c'):
    value=meteo.get(field)
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not -60<=value<=60:
        raise ValueError('Temperature meteo non valide.')
if meteo['min_c']>meteo['max_c'] or len(meteo['condizioni'])>90:
    raise ValueError('Previsione meteo non valida o troppo lunga.')
def degrees(value):
    return f'{value:g} °C'
weather_line=f"Min {degrees(meteo['min_c'])}  ·  Max {degrees(meteo['max_c'])}"

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
def paragraph(x,top,width,body,size=9.0,leading=10.8,font='Serif',max_height=None,color=ink,strict=False):
    body=html.escape(body).replace('\n','<br/>')
    while True:
        st=ParagraphStyle('lulu',fontName=font,fontSize=size,leading=leading,textColor=color)
        p=Paragraph(body,st);_,h=p.wrap(width,1000)
        if max_height is None or h<=max_height:
            break
        if strict:
            if size <= 8.0:
                raise ValueError('Testo troppo lungo per il riquadro: accorciare la sintesi prima di pubblicare.')
            size-=.15; leading-=.15
        else:
            words=body.split()
            while words:
                words=words[:-1];p=Paragraph(' '.join(words)+'…',st);_,h=p.wrap(width,1000)
                if h<=max_height:break
            break
    p.drawOn(c,x,top-h);return top-h
def label(x,y,s):text(x,y,s.upper(),8.1,'SerifB',burg)
def story(x,top,width,k,small=False,bottom=None):
    item=items[k]
    title_size=12.4 if small else 14.4
    body_size=8.5 if small else 9.0
    title_bottom=paragraph(x,top,width,item['title'],title_size,title_size+1.0,'SerifB',max_height=42,strict=True)
    if bottom is None: bottom=top-(116 if small else 124)
    body_bottom=paragraph(x,title_bottom-5,width,item['description'],body_size,body_size+1.5,
        max_height=title_bottom-5-bottom-12,strict=True)
    text(x,body_bottom-10,item['source'],6.8,'SerifI',muted)
    c.linkURL(item['url'],(x,bottom,x+width,top),relative=0)
    return body_bottom


def weather_icon(x,y,description):
    # Disegno vettoriale: nessuna dipendenza da font emoji.
    import math
    desc=description.lower()
    rain=any(word in desc for word in ('piogg','rovesc','tempor','piov'))
    snow=any(word in desc for word in ('nev','neve'))
    fog=any(word in desc for word in ('nebb','fosch'))
    cloud=rain or snow or any(word in desc for word in ('nuvol','copert'))
    sun=not (rain or snow or fog or 'coperto' in desc)
    c.saveState()
    if sun:
        c.setStrokeColor(HexColor('#c49027'));c.setFillColor(HexColor('#efc65c'));c.setLineWidth(.8)
        sx=x-3 if cloud else x; sy=y+3 if cloud else y
        c.circle(sx,sy,4.2,fill=1,stroke=1)
        for angle in range(0,360,45):
            a=math.radians(angle)
            c.line(sx+6*math.cos(a),sy+6*math.sin(a),sx+8*math.cos(a),sy+8*math.sin(a))
    if cloud:
        c.setStrokeColor(HexColor('#89949b'));c.setFillColor(HexColor('#e6ebed'));c.setLineWidth(.7)
        p=c.beginPath();p.moveTo(x-7,y-4)
        p.curveTo(x-12,y-4,x-12,y+3,x-7,y+3)
        p.curveTo(x-7,y+10,x+3,y+10,x+4,y+4)
        p.curveTo(x+12,y+6,x+14,y-4,x+7,y-4)
        p.close();c.drawPath(p,fill=1,stroke=1)
    if rain or snow:
        c.setStrokeColor(HexColor('#668ba5'));c.setLineWidth(.8)
        for dx in (-5,1,7):
            c.line(x+dx,y-6,x+dx-2,y-9)
            if snow:c.line(x+dx-2,y-6,x+dx,y-9)
    if fog:
        c.setStrokeColor(HexColor('#89949b'));c.setLineWidth(1)
        for dy in (-4,0,4):c.line(x-10,y+dy,x+10,y+dy)
    c.restoreState()

# Testata e data
weather_icon(M+11,H-27,meteo['condizioni'])
label(M+30,H-30,'METEO · MACERATA')
paragraph(M+148,H-21,CW-288,meteo['condizioni'],8.4,9.5,max_height=19,strict=True)
c.setFont('SansB',8.0);c.setFillColor(ink);c.drawRightString(W-M,H-30,weather_line)
c.linkURL(meteo['url'],(M,H-40,W-M,H-12),relative=0)
line(M,H-44,W-M,H-44,burg,1.1)
centered(H-58,'IL QUOTIDIANO CHE SI LEGGE CON IL CAFFÈ',8.6,'SerifB',muted)
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
label(xs[0],T,'LA BUONA NOTIZIA');label(xs[1],T,'MACERATA')
story(xs[0],T-7,tw,'buona',True,bottom=T-119);story(xs[1],T-7,tw,'marche',True,bottom=T-119)
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
paragraph(M,B2-24,half,items['cultura']['title'],14.0,15.2,'SerifB',max_height=49,strict=True)
text(M,B2-76,items['cultura']['source'],7.0,'SerifI',muted)
paragraph(x2,B2-22,half,items['cultura']['description'],8.8,10.4,max_height=62,strict=True)
# Psicologia prima delle fonti
P=H-727;line(M,P,W-M,P,burg,1.0)
label(M,P-15,'LA MENTE IN POCHE RIGHE')
text(M,P-30,psych[0],10.4,'SansB')
paragraph(M,P-35,CW,psych[1],8.8,10.2,'Sans',max_height=28)
# Fonti sempre ultime
F=49;line(M,F,W-M,F,HexColor('#b5a99a'),.5)
sources=' · '.join(dict.fromkeys([x['source'] for x in items.values() if x['source']]+[meteo['source']]))
paragraph(M,F-5,CW,'FONTI: '+(sources or 'Feed non disponibili: controllare i link sul sito'),7.1,8.2,max_height=18,color=muted)
text(M,14,'Notizie: sintesi originali con fonti verificate · Poesia integrale di pubblico dominio',7.1,'SerifI',muted)
c.showPage();c.save()
# JPEG direttamente stampabile dalla Canon; A4 150 dpi (1240 x 1754)
pdf=fitz.open(os.path.join(ROOT,'giornale.pdf'))
pix=pdf[0].get_pixmap(matrix=fitz.Matrix(150/72,150/72),alpha=False)
pix.save(os.path.join(ROOT,'giornale.jpg'),jpg_quality=85)
with open(os.path.join(ROOT,'edizione.json'),'w',encoding='utf8') as f:
    json.dump({'data':day,'generata_alle':now.isoformat(),'notizie':items,'meteo':meteo,'sudoku':puzzle,'soluzione_sudoku':solution},f,ensure_ascii=False,indent=2)
asset_version=now.strftime('%Y%m%d%H%M%S')
links=''.join('<li><b>'+html.escape('Macerata' if k=='marche' else k.capitalize())+'</b>: <a href="'+html.escape(v['url'],quote=True)+'">'+html.escape(v['title'])+'</a> ('+html.escape(v['source'])+')<p>'+html.escape(v['description'])+'</p></li>' for k,v in items.items() if v['url'])
page=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Buongiorno Lulù — {day}</title><style>body{{font-family:Georgia,serif;background:#eee8de;color:#25221e;max-width:850px;margin:20px auto;padding:16px}}h1,p{{text-align:center}}img{{display:block;width:100%;box-shadow:0 3px 14px #aaa}}a{{color:#702c34}}</style></head><body><h1>Buongiorno Lulù</h1><p>{longdate}</p><h2>Meteo del giorno a Macerata</h2><p>{html.escape(meteo['condizioni'])} {html.escape(weather_line)}<br><a href="{html.escape(meteo['url'],quote=True)}">Previsioni: {html.escape(meteo['source'])}</a></p><a href="giornale.jpg?v={asset_version}"><img src="giornale.jpg?v={asset_version}" alt="Giornale del giorno A4"></a><p><a href="giornale.pdf?v={asset_version}">Scarica il giornale PDF</a> · <a href="giornale.jpg?v={asset_version}">JPEG per la Canon</a></p><h2>Fonti delle notizie</h2><ul>{links}</ul><p>Selezione e sintesi con assistenza AI. Fonti originali collegate per approfondimenti e verifica.</p></body></html>'''
with open(os.path.join(ROOT,'index.html'),'w',encoding='utf8') as f:f.write(page)
print('Edizione generata:',day,os.path.getsize(os.path.join(ROOT,'giornale.jpg')),'byte')
