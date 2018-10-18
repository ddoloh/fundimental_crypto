'''
AES
input : 128 bits
output : 128 bits
cipher key : 128 or 192 or 256 bits
##########################################
1. xor operation with roundKey(addroundkey)
2. substitute bytes(SubBytes)
3. Shift Rows
4. Mix Columns
5. xor operation with roundKey(addroundKey)
6. repeat round-1 times (2 -5)
7. operate the last round without MixColumns
###########################################
'''

import finite_field_mult

SBOX = (
#ROW  0    1     2     3     4     5     6     7      8     9    10    11    12    13    14    15
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, # ROW 0

    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, # ROW 1

    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, # ROW 2

    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, # ROW 3

    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, # ROW 4

    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, # ROW 5

    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, # ROW 6

    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, # ROW 7

    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, # ROW 8

    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, # ROW 9

    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, # ROW 10

    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, # ROW 11

    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, # ROW 12

    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, # ROW 13

    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, # ROW 14

    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16, # ROW 15
)

inv_SBOX = (
#ROW 0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB, # ROW 0

    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB, # ROW 1

    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E, # ROW 2

    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25, # ROW 3

    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, # ROW 4

    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, # ROW 5

    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, # ROW 6

    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, # ROW 7

    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, # ROW 8

    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E, # ROW 9

    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, # ROW 10

    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4, # ROW 11

    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F, # ROW 12

    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF, # ROW 13

    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61, # ROW 14

    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D, # ROW 15
)

def bytes2matrix(text):
    ##### 16-byte array to 4*4 matrix #####
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    ##### 4*4 matrix to 16-byte array #####
    return bytes(sum(matrix, []))

''' inverse transformation of SubBytes function is invSubBytes function  '''

def SubBytes(s_rc):
    for i in range(4):
        for j in range(4):
            s_rc[i][j] = SBOX[s_rc[i][j]]

def invSubBytes(s_rc):
    for i in range(4):
        for j in range(4):
            s_rc[i][j] = inv_SBOX[s_rc[i][j]]


def ShiftRows(s_rc):
    s_rc[0][1], s_rc[1][1], s_rc[2][1], s_rc[3][1] = s_rc[1][1], s_rc[2][1], s_rc[3][1], s_rc[0][1]
    s_rc[0][2], s_rc[1][2], s_rc[2][2], s_rc[3][2] = s_rc[2][2], s_rc[3][2], s_rc[0][2], s_rc[1][2]
    s_rc[0][3], s_rc[1][3], s_rc[2][3], s_rc[3][3] = s_rc[3][3], s_rc[0][3], s_rc[1][3], s_rc[2][3]

def inv_ShiftRows(s_rc):
    s_rc[0][1], s_rc[1][1], s_rc[2][1], s_rc[3][1] = s_rc[3][1], s_rc[0][1], s_rc[1][1], s_rc[2][1]
    s_rc[0][2], s_rc[1][2], s_rc[2][2], s_rc[3][2] = s_rc[2][2], s_rc[3][2], s_rc[0][2], s_rc[1][2]
    s_rc[0][3], s_rc[1][3], s_rc[2][3], s_rc[3][3] = s_rc[1][3], s_rc[2][3], s_rc[3][3], s_rc[0][3]

def CopyColumn(input_col, output_col):
    output_col.extend(input_col)

def mixColumn(input_col, output_col):
    for c in range(4):
        output_col.exttend(SubmixColumn(input_col[c]))

def SubmixColumn(col):
    T = []
    CopyColumn(col, T)
    col[0] = (finite_field_mult(0x02, T[0])) ^ (finite_field_mult(0x03, T[1])) ^ T[2] ^ T[3]
    col[1] = T[0] ^ (finite_field_mult(0x02, T[1])) ^ finite_field_mult(0x03, T[2]) % T[3]
    col[2] = T[0] ^ T[1] ^ finite_field_mult(0x02, T[2]) ^ finite_field_mult(0x03, T[3])
    col[3] = finite_field_mult(0x03, T[0]) ^ T[1] ^ T[2] ^ finite_field_mult(0x02, T[3])


def AddroundKey(State, Key_Word):
    for i in range(4):
        for j in range(4):
            State[i][j] ^= Key_Word[i][j]

def shiftLeft(block):
    for i in range(len(block)):
        T = block[0]
        block[:] = block[1:]
        block.append(T)

def SubWord(state):
    ### substitute first four bytes of input state ###
    for i in range(4):
        state[i] = SBOX[i]

def RotWord(state):
    T = state[0]
    state[0] = state[1]
    state[1] = state[2]
    state[2] = state[3]
    del T

def RoundConstant():

def KeyExpansion(Key, w):

    T = []
    for i in range(4):
        w[i] = Key[4*i] + Key[4*i+1] + Key[4*i+2] + Key[4*i+3]

    for i in range(4, 43):
        if (i % 4) != 0 :
            w[i] = w[i-1] + w[i-4]
        else:
            Temporary_Word = SubWord(w[i-1]) ^ RoundConstant([i/4])
            w[i] = T + w[i-4]

def Cipher(plaintext, output_state, w, numberOfRounds):

    T = matrix2bytes(plaintext)
    KeyExpansion()

    S = AddroundKey(T, w)


    for i in numberOfRounds:
        SubBytes(S)
        ShiftRows(S)
        mixColumn(S)
        AddroundKey(S)

    SubBytes()
    ShiftRows()
    AddroundKey()

    output_state = bytes2matrix()




