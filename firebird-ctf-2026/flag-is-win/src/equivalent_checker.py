strlen = 36
inversions = (21, 25, 14, 21, 26, 2, 15, 24, 9, 6, 13, 2, 3, 14, 0, 5, 9, 15, 11, 5, 10, 12, 0, 2, 5, 1, 6, 2, 6, 0, 2, 4, 0, 1, 0, 0,)
sorted_chars = "vvsssrrooonnnmllkiiiiggfedaaaa______"

def main():
    s = input("Flag: ").strip()
    if not s.startswith("firebird{") or not s.endswith("}"):
        print("WRONGFLAG")
        return
    s = s[9:-1]  # Remove firebird{ and }
    if len(s) != strlen:
        print("WRONGFLAG")
        return
    
    for i in range(strlen):
        cnt = sum(1 for c in s[:-(i+1)] if c > s[-(i+1)])
        if cnt != inversions[i]:
            print("WRONGFLAG")
            return
    
    sorted_s = ''.join(sorted(s)[::-1])
    if sorted_s != sorted_chars:
        print("WRONGFLAG")
        return
    
    print("CORRECTFLAG")
    
if __name__ == "__main__":
    main()