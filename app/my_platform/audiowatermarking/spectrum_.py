"""A python script to perform audio watermark embedding/detection
   on the basis of direct-sequence spread spectrum method."""

# Copyright (C) 2020 by Akira TAMAMORI
# Modified 2021 by Ziphozihle Luvuno

import  numpy  as  np
from scipy.io import wavfile
from pydub import AudioSegment
import shutil
import os
from app.settings import  MEDIA_ROOT, AUDIO_ROOT,BASE_DIR

#HOST_SIGNAL_FILE  =  "host1.wav"                        # Watermark embedding destination file
WATERMARK_SIGNAL_FILE  =  "wmed_signal.wav" 
PSEUDO_RAND_FILE  =  'pseudo_rand.dat'                 # Pseudo-random number sequence file
WATERMARK_ORIGINAL_FILE  =  'watermark_ori.dat'        # original watermark signal
WATERMARK_EXTENDED_FILE  =  'watermark_extended.dat' #extended   watermark signal

REP_CODE  =  True                  # Use repeated embedding
FRAME_LENGTH  =  1024 #frame              length
CONTROL_STRENGTH  =  0.03          # Embedded strength
OVERLAP  =  0.0                    # Frame analysis overlap rate
NUM_REPS  =  3                     # number of embedded iterations




def mono_conversion(raw__file:str, preprocessed_file:str="host1.wav",output_format:str="wav"):
    """ convert sound to have one change"""
    sound = AudioSegment.from_wav(raw__file)
    sound = sound.set_channels(1)
    sound.export(preprocessed_file, format=output_format)

def fix(xs):
    """
    A emuration of MATLAB 'fix' function.
    borrowed from https://ideone.com/YjJwOh
    """

    if xs >= 0:
        res = np.floor(xs)
    else:
        res = np.ceil(xs)
    return res

def embed_sound(raw__file:str, preprocessed_file:str="host1.wav"):
    """ Embed watermark in the sound file
    Args. raw__file: Raw file might have two channels ore different type thus needs a conversion
    Args. preprocessed_file: preprocessed has two channels
    """

    mono_conversion(raw__file,preprocessed_file,'wav')
    #Pseudo random sequence (PRS)
    prs = np.random.rand(1, FRAME_LENGTH) - 0.5
    prs1 = prs
    # Save pseudo-random sequence
    with open(PSEUDO_RAND_FILE, 'w') as f:
        for d in np.squeeze(prs):
            
            f.write("%f\n" % d)

    #Open the embedded audio file
    sr, host_signal = wavfile.read(preprocessed_file)
    signal_len  =  len ( host_signal )

    #Frame movement amount (hop_length)
    frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))

    # Overlap length with adjacent frame
    overlap_length = int(FRAME_LENGTH * OVERLAP)

    # Number of bits that can be embedded
    embed_nbit = fix((signal_len - overlap_length) / frame_shift)

    if REP_CODE:
        # Substantial number of embeddable bits
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    # Integer
    frame_shift = int(frame_shift)
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    #Create original watermark signal (bit string of 0 and 1)
    wmark_original = np.random.randint(2, size=int(effective_nbit))

    #Save original watermark signal
    with open(WATERMARK_ORIGINAL_FILE, 'w') as f:
        for d in wmark_original:
            f.write("%d\n" % d)
            

    # Extend the watermark signal
    if REP_CODE:
        wmark_extended = np.repeat(wmark_original, NUM_REPS)
    else:
        wmark_extended = wmark_original

    #Save extended watermark signal
    with open(WATERMARK_EXTENDED_FILE, 'w') as f:
        for d in np.squeeze(wmark_extended):
            f.write("%f\n" % d)
            

    # Generate a watermarked signal
    pointer = 0
    wmed_signal = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    for  i  in  range ( embed_nbit ):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        alpha = CONTROL_STRENGTH * np.max(np.abs(frame))

        #Embed information according to bit value
        if wmark_extended[i] == 1:
            frame = frame + alpha * prs
        else:
            frame = frame - alpha * prs

        wmed_signal[frame_shift * i: frame_shift * (i+1)] = \
            frame[0, 0:frame_shift]

        pointer = pointer + frame_shift

    wmed_signal = np.concatenate(
        (wmed_signal, host_signal[len(wmed_signal): signal_len]))

    # Save the watermarked signal as wav

    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    
    embedded_file = "encoded" + raw__file.split('/')[-1]

    wavfile.write(embedded_file, sr, wmed_signal)


def move_sound_dep(raw__file,embedded_file):
    
    
    """Function to move the sound files to the correct folder"""    
    original_file_location = "sound/" + raw__file
    shutil.move(os.path.join(BASE_DIR, 'pseudo_rand.dat'), AUDIO_ROOT+'/pseudo_rand.dat')
    shutil.move(os.path.join(BASE_DIR, 'watermark_extended.dat'), AUDIO_ROOT+'/watermark_extended.dat')
    shutil.move(os.path.join(BASE_DIR, 'watermark_ori.dat'), AUDIO_ROOT+'/watermark_ori.dat')
    shutil.move(os.path.join(BASE_DIR, "host1.wav"), AUDIO_ROOT+"/host1.wav")
    shutil.move(os.path.join(MEDIA_ROOT, original_file_location), AUDIO_ROOT+raw__file) 
    shutil.move(os.path.join(BASE_DIR, embedded_file), MEDIA_ROOT + "/sound/" + embedded_file)
    print('Dependency files in the audiowatermarking folders')

