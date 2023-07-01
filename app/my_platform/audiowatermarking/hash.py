import hashlib
#import imagehash
#
#hash = imagehash.average_hash(Image.open('input.png'))
#hash1 = imagehash.average_hash(Image.open('output.png'))
#
#print(hash)
#
#print(hash1)
#
#print(hash == hash1)
#
#
## The Above is a different method which is not powerful enoough to solve for this. You can just use it to reference the fact that we are using something better
#

#filename = "input.png"
#filename1 = "output.png"
original_file = 'wmed_signal.wav'
watermarked_file ='wmed_signal2.wav'


"""A python script to perform audio watermark extraction"""

# Copyright (C) 2020 by Akira TAMAMORI
# Modified 2021 by Ziphozihle Luvuno


def extract_audio(original_file,watermarked_file):
    with open(original_file, "rb") as f:
        bytes = f.read()
        hash_orignal = hashlib.sha256(bytes).hexdigest()
        

    with open(watermarked_file, "rb") as f:
        bytes1 = f.read()
        hash_watermarked = hashlib.sha256(bytes1).hexdigest()

    if hash_orignal == hash_watermarked:
        return "File Encoding Verified"
    
    return "File Encoding Unverified"
        




