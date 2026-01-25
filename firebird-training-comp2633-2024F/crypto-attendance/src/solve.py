from pwn import *

HOST = "localhost"
PORT = 3000

context.log_level = "debug"
p = remote(HOST, PORT)

p.sendline(b"00" * 100)
p.recvuntil(b"flag_enc = ")

flag_enc = p.recvline().strip().decode()[1:-1]
flag_enc = bytes.fromhex(flag_enc)

p.recvuntil(b"message_enc = ")
message_enc = p.recvline().strip().decode()[1:-1]
message_enc = bytes.fromhex(message_enc)

flag = xor(flag_enc, message_enc)
print(flag)
