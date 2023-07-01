def string_to_bits(s):
    # Convert string to byte array
    b = bytes(s, "utf-8")
    # Convert byte array to bits
    bits = ''.join([bin(byte)[2:].zfill(8) for byte in b])
    return bits


# Example usage
my_string = "Helloworld!"
bits = string_to_bits(my_string)
print(len(bits))
