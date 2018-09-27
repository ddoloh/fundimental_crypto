### This is for Information Security course, Spring semester, 2008   ###
### Hansung University, Advisor: Prof. Dongyoung Koo                 ###
### 1st homework of DES implementation                               ###

### BEGIN - DO NOT CHANGE - BEGIN ###
# In the below permutation tables, values of contents are 1 less than
#                                  the given values in FIPS 46-3.
# This is because the logical count starts from 1 as described in FIPS 46-3.
# However, when it comes to the implementation of the given document,
#          the index of an array starts from 0, not from 1.
InitialPermutationTable = [57, 49, 41, 33, 25, 17, 9, 1,
                           59, 51, 43, 35, 27, 19, 11, 3,
                           61, 53, 45, 37, 29, 21, 13, 5,
                           63, 55, 47, 39, 31, 23, 15, 7,
                           56, 48, 40, 32, 24, 16, 8, 0,
                           58, 50, 42, 34, 26, 18, 10, 2,
                           60, 52, 44, 36, 28, 20, 12, 4,
                           62, 54, 46, 38, 30, 22, 14, 6]
FinalPermutationTable = [39, 7, 47, 15, 55, 23, 63, 31,
                         38, 6, 46, 14, 54, 22, 62, 30,
                         37, 5, 45, 13, 53, 21, 61, 29,
                         36, 4, 44, 12, 52, 20, 60, 28,
                         35, 3, 43, 11, 51, 19, 59, 27,
                         34, 2, 42, 10, 50, 18, 58, 26,
                         33, 1, 41, 9, 49, 17, 57, 25,
                         32, 0, 40, 8, 48, 16, 56, 24]
ExpansionPermutationTable = [31, 0, 1, 2, 3, 4,
                             3, 4, 5, 6, 7, 8,
                             7, 8, 9, 10, 11, 12,
                             11, 12, 13, 14, 15, 16,
                             15, 16, 17, 18, 19, 20,
                             19, 20, 21, 22, 23, 24,
                             23, 24, 25, 26, 27, 28,
                             27, 28, 29, 30, 31, 0]
StraightPermutationTable = [15, 6, 19, 20,
                            28, 11, 27, 16,
                            0, 14, 22, 25,
                            4, 17, 30, 9,
                            1, 7, 23, 13,
                            31, 26, 2, 8,
                            18, 12, 29, 5,
                            21, 10, 3, 24]
ParityDropTable = [56, 48, 40, 32, 24, 16, 8,
                   0, 57, 49, 41, 33, 25, 17,
                   9, 1, 58, 50, 42, 34, 26,
                   18, 10, 2, 59, 51, 43, 35,
                   62, 54, 46, 38, 30, 22, 14,
                   6, 61, 53, 45, 37, 29, 21,
                   13, 5, 60, 52, 44, 36, 28,
                   20, 12, 4, 27, 19, 11, 3]
KeyCompressionTable = [13, 16, 10, 23, 0, 4,
                       2, 27, 14, 5, 20, 9,
                       22, 18, 11, 3, 25, 7,
                       15, 6, 26, 19, 12, 1,
                       40, 51, 30, 36, 46, 54,
                       29, 39, 50, 44, 32, 47,
                       43, 48, 38, 55, 33, 52,
                       45, 41, 49, 35, 28, 31]
# In the below substitution tables, values of contents are exactly the same as
#                                  the given values in FIPS 46-3.
# You can check it from the textbook "Cryptography and Network Security" written by Behrouz A. Forouzan
S_BOX_1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],  ### Row 0
           [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],  ### Row 1
           [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],  ### Row 2
           [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]  ### Row 3
           ]
S_BOX_2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],  ### Row 0
           [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],  ### Row 1
           [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],  ### Row 2
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]  ### Row 3
           ]
S_BOX_3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],  ### Row 0
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],  ### Row 1
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],  ### Row 2
           [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]  ### Row 3
           ]
S_BOX_4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],  ### Row 0
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],  ### Row 1
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],  ### Row 2
           [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]  ### Row 3
           ]
S_BOX_5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],  ### Row 0
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],  ### Row 1
           [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],  ### Row 2
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]  ### Row 3
           ]
S_BOX_6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],  ### Row 0
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],  ### Row 1
           [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],  ### Row 2
           [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]  ### Row 3
           ]
S_BOX_7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],  ### Row 0
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],  ### Row 1
           [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],  ### Row 2
           [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]  ### Row 3
           ]
S_BOX_8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],  ### Row 0
           [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],  ### Row 1
           [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],  ### Row 2
           [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]  ### Row 3
           ]
SubstituteTables = [S_BOX_1, S_BOX_2, S_BOX_3, S_BOX_4,
                    S_BOX_5, S_BOX_6, S_BOX_7, S_BOX_8]

# The below ShiftTable is used to generate round keys
ShiftTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


### END - DO NOT CHANGE - END ###

def permute(inBlock_length, outBlock_length, inBlock, outBlock, permuteTable):
    ### Function permute: apply permutation given inBlock of length inBlock_length and permutation table, \
    ###                   make the permuted block, outBlock, of length outBlock_length
    ### BEGIN - description of parameters
    ###   inBlock_length:      bitlength of input block
    ###   outBlock_length:     bitlength of output block
    ###   plainBlock:          plaintext block of inBlock_length bits
    ###   permuteTable:        permutation table to be applied
    ###   outBlock:            permuted plaintext block after application of permuteTable
    ### END - description of parameters
    # Notice that 'assert' verifies whether the given parameters have exactly the specified length
    assert (len(inBlock) == inBlock_length)

    # Notice that the passed parameters should not be assigned inside a method in this practice
    # Although the assignment operator '=' works without triggering any error message,
    # the resultant block (say 'outBlock' in this method) will be treated as a new local variable and
    # you may not use the expected result outside of this method
    # In other words, the caller cannot receive the updated outBlock
    ## This is a programming issue as desired in Python language
    ## So, we will use of the form variableToCopy[:] = toBeCopied[:],
    ## which allow us to maintain the reference of the variableToCopy ('outBlock' in this method)
    ## without allocating new local variable
    outBlock[:] = []

    for i in range(len(permuteTable)):
        outBlock.append(inBlock[permuteTable[i]])

    assert (len(outBlock) == outBlock_length)


def split(inBlock_length, outBlock_length, inBlock, leftBlock, rightBlock):
    ### Function 'split': split given inBlock of length inBlock_length \
    ###                   into the fixed-sized sub-blocks of length outBlock_length
    ###                   the permuted block becomes equally split sub-blocks,
    ###                   that is leftBlock and rightBlock, of length outBlock_length
    ###
    ### BEGIN - description of parameters
    ###   inBlock_length:      bitlength of input block
    ###   outBlock_length:     bitlength of output blocks
    ###   inBlock:             input block of length inBlock_length
    ###   leftBlock:           a sequence of leading block of length outBlock_length, that is split from inBlock
    ###   rightBlock:          a sequence of trailing block of length outBlock_length, that is also split from inBlock
    ### END - description of parameters
    assert (len(inBlock) == inBlock_length)  # Verify whether the length of input block is as specified

    leftBlock[:] = inBlock[: int(inBlock_length / 2)]
    rightBlock[:] = inBlock[int(inBlock_length / 2):]

    assert (len(leftBlock) == outBlock_length)
    assert (len(rightBlock) == outBlock_length)


def combine(inBlock_length, outBlock_length, leftBlock, rightBlock, outBlock):
    ### Function combine: combine the given leftBlock and rightBlock of length inBlock_length
    ###                   into a single block (outBlock) of length outBlock_length
    ###
    ### BEGIN - description of Input parameters
    ###   inBlock_length:     bitlength of input block, leftBlock and rightBlock
    ###                       (two input blocks should have the equal bitlength)
    ###   outBlock_length:    bitlength of output block, which should be double of the inBlock_length in bitlength
    ###   leftBlock:          a sequence of leading block of length inBlock_length
    ###   rightBlock:         a sequence of trailing block of length inBlock_length
    ###   outBlock:           a concatenated block such as leftBlock || rightBlock of length outBlock_length
    assert (len(leftBlock) == inBlock_length)
    assert (len(rightBlock) == inBlock_length)

    ### BEGIN - TODO (insert code here)
    del outBlock[:]
    outBlock.extend(leftBlock)
    outBlock.extend(rightBlock)

    ### END - TODO

    assert (len(outBlock) == outBlock_length)



def copy(block_length, inBlock, outBlock):
    ### Function copy: copy given block of length block_length to output block
    ### BEGIN - description of parameters
    ###   block_length:        bitlength of input/output block
    ###   outBlock_length:     bitlength of output blocks
    ###   inBlock:             input block of length inBlock_length
    ###   outBlock:            copied block
    ### END - description of parameters

    assert (len(inBlock) == block_length)  # Verify whether the length of input block is as specified

    ### BEGIN - TODO (insert code from here)
    del outBlock[:]
    outBlock.extend(inBlock)
    ### END - TODO


    assert (len(outBlock) == block_length)


def exclusiveOr(block_length, inBlock1, inBlock2, outBlock):
    ### Function exclusiveOr: compute bitwise exclusive or (XOR) operation on two blocks,
    ###                       inBlock1 and inBlock2, then generate the resultant block, outBlock
    ### BEGIN - description of parameters
    ###   block_length:         bitlength of input/output block
    ###   inBlock1:             first operand of XOR operation
    ###   inBlock2:             second operand of XOR operation
    ###   outBlock:             result of XOR operation
    assert (len(inBlock1) == len(inBlock2) == block_length)

    outBlock[:] = inBlock2[:]

    ### BEGIN - TODO (insert code here)
    for i in range(block_length):
        outBlock[i] ^= inBlock1[i]

    ### END - TODO

    assert (len(outBlock) == block_length)


def substitute(inBlock, outBlock, SubstituteTables):
    ### Function substitute: apply the given substitution table on inBlock to get the outBlock
    ###
    ### BEGIN - description of parameters
    ###   inBlock:               input block to be applied to the given SubstituteTables
    ###   outBlock:              resultant block after application of SubstituteTables on inBlock
    ###   SubstituteTables:      S-Box tables in DES function
    ### END - description of parameters
    assert (len(inBlock) == 48)
    assert (len(SubstituteTables) == 8)
    for i in range(8):
        assert (len(SubstituteTables[i]) == 4)
        for j in range(4):
            assert (len(SubstituteTables[i][j]) == 16)

    ### BEGIN - TODO (insert code here)

    # ---- identical Function ----
    preoutBlock = [0] * 32
    # outBlock = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ----------------------------
    for i in range(7):
        row = 2 * inBlock[i * 6] + inBlock[(i + 6) + 5]
        col = 8 * inBlock[(i * 6) + 1] + 4 * inBlock[(i * 6) + 2] + \
              2 * inBlock[(i * 6) + 3] + inBlock[(i * 6) + 4]

        value = SubstituteTables[i][row][col]

        preoutBlock[i*4] = value % 8
        preoutBlock[i*4+1] = value % 4
        preoutBlock[i*4+2] = value % 2
        preoutBlock[i*4+3] = value

    outBlock.extend(preoutBlock)

    ### END - TODO

    assert (len(outBlock) == 32)



def function(inBlock, RoundKey, outBlock):
    ### Function function: DES function as described in the textbook
    ###
    ### BEGIN - description of parameters
    ###   inBlock:            input block for DES function
    ###   RoundKey:           48-bit round key for each round
    ###   outBlock:           output block after DES function
    ### END - description of parameters

    assert (len(inBlock) == 32)
    assert (len(RoundKey) == 48)

    T1 = []
    T2 = []
    T3 = []

    ### BEGIN - TODO (insert code here)
    print(inBlock)
    permute(32, 48, inBlock, T1, ExpansionPermutationTable)
    print("T1:  ", len(T1), T1)
    exclusiveOr(48, T1, RoundKey, T2)
    print("T2:  ", len(T2), T2)
    substitute(T2, T3, SubstituteTables)
    print("T3:  ", len(T3), T3)
    permute(32, 32, T3, outBlock, StraightPermutationTable)

    del T1, T2, T3
    ### END - TODO

    assert (len(outBlock) == 32)


def mixer(leftBlock, rightBlock, RoundKey):
    ### Function mixer: mixing part in the Feistel network in a round of DES
    ###
    ### BEGIN - description of parameters
    ###   leftBlock:            32-bit leading sub-block of the 64-bit input/output block
    ###   rightBlock:           32-bit trailing sub-block as the 64-bit input/output block
    ###   RoundKey:             round key to be XORed with right sub-block
    ### END - description of parameters
    assert (len(leftBlock) == 32)
    assert (len(rightBlock) == 32)
    assert (len(RoundKey) == 48)

    T1 = []
    T2 = []
    T3 = []

    ### BEGIN - TODO (insert code here)

    copy(32,rightBlock, T1)
    function(T1, RoundKey, T2)
    exclusiveOr(32, leftBlock, T2, T3)
    copy(32, T3, rightBlock)

    del T1, T2, T3

    ### END - TODO


def swapper(leftBlock, rightBlock):
    ### Function swapper: switch leftBlock and rightBlock
    ###
    ### BEGIN - description of parameters
    ###   leftBlock:           left sub-block as input
    ###                        but the contents would be that of right sub-block at the end of this function
    ###   rightBlock:          right sub-block as input
    ###                        but the contents would be that of left sub-block at the end of this function
    ### END - description of parameters
    assert (len(leftBlock) == 32)
    assert (len(rightBlock) == 32)

    T = []

    ### BEGIN - TODO (insert code here)
    copy(32, leftBlock, T)
    copy(32, rightBlock, leftBlock)
    copy(32, T, rightBlock)

    del T
    ### END - TODO


def Cipher(plainBlock, RoundKeys, cipherBlock):
    ### Function Cihper: DES application to generate encrypted data
    ###
    ### BEGIN - description of parameters
    ###   plainBlock:            plaintext block to be encrypted of length 64-bit
    ###   RoundKeys:             16 round keys with each 48 bit-length
    ###   cipherBlock:           ciphertext of length 64-bit after encryption of the plainBlock
    ### END - description of parameters
    assert (len(plainBlock) == 64)
    assert (len(RoundKeys) == 16)
    for i in range(15):
        assert (len(RoundKeys[i]) == 48)

    inBlock = []
    leftBlock = []
    rightBlock = []
    outBlock = []

    ### BEGIN - Uncomment when you test result for each round  in the report
    print ("=" * 60 + "\nPlaintext: %s" % \
          BinaryArrayToHexString(plainBlock, 16))
    ### END - Uncomment when you test result for each round  in the report

    permute(64, 64, plainBlock, inBlock, InitialPermutationTable)
    ### BEGIN - Uncomment when you test result for each round  in the report
    print ("-" * 60 + "\nAfter initial permutation: %s" % \
          BinaryArrayToHexString(inBlock, 16))
    ### END - Uncomment when you test result for each round  in the report

    split(64, 32, inBlock, leftBlock, rightBlock)
    ### BEGIN - Uncomment when you test result for each round  in the report
    print ("After splitting: L0 = %s,\tR0 = %s" % \
          (BinaryArrayToHexString(leftBlock, 8), \
           BinaryArrayToHexString(rightBlock, 8)) )

    print ("-" * 60 + "\nRound\t\tLeft\t\tRight\t\tRound Key")
    ### END - Uncomment when you test result for each round  in the report
    for round in range(16):
        mixer(leftBlock, rightBlock, RoundKeys[round])
        if (round != 15):   swapper(leftBlock, rightBlock)
        ### BEGIN - Uncomment when you test result for each round  in the report
        print ("Round %3d:\t%s\t%s\t%s" % \
              ((round + 1), \
               BinaryArrayToHexString(leftBlock, 8), \
               BinaryArrayToHexString(rightBlock, 8), \
               BinaryArrayToHexString(RoundKeys[round], 12)))
        ### END - Uncomment when you test result for each round  in the report

    combine(32, 64, leftBlock, rightBlock, outBlock)
    ### BEGIN - Uncomment when you test result for each round  in the report
    print ("-" * 60 + "\nAfter combination: %s" % \
          BinaryArrayToHexString(outBlock, 16) )
    ### END - Uncomment when you test result for each round  in the report

    permute(64, 64, outBlock, cipherBlock, FinalPermutationTable)
    ### BEGIN - Uncomment when you test result for each round  in the report
    print ("Ciphertext: %s\t(after final permutation)" %
           BinaryArrayToHexString(cipherBlock, 16))
    ### END - Uncomment when you test result for each round  in the report

    assert (len(cipherBlock) == 64)


def Key_Generator(keyWithParities, RoundKeys, ShiftTable):
    ### Function Key_Generator: round key generation algorithm
    ###
    ### BEGIN - description of parameters
    ###   keyWithParities:        64-bit input key
    ###   RoundKeys:              16 48-bit round keys to be generated from keyWithParities
    ###   ShiftTable:             shift table indicating the amound of circular shift left
    assert (len(keyWithParities) == 64)
    assert (len(ShiftTable) == 16)

    cipherKey = []
    leftKey = []
    rightKey = []
    preRoundKey = []

    ### BEGIN - TODO (insert code here)

    permute(64, 56, keyWithParities, cipherKey, ParityDropTable)
    split(56, 28, cipherKey, leftKey, rightKey)

    for round in range(15):
        shiftLeft(leftKey, ShiftTable[round])
        shiftLeft(rightKey, ShiftTable[round])
        combine(28, 56, leftKey, rightKey, preRoundKey)
        permute(56, 48, preRoundKey, RoundKeys[round], KeyCompressionTable)

    ### END - TODO

    assert (len(RoundKeys) == 16)
    for round in range(15):
        assert (len(RoundKeys[round]) == 48)


def shiftLeft(block, numOfShifts):
    ### Function shiftLeft: perform circular shift left operation by numofShifts bits
    ###
    ### BEGIN - description of parameters
    ###   block:            28-bit block to be shifted
    ###   numOfShifts:      bits to be shifted
    assert (len(block) == 28)

    ### BEGIN - TODO (insert code here)
    for i in range(numOfShifts):
        T = block[0]
        block[:] = block[1:]
        block.append(T)
    ### END - TODO


### BEGIN - DO NOT CHANGE - BEGIN ###
### The below functions are helper functions for easy transformation between
### hexadecimal representation of strings and array(s) of binary representation
def H2B(letter):
    if (letter.isdigit()):
        return int(letter)
    elif (letter == "a" or letter == "A"):
        return 10
    elif (letter == "b" or letter == "B"):
        return 11
    elif (letter == "c" or letter == "C"):
        return 12
    elif (letter == "d" or letter == "D"):
        return 13
    elif (letter == "e" or letter == "E"):
        return 14
    elif (letter == "f" or letter == "F"):
        return 15


def HexStringToBinaryArray(inString):
    result = []
    value = 0
    for currentLetter in inString:
        value = H2B(currentLetter)
        if (value == None):
            return None
        result.append(value / 8)
        value = value % 8
        result.append(value / 4)
        value = value % 4
        result.append(value / 2)
        value = value % 2
        result.append(value)
    return result


def B2H(value):
    if (value < 10):
        return str(value)
    elif (value == 10):
        return "A"
    elif (value == 11):
        return "B"
    elif (value == 12):
        return "C"
    elif (value == 13):
        return "D"
    elif (value == 14):
        return "E"
    elif (value == 15):
        return "F"


def MatchBitLength(strVal, bitLength):
    result = strVal
    if (len(strVal) > bitLength):
        result = "0" * (bitLength - len(strVal) % bitLength) + result
    return result


def BinaryArrayToHexString(inArray, reqLen):
    value = 0
    resultString = ""
    resultArray = []
    for i in range(len(inArray)):
        if (type(inArray[0]) == list):
            value = 0
            for j in range(len(inArray[i])):
                value = value * 2 + inArray[i][j]
            while (value != 0):
                resultString = B2H(value % 16) + resultString
                value /= 16
            resultArray.append(resultString)
            resultString = ""
        else:
            value = value * 2 + inArray[i]

    if (type(inArray[0]) == list):
        return resultArray
    while (value != 0):
        resultString = B2H(value % 16) + resultString
        value /= 16
    if (len(resultString) < reqLen):
        resultString = "0" * (reqLen - len(resultString) % reqLen) + resultString
    return resultString


### END - DO NOT CHANGE - END ###

def main():
    # definition of main function
    # This is a test case of the above functions, that is DES
    # See p. 192 in the textbook
    print("Encryption")
    RoundKeys = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    plaintext = HexStringToBinaryArray("123456ABCD132536")
    key = HexStringToBinaryArray("AABB09182736CCDD")
    Key_Generator(key, RoundKeys, ShiftTable)
    ciphertext = []
    Cipher(plaintext, RoundKeys, ciphertext)

    print("\n\nDecryption")
    restored = []
    reverse_RoundKeys = []
    reverse_RoundKeys[:] = RoundKeys[:]
    reverse_RoundKeys.reverse()
    Cipher(ciphertext, reverse_RoundKeys, restored)
    print("-" * 60 + "\nResult")
    print("plaintext:\t\t%s\nciphertext:\t\t%s\ndecrypted plaintext:\t%s" % \
          (BinaryArrayToHexString(plaintext, 16), \
           BinaryArrayToHexString(ciphertext, 16), \
           BinaryArrayToHexString(restored, 16)))


main()  # invocation of main function