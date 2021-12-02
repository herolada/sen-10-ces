from similarity import get_similarity
from translate import translate_text

class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.translation = None
        self.correct_translation = None
        self.score = None

    def generate_correct_translation(self):
        if self.translation is not None:
            self.correct_translation = translate_text(self.sentence)
        else:
            self.correct_translation = None

    def calculate_score(self):
        if self.translation is not None and self.correct_translation is not None:
            self.score = get_similarity(self.translation, self.correct_translation)
        else:
            self.score = -1
    
