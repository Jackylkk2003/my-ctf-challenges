from typing import List

raw_rules = [
    ("VARFAILEOVlowercase", "VARFAILEOV"),
    ("lowercaseVARFAILEOV", "VARFAILEOV"),
    ("VARFAILEOVUPPERCASE", "VARFAILEOV"),
    ("UPPERCASEVARFAILEOV", "VARFAILEOV"),
    ("VARFAILEOV", "WRONGFLAG"),
    ("firebird{", "VAR001EOV"),
    ("}", "VAR002EOV"),
    ("VAR001EOVVAR001EOV", "VARFAILEOV"),
    ("lowercaseVAR001EOV", "VARFAILEOV"),
    ("VAR002EOVlowercase", "VARFAILEOV"),
    ("VAR002EOVVAR002EOV", "VARFAILEOV"),
    ("VAR001EOVVAR002EOV", "VARFAILEOV"),
    ("VAR002EOVVAR001EOV", "VARFAILEOV"),
    ("VAR002EOV", "VARSTRENDEOV"),
    ("VAR001EOV", "VARSTRSTARTEOVVARSTR00EOV"),
]

for i in range(36):
    old = f"VARSTR{i:>02}EOVlowercase"
    new = f"lowercaseVARSTR{i+1:>02}EOV"
    raw_rules.append((old, new))

raw_rules.append(("VARSTR36EOVlowercase", "lowercaseVARFAILEOV"))

for i in range(36):
    old = f"VARSTR{i:>02}EOVVARSTRENDEOV"
    new = "VARFAILEOV"
    raw_rules.append((old, new))
    
raw_rules.append(("VARSTR36EOVVARSTRENDEOV", "VARCNTSTARTEOVVARSTRENDEOVVARCOUNT21EOVVARCOUNT25EOVVARCOUNT14EOVVARCOUNT21EOVVARCOUNT26EOVVARCOUNT02EOVVARCOUNT15EOVVARCOUNT24EOVVARCOUNT09EOVVARCOUNT06EOVVARCOUNT13EOVVARCOUNT02EOVVARCOUNT03EOVVARCOUNT14EOVVARCOUNT00EOVVARCOUNT05EOVVARCOUNT09EOVVARCOUNT15EOVVARCOUNT11EOVVARCOUNT05EOVVARCOUNT10EOVVARCOUNT12EOVVARCOUNT00EOVVARCOUNT02EOVVARCOUNT05EOVVARCOUNT01EOVVARCOUNT06EOVVARCOUNT02EOVVARCOUNT06EOVVARCOUNT00EOVVARCOUNT02EOVVARCOUNT04EOVVARCOUNT00EOVVARCOUNT01EOVVARCOUNT00EOVVARCOUNT00EOVVARPOPEOV"))

for c in "abcdefghijklmnopqrstuvwxyz":
    old = f"{c}VARCNTSTARTEOVVARSTRENDEOV"
    new = f"VARCOUNTING{c.upper()}00EOVVARSTRENDEOV{c}"
    raw_rules.append((old, new))

raw_rules.append(("_VARCNTSTARTEOVVARSTRENDEOV", "VARCOUNTINGUNDER00EOVVARSTRENDEOV_"))

for i in range(36):
    old = f"lowercaseVARCOUNT{i:>02}EOV"
    new = f"VARCOUNT{i:>02}EOVlowercase"
    raw_rules.append((old, new))

for i in range(36):
    for c1 in "_abcdefghijklmnopqrstuvwxyz":
        for c2 in "_abcdefghijklmnopqrstuvwxyz":
            up = c1.upper() if c1 != "_" else "UNDER"
            old = f"{c2}VARCOUNTING{up}{i:>02}EOV"
            if c2 > c1:
                new = f"VARCOUNTING{up}{i+1:>02}EOV{c2}"
            else:
                new = f"VARCOUNTING{up}{i:>02}EOV{c2}"
            raw_rules.append((old, new))

for i in range(36):
    old = f"VARCNT{i:>02}EOVlowercase"
    new = f"lowercaseVARCNT{i:>02}EOV"
    raw_rules.append((old, new))

for i in range(36):
    for c in "_abcdefghijklmnopqrstuvwxyz":
        up = c.upper() if c != "_" else "UNDER"
        old = f"VARSTRSTARTEOVVARCOUNTING{up}{i:>02}EOV"
        new = f"VARSTRSTARTEOVVARCNT{i:>02}EOV"
        raw_rules.append((old, new))

for i in range(36):
    for j in range(36):
        old = f"VARCNT{i:>02}EOVVARSTRENDEOVVARCOUNT{j:>02}EOV"
        if i == j:
            new = f"VARCNTSTARTEOVVARSTRENDEOV"
        else:
            new = f"VARFAILEOV"
        raw_rules.append((old, new))

raw_rules.append(("VARSTRSTARTEOVVARCNTSTARTEOVVARSTRENDEOV", "vvsssrrooonnnmllkiiiiggfedaaaa______VARSEPEOV"+"VARBUBBLEEOV"*36))

for c1 in "_abcdefghijklmnopqrstuvwxyz":
    for c2 in "_abcdefghijklmnopqrstuvwxyz":
        old = f"VARBUBBLEEOV{c1}{c2}"
        if c1 > c2:
            new = f"{c2}VARBUBBLEEOV{c1}"
        else:
            new = f"{c1}VARBUBBLEEOV{c2}"
        raw_rules.append((old, new))

for c in "_abcdefghijklmnopqrstuvwxyz":
    old = f"VARBUBBLEEOV{c}VARPOPEOV"
    new = f"{c}VARPOPEOV"
    raw_rules.append((old, new))

for c1 in "_abcdefghijklmnopqrstuvwxyz":
    for c2 in "_abcdefghijklmnopqrstuvwxyz":
        old = f"{c1}VARSEPEOV{c2}"
        if c1 == c2:
            new = f"VARSEPEOV"
        else:
            new = f"VARFAILEOV"
        raw_rules.append((old, new))

raw_rules.append(("VARSEPEOVVARPOPEOV", "CORRECTFLAG"))

raw_rules.append(("lowercase", "VARFAILEOV"))

rules: List[tuple[str, str]] = []

for old, new in raw_rules:
    if "UPPERCASE" in old:
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
            rules.append((old.replace("UPPERCASE", char), new.replace("UPPERCASE", char)))
    elif "lowercase" in old:
        for char in "_abcdefghijklmnopqrstuvwxyz":
            rules.append((old.replace("lowercase", char), new.replace("lowercase", char)))
    else:
        rules.append((old, new))

with open("rules.txt", "w") as f: # Rename later
    for old, new in rules:
        f.write(f'"{old}" is "{new}"\n')