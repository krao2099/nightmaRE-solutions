from pwn import *
elf = ELF("svc")
print(f"plt addr for puts {hex(elf.symbols['plt.puts'])}")
print(f"got addr for puts {hex(elf.symbols['got.puts'])}")

# objdump -d -j .plt svc
