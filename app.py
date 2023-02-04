import os

import openai
from datetime import timedelta 
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
openai.api_key = "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"
app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=10) 




@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        
        animal = request.form["animal"]
        conversation = session.get("conversation", "------\n")
        session["conversation"] = conversation
        message = handle_input(animal, "me", "you")
        
        
        #session["conversation"] = ''
           


        #return redirect(url_for("index", result=response.choices[0].text))
        return redirect(url_for("index", result=message))
    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(conversation_history):
    return f" pretend to be an English conversation teacher and have a conversation in 40 words. Also, if the English is not natural, naturally correct it and teach after the 'you:'. Respond only with text, and do not include code, etc.\n\n{conversation_history}"

def handle_input(
               input_str : str,
                USERNAME : str,
                 AI_NAME : str,
                 ):
    """Updates the conversation history and generates a response using GPT-3."""
    # Update the conversation history
    conversation = session["conversation"]
    conversation += f"{USERNAME}: {input_str}\n"
    conversation += f"{AI_NAME}: "
   
    # Generate a response using GPT-3
    message = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(conversation),
                temperature=0.6,
                max_tokens = 100,
               )
    # Update the conversation history
    conversation += f"{message.choices[0].text}\n"
    
    session['conversation'] = conversation
      
    return message.choices[0].text