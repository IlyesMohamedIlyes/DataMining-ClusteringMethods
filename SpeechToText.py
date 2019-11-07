import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('SAY SOMETHING')
    sr.SAMPLE_RATE = 48000
    audio = r.listen(source)
    print('TIME OVER. THANKS')

try:
    print('TEXT\n' + r.recognize_google(audio))
except:
    pass
