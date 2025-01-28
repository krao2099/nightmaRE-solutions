No PIE with canary. 64 bit


`docker build -t svc_netcat .`
`docker run --rm -p 12345:12345 svc_netcat`

buffer is 168 bytes read 248

Need to leak canary

We control input to puts, so if we remove a null terminator it will kepp printing and leak the canary

`docker build -f dockerfile.debug -t gdb-svc .`

`docker run -it --rm gdb-svc`

Find plt and got puts via ghidra or objdump

Print addrs out /bin/sh system and puts via gdb container

