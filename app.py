import os

import openai
from datetime import timedelta 
from flask import Flask, redirect, render_template, request, url_for, session, jsonify

app = Flask(__name__)
openai.api_key = "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"
app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=10) 




@app.route("/", methods=("GET", "POST"))
def index():
    session['conversation'] = ''
    return render_template("index.html")




@app.route("/output", methods=['Get', 'POST'])
def output():
    animal = request.json['user_input']
    voc_level = request.json['slider_value']
    tex_length = request.json['slider_value2']

    voc_level, tex_length = update_value(voc_level, tex_length)
    
  
        

    conversation = session.get("conversation", "------<br>")
    session["conversation"] = conversation
    message = handle_input(animal, "me", "you", voc_level, tex_length)
        
        
        #session["conversation"] = ''
           


        #return redirect(url_for("index", result=response.choices[0].text))
    return jsonify(message)




def update_value(voc_level, tex_length):
    voc_level = int(voc_level)
    tex_length = int(tex_length)
    # 必要な処理を行う
    if voc_level < 33:
            voc = "lower elementary school level vocabulary "
    if 33 <= voc_level < 66:
            voc = "middle school level vocabulary "
    if voc_level >= 66:
            voc = "a linguist level vocabulary "

    if tex_length < 33:
        length = 10
    if 33<= tex_length < 66:
        length = 20
    if tex_length >= 66:
        length = 35

    return voc, length





def generate_prompt(conversation_history, voc_level, tex_length):
    return f" pretend to be an English conversation teacher and have a conversation at {voc_level} and in {tex_length} words or less after the 'you:'. Respond only with text, and do not include code, etc.\n\n{conversation_history}"

def handle_input(
               input_str : str,
                USERNAME : str,
                 AI_NAME : str,
                 voc_level,
                 tex_length):
    """Updates the conversation history and generates a response using GPT-3."""
    # Update the conversation history
    conversation = session["conversation"]
    conversation += f"{USERNAME}: {input_str}<br>"
    conversation += f"{AI_NAME}: "
   
    # Generate a response using GPT-3
    message = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(conversation, voc_level, tex_length),
                temperature=0.6,
                max_tokens = 100,
               )
    # Update the conversation history
    conversation += f"{message.choices[0].text}<br> "
    
    session['conversation'] = conversation
      
    return message.choices[0].text