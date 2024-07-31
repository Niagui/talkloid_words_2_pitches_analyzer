import os, io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa, re
import record, freq2note
from gtts import gTTS

TEST_PATH = 'audio/sigma.wav'


"""
How this works:

Basically you start with an audio (u can get it from TTS)

we split the word on silence
The speech recognizer will recognize all the words
We use an re command to split all those words into syllables by taking 
a pretty bad average time taken per syllable in time segments.

Then for each time segment we detect the pitches.


"""

def getAudioFromTTS(phrase, filename='audio/output.wav'):
    tts = gTTS(text=phrase, lang='en', timeout=10)
    tts.save('temp.mp3')

    audio = AudioSegment.from_mp3('temp.mp3')
    audio.export('audio/' + filename + '.wav', format='wav')
    os.remove('temp.mp3')
    return 'audio/' + filename + '.wav'


#this thingy should give you all the words
def detectWords(audio_path:str) -> list[tuple[str, int|float, int|float]]:

    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)
    audioSegments = split_on_silence(audio, min_silence_len=350, silence_thresh=-40)   #attempt to split words

    timestamps = []
    curTime = 0

    #use buffer to export temporary wav file and recognize the phrase
    for audioSegment in audioSegments:
        buffer = io.BytesIO()
        audioSegment.export(buffer, format='wav')
        buffer.seek(0)  #rewind
        with sr.AudioFile(buffer) as source:
            audio = recognizer.record(source)       #get audio 
            try:
                words = recognizer.recognize_sphinx(audio).split()      #get words
                segmentLen = len(audioSegment)/1000                     #get length of each phrase/sentence
                wordLen = round((segmentLen / len(words)), 4)           #get average length of a word
                for word in words:
                    timestamps.append((word, curTime, round((curTime + wordLen), 4)))
                    curTime += wordLen
            except LookupError:
                print("Look up Error: Could not understand audio")
            except ZeroDivisionError:
                print("Empty segment detected... keep moving")
    return timestamps


def segment_into_syllables(word):
    syllables = re.findall(r'[^aeiou]*[aeiou]+(?:[^aeiou]*$|[^aeiou](?=[^aeiou]))?', word, re.I)
    return syllables


def detectPitches(audio):
    pitches, magnitudes = librosa.core.piptrack(y=audio, hop_length=2048, win_length=2048)
    pitchLst = []
    for frame in range(pitches.shape[1]):   
        index = magnitudes[:, frame].argmax()
        pitch = pitches[index, frame]
        if pitch > 0:
            pitchLst.append(freq2note.freqToNote(pitch))
    return pitchLst


def extract_syllables(audio_path: str):
    timestamps = detectWords(audio_path)
    audio = AudioSegment.from_wav(audio_path)
    
    for word, start, end in timestamps:
        try:
            #print(word, start*1000, end*1000)
            syllables = segment_into_syllables(word)
            #print(f"Word: {word}, Syllables: {syllables}")
            
            #take average syllable len (not very accurate tho)
            syllable_pitches = []
            word_audio = audio[(start*1000):(end*1000)]
            syllable_Len = (end - start) / len(syllables)
            
            for i, syllable in enumerate(syllables):
                syllable_start = i * syllable_Len
                syllable_end = (i + 1) * syllable_Len
                syllable_audio_segment = word_audio[(syllable_start*1000):(syllable_end*1000)]

                buffer = io.BytesIO()
                syllable_audio_segment.export(buffer, format='wav')
                buffer.seek(0)
                y, sr = librosa.load(buffer, sr=None)
                pitch_list = detectPitches(y)
                if pitch_list:
                    syllable_pitches.append((syllable, pitch_list))
                else:
                    syllable_pitches.append("undetected")
        except ZeroDivisionError:
            print("Fail to detect a syllable...")
        
        print(f"Word: {word}\nSyllable -- Pitches: {syllable_pitches}\n")



def pitch_analysis():
    phrase = input("Enter the phrase to be analyzed:")
    path = input("Enter filename (default to be your phrase):")
    if not path:
       path = phrase
    print(phrase)
    audio_path = getAudioFromTTS(phrase, path)
    extract_syllables(audio_path=audio_path)
    return


if __name__ == '__main__':

    #user interface

    print("\nThis is a pitch analyser that breaks down a spoken phrase into syllables and their corresponding pitches.\n"+
          "this is designed to assist making talkaloids withint vocaloid and other vocal synthesizers\n\n")
    
    option = input("Enter 1 to use an audio from file\n"+
                  "Enter 2 to record yourself\n"+
                  "Enter anything else to use a TTS(text to speech) speaker from google: ")
    if option == '1':
        path = input("Enter audio path (with format):")
        path = 'audio/' + path
        extract_syllables(path)
    elif option == '2':
        duration = int(input("how long would you like to record (in seconds)?"))
        filename = input("Enter filename (without format, e.g. output don't add .wav to it):")
        filename = 'audio/' + filename + '.wav'
        record.record_audio(filename, duration)
        extract_syllables(filename)
    else:
        pitch_analysis()
