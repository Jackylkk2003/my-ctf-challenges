# Simple pwn template

from pwn import *

gdbscripts = "handle SIGALRM ignore\n"           # You can also add breakpoints here

# Update the following variables to match your target binary and remote server
exe = './dice'
remote_url = 'HOST'
port = 0

context.terminal = ["tmux", "splitw", "-h"]      # If you are using tmux, if not, then comment this out
context.log_level = 'debug'                      # Print more information
context.binary = exe                             # Load binary information
elf = ELF(exe)                                   # Load ELF

# with process(exe) as io:                       # Local run
#     io.interactive()

# with remote(remote_url, port) as io:           # Remote run
#     io.interactive()

# with gdb.debug(exe, gdbscripts) as io:         # Debugging run (run with gdb)
#     io.interactive()
