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
filename2 = 'wmed_signal.wav'
filename3='wmed_signal2.wav'

with open(filename2, "rb") as f:
    bytes = f.read()
    hash = hashlib.sha256(bytes).hexdigest()
    print(hash)

with open(filename3, "rb") as f:
    bytes1 = f.read()
    hash1 = hashlib.sha256(bytes1).hexdigest()
    print(hash1)



print(hash == hash1)
