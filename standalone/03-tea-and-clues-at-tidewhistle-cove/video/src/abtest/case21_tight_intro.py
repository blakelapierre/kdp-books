from PIL import Image, ImageDraw, ImageFont
G="/usr/share/fonts/truetype/sand-box/google/"
import glob
def F(pat,s): return ImageFont.truetype(sorted(glob.glob(G+pat))[0], s)
INK=(28,28,28); RED=(178,34,34); PAPER=(250,249,244)
bg=Image.open("bg.png").convert("RGB"); _c=bg.getpixel((20,960)); ImageDraw.Draw(bg).rectangle((0,915,1080,1035),fill=_c); hook=Image.open("hook.png").convert("RGB")
def ctext(d,y,t,f,c,W=1080):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c)
def panel(im, box):
    d=ImageDraw.Draw(im); d.rounded_rectangle(box,radius=30,fill=PAPER,outline=INK,width=6); return d
# A: question over the scene
a=bg.copy(); d=panel(a,(40,120,1040,520))
fq=F("Playfair*/*Black*.ttf",112) if glob.glob(G+"Playfair*/*Black*.ttf") else F("Crimson Text/CrimsonText-Bold.ttf",120)
ctext(d,150,"Who took the",fq,INK); ctext(d,290,"Spanish coins?",fq,INK)
ctext(d,440,"CASE 21",F("IBM Plex Sans Condensed/IBMPlexSansCondensed-Bold.ttf",50),RED); a.save("iA.png")
# B: suspects flash
b=bg.copy(); strip=hook.crop((50,1150,1030,1585)).resize((980,435)); b.paste(strip,(50,90))
d=ImageDraw.Draw(b); d.rounded_rectangle((40,80,1040,535),radius=20,outline=INK,width=6)
fl=F("IBM Plex Sans Condensed/IBMPlexSansCondensed-Bold.ttf",54)
d.rounded_rectangle((140,30,940,100),radius=16,fill=RED); ctext(d,32,"3 SUSPECTS \u00b7 1 THIEF",fl,PAPER); ctext(d,935,"Demelza? Pip? Mr Nankervis?",F("Crimson Text/CrimsonText-Bold.ttf",66),INK); b.save("iB.png")
# C: pause line
c=bg.copy(); d=panel(c,(60,200,1020,440))
ctext(d,225,"PAUSE WHEN YOU",F("IBM Plex Sans Condensed/IBMPlexSansCondensed-Bold.ttf",78),RED)
ctext(d,325,"SPOT THE CLUE",F("IBM Plex Sans Condensed/IBMPlexSansCondensed-Bold.ttf",88),INK); c.save("iC.png")
