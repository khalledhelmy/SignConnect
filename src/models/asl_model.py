import os
import imageio.v2 as imageio

class ASLModel:
    def __init__(self, dataset_path, frame_duration=0.5):
        self.dataset_path = dataset_path
        self.frame_duration = frame_duration

    def get_letter_image(self, letter):
        letter = letter.upper()

        folder = os.path.join(self.dataset_path, letter)
        if not os.path.exists(folder):
            return None

        images = [
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]

        if not images:
            return None

        first_image_path = os.path.join(folder, images[0])
        return imageio.imread(first_image_path)

    def create_video(self, word):
        frames = []

        for letter in word:
            if not letter.isalpha():
                continue

            img = self.get_letter_image(letter)
            if img is None:
                continue

            repeat_frames = int(self.frame_duration * 25)
            frames.extend([img] * repeat_frames)

        if not frames:
            return None

        out_path = "asl_word.mp4"
        imageio.mimsave(out_path, frames, fps=25)

        return out_path
