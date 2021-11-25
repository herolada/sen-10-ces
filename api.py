from flask import Flask, request
from flask_restx import Api, Resource
import json
import six
from google.cloud import translate_v2 as translate
from translate import translate_text

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
sentences_dict = {
                'german':
                    {'sentences': ["Der Bebauungsplan für das Gebiet rund um den Humboldthafen am Hauptbahnhof in Mitte muss neu aufgestellt werden.",
                        "Das teilte die Senatsverwaltung für Stadtentwicklung am Mittwoch mit."],},
                'czech':
                    {'sentences': ["Jak se máš?","Tohle je zajímavá věta."]}
                }

sentences = None

def generate_sentences(language):
    return sentences_dict[language]

@app.route("/sentences/<language>")  # Define the route
class Sentences(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get sentences in the given language.")  # Documentation of route
    def get(self, language):
        if language in languages:
            sentences = generate_sentences(language)
            return sentences
        else:
            app.abort(400, status="Language not supported", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

def check_sentence_id(sentence_id):
    return True

translations = {}

parser = app.parser()
parser.add_argument('data', type=str, help='Translation', location='form')

@app.route("/translations/<sentence_id>")
class Translations(Resource):
    
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Post translation of given sentence.")

    @app.expect(parser)
    def put(self, sentence_id):
        if check_sentence_id(sentence_id):
            translations['sentence_id'] = request.form['data']
            return {'translation': translations['sentence_id']}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            return {'translation': translations['sentence_id']}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

correct_translations = {}

@app.route("/correct_translations/<sentence_id>")
class CorrectTranslations(Resource):    
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get correct translation of the given sentence.")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            sentence = sentences[sentence_id]
            correct_translation = translate_text(sentence)
            correct_translations[sentence_id] = correct_translation
            return {'correct_translation': correct_translation}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

"""Run Flask app"""
if __name__ == '__main__':
    flask_app.run(debug=True)
