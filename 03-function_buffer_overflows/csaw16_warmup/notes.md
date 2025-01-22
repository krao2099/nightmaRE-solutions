vulnerable call to gets(). Leaks address of easy() func

Need to overwrite 0x48 bytes as per ghidra

Needed to skip extra stack push to maintain stack alignment