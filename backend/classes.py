from similarity import get_similarity
from translate import translate_text
import json
import time

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
        timeout = time.time() + 10
        while (self.translation is None or self.correct_translation is None and time.time() < timeout):
            time.sleep(0.02)
        if self.translation is not None and self.correct_translation is not None:
            self.score = get_similarity(self.translation, self.correct_translation)
        else:
            self.score = "TIMEOUT"
            
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
