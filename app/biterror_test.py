import os
import numpy as np


def compare_files(original_file, watermarked_file):
    """
    Compare two binary files and return the bit rate error
    """
    with open(original_file, "rb") as f1, open(watermarked_file, "rb") as f2:
        data1 = f1.read()
        data2 = f2.read()

    try:
        
        n_bits = len(data1) * 8
        n_errors = 0
        
        for i in range(n_bits):
            #breakpoint()
            if data1[i//8] & (1 << (i % 8)) != data2[i//8] & (1 << (i % 8)):
                n_errors += 1
                print(n_errors)
                bit_rate_error = float(n_errors) / float(n_bits)
            else:
                
                bit_rate_error = 0
    except:
        print("no good2")
        n_bits = len(data2) * 8
        n_errors = 0
        for i in range(n_bits):
            if data1[i//8] & (1 << (i % 8)) != data2[i//8] & (1 << (i % 8)):
                n_errors += 1
                bit_rate_error = float(n_errors) / float(n_bits)

    return print("bit_rate_error: ", bit_rate_error)


# # Example usage
# original_file = "C:/files_/text1.txt"
# watermarked_file = "C:/files_/text3.txt"
# rate_error = compare_files(original_file, watermarked_file)
# print("Bit rate error:", rate_error)


# def compare_files1(input_file1, input_file2):

#     with open(input_file1, 'r') as file:
#         signal1 = file.read().replace('\n', '')
#     with open(input_file2, 'r') as file:
#         signal2 = file.read().replace('\n', '')

#     # Convert the signals to arrays of 0s and 1s

#     signal1_bits = np.array([int(float(bit)) for bit in signal1])
#     signal2_bits = np.array([int(float(bit)) for bit in signal2])

#     # Calculate the number of bits and errors
#     num_bits = len(signal1_bits)
#     num_errors = np.sum(signal1_bits != signal2_bits)

#     # Calculate the bit error rate (BER) and bit rate (BR)
#     BER = num_errors / num_bits
#     BR = num_bits / 1e6

#     # Write the results to the output file

#     print(f"Bit rate: {BR:.2f} Mbps\n")
#     print(f"Bit error rate: {BER:.2e}\n")


# compare_files1(original_file, watermarked_file)
