import time
from bitarray import bitarray
from math import floor

def zero_out(array,length): # zero out the array from 0 to 256
    for i in range(length):  # zero out count array
        array.insert(i,0)
    return array

def cdf(count,cum_count): # populate cum_count array
    for i in range(1,257):
        cum_count[i] += count[i-1]
        cum_count[i] += cum_count[i-1]
    return cum_count

def fill(count,seq):
    total_count = 0
    for byte in seq: # fill count and total_count
        count[byte] += 1
        total_count += 1
    return count,total_count

def flipBit(string):
    bits = int(string,base=2)
    bits = bin(int(string,base=2))[2:].zfill(8)
    bitz = bits[0]
    if bitz == '0':
        bits = '1'+string[1:]
    if bitz == '1':
        bits = '0'+string[1:]
    return bits
def giveCoB(string):
    bits = int(string,base=2)
    bits = bin(int(string,base=2))[2:].zfill(8)
    bitz = bits[0]
    if bitz == '0':
        bits = '1'
    if bitz == '1':
        bits = '0'
    return bits

def count_decode(cum_count):
    count=info
    #print("info:",info)
    for i in range(256):
        count[i] = 0

    return count

def binary(num):
    byte = bin(num)[2:].zfill(8)
    return byte

def encode(seq):
    start_time = time.time()
    print()
    print("-----------------------")
    print("STARTING COMPRESSION...")

    count = [] # count:symbol frequency array.
    cum_count = [] # cum_count:cdf array.
    outbytes = [] # outbytes:output sequnce of bytes
    scale3 = 0 # cale3: # of E3 remappings.
    lower = 0 # lower:lower bound
    upper = 255 # upper bound

    count = zero_out(count,256) # zero out count array
    count,total_count = fill(count,seq)
    cum_count = zero_out(cum_count, 257) # zero out cum_count array
    cum_count = cdf(count, cum_count) # populate cum_count

    #print(" seq is : ", seq)
    print("\t INPUT FILE SIZE: ", total_count, " BYTES")

    for byte in seq: # **(get symbol)**loop over input byte seq
        #print("encoding : ", byte)
        bin_low = bin(lower)[2:].zfill(8)
        bin_up = bin(upper)[2:].zfill(8)

        # calculate new upper and lower values to be used in calculations.
        lower_old = lower
        upper_old = upper
        lower = floor(lower_old + ((upper_old - lower_old  +1) * cum_count[byte]) / total_count) # (l)
        upper = floor(lower_old + (((upper_old - lower_old + 1) * cum_count[byte + 1]) / total_count) - 1) # (u)

        # convert upper and lower bounds to binary
        bin_low = bin(lower)[2:].zfill(8)
        bin_up = bin(upper)[2:].zfill(8)

        while ( (bin_low[0] == bin_up[0]) or ((bin_low[1] == '1') and (bin_up[1] == '0')) ):
            # convert upper and lower bounds to binary
            bin_low = bin(lower)[2:].zfill(8)
            bin_up = bin(upper)[2:].zfill(8)

            if bin_low[0] == bin_up[0]:
               # print("equal")
                # shift msb out to the output
                outbytes.append(bin_low[0]) # **(send b)**
                #print("SHIFT OUT = ", bin_low[0])
                lower = int(bin_low[1:8] + '0', base = 2) # **(shift l to the left by 1 bit and shift 0 into LSB)**
                upper = int(bin_up[1:8] + '1', base = 2) # **(shift u to the left by 1 bit and shft 1 inot LSB)**

                while scale3 > 0:
                   # print("scale3: ",giveCoB(bin_low))
                    outbytes.append(giveCoB(bin_low))# **(send complement of b)**
                    scale3 += -1 # **(decrement scale3)**

            else:# **(E3 condition holds)** may need to switch lower and upper
                if ((bin_low[1] == '1') and (bin_up[1] == '0') ): # check second bits
                    #print("**SHIFT E3**")
                    lower = int(bin_low[0] + bin_low[2:8] + '0', base = 2) # **(shift l to the left by 1 bit and shift 0 into LSB)**
                    upper = int(bin_up[0] + bin_up[2:8] + '1', base = 2) # **(shift u to the left by 1 bit and shft 1 inot LSB)**
                    bin_low = bin(lower)[2:].zfill(8)
                    bin_up = bin(upper)[2:].zfill(8)
                    scale3 += 1 # **(increment scale3)**

    outbytes.append(bin_low[0])

    while scale3 > 0:
        outbytes.append('1')
        scale3 += -1

    outbytes.append(bin_low[1:8])

    out = "".join(outbytes)

    output = bitarray(out)
    outbytes = out

    outsize = (len(out)/8)
    end_time = time.time()
    print("\t OUTPUT FILE SIZE : ", round(outsize), " BYTES.")
    print("\t COMPRESSION RATIO : {:.1f}".format(total_count/outsize), " INPUT BYTES PER OUTPUT BYTES." )
    print("\t TIME ELAPSED {:.5f}".format((end_time-start_time)), "SECONDS.")
    print("DONE COMPRESSING...")

    print()
    return (outstuff, cum_count)

    def decode(seq, info):
    start_time = time.time()
    print()
    print("BEGINNING DECODING CALCULATIONS... ")

    cum_count = info # cum_count:cdf array.
    message = "" # outbytes:output sequnce of bytes
    lower = 0 # lower:lower bound
    upper = 255 # upper bound
    total_count = info[len(info)-1]
    m = 8 # number of bits in buffer
    offset=0
    output = bytearray()

    k = 0

    for byte in seq:
        message = message + binary(byte)

    for i in range(total_count):

        t_bin = message[offset:offset+8] # **(read first m bits of received bitstream into tag t)**
        t = int(t_bin,base=2)
        x = ( (((t - lower + 1) * total_count) - 1 ) / (upper - lower + 1))

        for j in range(256):
            if x >= cum_count[j]:
                varx = 0
            else:
                output.append(j-1)

                lower_old = lower
                upper_old = upper

                lower = floor(lower_old + (( upper_old - lower_old + 1 ) * cum_count[j-1]) / total_count)
                upper = floor(lower_old + ((( upper_old - lower_old + 1 ) * cum_count[j]) / total_count) - 1)

                bin_low = binary(lower)
                bin_up = binary(upper)

                # COMPARE MSB OF LOWER AND UPPER
                while(True):
                    if bin_low[0] == bin_up[0]:

                        #shift out msb
                        lower = int(bin_low[1:8] + '0',base = 2)
                        upper = int(bin_up[1:8] + '1', base = 2)
                        bin_low = binary(lower)
                        bin_up = binary(upper)

                        offset += 1
                    else:
                        break

                #check E3
                while(True):
                    bin_low = binary(lower)
                    bin_up = binary(upper)

                    if ( (bin_low[1] == '1') and (bin_up[1] == '0')):
                        lower = int(bin_low[0] + bin_low[2:8] + '0', base = 2)
                        upper = int(bin_up[0] + bin_up[2:8] + '1', base = 2)
                        bin_low = binary(lower)
                        bin_up = binary(upper)

                        message = message[:offset] + str(1 - int(message[offset+1])) + message[offset+2:]
                        tag = message[offset:offset+m]
                        int_tag = int(tag,base = 2)
                break

    output = bytes(output)

    end_time = time.time()
    print("\t INPUT FILE SIZE : ",len(seq), " BYTES.")
    print("\t OUTPUT FILE SIZE : ", len(output), " BYTES.")
    print("\t TIME ELAPSED {:.5f}".format((end_time-start_time)), "SECONDS.")
    print("DONE DECODING.")
    print("-----------------------")
    print()
    return output
