from array import array

VARBYTE = 0
SIMPLE9 = 1
SHIFT = 128
CODE_SHIFT = 28
SHIFTS = [28, 14, 9, 7, 5, 4, 3, 2, 1]
NUMS = [
    (1, (1 << SHIFTS[0]) - 1),
    (2, (1 << SHIFTS[1]) - 1),
    (3, (1 << SHIFTS[2]) - 1),
    (4, (1 << SHIFTS[3]) - 1),
    (5, (1 << SHIFTS[4]) - 1),
    (7, (1 << SHIFTS[5]) - 1),
    (9, (1 << SHIFTS[6]) - 1),
    (14, (1 << SHIFTS[7]) - 1),
    (28, (1 << SHIFTS[8]) - 1)
    ]

def varbyte(val, unpack=False):
    if unpack:
        return varbyte_unpack(val)
    return varbyte_pack(val)

def varbyte_pack(nums):
    arr = array("B")
    for num in nums:
        result = list()
        tmp = num % SHIFT
        num //= SHIFT
        while num > 0:
            tmp += SHIFT
            result.insert(0, tmp)
            tmp = num % SHIFT
            num /= SHIFT
        result.insert(0, tmp)
        arr.extend(result)
    return arr

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

def simple9(val, unpack=False):
    if unpack:
        return simple9_unpack(val)
    return simple9_pack(val)

def simple9_pack(nums):
    arr = array("L")
    if (arr.itemsize > 4):
        arr = array("I")
    while nums:
        for i in xrange(1, len(NUMS)):
            if max(nums[:NUMS[i][0]]) > NUMS[i][1]:
                i -= 1
                break
            if len(nums) <= NUMS[i][0]:
                break
        num = 0
        for j in xrange(min(NUMS[i][0], len(nums))):
            num = (num << SHIFTS[i]) + nums.pop(0)
        num += i << CODE_SHIFT
        print bin(num), NUMS[i]
        arr.append(num)
    return arr

def simple9_unpack(arr):
    res = list()
    for num in arr:
        tmp = list()
        i = num >> CODE_SHIFT
        num = num & ((1 << CODE_SHIFT) - 1)
        while num  > 0:
            tmp.append(int(num & NUMS[i][1]))
            num >>= SHIFTS[i]
        res += tmp[::-1]
    return res