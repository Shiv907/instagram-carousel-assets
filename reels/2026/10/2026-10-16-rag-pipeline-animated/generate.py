import os, math, glob, sys
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920; LIMIT=1536
G="/usr/share/fonts/truetype/sand-box/google/"
AB=G+"Archivo Black/ArchivoBlack-Regular.ttf"; PB=G+"Poppins/Poppins-Bold.ttf"; PSB=G+"Poppins/Poppins-SemiBold.ttf"; MONO=G+"IBM Plex Mono/IBMPlexMono-Bold.ttf"
F=lambda p,s:ImageFont.truetype(p,s)
YEL=(255,200,0,255); WHITE=(245,247,250,255); OUT=(10,12,18,255); CARD=(30,37,54,255); PANEL=(13,17,28,240)
CYAN=(34,211,238,255); ORANGE=(255,153,0,255); GREEN=(52,211,153,255); VIOLET=(167,139,250,255); RED=(248,92,92,255); MUTED=(160,170,190,255)
OUTDIR=sys.argv[1] if len(sys.argv)>1 else "out"
def L(): 
    im=Image.new("RGBA",(W,H),(0,0,0,0)); return im,ImageDraw.Draw(im)
def tw(d,s,f): b=d.textbbox((0,0),s,font=f,stroke_width=0); return b[2]-b[0]
def ctext(d,s,y,font,fill=WHITE,stroke=6,cx=W//2):
    b=d.textbbox((0,0),s,font=font); w=b[2]-b[0]
    x=cx-w//2-b[0]; d.text((x,y-b[1]),s,font=font,fill=fill,stroke_width=stroke,stroke_fill=OUT)
    bb=d.textbbox((x,y-b[1]),s,font=font,stroke_width=stroke); assert bb[0]>=40 and bb[2]<=W-40,("xclip",s,bb); return bb
def rich(d,parts,y,font,stroke=6):
    total=sum(tw(d,t,font) for t,_ in parts); assert total<=980,("wide",parts,total); x=(W-total)//2
    b=d.textbbox((0,0),"Ag",font=font)
    for t,c in parts: d.text((x,y-b[1]),t,font=font,fill=c,stroke_width=stroke,stroke_fill=OUT); x+=tw(d,t,font)
def arrow(d,p1,p2,col=WHITE,w=10,head=34):
    (x1,y1),(x2,y2)=p1,p2; a=math.atan2(y2-y1,x2-x1)
    d.line((x1,y1,x2-head*0.6*math.cos(a),y2-head*0.6*math.sin(a)),fill=col,width=w)
    d.polygon([(x2,y2),(x2+head*math.cos(a+2.6),y2+head*math.sin(a+2.6)),(x2+head*math.cos(a-2.6),y2+head*math.sin(a-2.6))],fill=col)
# ---- icons (cx,cy,s=size) ----
def i_doc(d,cx,cy,s,col=CYAN,label=None):
    x0,y0,x1,y1=cx-s*0.38,cy-s/2,cx+s*0.38,cy+s/2; f=s*0.25
    d.polygon([(x0,y0),(x1-f,y0),(x1,y0+f),(x1,y1),(x0,y1)],fill=WHITE,outline=OUT,width=4)
    d.polygon([(x1-f,y0),(x1-f,y0+f),(x1,y0+f)],fill=(200,205,215,255))
    for k in range(4): d.line((x0+s*0.12,y0+s*(0.38+k*0.13),x1-s*0.12,y0+s*(0.38+k*0.13)),fill=(150,160,180,255),width=max(3,int(s*0.04)))
    if label:
        d.rounded_rectangle((x0-s*0.08,cy-s*0.02,x1-s*0.1,cy+s*0.24),radius=8,fill=RED); ff=F(PB,int(s*0.2)); b=d.textbbox((0,0),label,font=ff)
        d.text(((x0-s*0.08+x1-s*0.1)/2-(b[2]-b[0])/2-b[0],cy+s*0.11-(b[1]+b[3])/2),label,font=ff,fill=WHITE)
def i_chunks(d,cx,cy,s,col=ORANGE):
    for k in range(3):
        y=cy-s*0.42+k*s*0.3; d.rounded_rectangle((cx-s*0.4,y,cx+s*0.4,y+s*0.22),radius=8,fill=col,outline=OUT,width=3)
def i_vec(d,cx,cy,s,col=VIOLET):
    hs=[0.5,0.85,0.3,0.7,0.45]
    for k,h in enumerate(hs):
        x=cx-s*0.42+k*s*0.18; d.rectangle((x,cy+s*0.4-h*s*0.8,x+s*0.12,cy+s*0.4),fill=col)
def i_db(d,cx,cy,s,col=GREEN):
    x0,x1=cx-s*0.38,cx+s*0.38; e=s*0.2
    for k in (2,1,0):
        y=cy-s*0.42+k*s*0.28; d.rectangle((x0,y+e/2,x1,y+e/2+s*0.28),fill=col); d.ellipse((x0,y+s*0.28,x1,y+s*0.28+e),fill=col)
        d.ellipse((x0,y,x1,y+e),fill=(150,240,200,255),outline=OUT,width=3)
def i_user(d,cx,cy,s,col=CYAN):
    d.ellipse((cx-s*0.18,cy-s*0.45,cx+s*0.18,cy-s*0.09),fill=col); d.pieslice((cx-s*0.38,cy-s*0.02,cx+s*0.38,cy+s*0.74),180,360,fill=col)
def i_search(d,cx,cy,s,col=GREEN):
    r=s*0.28; d.ellipse((cx-s*0.15-r,cy-s*0.15-r,cx-s*0.15+r,cy-s*0.15+r),outline=col,width=int(s*0.1))
    d.line((cx+s*0.06,cy+s*0.06,cx+s*0.4,cy+s*0.4),fill=col,width=int(s*0.13))
def i_chip(d,cx,cy,s,col=YEL):
    for k in range(4):
        o=-s*0.27+k*s*0.18
        for (a,b,c2,e) in [(cx+o,cy-s*0.48,cx+o,cy-s*0.3),(cx+o,cy+s*0.3,cx+o,cy+s*0.48),(cx-s*0.48,cy+o,cx-s*0.3,cy+o),(cx+s*0.3,cy+o,cx+s*0.48,cy+o)]: d.line((a,b,c2,e),fill=col,width=6)
    d.rounded_rectangle((cx-s*0.32,cy-s*0.32,cx+s*0.32,cy+s*0.32),radius=14,fill=col,outline=OUT,width=4)
    ff=F(AB,int(s*0.2)); b=d.textbbox((0,0),"AI",font=ff); d.text((cx-(b[2]-b[0])/2-b[0],cy-(b[1]+b[3])/2),"AI",font=ff,fill=OUT)
def i_bubble(d,cx,cy,s,col=GREEN):
    d.rounded_rectangle((cx-s*0.45,cy-s*0.38,cx+s*0.45,cy+s*0.22),radius=20,fill=col,outline=OUT,width=4)
    d.polygon([(cx-s*0.2,cy+s*0.2),(cx-s*0.32,cy+s*0.45),(cx,cy+s*0.2)],fill=col)
    d.line((cx-s*0.2,cy-s*0.08,cx-s*0.05,cy+s*0.06,cx+s*0.22,cy-s*0.22),fill=OUT,width=int(s*0.08),joint="curve")
def i_bot(d,cx,cy,s):
    # antenna + head + eyes + body
    d.line((cx,cy-s*0.62,cx,cy-s*0.45),fill=WHITE,width=10); d.ellipse((cx-22,cy-s*0.62-22,cx+22,cy-s*0.62+22),fill=YEL,outline=OUT,width=4)
    d.rounded_rectangle((cx-s*0.42,cy-s*0.45,cx+s*0.42,cy+s*0.05),radius=50,fill=WHITE,outline=OUT,width=6)
    d.rounded_rectangle((cx-s*0.33,cy-s*0.36,cx+s*0.33,cy-s*0.04),radius=36,fill=(20,26,40,255))
    for ex in (-0.15,0.15): d.ellipse((cx+s*ex-24,cy-s*0.2-24,cx+s*ex+24,cy-s*0.2+24),fill=CYAN)
    d.rounded_rectangle((cx-s*0.3,cy+s*0.1,cx+s*0.3,cy+s*0.5),radius=40,fill=WHITE,outline=OUT,width=6)
    d.ellipse((cx-28,cy+s*0.22,cx+28,cy+s*0.22+56),fill=YEL,outline=OUT,width=4)
    # arm reaching right
    d.line((cx+s*0.28,cy+s*0.22,cx+s*0.52,cy+s*0.1),fill=WHITE,width=30); d.ellipse((cx+s*0.52-26,cy+s*0.1-26,cx+s*0.52+26,cy+s*0.1+26),fill=WHITE,outline=OUT,width=5)
def box(d,y,h,col,label,icon=None,sub=None,size=60):
    d.rounded_rectangle((110,y,970,y+h),radius=40,fill=CARD,outline=col,width=6)
    if icon: icon(d,230,y+h/2,h*0.62)
    tx=340 if icon else W//2; f=F(PB,size)
    lines=[(label,f,WHITE)]+([(sub,F(MONO,40),col)] if sub else [])
    hs=[d.textbbox((0,0),t,font=ff)[3]-d.textbbox((0,0),t,font=ff)[1] for t,ff,_ in lines]; gap=22; tot=sum(hs)+gap*(len(lines)-1); yy=y+h/2-tot/2
    for (t,ff,c),hh in zip(lines,hs):
        b=d.textbbox((0,0),t,font=ff); x=tx if icon else W//2-(b[2]-b[0])//2
        d.text((x-b[0],yy-b[1]),t,font=ff,fill=c,stroke_width=3,stroke_fill=OUT); assert x+(b[2]-b[0])<=945,("boxclip",t); yy+=hh+gap
def make_bg():
    im=Image.new("RGBA",(W,H),(9,12,20,255)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line((0,y,W,y),fill=(int(14-5*t),int(18-6*t),int(32-12*t),255))
    g,gd=L()
    for x in range(0,W,90): gd.line((x,0,x,LIMIT),fill=(255,255,255,12),width=2)
    for y in range(0,LIMIT,90): gd.line((0,y,W,y),fill=(255,255,255,12),width=2)
    im.alpha_composite(g); p,pd=L()
    pd.rounded_rectangle((60,280,W-60,1500),radius=48,fill=PANEL,outline=(255,255,255,40),width=3)
    im.alpha_composite(p); return im
S={}
def scene(n): 
    def reg(f): S[n]=f; return f
    return reg
@scene(1)
def s1(add):
    im,d=L(); i_bot(d,470,780,520); add("01-icon-chatbot",im)
    im,d=L(); i_doc(d,770,790,230,label="PDF"); add("02-icon-pdf",im)
    im,d=L(); ctext(d,"Aapke PDFs se",1170,F(AB,92)); ctext(d,"answer kaise?",1290,F(AB,92),fill=YEL); add("03-text-hook",im)
@scene(2)
def s2(add):
    f=F(AB,150); fw=F(AB,104)
    im,d=L(); ctext(d,"RAG =",400,f,fill=YEL,stroke=8); add("01-text-rag-equals",im)
    for i,(w,n) in enumerate([("Retrieval","02-text-retrieval"),("Augmented","03-text-augmented"),("Generation","04-text-generation")]):
        im,d=L(); rich(d,[(w[0],YEL),(w[1:],WHITE)],700+i*220,fw,stroke=7); add(n,im)
@scene(3)
def s3(add):
    y0,h,g=340,200,100; items=[("Documents",i_doc,CYAN,None),("Chunks",i_chunks,ORANGE,None),("Embeddings",i_vec,VIOLET,"[0.12, -0.4, ...]"),("Vector DB",i_db,GREEN,None)]
    names=["01-box-documents","03-box-chunks","05-box-embeddings","07-box-vector-db"]
    for i,(lab,ic,col,sub) in enumerate(items):
        y=y0+i*(h+g)
        if i>0:
            im,d=L(); arrow(d,(W//2,y-g+14),(W//2,y-14)); add(f"0{2*i}-arrow-{i}",im)
        im,d=L(); box(d,y,h,col,lab,ic,sub); add(names[i],im)
@scene(4)
def s4(add):
    im,d=L(); ctext(d,"Retrieval",330,F(AB,100),fill=YEL,stroke=7); add("01-label-retrieval",im)
    y0,h,g=490,170,85; items=[("User question",i_user,CYAN),("Embedding",i_vec,VIOLET),("Search in Vector DB",i_search,GREEN),("Top chunks returned",i_chunks,ORANGE)]
    k=2
    for i,(lab,ic,col) in enumerate(items):
        y=y0+i*(h+g)
        if i>0:
            im,d=L(); arrow(d,(W//2,y-g+12),(W//2,y-12)); add(f"{k:02d}-arrow-{i}",im); k+=1
        im,d=L(); box(d,y,h,col,lab,ic,size=54); add(f"{k:02d}-box-"+lab.lower().replace(" ","-"),im); k+=1
@scene(5)
def s5(add):
    im,d=L(); ctext(d,"Generation",330,F(AB,100),fill=YEL,stroke=7); add("01-label-generation",im)
    def sm(d,x0,lab,ic,col):
        d.rounded_rectangle((x0,500,x0+380,700),radius=36,fill=CARD,outline=col,width=6); ic(d,x0+75,600,100)
        f=F(PB,44); b=d.textbbox((0,0),lab,font=f); d.text((x0+135-b[0],600-(b[1]+b[3])/2),lab,font=f,fill=WHITE,stroke_width=3,stroke_fill=OUT); assert x0+140+b[2]-b[0]<=x0+365,(lab,b)
    im,d=L(); sm(d,110,"Chunks",i_chunks,ORANGE); add("02-box-chunks",im)
    im,d=L(); ctext(d,"+",560,F(AB,90),stroke=6); add("03-plus",im)
    im,d=L(); sm(d,590,"Question",i_user,CYAN); add("04-box-question",im)
    im,d=L(); arrow(d,(295,712),(470,850)); arrow(d,(785,712),(610,850)); add("05-arrows-to-llm",im)
    im,d=L(); box(d,870,210,YEL,"LLM",i_chip,size=80); add("06-box-llm",im)
    im,d=L(); arrow(d,(W//2,1095),(W//2,1205)); add("07-arrow-to-answer",im)
    im,d=L(); box(d,1220,200,GREEN,"Answer",i_bubble,size=70); add("08-box-answer",im)
@scene(6)
def s6(add):
    im,d=L(); d.rounded_rectangle((110,420,970,820),radius=44,fill=CARD,outline=YEL,width=8)
    ctext(d,"Amazon Bedrock",500,F(AB,82)); ctext(d,"Knowledge Bases",640,F(AB,82),fill=YEL); add("01-box-bedrock-kb",im)
    im,d=L(); ctext(d,"=",880,F(AB,130),stroke=7); add("02-equals",im)
    im,d=L(); ctext(d,"ye sab managed",1080,F(AB,92),stroke=7); add("03-text-ye-sab-managed",im)
    im,d=L(); xs=[260,430,600,770]; 
    for x,ic in zip(xs,[i_doc,i_chunks,i_vec,i_db]): ic(d,x,1300,120)
    for a,b in zip(xs,xs[1:]): arrow(d,(a+65,1300),(b-65,1300),w=6,head=20)
    add("04-icons-pipeline-managed",im)
@scene(7)
def s7(add):
    im,d=L(); d.rounded_rectangle((110,420,970,640),radius=44,fill=CARD,outline=VIOLET,width=6); ctext(d,"Next:",445,F(AB,60),fill=YEL); ctext(d,"Keyword vs Semantic",535,F(AB,62)); add("01-card-next-embeddings",im)
    im,d=L(); ctext(d,"|",690,F(AB,90),fill=MUTED,stroke=0); add("02-divider",im)
    im,d=L(); d.rounded_rectangle((110,850,970,1070),radius=44,fill=CARD,outline=YEL,width=6); rich(d,[("Follow",WHITE),(" + ",YEL),("Save",WHITE)],920,F(AB,96)); add("03-card-follow-save",im)
    im,d=L(); ctext(d,"@shivanshu_builds",1200,F(PB,64),stroke=4); add("04-handle",im)
def run():
    bg=make_bg(); rows={}; comps=[]
    for n in sorted(S):
        out=f"{OUTDIR}/scene{n}"; os.makedirs(out,exist_ok=True)
        for f in glob.glob(out+"/*.png"): os.remove(f)
        bg.save(f"{out}/bg.png"); comp=bg.copy(); names=[]
        def add(name,im):
            bb=im.getchannel("A").getbbox(); assert bb and bb[3]<=LIMIT and bb[1]>=0,(n,name,bb)
            im.save(f"{out}/{name}.png"); comp.alpha_composite(im); names.append((name,bb))
        S[n](add); comp.convert("RGB").save(f"{out}/composite.png"); rows[n]=names; comps.append(comp)
    tw_,th_=360,640; sh=Image.new("RGB",(tw_*4+50,th_*2+30),(40,40,40))
    for i,c in enumerate(comps): sh.paste(c.convert("RGB").resize((tw_,th_)),(10+(i%4)*(tw_+10),10+(i//4)*(th_+10)))
    sh.save(f"{OUTDIR}/contact-sheet.png")
    for n,v in rows.items(): print(n,v)
if __name__=="__main__": run()
