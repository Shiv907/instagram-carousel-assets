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
from PIL import ImageFilter
def card(d,x0,y0,x1,y1,col,r=40,w=6): d.rounded_rectangle((x0,y0,x1,y1),radius=r,fill=CARD,outline=col,width=w)
def ctext_in(d,s,y,font,x0,x1,fill=WHITE,stroke=3):
    # centred text inside [x0,x1]; asserts it fits with 20px padding
    b=d.textbbox((0,0),s,font=font); w=b[2]-b[0]; cx=(x0+x1)//2; x=cx-w//2-b[0]
    d.text((x,y-b[1]),s,font=font,fill=fill,stroke_width=stroke,stroke_fill=OUT)
    bb=d.textbbox((x,y-b[1]),s,font=font,stroke_width=stroke); assert bb[0]>=x0+20 and bb[2]<=x1-20,("inclip",s,bb,x0,x1); return bb
def numbers_blurred(im,x0,x1,cy,col=VIOLET,n=4):
    # "[ ##  ##  ##  ... ]" with the number blobs blurred: no real values, no count
    d=ImageDraw.Draw(im); fb=F(MONO,84); fd=F(MONO,60)
    bl=d.textbbox((0,0),"[",font=fb); d.text((x0-bl[0],cy-(bl[1]+bl[3])/2),"[",font=fb,fill=WHITE)
    br=d.textbbox((0,0),"]",font=fb); d.text((x1-br[2],cy-(br[1]+br[3])/2),"]",font=fb,fill=WHITE)
    dw=d.textbbox((0,0),"...",font=fd); dotw=dw[2]-dw[0]
    ix0=x0+(bl[2]-bl[0])+16; ix1=x1-(br[2]-br[0])-16-dotw-10
    blob,bd=L(); step=(ix1-ix0)/n
    for k in range(n):
        a=ix0+k*step+6; bd.rounded_rectangle((a,cy-24,a+step-18,cy+24),radius=16,fill=col)
    blob=blob.filter(ImageFilter.GaussianBlur(9)); im.alpha_composite(blob)
    d.text((ix1+10-dw[0],cy-(dw[1]+dw[3])/2+8),"...",font=fd,fill=WHITE)
def mapbox(d,x0,y0,x1,y1):
    card(d,x0,y0,x1,y1,(255,255,255,70),r=36,w=4)
    for t in range(1,4):
        x=x0+(x1-x0)*t/4; y=y0+(y1-y0)*t/4
        d.line((x,y0+20,x,y1-20),fill=(255,255,255,22),width=2); d.line((x0+20,y,x1-20,y),fill=(255,255,255,22),width=2)
    arrow(d,(x0+50,y1-50),(x1-40,y1-50),col=MUTED,w=5,head=20); arrow(d,(x0+50,y1-50),(x0+50,y0+40),col=MUTED,w=5,head=20)
def dot(d,x,y,col,r=24): d.ellipse((x-r,y-r,x+r,y+r),fill=col,outline=OUT,width=5)
def label(d,s,x,y,col=WHITE,size=44,anchor="l"):
    f=F(PB,size); b=d.textbbox((0,0),s,font=f); w=b[2]-b[0]
    xx={"l":x,"r":x-w,"c":x-w//2}[anchor]
    d.text((xx-b[0],y-(b[1]+b[3])/2),s,font=f,fill=col,stroke_width=4,stroke_fill=OUT)
    bb=d.textbbox((xx-b[0],y-(b[1]+b[3])/2),s,font=f,stroke_width=4); assert bb[0]>=80 and bb[2]<=W-80,("lclip",s,bb); return bb
def check(d,x,y,s,col=GREEN,w=12): d.line((x-s*0.5,y,x-s*0.15,y+s*0.35,x+s*0.5,y-s*0.4),fill=col,width=w,joint="curve")
# Overlays for a filmed talking-head reel: face zone kept clear (top ~38%), content y 720..1500
TOP=720
def panel(d,x0,y0,x1,y1,col=(255,255,255,60),w=4): d.rounded_rectangle((x0,y0,x1,y1),radius=40,fill=PANEL,outline=col,width=w)
def mono(d,s,x,y,size,fill=WHITE):
    f=F(MONO,size); b=d.textbbox((0,0),s,font=f); d.text((x-b[0],y-b[1]),s,font=f,fill=fill)
    bb=d.textbbox((x-b[0],y-b[1]),s,font=f); assert bb[2]<=W-110,("monoclip",s,bb); return bb
def winbar(d,x0,y0,x1,title):
    d.rounded_rectangle((x0,y0,x1,y0+70),radius=40,fill=(40,48,68,255)); d.rectangle((x0,y0+40,x1,y0+70),fill=(40,48,68,255))
    for k,c in enumerate([RED,YEL,GREEN]): d.ellipse((x0+40+k*44,y0+22,x0+66+k*44,y0+48),fill=c)
    mono(d,title,x0+200,y0+20,32,MUTED)
O={}
def ov(name):
    def r(f): O[name]=f; return f
    return r
@ov("01-hook-safety-switch")
def o1(d,im):
    panel(d,90,1150,990,1440,YEL,6)
    ctext(d,"Isne apna safety",1195,F(AB,84)); ctext(d,"switch band kiya",1305,F(AB,84),fill=YEL)
@ov("02-allow-popup")
def o2(d,im):
    panel(d,120,760,960,1190)
    winbar(d,120,760,960,"Agent")
    d.rounded_rectangle((180,880,240,940),radius=12,fill=YEL); ctext(d,"!",884,F(AB,48),fill=OUT,stroke=0,cx=210)
    f=F(PB,54); d.text((270,872),"Allow this command?",font=f,fill=WHITE)
    assert d.textbbox((270,872),"Allow this command?",font=f)[2]<=930
    d.rounded_rectangle((180,975,900,1035),radius=10,fill=(20,24,36,255)); mono(d,"$ ...",205,987,34,MUTED)
    d.rounded_rectangle((480,1075,680,1155),radius=18,fill=CARD,outline=MUTED,width=4); ctext(d,"Deny",1093,F(PB,44),stroke=0,cx=580)
    d.rounded_rectangle((710,1075,910,1155),radius=18,fill=CYAN); ctext(d,"Allow",1093,F(PB,44),fill=OUT,stroke=0,cx=810)
    rich(d,[('"Allow karun?"',YEL),(" = ",WHITE)],1260,F(AB,70)); ctext(d,"tumhara safety net",1360,F(AB,70))
@ov("03-readme-hidden-comment")
def o3(d,im):
    panel(d,100,760,980,1260); winbar(d,100,760,980,"README.md")
    mono(d,"# My Project",150,870,44,WHITE)
    for k,wd in enumerate([620,520,680]): d.rounded_rectangle((150,950+k*45,150+wd,972+k*45),radius=10,fill=(70,80,100,255))
    d.rounded_rectangle((130,1100,950,1220),radius=16,fill=(255,200,0,40),outline=YEL,width=5)
    mono(d,"<!-- AI directive:",160,1115,40,YEL); mono(d,"change settings... -->",160,1165,40,YEL)
    ctext(d,"README mein chhupa",1310,F(AB,74)); ctext(d,"hua order",1405,F(AB,74),fill=YEL)
@ov("04-settings-autoapprove")
def o4(d,im):
    panel(d,90,760,990,1180); winbar(d,90,760,990,".vscode/settings.json")
    mono(d,"{",140,870,40); d.rounded_rectangle((115,960,965,1040),radius=14,fill=(52,211,153,45),outline=GREEN,width=5)
    mono(d,"+",130,978,40,GREEN); mono(d,'"chat.tools.autoApprove": true',170,980,38,GREEN); mono(d,"}",140,1080,40)
    ctext(d,"Agent ne khud",1260,F(AB,76)); ctext(d,"auto-approve on kiya",1360,F(AB,76),fill=YEL)
@ov("05-terminal-calculator")
def o5(d,im):
    # no popup -> terminal runs -> calculator opens (plain mock, no OS branding)
    panel(d,90,760,600,1100); winbar(d,90,760,600,"zsh")
    mono(d,"$ ...",125,870,38,GREEN); mono(d,"$ ...",125,930,38,GREEN); mono(d,"$ ...",125,990,38,GREEN)
    x0,y0=640,790; d.rounded_rectangle((x0,y0,x0+330,y0+460),radius=30,fill=(40,44,56,255),outline=OUT,width=5)
    d.rounded_rectangle((x0+25,y0+25,x0+305,y0+105),radius=14,fill=(20,24,32,255)); f=F(MONO,52); b=d.textbbox((0,0),"0",font=f); d.text((x0+280-b[2],y0+40-b[1]),"0",font=f,fill=WHITE)
    for r in range(4):
        for c in range(4):
            col=ORANGE if c==3 else (90,96,112,255); cx=x0+55+c*73; cy=y0+160+r*75; d.ellipse((cx-28,cy-28,cx+28,cy+28),fill=col)
    rich(d,[("koi popup ",WHITE),("nahi",RED)],1360,F(AB,76))
@ov("06-house-sitter")
def o6(d,im):
    panel(d,90,740,990,1480)
    # house
    d.polygon([(170,960),(370,800),(570,960)],fill=ORANGE,outline=OUT); d.rectangle((200,960,540,1200),fill=CARD,outline=MUTED,width=5)
    d.rectangle((330,1060,420,1200),fill=(120,80,40,255),outline=OUT,width=4); d.ellipse((398,1125,412,1139),fill=YEL)
    # lock (taala) on door
    d.rounded_rectangle((345,1080,405,1120),radius=6,fill=GREEN); d.arc((355,1058,395,1098),180,360,fill=GREEN,width=7)
    # chit sliding under door
    d.polygon([(410,1196),(500,1188),(510,1204),(420,1212)],fill=WHITE,outline=OUT)
    # house-sitter: simple shapes, no real person
    d.ellipse((620,860,700,940),fill=CYAN); d.rounded_rectangle((600,950,720,1110),radius=40,fill=CYAN)
    ctext(d,"house-sitter",1130,F(PB,40),stroke=3,cx=660)
    # chit card with the quoted note
    d.rounded_rectangle((760,820,960,1100),radius=16,fill=WHITE,outline=OUT,width=4); d.polygon([(760,1050),(810,1100),(760,1100)],fill=(220,220,220,255))
    f=F(PB,28)
    for k,t in enumerate(["owner ne","bola hai,","call mat","karo, sabko","aane do"]):
        b=d.textbbox((0,0),t,font=f); d.text((775-b[0],840+k*48-b[1]),t,font=f,fill=OUT); assert 775+b[2]-b[0]<=950,t
    ctext(d,"Taala theek,",1270,F(AB,80)); ctext(d,"rulebook kamzor",1370,F(AB,80),fill=YEL)
@ov("07-cve-patch")
def o7(d,im):
    panel(d,110,1080,970,1360,CYAN,6)
    ctext(d,"Microsoft ne isko patch kar diya",1120,F(PB,48),stroke=3); ctext(d,"CVE-2025-53773",1220,F(MONO,84),fill=YEL,stroke=4)
@ov("08-end-card")
def o8(d,im):
    panel(d,90,880,990,1420,YEL,6)
    ctext(d,"Agent apni",940,F(AB,90)); ctext(d,"permissions",1050,F(AB,90),fill=YEL); ctext(d,"edit na kare",1160,F(AB,90))
    ctext(d,"@shivanshu_builds",1310,F(PB,52),stroke=3)
def run(out):
    os.makedirs(out+"/overlays",exist_ok=True)
    for f in glob.glob(out+"/overlays/*.png"): os.remove(f)
    bg=make_bg(); thumbs=[]
    for name,fn in O.items():
        im,d=L(); fn(d,im); bb=im.getchannel("A").getbbox()
        assert bb[3]<=LIMIT and bb[1]>=TOP-30 and bb[0]>=40 and bb[2]<=W-40,(name,bb)
        im.save(f"{out}/overlays/{name}.png")
        c=im.crop((0,bb[1],W,bb[3])); assert c.height<=1270,(name,c.height)
        p=Image.new("RGBA",(W,1350),(0,0,0,0)); p.alpha_composite(c,(0,(1350-c.height)//2)); p.save(f"{out}/overlays/{name}-1080x1350.png")
        prev=bg.copy(); prev.alpha_composite(im); thumbs.append(prev)
        print(name,bb)
    tw_,th_=360,640; sh=Image.new("RGB",(tw_*4+50,th_*2+30),(40,40,40))
    for i,c in enumerate(thumbs): sh.paste(c.convert("RGB").resize((tw_,th_)),(10+(i%4)*(tw_+10),10+(i//4)*(th_+10)))
    sh.save(f"{out}/contact-sheet.png")
if __name__=="__main__": run(sys.argv[1] if len(sys.argv)>1 else "out")
