import os

import ollama
import requests
import json
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        gptprompt = request.form["gptprompt"]
        '''
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=generate_prompt1(gptprompt),
            max_tokens=2048,
            temperature=0.6,
        )
        questions = response.choices[0].text.strip()
        '''
        prompt = generate_prompt1(gptprompt)
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type":"application/json"}
        data = {"model":"mistral", "prompt": prompt, "stream": False}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_text = response.text
        datajson = json.loads(response_text)
        actualresponse = datajson["response"]
        '''
        response = ollama.chat(model='mistral', messages=[
            {
                 'role': 'user',
                 'content': prompt,
            },
        ])
        '''
        print(actualresponse)
        return redirect(url_for("result", result=actualresponse))

    #result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/result", methods=['GET', 'POST'])
def result():
    result = request.args.get('result')
    return render_template("result.html", result=result)


def generate_prompt1(gptprompt):
    return gptprompt

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
