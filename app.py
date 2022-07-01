#!flask/bin/python
from flask import Flask, render_template, redirect, url_for, request
import requests
import urllib

restfulAPI = 'http://cisc5550fernando.eastus.azurecontainer.io:5001/api/tasks'

def translator(json_file, target_language):
    import os
    from google.cloud import translate_v2 as translate
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fmartinezlopezGTranslateKey.json'
    translate_client = translate.Client()
    for entry in json_file:
        entry['what_to_do'] = translate_client.translate(entry['what_to_do'], target_language=target_language)['translatedText']
    return json_file

available_langs = [{'name':'Arabic', 'code': 'ar'},
                {'name':'Chinese', 'code': 'zh'},
                {'name':'English', 'code': 'en'},
                {'name':'French', 'code': 'fr'},
                {'name':'German', 'code': 'de'},
                {'name':'Italian', 'code': 'it'},
                {'name':'Portuguese', 'code': 'pt'},
                {'name':'Spanish', 'code': 'es'}]

app = Flask(__name__)
app.config.from_object(__name__)

translated = False
translate_to = ''

@app.route("/")
def show_list():
    response = requests.get(restfulAPI)
    response = response.json()
    if translated:
        translated_response = translator(response, target_language=translate_to)
        return render_template('index.html', todolist=translated_response, languages=available_langs, translated=translated)
    else:
        return render_template('index.html', todolist=response, languages=available_langs, translated=translated)

@app.route("/add", methods=['POST'])
def add_entry():
    requests.post(restfulAPI, json={
                                        "what_to_do": request.form['what_to_do'], 
                                        "due_date": request.form['due_date']})
    return redirect(url_for('show_list'))

@app.route("/delete/<item>")
def delete_entry(item):
    item = urllib.parse.quote(item)
    requests.delete(restfulAPI+'/'+item)
    return redirect(url_for('show_list'))

@app.route("/mark/<item>")
def mark_as_done(item):
    item = urllib.parse.quote(item)
    requests.put(restfulAPI+'/'+item)
    return redirect(url_for('show_list'))

@app.route("/translate", methods=['POST','GET'])
def translate_entries():
    global translated
    global translate_to
    if translated == False:
        translated = True
        translate_to = request.form['code']
    else:
        translated = False
    return redirect(url_for('show_list'))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5003)