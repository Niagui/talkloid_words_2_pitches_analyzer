This is a sketchy personal project to help with talkloid creation. It uses the google cloud Text To Speech API to generate speaking audio, the convert it to pitches that could be used in vocaloid music production. <br>
You can record your own voice for the pitch detection or use already existing audio files. The result may not be very accurate, but it should be good enough.

# Instruction

To install dependencies, run:

``pip install -r requirements.txt``

Run ``pitchAnalyzer`` to use the program. **All the related audio files will be and should be placed in the ``audio`` subfolder (You can change that in the main function).**  If the result if off pretty badly, consider adjusting the parameters of the 
``split_on_silence`` function: https://github.com/jiaaro/pydub/blob/master/pydub/silence.py


![image](https://github.com/user-attachments/assets/9bd07a02-8d2a-4e18-a84e-1d1f481b42c7) <br>
Meet miku, our lord and savior.


