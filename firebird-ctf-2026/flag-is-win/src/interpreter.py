from rules import rules

flag = "firebird{algo_is_markov_and_inversion_is_flag}"
s = "firebird{testing_flag}" # For testing

while True:
    for old, new in rules:
        if old in s:
            s = s.replace(old, new, 1)
            break
    else:
        break
print("Testing output:", s) # Should be WRONGFLAG

while True:
    for old, new in rules:
        if old in flag:
            flag = flag.replace(old, new, 1)
            break
    else:
        break
print("Flag output:", flag) # Should be CORRECTFLAG