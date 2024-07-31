#based on https://newt.phys.unsw.edu.au/jw/notes.html

import numpy as np

def freqToNote(freq: int | float) -> str:
    """ convert frequency to a pitch in the 12 TET system. 
    Takes the closest note as a string.

    Args:
        freq (int | float): Any frequency 

    Returns:
        str: [pitch + octave] combination
    """
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    midi = int(12 * np.log2(freq / 440.0) + 69)
    return f'{notes[midi % 12]}{midi // 12 - 1}'

#print(freqToNote(440))