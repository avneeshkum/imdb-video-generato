# ============================================
#   modules/video_assembler.py
#   MoviePy + Pillow se final 2-min video assemble karta hai
# ============================================

import os
import imageio_ffmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip,
)
from config import TEMP_DIR, OUTPUT_DIR

VIDEO_W, VIDEO_H = 1920, 1080
VIDEO_SIZE       = (VIDEO_W, VIDEO_H)
FPS              = 24


# ── Font helper ───────────────────────────────────────────────────────────────

def _get_font(size: int, bold: bool = False):
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans{'-Bold' if bold else ''}.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ── Image helpers ─────────────────────────────────────────────────────────────

def _resize_crop(img_path: str, out_suffix: str = "_rc") -> str:
    """Resize + center-crop to VIDEO_SIZE"""
    img     = Image.open(img_path).convert("RGB")
    w, h    = img.size
    ratio_s = VIDEO_W / VIDEO_H
    ratio_i = w / h

    if ratio_i > ratio_s:           # wider than target → fit height
        new_h = VIDEO_H
        new_w = int(new_h * ratio_i)
    else:                           # taller than target → fit width
        new_w = VIDEO_W
        new_h = int(new_w / ratio_i)

    img  = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - VIDEO_W) // 2
    top  = (new_h - VIDEO_H) // 2
    img  = img.crop((left, top, left + VIDEO_W, top + VIDEO_H))

    out = img_path.rsplit(".", 1)[0] + out_suffix + ".jpg"
    img.save(out, quality=92)
    return out


def _dark_overlay(img_path: str, alpha: int = 110) -> str:
    """Semi-transparent dark overlay for text readability"""
    img     = Image.open(img_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    out_img = Image.alpha_composite(img, overlay).convert("RGB")
    out     = img_path.replace("_rc", "_ov")
    out_img.save(out, quality=92)
    return out


def _title_card(title: str, year: str, rating: float, tagline: str) -> str:
    """Create a cinematic title card (dark bg + text)"""
    img  = Image.new("RGB", VIDEO_SIZE, (10, 10, 22))
    draw = ImageDraw.Draw(img)

    # Subtle gradient-like top bar
    for y in range(8):
        draw.line([(0, y), (VIDEO_W, y)], fill=(255, 180, 50, int(60 * y / 8)))

    font_title   = _get_font(100, bold=True)
    font_year    = _get_font(44)
    font_tagline = _get_font(36)

    cx = VIDEO_W // 2

    # Title
    draw.text((cx, VIDEO_H // 2 - 80), title,
              fill=(255, 255, 255), font=font_title, anchor="mm")
    # Year + rating
    draw.text((cx, VIDEO_H // 2 + 30), f"{year}   •   {rating}/10 on IMDB",
              fill=(200, 200, 200), font=font_year, anchor="mm")
    # Tagline
    if tagline:
        draw.text((cx, VIDEO_H // 2 + 100), f'"{tagline}"',
                  fill=(160, 160, 160), font=font_tagline, anchor="mm")

    out = os.path.join(TEMP_DIR, "title_card.jpg")
    img.save(out, quality=95)
    return out


def _lower_third(base_img_path: str, text: str, out_name: str) -> str:
    """Add a lower-third text overlay onto an image"""
    img  = Image.open(base_img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = _get_font(38, bold=True)

    # Dark bar behind text
    bar_h = 70
    draw.rectangle([(0, VIDEO_H - bar_h - 10), (VIDEO_W, VIDEO_H)],
                   fill=(0, 0, 0, 180))
    draw.text((60, VIDEO_H - bar_h + 10), text,
              fill=(255, 200, 50), font=font)

    out = os.path.join(TEMP_DIR, out_name)
    img.save(out, quality=92)
    return out


# ── Main assembler ────────────────────────────────────────────────────────────

def assemble_video(movie_data: dict, script_data: dict, full_audio_path: str) -> str:
    """
    Sab kuch combine karo aur MP4 output karo.
    Returns: path to final video file
    """
    print("\n[4/4] Video assemble kar raha hoon (MoviePy)...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR,   exist_ok=True)

    audio          = AudioFileClip(full_audio_path)
    total_duration = audio.duration
    sections       = script_data["sections"]

    # ── Prepare image frames ──────────────────────────────────────────────────
    frames = []  # list of (image_path, duration_seconds)

    # 1. Title card — 6 seconds
    title_img = _title_card(
        movie_data["title"],
        movie_data["year"],
        movie_data["rating"],
        movie_data.get("tagline", ""),
    )
    frames.append((title_img, 6))

    # 2. Poster — ~18 seconds (hook section)
    if movie_data.get("poster_path"):
        poster = _resize_crop(movie_data["poster_path"])
        poster = _dark_overlay(poster, alpha=90)
        poster = _lower_third(poster, f"{movie_data['title']} ({movie_data['year']})", "poster_lt.jpg")
        frames.append((poster, 18))

    # 3. Backdrops — fill remaining time evenly
    backdrops = movie_data.get("backdrop_paths", [])
    used      = sum(d for _, d in frames)
    remaining = max(total_duration - used, 10)

    if backdrops:
        per_bd = remaining / len(backdrops)
        for i, bd in enumerate(backdrops):
            rc  = _resize_crop(bd, f"_rc{i}")
            ov  = _dark_overlay(rc, alpha=100)
            frames.append((ov, per_bd))
    else:
        # Fallback: re-use poster or black screen
        if movie_data.get("poster_path"):
            frames.append((poster, remaining))
        else:
            frames.append((None, remaining))

    # ── Build MoviePy clips ───────────────────────────────────────────────────
    clips = []
    for img_path, dur in frames:
        if img_path and os.path.exists(img_path):
            clip = ImageClip(img_path, duration=dur)
        else:
            clip = ColorClip(size=VIDEO_SIZE, color=[8, 8, 18], duration=dur)
        clips.append(clip.set_fps(FPS))

    video = concatenate_videoclips(clips, method="compose")

    # Set audio first, then trim length to prevent audio track drop
    video = video.set_audio(audio)

    # Trim to exact audio length
    if video.duration > audio.duration:
        video = video.subclip(0, audio.duration)

    final = video

    # ── Write output ──────────────────────────────────────────────────────────
    safe   = "".join(c for c in movie_data["title"] if c.isalnum() or c in " _-").strip()
    out_path = os.path.join(OUTPUT_DIR, f"{safe}_video.mp4")

    print(f"      Rendering MP4 ({total_duration:.1f}s) ... please wait")
    final.write_videofile(
        out_path,
        fps             = FPS,
        codec           = "libx264",
        audio_codec     = "aac",
        remove_temp     = True,
        verbose         = False,
        logger          = None,
    )

    print(f"      Saved: {out_path}")
    return out_path