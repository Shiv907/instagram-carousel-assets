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
    im.alpha_composite(p); return im# Overlays for filmed talking-head reel: face in TOP THIRD, content lower two-thirds
TOP=700  # start content around here (top third ends ~640)
def panel(d,x0,y0,x1,y1,col=(255,255,255,60),w=4):
    d.rounded_rectangle((x0,y0,x1,y1),radius=40,fill=PANEL,outline=col,width=w)
def mono(d,s,x,y,size,fill=WHITE):
    f=F(MONO,size); b=d.textbbox((0,0),s,font=f); d.text((x-b[0],y-b[1]),s,font=f,fill=fill)
    bb=d.textbbox((x-b[0],y-b[1]),s,font=f); assert bb[2]<=W-90,("monoclip",s,bb); return bb
def winbar(d,x0,y0,x1,title):
    d.rounded_rectangle((x0,y0,x1,y0+70),radius=40,fill=(40,48,68,255)); d.rectangle((x0,y0+40,x1,y0+70),fill=(40,48,68,255))
    for k,c in enumerate([RED,YEL,GREEN]): d.ellipse((x0+40+k*44,y0+22,x0+66+k*44,y0+48),fill=c)
    mono(d,title,x0+200,y0+20,32,MUTED)
def check(d,x,y,s=28,col=GREEN,w=8):
    d.line((x-s*0.5,y,x-s*0.15,y+s*0.35,x+s*0.5,y-s*0.4),fill=col,width=w,joint="curve")
def key_icon(d,cx,cy,s,col=YEL):
    d.ellipse((cx-s*0.35,cy-s*0.45,cx+s*0.35,cy+s*0.05),outline=col,width=int(s*0.12))
    d.rectangle((cx-s*0.08,cy,cx+s*0.08,cy+s*0.55),fill=col)
    d.rectangle((cx+s*0.08,cy+s*0.35,cx+s*0.32,cy+s*0.48),fill=col)
    d.rectangle((cx+s*0.08,cy+s*0.18,cx+s*0.24,cy+s*0.28),fill=col)
def lock_icon(d,cx,cy,s,col=RED):
    d.arc((cx-s*0.28,cy-s*0.55,cx+s*0.28,cy-s*0.05),180,360,fill=col,width=int(s*0.14))
    d.rounded_rectangle((cx-s*0.38,cy-s*0.1,cx+s*0.38,cy+s*0.45),radius=14,fill=col,outline=OUT,width=4)
    d.ellipse((cx-10,cy+s*0.05,cx+10,cy+s*0.05+20),fill=OUT)
O={}
def ov(name):
    def r(f): O[name]=f; return f
    return r

@ov("01-hook-signed-malware")
def o1(d,im):
    panel(d,90,1080,990,1440,YEL,6)
    ctext(d,"Signed release,",1140,F(AB,84)); ctext(d,"phir bhi malware",1265,F(AB,84),fill=YEL)

@ov("02-trust-chain")
def o2(d,im):
    panel(d,90,720,990,1480)
    ctext(d,"Trust chain",760,F(AB,64),fill=MUTED,stroke=3)
    items=[("Signed",),("Attested",),("Trusted Publisher",)]
    y=860
    for (lab,) in items:
        d.rounded_rectangle((160,y,920,y+90),radius=22,fill=CARD,outline=GREEN,width=5)
        check(d,220,y+48,32,GREEN,9)
        f=F(PB,48); b=d.textbbox((0,0),lab,font=f); d.text((280-b[0],y+45-(b[1]+b[3])/2),lab,font=f,fill=WHITE,stroke_width=2,stroke_fill=OUT)
        y+=110
    d.rounded_rectangle((160,y+20,920,y+130),radius=22,fill=CARD,outline=RED,width=6)
    ctext(d,"source: lookalike repo",y+55,F(AB,52),fill=RED,stroke=4)
    # provenance caption from on-screen text
    ctext(d,"Provenance ≠ sahi source",y+170,F(AB,56),fill=YEL,stroke=4)

@ov("03-pip-pth-drop")
def o3(d,im):
    panel(d,90,740,990,1280); winbar(d,90,740,990,"terminal")
    mono(d,"$ pip install litellm",140,860,42,GREEN)
    mono(d,"Collecting ...",140,930,38,MUTED)
    mono(d,"Installing ...",140,990,38,MUTED)
    # .pth file dropping into site-packages folder
    d.rounded_rectangle((180,1080,900,1220),radius=20,fill=(255,200,0,35),outline=YEL,width=5)
    mono(d,"site-packages/",220,1100,36,MUTED)
    mono(d,"↓  cook.pth",220,1160,44,YEL)
    ctext(d,".pth har Python start pe",1350,F(AB,68))

@ov("04-cook-pth-zoom")
def o4(d,im):
    panel(d,90,740,990,1280); winbar(d,90,740,990,"cook.pth")
    mono(d,"# site-packages/cook.pth",140,860,36,MUTED)
    d.rounded_rectangle((140,960,940,1080),radius=16,fill=(255,200,0,45),outline=YEL,width=6)
    mono(d,"import cook",200,990,64,YEL)
    d.rounded_rectangle((180,1130,900,1230),radius=18,fill=CARD,outline=CYAN,width=4)
    ctext(d,"runs at every Python start",1160,F(PB,40),stroke=3)
    ctext(d,"Import kiya? Zarurat nahi",1360,F(AB,68),fill=YEL)

@ov("05-master-key")
def o5(d,im):
    panel(d,90,720,990,1480)
    # building (simple floors)
    bx,by=180,800
    d.rectangle((bx,by+80,bx+280,by+520),fill=CARD,outline=MUTED,width=5)
    d.polygon([(bx-20,by+80),(bx+140,by), (bx+300,by+80)],fill=ORANGE,outline=OUT)
    for r in range(4):
        for c in range(3):
            x=bx+40+c*75; y=by+130+r*95
            d.rounded_rectangle((x,y,x+50,y+55),radius=6,fill=CYAN if (r,c)!=(3,1) else YEL)
    # master key (big) + burglar copy (small, red)
    key_icon(d,700,980,160,YEL)
    ctext(d,"master key",1120,F(PB,36),stroke=2,cx=700)
    key_icon(d,880,1120,90,RED)
    ctext(d,"burglar",1220,F(PB,32),fill=RED,stroke=2,cx=880)
    ctext(d,"copy",1265,F(PB,32),fill=RED,stroke=2,cx=880)
    # arrow from copy toward building
    arrow(d,(820,1100),(520,1050),col=RED,w=8,head=24)
    ctext(d,"Master key pe",1330,F(AB,72)); ctext(d,"burglar copy",1415,F(AB,72),fill=YEL)

@ov("06-tokens-keys-lock")
def o6(d,im):
    panel(d,90,740,990,1460)
    ctext(d,"Tokens se pipeline hijack",780,F(AB,60),fill=YEL,stroke=4)
    labels=["AWS","GCP","Azure","LLM API"]
    xs=[200,400,600,800]
    for x,lab in zip(xs,labels):
        d.rounded_rectangle((x-70,920,x+70,1080),radius=18,fill=CARD,outline=CYAN,width=4)
        key_icon(d,x,970,70,CYAN)
        f=F(PB,28); b=d.textbbox((0,0),lab,font=f); d.text((x-(b[2]-b[0])/2-b[0],1035-b[1]),lab,font=f,fill=WHITE)
    for a,b_ in zip(xs,xs[1:]): arrow(d,(a+75,1000),(b_-75,1000),col=MUTED,w=5,head=16)
    arrow(d,(W//2,1100),(W//2,1180),col=RED,w=10)
    lock_icon(d,W//2,1320,110,RED)
    ctext(d,"cloud + AI keys",1420,F(PB,44),stroke=3)

@ov("07-fix-checklist")
def o7(d,im):
    panel(d,90,720,990,1480)
    ctext(d,"Fix",760,F(AB,64),fill=MUTED,stroke=3)
    items=[("Pin + hash",GREEN),("CodeArtifact Upstream BLOCK",CYAN),("IAM roles",ORANGE),("Rotate all",YEL)]
    y=860
    for lab,col in items:
        d.rounded_rectangle((140,y,940,y+110),radius=24,fill=CARD,outline=col,width=5)
        check(d,200,y+58,30,col,8)
        f=F(PB,46 if len(lab)<22 else 40); b=d.textbbox((0,0),lab,font=f)
        d.text((260-b[0],y+55-(b[1]+b[3])/2),lab,font=f,fill=WHITE,stroke_width=2,stroke_fill=OUT)
        assert 260+(b[2]-b[0])<=900,(lab,b)
        y+=130
    ctext(d,"Pin + hash, roles, rotate",1420,F(AB,56),fill=YEL,stroke=4)

@ov("08-end-card")
def o8(d,im):
    panel(d,90,900,990,1420,YEL,6)
    ctext(d,"Provenance ≠ trust",1040,F(AB,84),fill=YEL)
    ctext(d,"@shivanshu_builds",1240,F(PB,52),stroke=3)

def cover(path):
    im=make_bg(); d=ImageDraw.Draw(im)
    # key + lock motif (no logos)
    lay,ld=L()
    key_icon(ld,420,480,140,YEL)
    lock_icon(ld,680,500,100,RED)
    im.alpha_composite(lay); d=ImageDraw.Draw(im)
    # Cover title from script: "Signed release mein malware"
    lines=[("SIGNED RELEASE",YEL,92),("MEIN",WHITE,92),("MALWARE",WHITE,110)]
    y=700
    for t,c,s in lines:
        f=F(AB,s)
        while d.textbbox((0,0),t,font=f,stroke_width=10)[2]>920: s-=4; f=F(AB,s)
        bb=ctext(d,t,y,f,fill=c,stroke=10); y=bb[3]+24
    d.rounded_rectangle((W//2-90,y+10,W//2+90,y+34),12,fill=YEL,outline=OUT,width=6)
    ctext(d,"@shivanshu_builds",y+90,F(AB,40),stroke=5)
    bottom=y+140
    assert bottom<=1620 and bottom<=H-300,("cover",bottom)
    im.convert("RGB").save(path,quality=92)
    return bottom

def run(out):
    os.makedirs(out+"/overlays",exist_ok=True)
    for f in glob.glob(out+"/overlays/*.png"): os.remove(f)
    bg=make_bg(); thumbs=[]
    for name,fn in O.items():
        im,d=L(); fn(d,im); bb=im.getchannel("A").getbbox()
        assert bb and bb[3]<=LIMIT and bb[1]>=TOP-40 and bb[0]>=40 and bb[2]<=W-40,(name,bb)
        im.save(f"{out}/overlays/{name}.png")
        c=im.crop((0,bb[1],W,bb[3])); assert c.height<=1270,(name,c.height)
        p=Image.new("RGBA",(W,1350),(0,0,0,0)); p.alpha_composite(c,(0,(1350-c.height)//2)); p.save(f"{out}/overlays/{name}-1080x1350.png")
        prev=bg.copy(); prev.alpha_composite(im); thumbs.append(prev)
        print(name,bb)
    tw_,th_=360,640; sh=Image.new("RGB",(tw_*4+50,th_*2+30),(40,40,40))
    for i,c in enumerate(thumbs): sh.paste(c.convert("RGB").resize((tw_,th_)),(10+(i%4)*(tw_+10),10+(i//4)*(th_+10)))
    sh.save(f"{out}/contact-sheet.png")
    bottom=cover(f"{out}/cover.jpg"); print("cover bottom",bottom)
if __name__=="__main__": run(sys.argv[1] if len(sys.argv)>1 else "out")
