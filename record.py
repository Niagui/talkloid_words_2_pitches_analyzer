import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def record_audio(filename, duration=10, fs=44100):
    """
    Record audio from your mic and save it as a .wav file. 
    Change the recod duration constant to change how long you wanna record

    Arguments:
        filename: The name of the output .wav file
        duration: Duration of the recording in seconds (default is 10 seconds)
        fs: Sampling rate (default is 44100 Hz)

    """
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    
    # Normalize audio to 16-bit range
    audio = (audio * np.iinfo(np.int16).max).astype(np.int16)
    wav.write(filename, fs, audio)
    print(f"Audio saved to {filename}")





if __name__ == "__main__":
    print("Enter filename:")
    userinput = input() 
    output_filename = userinput + '.wav'
    record_audio(output_filename)