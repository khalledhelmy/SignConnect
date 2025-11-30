import os
import io
import tempfile
from moviepy.editor import ImageSequenceClip

# Configuration: where local data folder is. When deployed to use GitHub, change to download from raw GitHub.
BASE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "asl_alphabet")
# The function will look for images in project/asl_alphabet/<LETTER>/*.jpg

def create_video_for_letter(letter: str, fps: int = 1):
    # normalize letter
    key = letter.lower()
    if key in ["space", "del", "nothing"]:
        folder = key
    else:
        folder = letter.upper()
    folder_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "asl_alphabet", folder))
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"No folder for letter '{letter}' (expected: {folder_path})")
    # collect image files sorted
    imgs = []
    for fname in sorted(os.listdir(folder_path)):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            imgs.append(os.path.join(folder_path, fname))
    if not imgs:
        raise FileNotFoundError(f"No images found for letter '{letter}' in {folder_path}")
    # create temporary file for video
    # MoviePy requires writing to a filename (not directly to BytesIO) for write_videofile, so use temp file
    tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tmpf_name = tmpf.name
    tmpf.close()
    # create clip
    # fps=1 means each image displayed 1 second (reasonable duration)
    clip = ImageSequenceClip(imgs, fps=fps)
    # write to file
    clip.write_videofile(tmpf_name, codec="libx264", audio=False, verbose=False, logger=None)
    # read bytes into BytesIO
    bio = io.BytesIO()
    with open(tmpf_name, "rb") as f:
        bio.write(f.read())
    # cleanup temp file
    try:
        os.remove(tmpf_name)
    except:
        pass
    bio.seek(0)
    return bio