from flask import Flask, redirect, url_for, request, render_template
from flask_restx import Api,Resource

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="VIA app",
          description="Demo app for via")

@app.route('/language', methods = ['GET','POST'])
def language():
    if request.method == 'POST':
        language = request.form['language']
        return redirect(url_for('main', language = language, sentences_left = 10))

    return render_template('language.html')

@app.route('/<language>/<sentences_left>', methods = ['POST', 'GET'])
def main(sentences_left = 10, language = 'german'):
    template_vars = {'senteces_left':sentences_left,'language':language}
    
    # Sentence to be translated.
    if language == 'german':
        template_vars['sentence'] = "Ich habe keine Ahnung."
    elif language == 'czech':
        template_vars['sentence'] = "Nemám ponětí."

    # HTTP 
    if request.method == 'POST':
        translation = request.form['translation']
        # compare translation to original
        # score = ...
        # template_vars['score'] = score
        pass
    elif request.method == 'GET':
        pass

    return render_template('main.html',template_vars = template_vars)
    

if __name__ == '__main__':
   app.run(debug = True)