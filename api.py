from re import A
from flask import Flask, request
from flask_restx import Api, Resource
import json
import six
from google.cloud import translate_v2 as translate
from translate import translate_text
from similarity import get_similarity
from classes import Sentence
import queue

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Sen-10-ces",
          description="Train your language skills on real-world sentences.")

# **********************************************************************
# **********************************************************************
# **********************************************************************

# SUPPORTED LANGUAGES:
languages = ['german','czech']

chosen_language = None

parser = app.parser()
parser.add_argument('data', type=str, help='Chosen language', location='form')

@app.route("/languages/")
class Languages(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Choose language out of options.")

    @app.expect(parser)
    def put(self):
        chosen_language = request.form['data']
        if chosen_language in languages:
            return {'language': chosen_language}
        else:
            app.abort(400, status="Chosen language is not available", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

# TEMPORARY SENTENCES:
sentences_generator = {
                'german':
                    {'sentences': ["Der Bebauungsplan für das Gebiet rund um den Humboldthafen am Hauptbahnhof in Mitte muss neu aufgestellt werden.",
                        "Das teilte die Senatsverwaltung für Stadtentwicklung am Mittwoch mit."],},
                'czech':
                    {'sentences': ["Jak se máš?","Tohle je zajímavá věta."]}
                }

id_counter = 0

sentences_dict = {}
sentences_queue = queue.Queue()

# TODO: IMPLEMENT THIS IN A REAL WAY
def generate_sentences(language):
    return sentences_generator[language]

@app.route("/sentences/<language>")  # Define the route
class Sentences(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get sentences in the given language.")  # Documentation of route
    def get(self, language):
        if language in languages:
            sentences_json = generate_sentences(language)
            for sentence in sentences_json['sentences']:
                global id_counter
                s = Sentence(sentence)
                sentences_dict[str(id_counter)] = s
                sentences_queue.put(str(id_counter))
                id_counter += 1
            return sentences_json
        else:
            app.abort(400, status="Language not supported", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/next_sentence/")  # Define the route
class NextSentence(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get next sentence.")  # Documentation of route
    def get(self):
        if not sentences_queue.empty():
            s_id = sentences_queue.get()
            s = sentences_dict[s_id]
            return {'sentence': s.sentence}
        else:
            app.abort(400, status="No sentences left", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

def check_sentence_id(sentence_id):
    if sentence_id in sentences_dict.keys():
        return True
    return False

parser = app.parser()
parser.add_argument('data', type=str, help='Translation', location='form')

@app.route("/translations/<sentence_id>")
class Translations(Resource):
    
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Post translation of given sentence.")

    @app.expect(parser)
    def put(self, sentence_id):
        if check_sentence_id(sentence_id):
            s = sentences_dict[sentence_id]
            s.translation = request.form['data']
            sentences_dict[sentence_id] = s
            return {'translation': s.translation}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            s = sentences_dict[sentence_id]
            return {'translation': s.translation}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/correct_translations/<sentence_id>")
class CorrectTranslations(Resource):    
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get correct translation of the given sentence.")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            s = sentences_dict[sentence_id]
            s.generate_correct_translation()
            sentences_dict[sentence_id] = s
            return {'correct_translation': s.correct_translation}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/text_comparison/<sentence_id>")
class TextComparison(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Compare user translation and correct translation of a sentence.")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            s = sentences_dict[sentence_id]
            s.calculate_score()
            sentences_dict[sentence_id] = s
            return {'translation': s.translation, 'correct_translation': s.correct_translation, 'score': str(s.score)}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/confirm/<sentence_id>/<accept>")
class TranslationConfirmation(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="User either accepts or declines their translation of a sentence.")

    def post(self, sentence_id, accept):
        if check_sentence_id(sentence_id):
            if not accept:
                sentences_queue.put(sentence_id)
            return {'accept': accept}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************



# **********************************************************************
# **********************************************************************
# **********************************************************************
"""Run Flask app"""
if __name__ == '__main__':
    flask_app.run(debug=True)
