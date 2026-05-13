import whisper
from TTS.api import TTS
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import shutil

FONT = "C:/Windows/Fonts/arial.ttf"
FPS = 30

PARTS = [
    {
        "type": "intro",
        "narration": "Welcome. Here are five unsolved history mysteries that will shock you.",
    },
    {
        "type": "mystery",
        "number": 1,
        "title": "The Mary Celeste",
        "narration": "Mystery one. The Mary Celeste. In eighteen seventy two, this ship was found completely abandoned in the Atlantic Ocean. The crew vanished without any signs of struggle. No bodies were ever found.",
        "points": ["Found adrift in 1872", "Crew of 10 vanished", "No signs of struggle", "Never explained"]
    },
    {
        "type": "mystery",
        "number": 2,
        "title": "Amelia Earhart",
        "narration": "Mystery two. Amelia Earhart. In nineteen thirty seven, the worlds most famous female pilot disappeared over the Pacific Ocean. Despite massive searches, her plane and body were never found.",
        "points": ["Disappeared in 1937", "Flying over Pacific", "Massive search launched", "Never found"]
    },
    {
        "type": "mystery",
        "number": 3,
        "title": "The Voynich Manuscript",
        "narration": "Mystery three. The Voynich Manuscript. This six hundred year old book is written in a completely unknown language. No expert in the world has ever been able to decode it.",
        "points": ["600 year old book", "Unknown language", "Strange illustrations", "Never decoded"]
    },
    {
        "type": "mystery",
        "number": 4,
        "title": "The Dyatlov Pass Incident",
        "narration": "Mystery four. The Dyatlov Pass Incident. In nineteen fifty nine, nine experienced hikers died mysteriously in Russia. Their tent was torn open from the inside. No explanation has ever been found.",
        "points": ["9 hikers died in 1959", "Tent torn from inside", "Signs of extreme trauma", "Cause unknown"]
    },
    {
        "type": "mystery",
        "number": 5,
        "title": "The Roanoke Colony",
        "narration": "Mystery five. The Roanoke Colony. In fifteen eighty seven, one hundred and fifteen English settlers vanished from Roanoke Island. The only clue was the word Croatoan carved into a tree.",
        "points": ["115 settlers vanished", "Disappeared in 1587", "No bodies found", "Only clue: CROATOAN"]
    },
    {
        "type": "outro",
        "narration": "Which mystery shocked you the most? Leave a comment below. Like and subscribe for more history content.",
    },
]

COLORS = [
    ((15,  0, 35), (200, 100, 255)),
    (( 0, 15, 40), (100, 200, 255)),
    ((35, 10,  0), (255, 160,  50)),
    (( 0, 35, 15), ( 80, 255, 150)),
    ((35,  0,  0), (255, 100, 100)),
]

def get_fonts():
    try:
        return {
            "huge":   ImageFont.truetype(FONT, 95),
            "big":    ImageFont.truetype(FONT, 70),
            "medium": ImageFont.truetype(FONT, 42),
            "small":  ImageFont.truetype(FONT, 30),
            "tiny":   ImageFont.truetype(FONT, 24),
        }
    except:
        f = ImageFont.load_default()
        return {"huge":f,"big":f,"medium":f,"small":f,"tiny":f}

def make_intro_slide():
    img = Image.new('RGB', (1280, 720), (5, 5, 30))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    draw.rectangle([12,12,1268,708], outline=(255,200,0), width=7)
    draw.text((640, 170), "5 UNSOLVED", fill=(255,200,0), font=fonts["huge"], anchor="mm")
    draw.text((640, 290), "HISTORY MYSTERIES", fill=(255,255,255), font=fonts["big"], anchor="mm")
    draw.text((640, 400), "That Will SHOCK You!", fill=(255,120,0), font=fonts["medium"], anchor="mm")
    draw.rectangle([100,450,1180,454], fill=(255,200,0))
    draw.text((640, 520), "Watch all 5 mysteries", fill=(180,180,255), font=fonts["small"], anchor="mm")
    draw.text((640, 630), "LIKE  •  COMMENT  •  SUBSCRIBE", fill=(255,200,0), font=fonts["small"], anchor="mm")
    return img

def make_mystery_slide(part):
    idx = part["number"] - 1
    bg, tc = COLORS[idx]
    img = Image.new('RGB', (1280, 720), bg)
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    draw.rectangle([12,12,1268,708], outline=tc, width=5)
    draw.rectangle([40,25,320,72], fill=tc)
    draw.text((180, 49), f"Mystery #{part['number']} of 5", fill=(0,0,0), font=fonts["small"], anchor="mm")
    draw.text((640, 155), part["title"], fill=tc, font=fonts["big"], anchor="mm")
    draw.rectangle([80,205,1200,209], fill=tc)
    y = 270
    for point in part["points"]:
        draw.text((170, y), "►", fill=tc, font=fonts["medium"], anchor="mm")
        draw.text((680, y), point, fill=(220,220,220), font=fonts["medium"], anchor="mm")
        y += 78
    draw.rectangle([0,672,1280,720], fill=(0,0,0))
    draw.text((640, 696), "Like and Subscribe for more History Mysteries!", fill=(255,200,0), font=fonts["tiny"], anchor="mm")
    return img

def make_outro_slide():
    img = Image.new('RGB', (1280, 720), (5, 5, 30))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()
    draw.rectangle([12,12,1268,708], outline=(255,200,0), width=7)
    draw.text((640, 160), "Which Mystery", fill=(255,200,0), font=fonts["big"], anchor="mm")
    draw.text((640, 265), "Shocked You Most?", fill=(255,255,255), font=fonts["big"], anchor="mm")
    draw.rectangle([100,315,1180,319], fill=(255,200,0))
    draw.text((640, 390), "Comment below!", fill=(255,120,0), font=fonts["medium"], anchor="mm")
    draw.text((640, 475), "LIKE this video", fill=(255,200,0), font=fonts["medium"], anchor="mm")
    draw.text((640, 555), "SUBSCRIBE for more", fill=(100,200,255), font=fonts["medium"], anchor="mm")
    draw.text((640, 645), "New mystery videos every week!", fill=(150,150,150), font=fonts["small"], anchor="mm")
    return img

def make_slide(part):
    if part["type"] == "intro":
        return make_intro_slide()
    elif part["type"] == "mystery":
        return make_mystery_slide(part)
    else:
        return make_outro_slide()

def get_duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

if __name__ == "__main__":
    print("="*55)
    print("  YouTube Bot - History Mysteries Pipeline")
    print("="*55)

    # STEP 1 - Generate audio for each part separately
    print("\nSTEP 1: Generating voice for each part...")
    tts = TTS(model_name="tts_models/en/vctk/vits")
    part_files = []
    part_durations = []

    for i, part in enumerate(PARTS):
        fname = f"part_{i}.wav"
        print(f"  Generating part {i+1} of {len(PARTS)}: {part['type']}...")
        tts.tts_to_file(text=part["narration"], file_path=fname, speaker="p273")
        dur = get_duration(fname)
        part_files.append(fname)
        part_durations.append(dur)
        print(f"    Done! Duration: {dur:.1f}s")

    # STEP 2 - Join all audio parts
    print("\nSTEP 2: Joining all audio parts...")
    with open("audio_list.txt", "w") as f:
        for pf in part_files:
            f.write(f"file '{pf}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", "audio_list.txt", "-c", "copy", "voiceover.wav"
    ])
    for pf in part_files:
        os.remove(pf)
    os.remove("audio_list.txt")
    print("voiceover.wav saved!")

    # STEP 3 - Generate subtitles
    print("\nSTEP 3: Generating subtitles...")
    model = whisper.load_model("base")
    result = model.transcribe("voiceover.wav")
    with open("subtitles.srt", "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"]):
            def fmt(s):
                h=int(s//3600); m=int((s%3600)//60)
                sec=int(s%60); ms=int((s%1)*1000)
                return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"
            f.write(f"{i+1}\n{fmt(seg['start'])} --> {fmt(seg['end'])}\n{seg['text'].strip()}\n\n")
    print("subtitles.srt saved!")

    # STEP 4 - Create thumbnail
    print("\nSTEP 4: Creating thumbnail...")
    make_intro_slide().save("thumbnail.png")
    print("thumbnail.png saved!")

    # STEP 5 - Create frames synced to each part duration
    print("\nSTEP 5: Creating synced video frames...")
    if os.path.exists("frames"):
        shutil.rmtree("frames")
    os.makedirs("frames")

    frame_idx = 0
    for i, (part, duration) in enumerate(zip(PARTS, part_durations)):
        slide = make_slide(part)
        frames_count = int(duration * FPS)
        label = part.get("title", part["type"])
        print(f"  Slide {i+1}: {label} = {duration:.1f}s = {frames_count} frames")
        for _ in range(frames_count):
            slide.save(f"frames/frame_{frame_idx:05d}.png")
            frame_idx += 1

    print(f"Total frames: {frame_idx}")

    # STEP 6 - Assemble final video
    print("\nSTEP 6: Assembling final video...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", "frames/frame_%05d.png",
        "-i", "voiceover.wav",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-shortest",
        "final_video.mp4"
    ]
    subprocess.run(cmd)

    print("\n" + "="*55)
    print("PIPELINE COMPLETE!")
    print("  voiceover.wav   - clean AI voice")
    print("  subtitles.srt   - auto subtitles")
    print("  thumbnail.png   - YouTube thumbnail")
    print("  final_video.mp4 - final video")
    print("="*55)