SHIFT_RIGHT = 128
SHIFT_LEFT = 256

def varbyte(num):
    tmp = num & MASK
    num >>= LEN2
    while num > 0:
        tmp = ((SHIFT_RIGHT + tmp) * SHIFT_LEFT) + num % SHIFT_RIGHT
        num //= SHIFT_RIGHT
    return tmp
