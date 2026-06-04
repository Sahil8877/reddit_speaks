import modules
import make_frame_audio
import get_post, get_caption, get_audio_pitch
from natsort import natsorted

IMG_PATH = 'Day 52 - Reddit Bot/assets/images'
AUD_PATH  = 'Day 52 - Reddit Bot/assets/audio'
OUT_PATH  = 'Day 52 - Reddit Bot/output'

for path in [IMG_PATH, AUD_PATH, OUT_PATH]:
    modules.os.makedirs(path, exist_ok=True)

MAX_IMAGE_COUNT = 12
DURATION = 1

def get_image_list(path):
    valid = {'.png', '.jpg', '.jpeg', '.webp'}
    return [f for f in natsorted(modules.os.listdir(path))
            if modules.os.path.splitext(f)[1].lower() in valid]

def retry(func, *args, descr="", retries=7, **kwargs):
    for attempt in range(1, retries + 1):
        print(f"\n{descr} attempt {attempt}/{retries}...\n")
        if func(*args, **kwargs):
            return True
    print(f"⚠️  All {retries} attempts failed: {descr}")
    return False

def reset_batch():
    """Clears images, audio, visited subreddits, and output.mp4."""
    # 1. Delete all images
    for f in get_image_list(IMG_PATH):
        modules.os.remove(f"{IMG_PATH}/{f}")
    
    # 2. Delete all audio files
    for f in modules.os.listdir(AUD_PATH):
        modules.os.remove(f"{AUD_PATH}/{f}")
    
    # 3. Delete output video (if exists)
    if modules.os.path.exists(f"{OUT_PATH}/output.mp4"):
        modules.os.remove(f"{OUT_PATH}/output.mp4")
    
    # 4. Reset visited subreddits file
    if modules.os.path.exists('Day 52 - Reddit Bot/visited.txt'):
        modules.os.remove('Day 52 - Reddit Bot/visited.txt')
    
    print("🔄 Batch reset complete. All images, audio, visited.txt, and output.mp4 removed.")

# ── movie builder
def movie_maker(imgs_list, caption_list, audio_pitch_list):
    audio_clips = []
    video_clips = []
    for i, pitch in enumerate(audio_pitch_list):
        audio_path = f'{AUD_PATH}/audio_{i}.wav'
        frame_fn = make_frame_audio.make_frame_factory(pitch, DURATION)
        tone = modules.AudioClip(frame_fn, duration=DURATION, fps=44100)
        tone.write_audiofile(audio_path, fps=44100, logger=None)
        audio_clips.append(modules.AudioFileClip(audio_path))
        print(f"  🎵 Audio {i+1}/{len(audio_pitch_list)} done  (pitch={pitch})")
    for i, img_file in enumerate(imgs_list):

        formatted_caption = modules.textwrap.fill(caption_list[i], width=10)

        clip = modules.ImageClip(f'{IMG_PATH}/{img_file}', duration=DURATION)
        text_clip = modules.TextClip(
            text=formatted_caption, font_size=30, color="white",
            stroke_width=4, stroke_color="black", duration=DURATION,
            size=(clip.w, clip.h)
        ).with_position("center")
        corner_clip = modules.TextClip(
            text=img_file.replace('.png', '').replace('.jpg', ''),
            font_size=20, color="white", stroke_width=2,
            stroke_color="black", duration=DURATION,
        ).with_position(("right", "top"))
        video_clips.append(modules.CompositeVideoClip([clip, text_clip, corner_clip]))
        print(f"  🖼️  Frame {i+1}/{len(imgs_list)} done")



    final_audio = modules.concatenate_audioclips(audio_clips)
    final_video = modules.concatenate_videoclips(video_clips, method="compose")
    final = final_video.with_audio(final_audio)
    print("\n🎬 Rendering final video...")
    final.write_videofile(f"{OUT_PATH}/output.mp4", fps=30)
    final.close()
    for v in video_clips: v.close()
    for a in audio_clips: a.close()
    print("✅ Done! Video saved to output/output.mp4\n")

# ── pipeline
imgs_list = get_image_list(IMG_PATH)
total_imgs = len(imgs_list)

if modules.os.path.exists(f"{OUT_PATH}/output.mp4"):
    print("✅ Output already exists. Delete output.mp4 to start a fresh batch.\n")
    try:
        check = input("Confirm reset? (Y/N): ").strip().upper()
        if check in ('Y', 'YES'):
            reset_batch()
            print("✅ Cleanup done. Please run the script again to start fresh.\n")
        else:
            print("Reset cancelled. Exiting.\n")
    except EOFError:
        print("No input. Exiting.\n")
    finally:
        exit()

elif total_imgs == MAX_IMAGE_COUNT:
    print(f"\n📦 All {MAX_IMAGE_COUNT} images collected. Building video...\n")
    caption_list = get_caption.get_caption(total_imgs, imgs_list, IMG_PATH)
    audio_pitch_list = get_audio_pitch.get_pitch_value(caption_list)
    movie_maker(imgs_list, caption_list, audio_pitch_list)

elif total_imgs < MAX_IMAGE_COUNT:
    print(f"📷 Images found : {total_imgs}/{MAX_IMAGE_COUNT}. Fetching new image now...")
    success = get_post.get_post(IMG_PATH)
    if not success:
        retry(get_post.get_post, IMG_PATH, descr="Fetching image")
    new_total = len(get_image_list(IMG_PATH))
    print(f"✅ Image saved. Progress: {new_total}/{MAX_IMAGE_COUNT}. Run again to continue.\n")

else:   # total_imgs > MAX_IMAGE_COUNT
    print(f"⚠️  Found {total_imgs} images, but max is {MAX_IMAGE_COUNT}.")
    