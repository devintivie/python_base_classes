

def bit_string_to_bool(string):
    return False
    # if string == '1' :
    #     return 


def int_bit_to_bool(value, shift):
    tmp = value >> shift
    return bool(tmp & 0x1)