from app.models.asl_model import ASLModel

class VideoController:
    def __init__(self, dataset_path):
        self.model = ASLModel(dataset_path)

    def generate_word_video(self, word):
        return self.model.create_video(word)
