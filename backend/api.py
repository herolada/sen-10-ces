from re import A
from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS
import json
import six
from google.cloud import translate_v2 as translate
from classes import Sentence
import queue
import threading
from wikipedia import generate_sentences

flask_app = Flask(__name__)
CORS(flask_app)

app = Api(app=flask_app,
          version="1.0",
          title="Sen-10-ces",
          description="Train your language skills on real-world sentences.")
# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/test/")  # Define the route
class Test(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="React test.")  # Documentation of route
    def get(self):
        return {'test': "tester"}

        
# **********************************************************************
# **********************************************************************
# **********************************************************************

# TEMPORARY SENTENCES:
sentences_generator = {
                'german':
                    {'sentences': ["Der Bebauungsplan für das Gebiet rund um den Humboldthafen am Hauptbahnhof in Mitte muss neu aufgestellt werden.",
                        "Das teilte die Senatsverwaltung für Stadtentwicklung am Mittwoch mit.",
                        "Ob zu Weihnachten, zum Geburtstag zum Danke sagen: Mit einem Bahn Gutschein haben Sie immer das passende Geschenk parat.",
                        "Fast alle Bahn-Angebote können Sie bei uns als Digitales Ticket buchen.",
                        "Sie können es direkt in der App buchen oder auf bahn.de kaufen.",
                        "Nein, Digitale Tickets sind nicht übertragbar.",
                        "Der Journalist Peter Limbourg ist seit 1. Oktober 2013 Intendant der Deutschen Welle.",
                        "Außerdem teilt die Bundesregierung der Deutschen Welle die im laufenden Haushaltsverfahren beschlossenen finanziellen Rahmendaten mit, soweit die Deutsche Welle betroffen ist.",
                        "Die Ost-Konferenz ist eine der zwei Konferenzen der Kontinentalen Hockey-Liga.",
                        "Die Sieger der beiden Divisionen und die sechs besten übrigen Mannschaften der Konferenz erreichen die Playoffs."],},
                'czech':
                    {'sentences': ["Ahoj","Sbohem"], 'sens':["Jak se máš?","Tohle je zajímavá věta.","Kapr je sladkovodní ryba.","Dnes jsem měl k obědu knedlíky.",
                    "Čistota je půl zdraví.", "Pásli ovce Valaši.", "Tuhle větu radši nepřekládej.", "Máš dvě koblihy.",
                    "Máma mele maso.", "Tak nám zabili Ferdinanda."]}
                }

user_data = {}
user_data['id_counter'] = 0
user_data['sentences_dict'] = {}
user_data['sentences_queue'] = queue.Queue()
user_data['language'] = ""

def reset_sentences(data):
    data['id_counter'] = 0
    data['sentences_dict'] = {}
    data['sentences_queue'] = queue.Queue()
    return data

# TODO: IMPLEMENT THIS IN A REAL WAY
""" def generate_sentences(language):
    return sentences_generator[language] """

# SUPPORTED LANGUAGES:
languages = ['german','czech']

chosen_language = None

parser = app.parser()
parser.add_argument('language', type=str, help='Chosen language', location='json')

@app.route("/languages/")
class Languages(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Choose language out of options.")

    @app.expect(parser)
    def post(self):
        chosen_language = request.get_json()['language']
        if chosen_language in languages:

            global user_data
            user_data = reset_sentences(user_data)
            user_data['language'] = chosen_language

            #sentences_json = generate_sentences(chosen_language)
            sentences_list = generate_sentences(chosen_language)

            #for sentence in sentences_json['sentences']:
            for sentence in sentences_list:
                s = Sentence(sentence)
                print(s.sentence)
                user_data['sentences_dict'][str(user_data['id_counter'])] = s
                user_data['sentences_queue'].put(str(user_data['id_counter']))
                user_data['id_counter'] += 1
            return {'done':"done"}
        else:
            app.abort(400, status="Chosen language is not available", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/remaining/")  # Define the route
class Remaining(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Returns remaining number of sentences.")  # Documentation of route
    def get(self):
        print("rem")
        remaining = 10
        try:
            remaining = user_data['sentences_queue'].qsize()
            if not user_data['language']:
                remaining = 10
        except:
            pass
        print("remain {}".format(user_data['sentences_queue'].qsize()))
        return {'remaining': remaining}

# **********************************************************************
# **********************************************************************
# **********************************************************************

""" # TEMPORARY SENTENCES:
sentences_generator = {
                'german':
                    {'sentences': ["Der Bebauungsplan für das Gebiet rund um den Humboldthafen am Hauptbahnhof in Mitte muss neu aufgestellt werden.",
                        "Das teilte die Senatsverwaltung für Stadtentwicklung am Mittwoch mit.",
                        "Ob zu Weihnachten, zum Geburtstag zum Danke sagen: Mit einem Bahn Gutschein haben Sie immer das passende Geschenk parat.",
                        "Fast alle Bahn-Angebote können Sie bei uns als Digitales Ticket buchen.",
                        "Sie können es direkt in der App buchen oder auf bahn.de kaufen.",
                        "Nein, Digitale Tickets sind nicht übertragbar.",
                        "Der Journalist Peter Limbourg ist seit 1. Oktober 2013 Intendant der Deutschen Welle.",
                        "Außerdem teilt die Bundesregierung der Deutschen Welle die im laufenden Haushaltsverfahren beschlossenen finanziellen Rahmendaten mit, soweit die Deutsche Welle betroffen ist.",
                        "Die Ost-Konferenz ist eine der zwei Konferenzen der Kontinentalen Hockey-Liga.",
                        "Die Sieger der beiden Divisionen und die sechs besten übrigen Mannschaften der Konferenz erreichen die Playoffs."],},
                'czech':
                    {'sentences': ["Jak se máš?","Tohle je zajímavá věta.","Kapr je sladkovodní ryba.","Dnes jsem měl k obědu knedlíky.",
                    "Čistota je půl zdraví.", "Pásli ovce Valaši.", "Tuhle větu radši nepřekládej.", "Máš dvě koblihy.",
                    "Máma mele maso.", "Tak nám zabili Ferdinanda."]}
                }

id_counter = 0

sentences_dict = {}
sentences_queue = queue.Queue()

# TODO: IMPLEMENT THIS IN A REAL WAY
def generate_sentences(language):
    print(language)
    return sentences_generator[language] """

""" @app.route("/sentences/<language>")  # Define the route
class Sentences(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get sentences in the given language.")  # Documentation of route
    def get(self, language):
        global sentences_queue
        global sentences_dict
        sentences_dict = {} 
        sentences_queue = queue.Queue()
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
 """
# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/next_sentence/")  # Define the route
class NextSentence(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get next sentence.")  # Documentation of route
    def get(self):
        if not user_data['sentences_queue'].empty():
            s_id = user_data['sentences_queue'].get()
            s = user_data['sentences_dict'][s_id]
            return {'sentence': s.sentence,
                    'id':s_id}
        else:
            return {'sentence': "Whooo! You finished all of the sentences!",
                    'id':99}

# **********************************************************************
# **********************************************************************
# **********************************************************************

def check_sentence_id(sentence_id):
    if sentence_id in user_data['sentences_dict'].keys():
        return True
    return False

parser = app.parser()
parser.add_argument('data', type=str, help='Translation', location='json')


@app.route("/translations/<sentence_id>")
class Translations(Resource):
    
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Post translation of given sentence.")

    @app.expect(parser)
    def post(self, sentence_id):
        if check_sentence_id(sentence_id):
            global user_data
            s = user_data['sentences_dict'][sentence_id]
            s.translation = request.get_json()['translation']
            user_data['sentences_dict'][sentence_id] = s
            return {'translation': s.translation}

        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

    def get(self, sentence_id):
        if check_sentence_id(sentence_id):
            s = user_data['sentences_dict'][sentence_id]
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
            s = user_data['sentences_dict'][sentence_id]
            s.generate_correct_translation()
            print(s.correct_translation)
            user_data['sentences_dict'][sentence_id] = s
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
            s = user_data['sentences_dict'][sentence_id]
            s.calculate_score()
            user_data['sentences_dict'][sentence_id] = s
            return {'score': s.score}
        else:
            app.abort(400, status="Invalid sentence id", statusCode="400")

# **********************************************************************
# **********************************************************************
# **********************************************************************

@app.route("/confirm/<sentence_id>/<accept>")
class TranslationConfirmation(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="User either accepts or declines their translation of a sentence.")

    def post(self, sentence_id, accept):
        global user_data
        if check_sentence_id(sentence_id):
            if not accept == 'true':
                user_data['sentences_queue'].put(sentence_id)
            print("accept {}".format(user_data['sentences_queue'].qsize()))
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
