from tabnanny import verbose
from tqdm import tqdm
import copy
F = GF(2**8)

def generate_s_box(a, b):
    a = F.from_integer(a)
    b = F.from_integer(b)

    new_s_box = ((a * F.from_integer(x) + b).to_integer() for x in range(256))
    return tuple(new_s_box)

def check_s_box(new_s_box):
    return any(new_s_box[new_s_box[x]] != x for x in range(256))

def check_s_box_2(new_s_box):
    return sum(i == new_s_box[i] for i in range(256)) == 0

def check_s_box_3(new_s_box):
    return sum((i ^^ new_s_box[i]) == 0xFF for i in range(256)) == 0

def check_s_box_4(new_s_box):
    return 70 < len(set(i - new_s_box[i] for i in range(256))) < 75

tot = 0

for a in tqdm(range(2, 256)):
    for b in range(0, 256):
        s_box_candidate = generate_s_box(a, b)
        identity_pos = [i for i in range(256) if s_box_candidate[i] == i][0]
        reverse_pos = [i for i in range(256) if (i ^^ s_box_candidate[i]) == 0xFF][0]
        s_box_candidate2 = list(copy.deepcopy(s_box_candidate))
        s_box_candidate2[identity_pos], s_box_candidate2[reverse_pos] = s_box_candidate2[reverse_pos], s_box_candidate2[identity_pos]
        if check_s_box(s_box_candidate2) and check_s_box_2(s_box_candidate2) and check_s_box_3(s_box_candidate2) and check_s_box_4(s_box_candidate2):
            print(f"Found good s_box with a={a}, b={b}:")
            print(s_box_candidate2)
            tot += 1

print(f"Total good s_boxes found: {tot}")
