  
# imports
from flask import Flask, render_template, url_for, json
from flask import request, redirect, flash, jsonify, make_response
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from model import *
import os, sys
import random
import string
import datetime
import speech_recognition as sr
from word2number import w2n


# Flask instance
app = Flask(__name__)

# create engine and enable sharing a session across threads
engine = create_engine('sqlite:///rctrl.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def wav2Vec():
    # Initialize the tokenizer
    tokenizer = Wav2Vec2Tokenizer.from_pretrained('facebook/wav2vec2-base-960h')

    # Initialize the model
    model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h')

    # Read the sound file
    waveform, rate = lb.load('record.wav', sr = 16000)

    # Tokenize the waveform
    input_values = tokenizer(waveform, return_tensors='pt').input_values

    # Retrieve logits from the model
    logits = model(input_values).logits

    # Take argmax value and decode into transcription
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)
    print(transcription,file=sys.stderr)



# add source that just speak above
def getSpeechRecognition():
    r = sr.Recognizer()
    voice = sr.AudioFile('recording/record.wav')
    with voice as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    return r.recognize_google(audio)

def getProcessedSpeech():
    speech = getSpeechRecognition()
    '''
    if((not speech.startswith('add') )and (not speech.startswith('remove'))):
        return False'''

    # STRING PROCESSING

    if(speech.startswith('add')):
        starts = 'add'
    else:
        starts = 'remove'
    # remove the first word
    speech = speech.split(' ', 1)[1]

    return [starts,speech]
    

@app.route('/')
def index():
    incomplete = session.query(Todo).filter_by(complete=False).all()
    complete = session.query(Todo).filter_by(complete=True).all()
  
    return render_template('index.html', incomplete=incomplete, complete=complete)
  


# add or remove
@app.route('/add', methods=['POST'])
def add():
    arr = getProcessedSpeech()
    print(arr,file=sys.stderr)
    if(arr[0] == 'add'):
        todo = Todo(text=arr[1], complete=False, created_at=datetime.datetime.now())
        session.add(todo)
        session.commit()
        
    if(arr[0] == 'remove'):
        deleteTodo = session.query(Todo).filter_by(id=int(arr[1].strip())).one()
        session.delete(deleteTodo)
        session.commit()

  
    return redirect(url_for('index'))
  
  
@app.route('/complete/<id>')
def complete(id):
    todo = session.query(Todo).filter_by(id=int(id)).first()
    todo.complete = True
    session.add(todo)
    session.commit()
  
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)