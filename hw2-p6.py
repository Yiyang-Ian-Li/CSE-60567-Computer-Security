# This implementation follows the DES standard, showing:
# 1. The 16 round keys generated from the key schedule.
# 2. The output of the f-function in each round.
# 3. The Ln and Rn values for each round.

# DES standard tables

# Initial Permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation (FP) or IP^-1
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9,  49, 17, 57, 25
]

# Permuted Choice 1 (PC-1)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

# Permuted Choice 2 (PC-2)
PC2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of left shifts per round for key schedule
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Expansion (E) table
E = [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# S-boxes (S1 to S8)
SBOXES = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    # S5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    # S6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    # S7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    # S8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

# Permutation (P-box) table for f-function output
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1,  15, 23, 26,
    5,  18, 31, 10,
    2,  8,  24, 14,
    32, 27, 3,  9,
    19, 13, 30, 6,
    22, 11, 4,  25
]

# Helper functions

def string_to_bitlist(s):
    """Convert a binary string to a list of integers (bits)."""
    return [int(bit) for bit in s]

def bitlist_to_string(b):
    """Convert a list of bits to a binary string."""
    return ''.join(str(bit) for bit in b)

def permute(bits, table):
    """Apply a permutation table on the bit list."""
    return [bits[i - 1] for i in table]

def left_rotate(bits, n):
    """Left rotate the list by n positions."""
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    """Bitwise XOR of two bit lists."""
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def sbox_substitution(bits48):
    """Apply the S-box substitution to a 48-bit list.
       Return a 32-bit list.
    """
    output = []
    for i in range(8):
        block = bits48[i*6:(i+1)*6]
        row = (block[0] << 1) | block[5]
        col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        sbox_val = SBOXES[i][row][col]
        # Convert the 4-bit number to bits
        output.extend([ (sbox_val >> 3) & 1, (sbox_val >> 2) & 1, (sbox_val >> 1) & 1, sbox_val & 1])
    return output

def f_function(R, round_key):
    """DES f-function: expand R, XOR with round key, substitute via S-boxes, then permute using P."""
    # Expansion from 32 to 48 bits
    R_expanded = permute(R, E)
    # XOR with round key (48 bits)
    xor_result = xor(R_expanded, round_key)
    # S-box substitution: result is 32 bits
    sbox_output = sbox_substitution(xor_result)
    # Permutation using P-box
    f_out = permute(sbox_output, P)
    return f_out, R_expanded, xor_result, sbox_output

def generate_round_keys(key_bits):
    """Generate 16 round keys from the 64-bit key bits using PC-1, left shifts, and PC-2."""
    # Apply PC-1 to get 56 bits
    key56 = permute(key_bits, PC1)
    # Split into C and D halves
    C = key56[:28]
    D = key56[28:]
    round_keys = []
    for round_no in range(16):
        # Perform left rotations according to shift schedule
        shifts = SHIFT_SCHEDULE[round_no]
        C = left_rotate(C, shifts)
        D = left_rotate(D, shifts)
        # Combine halves and apply PC-2 to get 48-bit round key
        combined = C + D
        round_key = permute(combined, PC2)
        round_keys.append(round_key)
    return round_keys

def des_decrypt(ciphertext_bits, round_keys):
    """Perform DES decryption (which is just DES encryption with round keys in reverse order)."""
    # Apply initial permutation
    permuted_bits = permute(ciphertext_bits, IP)
    # Split into left and right halves (32 bits each)
    L = permuted_bits[:32]
    R = permuted_bits[32:]
    # For logging round details
    round_logs = []
    # For decryption, use round keys in reverse order.
    for round_no in range(16):
        rk = round_keys[15 - round_no]  # reverse order for decryption
        # Save current L and R for logging
        current_L = L.copy()
        current_R = R.copy()
        # Compute f-function on R with current round key
        f_out, R_expanded, xor_result, sbox_out = f_function(R, rk)
        # New L becomes previous R
        new_L = R
        # New R is previous L XOR f_out
        new_R = xor(L, f_out)
        # Log round details
        round_logs.append({
            'round': round_no + 1,
            'round_key': bitlist_to_string(rk),
            'L_in': bitlist_to_string(current_L),
            'R_in': bitlist_to_string(current_R),
            'R_expanded': bitlist_to_string(R_expanded),
            'xor_result': bitlist_to_string(xor_result),
            'sbox_out': bitlist_to_string(sbox_out),
            'f_out': bitlist_to_string(f_out),
            'L_out': bitlist_to_string(new_L),
            'R_out': bitlist_to_string(new_R)
        })
        # Update L and R for next round
        L, R = new_L, new_R
    # Before final permutation, combine R and L (note the swap)
    combined = R + L
    # Apply final permutation
    plain_bits = permute(combined, FP)
    return plain_bits, round_logs

def bitlist_to_text(bits):
    """Convert a bit list (of length multiple of 8) to ASCII text."""
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        # Convert bits to a character
        value = 0
        for bit in byte:
            value = (value << 1) | bit
        text += chr(value)
    return text

def main():
    # Provided ciphertext and key in binary format
    ciphertext_bin = "1100101011101101101000100110010101011111101101110011100001110011"
    key_bin = "0100110001001111010101100100010101000011010100110100111001000100"
    # Convert to bit lists
    ciphertext_bits = string_to_bitlist(ciphertext_bin)
    key_bits = string_to_bitlist(key_bin)
    
    # Generate round keys from the key
    round_keys = generate_round_keys(key_bits)
    print("Round Keys:")
    for i, rk in enumerate(round_keys, 1):
        print(f"Round {i:2d}: {bitlist_to_string(rk)}")
    print("\nStarting DES decryption...\n")
    
    # Perform DES decryption
    plain_bits, round_logs = des_decrypt(ciphertext_bits, round_keys)
    
    # Print round logs for each round
    for log in round_logs:
        print(f"--- Round {log['round']} ---")
        print(f"Round Key  : {log['round_key']}")
        print(f"L_in       : {log['L_in']}")
        print(f"R_in       : {log['R_in']}")
        print(f"R_expanded : {log['R_expanded']}")
        print(f"XOR Result : {log['xor_result']}")
        print(f"S-box Out  : {log['sbox_out']}")
        print(f"f(R, K)    : {log['f_out']}")
        print(f"L_out      : {log['L_out']}")
        print(f"R_out      : {log['R_out']}\n")
    
    # Get plaintext from bit list
    plaintext = bitlist_to_text(plain_bits)
    print("Decrypted Plaintext (ASCII):")
    print(plaintext)

if __name__ == "__main__":
    main()
