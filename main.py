import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from bs4 import BeautifulSoup
import requests

import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',130)

def talk(text):
    engine.say(text)
    engine.runAndWait()
def ai(prompt):
 genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

 # Create the model
 generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 50,
  "response_mime_type": "text/plain",
 }

 model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
 )

 chat_session = model.start_chat(
  history=[
  ]
 )

 response = chat_session.send_message(prompt)
 return response.text

def take_command():
    try:
        with sr.Microphone() as source:
            print('JARVIS Turned ON: Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'bye' in command:
     talk("hope to see you soon!, good bye")
     exit()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    else:
        ques = command
        # info = wikipedia.summary(person, 1)
        # print(info)
        answer= ai(ques).lower()
        if 'ai' in answer:
            answer = answer.replace('ai', 'jarvis')
        print(answer)
        talk(answer)




while True:
    run_alexa()
