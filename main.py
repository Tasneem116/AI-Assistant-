from PyQt5.QtCore import QThread, pyqtSignal
# Importing necessary libraries
# selecting voices
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)


# text to speech
def say(text):
    engine.say(text)  # Uses pyttsx3 to say the provided text
    # print(text)  # Prints the text to the console
    engine.runAndWait()  # Ensures the speech is spoken and waits for it to finish
    engine.setProperty("rate", 150)  # Sets the speech rate to 150 words per minute


# conversation with AI
import openai
from config import updated_apikey

chatStr = ''  # to store conversation history


def chat(query):
    global chatStr
    # print(chatStr)
    try:
        openai.api_key = updated_apikey
        chatStr += f'user : {query}\nAI : '  # Append user query to chat history
        response = openai.Completion.create(
            model="text-davinci-003",  # davanci alternatives
            prompt=chatStr,
            temperature=0.7,  # hyper parameter
            max_tokens=256,  # prompt tokens limit value
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # print(f"Assistant: {response['choices'][0]['text']}")
        # assistant_response = response['choices'][0]['text']
        # say(response['choices'][0]['text'])
        chatStr += f'{response["choices"][0]["text"]}\n'
        return response['choices'][0]['text']
        # return assistant_response
    except Exception as e:
        print(f'An error occurred: {e}')


# for AI response generation (without conversation history)
import os

def ai_generate(prompt):
    try:
        openai.api_key = updated_apikey
        text = f'OpenAI response for prompt: {prompt}\n *****************\n\n'

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,  # hyper parameter
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # print(response['choices'][0]['text'])
        assistant_response = response['choices'][0]['text']
        text += response['choices'][0]['text']
        if not os.path.exists('Openai'):
            os.mkdir('Openai')
        with open(f'Openai/{"".join(prompt.split("ai")[1:])}.txt', 'w') as f:
            f.write(text)  # Save AI response to a text file
            return assistant_response

    except Exception as e:
        print(f'An error occurred: {e}')


# To tell weather
import requests
from bs4 import BeautifulSoup


def get_weather(query):
    try:
        # Check if the query contains "temperature" or "weather"
        # prompt engineering
        keyword = 'temperature' if 'temperature' in query else 'weather'

        words = query.split()
        indexes = words.index(keyword) + 1  # finding the index of keyword
        place = ' '.join(words[indexes:])  # Extract the location information from the query
        url = f'https://www.google.com/search?q={place} {keyword}'  # Construct a Google search URL
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.find('div', {'class': 'BNeawe'}).text
        # weather = f'Current {keyword} {place} is {info}'
        # print(f'Assistant: {weather}')
        assistant_response = f'Current {keyword} {place} is {info}'
        return assistant_response
        # return weather
    except Exception as e:
        return f'An error occurred: {e}'


# To open any website
import webbrowser
from googlesearch import search


def open_website(query):
    try:
        search_results = list(search(query, num_results=1))
        if search_results:
            website_url = search_results[0]
            # Extract the site name from the URL
            site_name = website_url.split('www.')[-1].split('.')[0]
            # print(f'Assistant: Opening {site_name} ...')
            # say(f"Opening {site_name} ...")
            # webbrowser.open(website_url)
            opening = f'Opening {site_name} ...'
            webbrowser.open(website_url)
            return opening
        else:
            # print("Assistant: Sorry, I couldn't find any relevant websites")
            # say("Sorry, I couldn't find any relevant websites.")
            sorry_msg = "Sorry, I couldn't find any relevant websites"
            return sorry_msg
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# To show best route from 1 des to other
def maps(des1, des2):
    url = "https://www.google.com/maps/dir/" + des1 + "/" + des2
    webbrowser.open(url)


# To Play a video on YouTube
import pywhatkit


def play_youtube_videos(query):
    video = query.replace('play'.lower(), '').replace('Jarvis'.lower(), '')
    # response engineering here
    assistant_response = f'playing {video}, enjoy.'
    pywhatkit.playonyt(video)
    return assistant_response


# automate email
import smtplib
from email.message import EmailMessage


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('syedatasneem958@gmail.com', 'ozrh jbfx qqvl byku')
    email = EmailMessage()
    email['From'] = 'Sender_Email'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)


# generates a random response phrase for a jarvis
import random

interaction_counter = 0  # Counter just for interacting purposes


def activate_assistant():
    starting_chat_phrases = ["Yes , how may I assist you?",
                             "Yes, What can I do for you?",
                             "How can I help you, ?",
                             "Jarvis at your service, what do you need?",
                             "Jarvis here, how can I help you today?",
                             "Yes, what can I do for you today?",
                             "Yes , what's on your mind?",
                             "Jarvis ready to assist, what can I do for you?",
                             "At your command,. How may I help you today?",
                             "Yes, . How may I be of assistance to you right now?",
                             "Yes , I'm here to help. What do you need from me?",
                             "Yes, I'm listening. What can I do for you, ?",
                             "How can I assist you today,?",
                             "Jarvis here, ready and eager to help. What can I do for you?",
                             "Yes, . How can I make your day easier?",
                             "Yes , what's the plan? How can I assist you today?",
                             "Yes, I'm here and ready to assist. What's on your mind,?"]

    continued_chat_phrases = ["yes", "I'm all ears", "go ahead, I'm listening", " I'm all set to listen up",
                              "I'm fully engaged, share your thoughts", " I'm all set to hear you out"]

    random_chat = ""
    if (interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else:
        random_chat = random.choice(continued_chat_phrases)

    return random_chat


# front-end work
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType
from jarvisUi import Ui_JarvisUi
from PyQt5.QtWidgets import QLineEdit


# for recognizing speech
import speech_recognition as sr

# importing necessary libraries to get updated news
from config import gnews_apikey
import json
import urllib.request

# importing libraries for sending whatsapp messages
import pywhatkit as kit
import datetime

class MainThread(QThread):
    user_signal = pyqtSignal(str)     # user queries
    assistant_signal = pyqtSignal(str)    # assistant queries
    input_signal = pyqtSignal(int)    # whatsapp phone number
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.task_execution()

    # take command from user
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            # r.energy_threshold = 600
            audio = r.listen(source)
            try:
                print('recognizing')
                query = r.recognize_google(audio, language='en-us')  # Convert audio to text  # US accent parameter
                # print(f'You: {query}')
                # self.update_conversation(query, None)
                query = query.lower()  # Convert text to lowercase
                return query
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand your speech.")
            except sr.RequestError as e:
                print(f"Sorry, an error occurred: {e}")

    # To get news headlines
    def get_news(self):
        assistant_response = 'What type of news are you interested in?, is it general, world, nation, business, technology, entertainment, sports, science or health?'
        self.assistant_signal.emit(assistant_response)
        say(assistant_response)
        category = ''
        categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science',
                      'health']
        user = self.takeCommand()
        self.user_signal.emit(user)
        for i in user.split():
            if i in categories:
                category += i
        url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=in&max=10&apikey={gnews_apikey}"
        headlines_message = f'Here are the top headlines on {category}'
        self.assistant_signal.emit(headlines_message)
        say(headlines_message)
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data["articles"]
            for i in range(3):
                title = f"Title: {articles[i]['title']}"
                self.assistant_signal.emit(title)
                say(title)
                description = f"Description: {articles[i]['description']}"
                self.assistant_signal.emit(description)
                say(description)

    # to send whatsapp messages
    def whatsapp_message(self):
        assistant_response = 'To whom you want to message? please enter a phone number below '
        self.assistant_signal.emit(assistant_response)
        say(assistant_response)
        number = int(input('Phone Number: '))
        self.input_signal.emit(number)
        assistant_response1 = 'For confirmation, please enter phone number again '
        self.assistant_signal.emit(assistant_response1)
        say(assistant_response1)
        confirm_number = input('Confirm Phone Number: ')
        self.input_signal.emit(confirm_number)

        if confirm_number == number:
            phone_number = f'+91{confirm_number}'
            assistant_response2 = 'what message do you want to send'
            self.assistant_signal.emit(assistant_response2)
            say(assistant_response2)
            message = self.takeCommand()
            self.user_signal.emit(message)
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 1  # Send the message one minute from now
            assistant_response3 = f"Scheduled to send at: {hour}:{minute}"
            self.assistant_signal.emit(assistant_response3)
            assistant_response4 = 'Your message is being sent, please wait...'
            self.assistant_signal.emit(assistant_response4)
            say(assistant_response4)
            kit.sendwhatmsg(phone_number, message, hour, minute)
            assistant_response5 = 'Message sent successfully!'
            self.assistant_signal.emit(assistant_response5)
            say(assistant_response5)
        else:
            assistant_response6 = 'Sorry, the phone number you entered is incorrect.'
            self.assistant_signal.emit(assistant_response6)
            say(assistant_response6)
            assistant_response7 = 'Please try again.'
            self.assistant_signal.emit(assistant_response7)
            say(assistant_response7)
            whatsapp_message(self)

    # to send an email
    def get_email_info(self):
        assistant_response = 'To Whom you want to send email, please enter a email address below '
        self.assistant_signal.emit(assistant_response)
        say(assistant_response)
        receiver = input("Enter The Receiver's Email:")
        self.input_signal.emit(receiver)
        receiver = receiver
        assistant_response2 = 'For confirmation, please enter email address again'
        self.assistant_signal.emit(assistant_response2)
        say(assistant_response2)
        confirm_receiver = input("Confirm Email Address: ")
        self.input_signal.emit(confirm_receiver)

        if confirm_receiver == receiver:
            assistant_response3 = 'What is the subject of your email?'
            self.assistant_signal.emit(assistant_response3)
            say(assistant_response3)
            subject = self.takeCommand()
            self.user_signal.emit(subject)
            assistant_response4 = 'Tell me the message of your email'
            self.assistant_signal.emit(assistant_response4)
            say(assistant_response4)
            message = self.takeCommand()
            self.user_signal.emit(message)
            send_email(receiver, subject, message)
            assistant_response5 = 'Your email is sent'
            self.assistant_signal.emit(assistant_response5)
            say(assistant_response5)
            assistant_response6 = 'Do you want to send more email?'
            self.assistant_signal.emit(assistant_response6)
            say(assistant_response6)
            send_more = self.takeCommand()
            self.user_signal.emit(send_more)
            if 'yes' in send_more:
                get_email_info(self)
            else:
                assistant_response7 = "Sure, just give me a shout if you'd like to send more emails"
                self.assistant_signal.emit(assistant_response7)
                say(assistant_response7)
        else:
            assistant_response3 = 'Sorry, the email address you entered is incorrect. Please try again'
            self.assistant_signal.emit(assistant_response3)
            say(assistant_response3)
            get_email_info(self)

    def testing(self, query):
        # query = self.takeCommand()

        if 'turn on front white lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response='Turning on front white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v1=1')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn off front white lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning off front white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v1=0')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn on back white lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning on back white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v2=1')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn off back white lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning off back white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v2=0')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn on front yellow lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning on front yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v3=1')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn off front yellow lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning off front yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v3=0')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn on back yellow lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning on back yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v4=1')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn off back yellow lights'.lower() in query:
            # self.user_signal.emit(query)
            assistant_response = 'Turning off back yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            webbrowser.open(
                'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v4=0')  # on light
            time.sleep(2)
            # keyword.press_and_release('ctrl + w')

        elif 'turn on all white lights'.lower() in query:
            assistant_response = 'Turning on all white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(1, 3):
                white_lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=1'
                webbrowser.open(white_lights_on)
                time.sleep(2)

        elif 'turn off all white lights'.lower() in query:
            assistant_response = 'Turning off all white lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(1, 3):
                white_lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=0'
                webbrowser.open(white_lights_on)
                time.sleep(2)

        elif 'turn on all yellow lights'.lower() in query:
            assistant_response = 'Turning on all yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(3, 5):
                yellow_lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=1'
                webbrowser.open(yellow_lights_on)
                time.sleep(2)

        elif 'turn off all yellow lights'.lower() in query:
            assistant_response = 'Turning off all yellow lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(3, 5):
                yellow_lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=0'
                webbrowser.open(yellow_lights_on)
                time.sleep(2)

        elif 'turn on all lights'.lower() in query:
            assistant_response = 'Turning on all lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(1, 5):
                lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=1'
                webbrowser.open(lights_on)
                time.sleep(2)

        elif 'turn off all lights'.lower() in query:
            assistant_response = 'Turning off all lights as requested'
            self.assistant_signal.emit(assistant_response)
            say(assistant_response)
            for i in range(1, 5):
                lights_on = f'https://blr1.blynk.cloud/external/api/update?token=-3sDYRzGHMZURla3YKXiDIlHjY00jG9W&v{i}=0'
                webbrowser.open(lights_on)
                time.sleep(2)

    # To perform tasks
    def perform_task(self):
        while True:
            query = self.takeCommand()  # Capture user's voice query
            # chat(query)
            if query is not None:
                try:
                    lights_query = ['white lights', 'yellow lights', 'all white lights', 'all yellow lights', 'all lights']
                    for i in lights_query:
                        if i.lower() in query:
                            self.user_signal.emit(query)
                            self.testing(query)

                    if 'using ai'.lower() in query:
                        assistant_response = ai_generate(prompt=query)
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        assistant_response1 = 'Done. is there anything else I can help you with?'
                        self.assistant_signal.emit(assistant_response1)
                        say(assistant_response1)
                        # Generate AI response based on the user's query

                    elif 'open camera'.lower() in query:
                        assistant_response = 'Opening camera...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        os.system('start microsoft.windows.camera:')

                    elif 'open notepad'.lower() in query:
                        assistant_response = 'Opening notepad...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        os.system('start notepad')

                    elif 'open command prompt'.lower() in query:
                        assistant_response = 'Opening command prompt...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        os.system('start cmd')

                    elif 'open calculator'.lower() in query:
                        assistant_response = 'Opening calculator...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        os.system('start calc')

                    elif 'open file explorer'.lower() in query:
                        assistant_response = 'Opening file explorer...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        os.system('start explorer')

                    elif 'temperature'.lower() in query or 'weather'.lower() in query:
                        assistant_response = get_weather(query)
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    elif 'updated news'.lower() in query:
                        self.user_signal.emit(query)
                        self.get_news()

                    # Feature source list  (websites)
                    elif "open".lower() in query:
                        query_parts = query.split()
                        website_query = " ".join(query_parts[query_parts.index("open") + 1:])
                        # Perform the web search and open the top result
                        assistant_response = open_website(website_query)
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    elif 'route'.lower() in query:
                        route = query.split('from')[-1].split('to')
                        assistant_response = f'The best route from {route[0]} to {route[1]} is...'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        maps(route[0], route[1])

                    elif 'play'.lower() in query:
                        # say(play_youtube_videos(self.query))
                        # import os
                        # .startfile(musicPath2)
                        assistant_response = play_youtube_videos(query)
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    elif 'the time'.lower() in query:
                        strfTime = datetime.datetime.now().strftime('%I:%M%p')
                        strfTime = strfTime.lstrip('0').replace(':', ' : ')
                        # response engineering here
                        assistant_response = f'The Time is {strfTime}'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    # reset command here
                    elif 'reset chat'.lower() in query:
                        global chatStr
                        chatStr = ''  # Reset the chat history
                        assistant_response = 'Chat is reset'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    # elif 'sleep'.lower() in query or 'you can sleep'.lower() in query or 'sleep now'.lower() in query:
                    #     say("okay. I'm going to sleep. You can wake me up anytime you need assistance.")
                    #     break

                    elif 'whatsapp message'.lower() in query:
                        assistant_response = self.whatsapp_message()
                        # calling the function
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)

                    elif "today's date".lower() in query or "date today".lower() in query:
                        # response engineering here
                        assistant_response = f'the date is {datetime.date.today()}'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    elif "send email".lower() in query or "send an email".lower() in query:
                        assistant_response = self.get_email_info()
                        # calling the function
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)

                    elif 'exit'.lower() in query.lower():
                        assistant_response = 'Okay! Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        jarvis.close()
                        exit()

                    elif 'jarvis'.lower() in query:
                        assistant_response = chat(query)
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)

                    else:
                        break

                except Exception as e:
                    print(e)

    # To execute task
    def task_execution(self):
        if __name__ == '__main__':
            while True:
                query = self.takeCommand()
                if query is not None:
                    if 'jarvis'.lower() in query:
                        global interaction_counter
                        interaction_counter += 1
                        phrases = activate_assistant()
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(phrases)
                        say(phrases)
                        self.perform_task()

                    if 'exit'.lower() in query:
                        assistant_response = 'Goodbye! If you ever have more questions or need assistance in the future, feel free to return. Have a wonderful day!'
                        self.user_signal.emit(query)
                        self.assistant_signal.emit(assistant_response)
                        say(assistant_response)
                        jarvis.close()
                        exit()

    def user_queries(self, query):
        # Emit a signal to update the UI in the main thread
        self.user_signal.emit(query)

    def assistant_queries(self, assistant_response):
        # Emit a signal to update the UI in the main thread
        self.assistant_signal.emit(assistant_response)

    def user_inputs(self, inputs):
        self.input_signal.emit(inputs)



import os
import webbrowser as web

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUi()
        self.ui.setupUi(self)

        self.thread = MainThread()
        self.thread.user_signal.connect(self.user_queries)
        self.thread.assistant_signal.connect(self.assistant_queries)
        self.thread.input_signal.connect(self.user_inputs)

        self.ui.pushButton_start.clicked.connect(self.startTask)
        self.ui.pushButton_exit.clicked.connect(self.close)
        self.ui.pushButton_chrome.clicked.connect(self.chrome_app)
        self.ui.pushButton_whatsapp.clicked.connect(self.whatsapp_app)
        self.ui.pushButton_youtube.clicked.connect(self.yt_app)
        self.ui.chat.clicked.connect(self.start_task)


    def chrome_app(self):
        os.startfile('C://Program Files//Google//Chrome//Application//chrome.exe')

    def yt_app(self):
        web.open('https://www.youtube.com/')

    def whatsapp_app(self):
        web.open('https://web.whatsapp.com/')

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C://Users//Dell//Pictures//JarvisGUI//Black.png")
        self.ui.bg_1.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C://Users//Dell//Pictures//JarvisGUI//spheres1_ai_improvisation_by_gleb.gif")
        self.ui.GIF_1.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie('C://Users//Dell//Pictures//JarvisGUI//1d735ad8eee8350adc96d50e1421ee6d.gif')
        self.ui.GIF_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie('C://Users//Dell//Pictures//JarvisGUI//coollogo_com-81931662.gif')
        self.ui.GIF_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def start_task(self):
        self.ui.responsebox_box.setText("Say 'Jarvis' to start"+'\n')
        self.thread.start()

    def user_queries(self, query):
        # Update UI in the main thread
        self.ui.responsebox_box.append(f'YOU: {query}\n')

    def assistant_queries(self, assistant_response):
        # Update UI in the main thread
        self.ui.responsebox_box.append(f'JARVIS: {assistant_response}\n')

    def user_inputs(self, inputs):
        self.ui.responsebox_box.append(inputs)

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss ap')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.date.setText(label_date)
        self.ui.time.setText(label_time)

import sys

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
