SHIFT = 128

def varbyte(val, unpack = None):
    if unpack:
        return varbyte_unpack(val)
    return varbyte_pack(val)

def varbyte_pack(num):
    result = list()
    tmp = num % SHIFT
    num //= SHIFT
    while num > 0:
        tmp += SHIFT
        result.insert(0, tmp)
        tmp = num % SHIFT
        num /= SHIFT
    result.insert(0, tmp)
    return result

def varbyte_unpack(arr):
    res = list()
    tmp = arr[0]
    new_id = 0
    for num in arr[1:]:
        if num >= SHIFT:
            tmp = tmp * SHIFT + num - SHIFT
        else:
            new_id += tmp
            res.append(new_id)
            tmp = num
    new_id += tmp
    res.append(new_id)
    return res
