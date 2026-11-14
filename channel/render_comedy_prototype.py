#!/usr/bin/env python3
"""Render the original 'One More Rep Lie' episode as a real pose-animated MP4.

This is a deterministic procedural 2D prototype, not a claim of hand-painted
frame-by-frame animation. It renders every frame and encodes with ffmpeg.
"""
import argparse, json, math, shutil, subprocess, tempfile, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=720,1280,24
BG=(105,111,99); INK=(35,38,34); CREAM=(229,222,203); BLUE=(83,101,112); RED=(174,82,68)

def font(size,bold=False):
    candidates=("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf")
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def ease(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)
def mix(a,b,t): return a+(b-a)*t
def segment(d,a,b,width=15,fill=INK):
    d.line((a,b),fill=fill,width=width)
    r=width//2
    for p in (a,b): d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=fill)

def character(im,cx,ground,kind,phase=0,face="neutral",scale=1,lean=0,arm=0):
    d=ImageDraw.Draw(im)
    # soft ground shadow
    d.ellipse((cx-78*scale,ground-13,cx+78*scale,ground+7),fill=(69,73,65))
    # torso and pelvis: deliberately graphic, hand-inked silhouette
    head=(cx+lean,ground-440*scale)
    hr=38*scale
    d.ellipse((head[0]-hr,head[1]-hr,head[0]+hr,head[1]+hr),fill=CREAM,outline=INK,width=max(3,int(7*scale)))
    # face, eyebrows and mouth
    ex=head[0]; ey=head[1]
    d.ellipse((ex-16*scale,ey-5*scale,ex-8*scale,ey+4*scale),fill=INK)
    d.ellipse((ex+8*scale,ey-5*scale,ex+16*scale,ey+4*scale),fill=INK)
    if face=="panic":
        d.arc((ex-17*scale,ey+7*scale,ex+18*scale,ey+31*scale),180,360,fill=INK,width=4)
        d.ellipse((ex-5*scale,ey+13*scale,ex+5*scale,ey+26*scale),fill=INK)
    elif face=="smug":
        d.arc((ex-18*scale,ey+2*scale,ex+20*scale,ey+26*scale),5,160,fill=INK,width=4)
    else: segment(d,(ex-14*scale,ey+17*scale),(ex+14*scale,ey+17*scale),3)
    if kind=="bro":
        # neck, exaggerated chest, narrow waist, large biceps
        segment(d,(cx,ground-394*scale),(cx,ground-365*scale),18*scale)
        d.ellipse((cx-78*scale,ground-382*scale,cx+78*scale,ground-245*scale),fill=CREAM,outline=INK,width=7)
        d.polygon([(cx-53*scale,ground-265*scale),(cx+53*scale,ground-265*scale),(cx+37*scale,ground-175*scale),(cx-37*scale,ground-175*scale)],fill=CREAM)
        d.line((cx-42*scale,ground-325*scale,cx+42*scale,ground-325*scale),fill=INK,width=4)
        shoulder=ground-354*scale; hip=ground-175*scale
        armw=27*scale
    else:
        segment(d,(cx,ground-395*scale),(cx,ground-190*scale),19*scale)
        shoulder=ground-360*scale; hip=ground-190*scale; armw=13*scale
    # legs: squat/buckling animation for bro
    squat=(ease((phase-4.5)/1.3) if kind=="bro" else 0)
    knee_y=ground-95*scale+45*squat
    hip_y=mix(hip,ground-140*scale,squat)
    for side in (-1,1):
        hx=cx+side*20*scale; kx=cx+side*(42 if side<0 else 35)*scale
        ax=cx+side*47*scale
        segment(d,(hx,hip_y),(kx,knee_y),17*scale)
        segment(d,(kx,knee_y),(ax,ground-10),15*scale)
        d.ellipse((ax-29*scale,ground-17,ax+20*scale,ground+1),fill=BLUE,outline=INK,width=4)
    # arms: both raised in a strain pose; spotter gestures then helps
    for side in (-1,1):
        sx=cx+side*63*scale; sy=shoulder
        if kind=="bro":
            lift=math.sin(phase*2.8)*10
            elbow=(cx+side*(105+arm*18)*scale,sy+45*scale+lift)
            wrist=(cx+side*(118+arm*30)*scale,sy+105*scale+lift)
            if phase>5.8:
                u=ease((phase-5.8)/1.2); elbow=(mix(elbow[0],cx+side*90*scale,u),mix(elbow[1],sy-20*scale,u)); wrist=(mix(wrist[0],cx+side*115*scale,u),mix(wrist[1],sy-70*scale,u))
        else:
            elbow=(cx+side*55*scale,sy+65*scale)
            wrist=(cx+side*(70+arm*55)*scale,sy+110*scale)
        segment(d,(sx,sy),elbow,armw)
        segment(d,elbow,wrist,armw)
        d.ellipse((wrist[0]-10*scale,wrist[1]-10*scale,wrist[0]+10*scale,wrist[1]+10*scale),fill=CREAM,outline=INK,width=4)

def frame(t):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    # gym wall panels, floor and equipment establish a consistent scene
    d.rectangle((0,0,W,870),fill=(119,124,110))
    for x in range(-80,W+100,180):
        d.line((x,0,x,870),fill=(105,111,99),width=3)
    d.rectangle((0,870,W,H),fill=(74,80,72))
    d.line((0,870,W,870),fill=(38,42,37),width=8)
    # rack uprights and plates
    d.rectangle((75,350,95,880),fill=BLUE,outline=INK,width=6)
    d.rectangle((625,350,645,880),fill=BLUE,outline=INK,width=6)
    d.line((75,430,645,430),fill=INK,width=12)
    # bench
    d.rounded_rectangle((235,760,500,820),radius=16,fill=BLUE,outline=INK,width=7)
    d.line((270,815,250,900),fill=INK,width=14); d.line((460,815,485,900),fill=INK,width=14)
    # barbell high, then lower as he fails
    drop=ease((t-5.0)/1.0)*95
    by=425+drop
    d.line((120,by,600,by),fill=INK,width=16)
    for x in (155,565):
        d.rounded_rectangle((x-22,by-75,x+22,by+75),radius=12,fill=(54,60,62),outline=INK,width=7)
        d.line((x-12,by-62,x+12,by+62),fill=(105,119,124),width=5)
    # character staging
    if t<2.8:
        face="smug"; lean=0; strain=0
    elif t<5.8:
        face="panic" if t>4.2 else "neutral"; lean=0; strain=1
    else:
        face="panic"; lean=8*math.sin(t*3); strain=1
    character(im,300,1090,"bro",t,face,1.12,lean,strain)
    character(im,540,1090,"spotter",t,"neutral",.82,0,1 if t>6.2 else 0)
    # caption strips with contrast and safe margins
    captions=[
      (0,2.0,"ONE MORE REP. EASY."),
      (2.0,4.0,"BRO: I GOT THIS."),
      (4.0,6.1,"THE BAR HAD OTHER PLANS."),
      (6.1,8.2,"SPOTTER: YOU GOOD?"),
      (8.2,10.7,"BRO: NEVER BETTER."),
      (10.7,13.2,"HE ESCAPES THE BENCH..."),
      (13.2,16.0,"...THEN ASKS FOR MORE WEIGHT."),
      (16.0,18.5,"SPOTTER HAS SEEN ENOUGH.")
    ]
    caption=next((s for a,b,s in captions if a<=t<b),"")
    d.rounded_rectangle((34,95,686,190),radius=20,fill=(29,32,29),outline=(211,202,180),width=3)
    f=font(30,True); box=d.textbbox((0,0),caption,font=f); tw=box[2]-box[0]
    d.text(((W-tw)//2,123),caption,font=f,fill=(248,241,222),stroke_width=1,stroke_fill=(20,22,20))
    # small visual impact marks during failure
    if 4.1<t<6.4:
        for k in range(3):
            x=245+k*48
            d.line((x,365,x-15,330),fill=(239,220,177),width=6)
    return im

def make_audio(path,duration):
    # Original synthesized comic percussion bed; no third-party music.
    rate=24000; n=int(rate*duration)
    events=[(0.0,180,.12),(2.1,130,.09),(4.35,85,.24),(5.15,65,.28),(8.1,220,.08),(13.2,160,.11),(16.1,95,.25)]
    with wave.open(str(path),"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        import struct
        buf=bytearray()
        for i in range(n):
            t=i/rate; v=0.0
            for start,freq,amp in events:
                dt=t-start
                if 0<=dt<.22:
                    env=math.exp(-dt*18)
                    v+=amp*env*(math.sin(2*math.pi*freq*dt)+.35*math.sin(2*math.pi*freq*2.03*dt))
            buf.extend(struct.pack("<h",int(max(-1,min(1,v))*25000)))
        w.writeframes(buf)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="out/stickman-comedy-prototype.mp4"); ap.add_argument("--episode",default="channel/sample-episode.json")
    args=ap.parse_args(); data=json.loads(Path(args.episode).read_text())
    duration=max(float(s["end"]) for s in data["shots"])
    if duration<8 or duration>35: raise SystemExit("Episode duration outside 8-35 second render contract")
    if shutil.which("ffmpeg") is None: raise SystemExit("ffmpeg is required")
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for i in range(math.ceil(duration*FPS)):
            frame(i/FPS).save(tmp/f"{i:05d}.png")
        audio=tmp/"original-sfx.wav"; make_audio(audio,duration)
        cmd=["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(tmp/"%05d.png"),"-i",str(audio),"-t",str(duration),"-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-preset","medium","-c:a","aac","-b:a","128k","-movflags","+faststart",str(out)]
        subprocess.run(cmd,check=True)
    print(json.dumps({"output":str(out),"duration_seconds":duration,"fps":FPS,"resolution":f"{W}x{H}","frames":math.ceil(duration*FPS),"audio":"original synthesized SFX only","review_status":"REVIEW_REQUIRED"}))
if __name__=="__main__": main()
