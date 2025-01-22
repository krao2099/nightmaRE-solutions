from pwn import *
p = process('./just_do_it')
p.sendline(b'P@SSW0RD\x00')
print(p.recvall())

