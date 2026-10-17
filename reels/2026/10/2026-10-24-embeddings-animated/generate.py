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
S={}
def scene(n):
    def reg(f): S[n]=f; return f
    return reg
@scene(1)
def s1(add):
    f=F(AB,70)
    im,d=L(); card(d,110,480,490,800,CYAN); ctext_in(d,"Sasta",560,f,110,490); ctext_in(d,"phone",660,f,110,490,fill=CYAN); add("01-card-sasta-phone",im)
    im,d=L(); card(d,590,480,970,800,ORANGE); ctext_in(d,"Budget",560,f,590,970); ctext_in(d,"mobile",660,f,590,970,fill=ORANGE); add("02-card-budget-mobile",im)
    im,d=L(); ctext(d,"=",590,F(AB,110),fill=YEL,stroke=6); add("03-equals",im)
    im,d=L(); ctext(d,"Kaise?",950,F(AB,80),stroke=6); add("04-text-kaise",im)
    im,d=L(); ctext(d,"Embeddings",1120,F(AB,120),fill=YEL,stroke=8); add("05-text-embeddings",im)
@scene(2)
def s2(add):
    im,d=L(); rich(d,[("Computer ",WHITE),("= ",YEL),("numbers",YEL)],400,F(AB,76),stroke=6); add("01-text-computer-equals-numbers",im)
    im,d=L(); card(d,110,720,400,900,CYAN); ctext_in(d,"phone",772,F(AB,64),110,400); ctext(d,"word",940,F(PB,48),fill=MUTED,stroke=3,cx=255); add("02-card-word",im)
    im,d=L(); arrow(d,(420,810),(500,810)); add("03-arrow",im)
    im,d=L(); card(d,520,720,970,900,VIOLET); numbers_blurred(im,550,940,810,n=2); d=ImageDraw.Draw(im); ctext(d,"numbers",940,F(PB,48),fill=MUTED,stroke=3,cx=745); add("04-numbers-blurred",im)
    im,d=L(); ctext(d,"words nahi samajhta,",1150,F(AB,64),stroke=5); ctext(d,"numbers samajhta hai",1250,F(AB,64),fill=YEL,stroke=5); add("05-text-numbers-samajhta-hai",im)
@scene(3)
def s3(add):
    im,d=L(); rich(d,[("Text",WHITE),(" → ",YEL),("numbers list",WHITE)],340,F(AB,76),stroke=6); add("01-text-text-to-numbers-list",im)
    im,d=L(); card(d,250,480,830,610,CYAN); ctext_in(d,"\"sasta phone\"",515,F(PB,58),250,830); add("02-card-text",im)
    im,d=L(); arrow(d,(W//2,625),(W//2,700)); add("03-arrow-in",im)
    im,d=L(); card(d,110,715,970,895,YEL,w=8); ctext_in(d,"embedding model",770,F(AB,70),110,970); add("04-box-embedding-model",im)
    im,d=L(); arrow(d,(W//2,910),(W//2,985)); add("05-arrow-out",im)
    im,d=L(); card(d,170,1000,910,1130,VIOLET); numbers_blurred(im,205,875,1065); add("06-numbers-list-blurred",im)
    im,d=L(); ctext(d,"meaning pakadti hai,",1220,F(AB,62),fill=YEL,stroke=5); ctext(d,"sirf spelling nahi",1320,F(AB,62),stroke=5); add("07-text-meaning-not-spelling",im)
@scene(4)
def s4(add):
    im,d=L(); rich(d,[("Similar meaning",WHITE)],330,F(AB,80),stroke=6); ctext(d,"= paas-paas",440,F(AB,80),fill=YEL,stroke=6); add("01-text-similar-meaning-paas-paas",im)
    im,d=L(); mapbox(d,140,580,940,1420); add("02-map",im)
    groups=[("03-dots-group-1",CYAN,[(330,760),(390,720),(370,820),(300,840),(430,790)]),
            ("04-dots-group-2",ORANGE,[(720,800),(780,760),(760,860),(690,880)]),
            ("05-dots-group-3",GREEN,[(520,1190),(590,1160),(560,1250),(480,1260),(620,1230)])]
    for name,col,pts in groups:
        im,d=L()
        for x,y in pts: dot(d,x,y,col,r=20)
        add(name,im)
@scene(5)
def s5(add):
    im,d=L(); mapbox(d,140,340,940,1120); add("01-map",im)
    im,d=L(); dot(d,330,540,CYAN); label(d,"sasta phone",370,540,col=CYAN); add("02-dot-sasta-phone",im)
    im,d=L(); dot(d,370,640,ORANGE); label(d,"budget mobile",410,640,col=ORANGE); add("03-dot-budget-mobile",im)
    im,d=L(); d.ellipse((260,470,800,710),outline=YEL,width=6); add("04-ring-paas-paas",im)
    im,d=L(); dot(d,800,960,RED); label(d,"mehenga laptop",770,1030,col=RED,anchor="r"); add("05-dot-mehenga-laptop",im)
    im,d=L(); rich(d,[("Sasta phone ",WHITE),("≈ ",YEL),("budget mobile",WHITE)],1200,F(AB,56),stroke=5); add("06-text-sasta-approx-budget",im)
    im,d=L(); rich(d,[("Mehenga laptop ",WHITE),("= ",YEL),("door",RED)],1320,F(AB,56),stroke=5); add("07-text-mehenga-laptop-door",im)
@scene(6)
def s6(add):
    im,d=L(); ctext(d,"Search aur RAG",330,F(AB,84),fill=YEL,stroke=6); add("01-text-search-aur-rag",im)
    im,d=L(); box(d,470,150,CYAN,"Tumhara sawaal",i_user,size=56); add("02-card-sawaal",im)
    im,d=L(); mapbox(d,140,760,940,1200)
    d.ellipse((200,860,700,1110),outline=YEL,width=6); dot(d,300,940,CYAN); label(d,"sasta phone",340,940,col=CYAN,size=40); dot(d,330,1030,ORANGE); label(d,"budget mobile",370,1030,col=ORANGE,size=40)
    dot(d,850,1120,RED,r=18); add("03-map-close-cluster",im)
    im,d=L(); arrow(d,(450,625),(450,850),col=GREEN,w=10); check(d,520,725,50); label(d,"meaning match",565,735,col=GREEN,size=44); add("04-arrow-meaning-match",im)
    im,d=L(); bb=label(d,"words match",W//2,1270,col=MUTED,size=48,anchor="c"); d.line((bb[0]-10,1272,bb[2]+10,1272),fill=RED,width=8); add("05-words-match-crossed",im)
    im,d=L(); rich(d,[("Meaning match, ",YEL),("not words",WHITE)],1360,F(AB,60),stroke=5); add("06-text-meaning-match-not-words",im)
@scene(7)
def s7(add):
    im,d=L(); d.rounded_rectangle((110,560,970,960),radius=44,fill=CARD,outline=YEL,width=8); ctext(d,"Amazon Bedrock:",640,F(AB,82)); add("01-card-amazon-bedrock",im)
    im,d=L(); ctext(d,"embedding models",780,F(AB,72),fill=YEL); add("02-text-embedding-models",im)
@scene(8)
def s8(add):
    im,d=L(); d.rounded_rectangle((110,380,970,720),radius=44,fill=CARD,outline=VIOLET,width=6)
    ctext(d,"Agle reel mein dekhenge",420,F(AB,54),fill=YEL); ctext(d,"yeh numbers store",520,F(AB,62)); ctext(d,"kahan hote hain",615,F(AB,62)); add("01-card-next",im)
    im,d=L(); ctext(d,"|",760,F(AB,90),fill=MUTED,stroke=0); add("02-divider",im)
    im,d=L(); d.rounded_rectangle((110,900,970,1120),radius=44,fill=CARD,outline=YEL,width=6); rich(d,[("Follow",WHITE),(" + ",YEL),("Comment",WHITE)],975,F(AB,76)); add("03-card-follow-comment",im)
    im,d=L(); ctext(d,"Same matlab, alag words?",1190,F(AB,60),fill=YEL,stroke=5); add("04-text-comment-prompt",im)
    im,d=L(); ctext(d,"@shivanshu_builds",1320,F(PB,64),stroke=4); add("05-handle",im)
def cover(path):
    # same look as the RAG reel cover: bg + panel, icon, Archivo Black title, accent bar, handle
    im=make_bg(); d=ImageDraw.Draw(im)
    lay,ld=L()
    for x,y,c in [(470,430,CYAN),(520,400,ORANGE),(510,470,VIOLET),(680,450,RED)]: dot(ld,x,y,c,r=26)
    ld.ellipse((415,350,585,520),outline=YEL,width=6)
    im.alpha_composite(lay); d=ImageDraw.Draw(im)
    lines=[("EMBEDDINGS",YEL,150),("KYA HOTE",WHITE,140),("HAIN?",WHITE,140)]
    y=620
    for t,c,s in lines:
        f=F(AB,s)
        while d.textbbox((0,0),t,font=f,stroke_width=10)[2]>900: s-=4; f=F(AB,s)
        bb=ctext(d,t,y,f,fill=c,stroke=10); y=bb[3]+28
    d.rounded_rectangle((W//2-90,y+10,W//2+90,y+34),12,fill=YEL,outline=OUT,width=6)
    ctext(d,"@shivanshu_builds",y+90,F(AB,40),stroke=5)
    im.convert("RGB").save(path,quality=92)
    return y+140
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
    bottom=cover(f"{OUTDIR}/cover.jpg"); assert bottom<=1680-0 and bottom<=H-300,("cover",bottom)
    for n,v in rows.items(): print(n,v)
    print("cover text bottom",bottom)
if __name__=="__main__": run()
