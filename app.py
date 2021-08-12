  
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

# Flask instance
app = Flask(__name__)

# create engine and enable sharing a session across threads
engine = create_engine('sqlite:///rctrl.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    incomplete = session.query(Todo).filter_by(complete=False).all()
    complete = session.query(Todo).filter_by(complete=True).all()
  
    return render_template('index.html', incomplete=incomplete, complete=complete)
  
  
@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False, created_at=datetime.datetime.now())
    session.add(todo)
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