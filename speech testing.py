import speech_recognition as sr
import os
import win32com.client


def say(s):
    speaker = win32com.client.Dispatch('SAPI.SpVoice') #alernate voices
    speaker.Speak(s)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.9  # hyper parameter
        r.energy_threshold = 400 # hyper parameter
        audio = r.listen(source)
        query = r.recognize_google(audio, language='en-in')
        print(f'user said: {query}')
        return query


if __name__ == '__main__':
    # print('PyCharm')
    say('hello, Jarvis AI assistant') # Name here
    print('listening...')
    text = takeCommand()
    say(text)

