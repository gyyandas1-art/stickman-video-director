#!/usr/bin/env python3
"""Render a narrated, captioned portrait psychology Short from a Gemini draft."""
import argparse, json, math, os, random, subprocess, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 480, 854, 30
BG = (251, 250, 246)
INK = (35, 37, 39)
RED = (214, 74, 65)
GREY = (190, 190, 184)

SOURCES = [
    {"title":"Gilovich, Medvec & Savitsky (2000), The Spotlight Effect in Social Judgment",
     "url":"https://pubmed.ncbi.nlm.nih.gov/10707330/",
     "claim_supported":"Original experiments found that people overestimated how many observers would notice or remember their shirt and discussion comments."},
    {"title":"Gilovich & Savitsky (1999), The Spotlight Effect and the Illusion of Transparency",
     "url":"https://www.psychologicalscience.org/journals/current-directions/1467-8721.00039/",
     "claim_supported":"Review describing the tendency to overestimate how much others notice our behaviour and appearance."}
]
HEADINGS = ["THE SPOTLIGHT EFFECT", "YOUR MIND ZOOMS IN", "THE ROOM ISN'T A CAMERA", "A REAL EXPERIMENT", "ZOOM OUT", "LESS SELF-CONSCIOUS"]
def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def load_font(path, size):
    try: return ImageFont.truetype(str(path), size)
    except Exception: return ImageFont.load_default()

def rough_line(draw, pts, width=4, fill=INK, seed=0):
    rng = random.Random(seed)
    for off in (0, 1):
        shifted=[(x+rng.uniform(-1.2,1.2), y+rng.uniform(-1.2,1.2)) for x,y in pts]
        draw.line(shifted, fill=fill, width=max(1,width-off), joint="curve")

def stick_figure(draw, cx, cy, scale=1.0, pose=0, shirt=False, blush=False, seed=0):
    s=scale
    # head and face
    r=29*s
    draw.ellipse((cx-r,cy-r,cx+r,cy+r), outline=INK, width=max(2,int(4*s)))
    draw.ellipse((cx-10*s,cy-5*s,cx-5*s,cy), fill=INK)
    draw.ellipse((cx+5*s,cy-5*s,cx+10*s,cy), fill=INK)
    draw.arc((cx-10*s,cy+1*s,cx+11*s,cy+19*s), 5, 165, fill=INK, width=max(2,int(3*s)))
    # neck/body
    rough_line(draw,[(cx,cy+r),(cx,cy+112*s)],max(2,int(4*s)),seed=seed)
    if shirt:
        draw.rounded_rectangle((cx-25*s,cy+45*s,cx+25*s,cy+100*s),radius=5*s,outline=RED,width=max(2,int(4*s)))
        draw.line((cx-14*s,cy+63*s,cx+12*s,cy+76*s),fill=RED,width=max(2,int(4*s)))
    # arms, three readable poses
    if pose == 0:
        arms=[(cx,cy+58*s,cx-48*s,cy+100*s,cx-65*s,cy+78*s),(cx,cy+58*s,cx+48*s,cy+100*s,cx+63*s,cy+78*s)]
    elif pose == 1:
        arms=[(cx,cy+58*s,cx-65*s,cy+28*s,cx-78*s,cy+5*s),(cx,cy+58*s,cx+55*s,cy+105*s,cx+73*s,cy+92*s)]
    elif pose == 2:
        arms=[(cx,cy+58*s,cx-65*s,cy+20*s,cx-72*s,cy-8*s),(cx,cy+58*s,cx+65*s,cy+20*s,cx+72*s,cy-8*s)]
    else:
        arms=[(cx,cy+58*s,cx-48*s,cy+100*s,cx-60*s,cy+100*s),(cx,cy+58*s,cx+48*s,cy+100*s,cx+60*s,cy+100*s)]
    for j,a in enumerate(arms): rough_line(draw,[(a[0],a[1]),(a[2],a[3]),(a[4],a[5])],max(2,int(4*s)),seed=seed+j)
    # legs
    rough_line(draw,[(cx,cy+112*s),(cx-42*s,cy+185*s),(cx-63*s,cy+185*s)],max(2,int(4*s)),seed=seed+4)
    rough_line(draw,[(cx,cy+112*s),(cx+42*s,cy+185*s),(cx+63*s,cy+185*s)],max(2,int(4*s)),seed=seed+5)
    if blush:
        draw.ellipse((cx-24*s,cy+5*s,cx-13*s,cy+12*s),fill=(238,160,148))
        draw.ellipse((cx+13*s,cy+5*s,cx+24*s,cy+12*s),fill=(238,160,148))

def draw_scene(t, scene_idx, local, caption, title_font, cap_font):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    # subtle hand-drawn grid
    for x in range(0,W,28): d.line((x,0,x,H),fill=(242,241,236),width=1)
    for y in range(0,H,28): d.line((0,y,W,y),fill=(242,241,236),width=1)
    # heading
    heading=HEADINGS[scene_idx]
    box=d.textbbox((0,0),heading,font=title_font)
    d.text(((W-(box[2]-box[0]))/2,58),heading,font=title_font,fill=INK)
    d.line((70,112,410,112),fill=(213,211,203),width=2)
    pulse=0.5+0.5*math.sin(local*math.pi*2)
    if scene_idx==0:
        stick_figure(d,240,300,1.0,pose=0,shirt=True,blush=True,seed=1)
        # spotlight
        d.polygon([(240,245),(130,700),(350,700)],fill=(250,222,216))
        stick_figure(d,240,300,1.0,pose=0,shirt=True,blush=True,seed=1)
        d.ellipse((100,250,380,560),outline=RED,width=3)
    elif scene_idx==1:
        stick_figure(d,240,295,1.0,pose=1,shirt=True,blush=True,seed=2)
        # magnifying lens on self
        x=330+int(8*pulse); y=390
        d.ellipse((x-48,y-48,x+48,y+48),outline=RED,width=5)
        d.line((x+34,y+34,x+75,y+75),fill=RED,width=7)
        d.text((75,670),"YOUR EXPERIENCE FEELS HUGE",font=cap_font,fill=RED)
    elif scene_idx==2:
        stick_figure(d,240,315,0.72,pose=3,shirt=True,seed=3)
        # three distracted observers
        for x in [75,390]:
            stick_figure(d,x,380,0.42,pose=0,seed=x)
            d.rounded_rectangle((x-25,560,x+25,625),radius=6,outline=(100,130,145),width=3)
            d.line((x-12,575,x+12,600),fill=(100,130,145),width=3)
        d.text((90,680),"EVERYONE HAS THEIR OWN FOCUS",font=cap_font,fill=INK)
    elif scene_idx==3:
        # shirt experiment card
        d.rounded_rectangle((55,205,425,635),radius=22,outline=INK,width=4,fill=(255,254,250))
        d.text((105,235),"THE T-SHIRT STUDY",font=cap_font,fill=RED)
        stick_figure(d,170,335,0.62,pose=0,shirt=True,seed=4)
        for x in [300,350,395]:
            d.ellipse((x-13,370,x+13,396),outline=INK,width=3)
            d.line((x,396,x,455),fill=INK,width=3)
            d.line((x,415,x-15,435),fill=INK,width=3)
            d.line((x,415,x+15,435),fill=INK,width=3)
        d.text((105,575),"ESTIMATED ATTENTION",font=cap_font,fill=INK)
        d.line((105,615,375,615),fill=RED,width=5)
    elif scene_idx==4:
        # crowd looks inward at own lives
        for x,y in [(90,290),(240,270),(390,290),(145,500),(335,500)]:
            stick_figure(d,x,y,0.45,pose=3,seed=x+y)
            d.ellipse((x-30,y-85,x+30,y-25),outline=(190,190,184),width=2)
        stick_figure(d,240,385,0.62,pose=0,shirt=True,seed=9)
        d.text((145,680),"ATTENTION IS DIVIDED",font=cap_font,fill=RED)
    else:
        stick_figure(d,240,310,0.82,pose=2,shirt=False,seed=10)
        d.rounded_rectangle((70,590,410,690),radius=18,outline=RED,width=3,fill=(255,252,248))
        d.text((112,620),"YOU ARE NOT THE WHOLE ROOM",font=cap_font,fill=INK)
    # tiny motion indicator / hand-drawn accent
    d.arc((60,145,420,500),190,250,fill=(210,206,196),width=2)
    # captions: a single centered semantic line
    if caption:
        txt=caption.strip()
        while d.textbbox((0,0),txt,font=cap_font)[2] > 420 and len(txt)>4:
            txt=" ".join(txt.split(" ")[:-1])
        b=d.textbbox((0,0),txt,font=cap_font)
        tw=b[2]-b[0]; th=b[3]-b[1]
        y=778
        d.rounded_rectangle((max(18,(W-tw)//2-14),y-8,min(W-18,(W+tw)//2+14),y+th+12),radius=10,fill=(255,254,250),outline=(221,218,210),width=1)
        d.text(((W-tw)/2,y),txt,font=cap_font,fill=INK)
    return im

def group_words(words):
    groups=[]; current=[]
    for w in words:
        token=w["word"].strip()
        if not token: continue
        if current and (w["start"]-current[-1]["end"]>0.42 or len(current)>=6 or sum(len(x["word"]) for x in current)+len(token)>34):
            groups.append({"start":current[0]["start"],"end":current[-1]["end"],"text":" ".join(x["word"].strip() for x in current)})
            current=[]
        current.append(w)
        if token.endswith((".", "?", "!", ",")) and len(current)>=3:
            groups.append({"start":current[0]["start"],"end":current[-1]["end"],"text":" ".join(x["word"].strip() for x in current)})
            current=[]
    if current: groups.append({"start":current[0]["start"],"end":current[-1]["end"],"text":" ".join(x["word"].strip() for x in current)})
    return groups

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("episode_dir",type=Path)
    args=ap.parse_args()
    root=args.episode_dir.resolve()
    draft_path=root/"episode-draft.json"; audio=root/"narration.wav"
    if not draft_path.is_file() or not audio.is_file(): raise SystemExit("episode-draft.json and narration.wav are required")
    episode=json.loads(draft_path.read_text())
    # Use the curated primary/review references; some scholarly hosts reject CI requests.
    # URL reachability is not used as a proxy for source validity or factual review.
    episode["sources"]=SOURCES
    draft_path.write_text(json.dumps(episode,indent=2,ensure_ascii=False)+"\n")
    try:
        from faster_whisper import WhisperModel
    except ImportError: raise SystemExit("faster-whisper missing")
    model=WhisperModel("base",device="cpu",compute_type="int8")
    segments,info=model.transcribe(str(audio),language="en",word_timestamps=True,vad_filter=True)
    words=[]
    for seg in segments:
        for w in (seg.words or []):
            if w.end>w.start: words.append({"start":float(w.start),"end":float(w.end),"word":w.word})
    if len(words)<50: raise SystemExit("Speech alignment returned too few words; inspect generated audio")
    captions=group_words(words)
    duration=float(words[-1]["end"])+0.35
    if not 40<=duration<=65: raise SystemExit(f"Audio duration {duration:.1f}s is outside the intended short range")
    font_path=Path("skills/directing-stickman-videos/assets/fonts/Caveat.ttf")
    title_font=load_font(font_path,42); cap_font=load_font(font_path,34)
    out=root/"publish-package"; out.mkdir(exist_ok=False)
    silent=out/"silent.mp4"; final=out/"psychology-spotlight-effect-short.mp4"
    cmd=["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",str(silent)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    total=math.ceil(duration*FPS)
    for frame in range(total):
        t=frame/FPS
        idx=min(5,int(t/duration*6))
        local=(t-(idx*duration/6))/(duration/6)
        caption=next((c["text"] for c in captions if c["start"]<=t<=c["end"]), "")
        im=draw_scene(t,idx,local,caption,title_font,cap_font)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    err=proc.stderr.read().decode("utf-8","replace")
    if proc.wait()!=0: raise SystemExit("FFmpeg video render failed: "+err[-2500:])
    run(["ffmpeg","-y","-i",str(silent),"-i",str(audio),"-map","0:v:0","-map","1:a:0","-vf","scale=720:1280:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(final)])
    # Thumbnail
    thumb=draw_scene(2.0,0,0.25,"",title_font,cap_font)
    thumb.save(out/"thumbnail.png")
    (out/"sources.md").write_text("# Research sources\n\n"+ "\n".join(f"- [{s['title']}]({s['url']}) — {s['claim_supported']}" for s in SOURCES)+"\n")
    description=f"{episode['title']}\n\n{episode['narration']}\n\nSources:\n"+"\n".join(s["url"] for s in SOURCES)
    (out/"youtube-description.txt").write_text(description+"\n")
    def srt_time(seconds):
        total_ms = max(0, round(float(seconds) * 1000))
        hours, remainder = divmod(total_ms, 3_600_000)
        minutes, remainder = divmod(remainder, 60_000)
        whole_seconds, milliseconds = divmod(remainder, 1000)
        return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"

    srt_cues = []
    for cue in captions:
        cue_text = cue["text"].strip()
        if cue_text:
            srt_cues.append(
                f"{len(srt_cues) + 1}\\n"
                f"{srt_time(cue['start'])} --> {srt_time(cue['end'])}\\n"
                f"{cue_text}"
            )
    if not srt_cues:
        raise SystemExit("Caption generation produced no non-empty SRT cues")
    srt_content = "\\n\\n".join(srt_cues) + "\\n"
    if "{c['text']}" in srt_content:
        raise SystemExit("SRT contains an unresolved caption template")
    (out/"captions.srt").write_text(srt_content)
    probe=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_name,width,height","-of","json",str(final)],text=True)
    probe_data=json.loads(probe)
    video_stream=next((s for s in probe_data.get("streams",[]) if s.get("codec_name")=="h264"),None)
    if not video_stream or video_stream.get("width") != 720 or video_stream.get("height") != 1280:
        raise SystemExit(f"Final MP4 must be 720x1280 H.264; got {video_stream}")
    if "{c['text']}" in srt_content or not srt_content.strip():
        raise SystemExit("Final SRT is empty or contains an unresolved template")
    (out/"quality-report.json").write_text(json.dumps({"video":str(final.name),"duration_seconds":duration,"resolution":f"{video_stream['width']}x{video_stream['height']}","fps":FPS,"caption_cues":len(srt_cues),"aligned_words":len(words),"sources_curated":len(SOURCES),"visual_review":"PENDING_HUMAN_REVIEW","publish_status":"REVIEW_REQUIRED"},indent=2)+"\\n")
    (out/"ffprobe.json").write_text(probe)
    print(json.dumps({"video":str(final),"duration":duration,"words":len(words),"captions":len(captions),"status":"REVIEW_REQUIRED"}))

if __name__=="__main__": main()
