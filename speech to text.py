import speech_recognition as sr

def speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Open the microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        # Recognize the speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        print(f"Sorry, an error occurred: {e}")

if __name__ == "__main__":
    speech_to_text()



