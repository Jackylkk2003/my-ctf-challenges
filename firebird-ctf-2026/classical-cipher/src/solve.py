from pwn import *
import string

HOST = "localhost"
PORT = 3000

# context.log_level = 'debug'
with remote(HOST, PORT) as io:
    io.recvuntil(b'Length of the message: ')
    n = int(io.recvline().strip())

    log.success(f'Message length: {n}')

    freq = [{x : [] for x in string.ascii_lowercase} for _ in range(n)]
    prev = 'a' * n
    cnt_rounds = 0

    for round_num in range(0x0b01):
        io.sendlineafter(b'c: ', b'a' * n)
        io.recvuntil(b'm: ')
        m = io.recvline().strip()
        io.recvuntil(b'ciphertext: ')
        ciphertext = io.recvline().strip()

        cnt = sum(1 for x in ciphertext if x == ord('a'))
        message = []
        for f, c in zip(freq, m):
            f[chr(c)].append(cnt)
            best_avg = -1
            best_char = 'a'
            for ch in string.ascii_lowercase:
                if not f[ch]:
                    continue
                avg = sum(f[ch]) / len(f[ch])
                if avg > best_avg:
                    best_avg = avg
                    best_char = ch
            message.append(best_char)
        new_message = ''.join(message)
        if new_message == prev:
            cnt_rounds += 1
        else:
            cnt_rounds = 1
            prev = new_message

        if cnt_rounds >= 300 and round_num != 0x0b00:
            log.success(f'Early stopping at round {round_num + 1} with stable guess: {new_message}')
            io.sendlineafter(b'c: ', b'a')
            break

        print(f'Round {round_num + 1}/{0x0b01}, Count: {cnt_rounds}, current best guess: {new_message}', end='\r')

    log.success(f'Final guess: {new_message}')
    io.sendlineafter(b'Message: ', new_message.encode())

    io.interactive()

