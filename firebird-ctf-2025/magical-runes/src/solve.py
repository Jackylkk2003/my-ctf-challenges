import copy

p = 127
m = 4099


def hash(s):
    h = 0
    for c in s:
        h = (h * p + ord(c)) % m
    return h


def check(arr, s):
    a = copy.deepcopy(arr)
    for i in range(len(s)):
        if hash(s[i:]) in a:
            a.remove(hash(s[i:]))
        else:
            return False
    return True


with open("grimoire.txt", "r") as f:
    s = f.read()
    arr = list(map(ord, s))

    known_flag = "firebird{"

    for i in range(len(known_flag)):
        for j in range(i, len(known_flag)):
            arr.remove(hash(known_flag[i : j + 1]))

    while len(arr) > 0:
        a = [i for i in range(32, 127) if check(arr, known_flag + chr(i))]
        assert len(a) == 1
        a = a[0]
        known_flag += chr(a)
        for j in range(len(known_flag)):
            arr.remove(hash(known_flag[j:]))

    print(known_flag)
