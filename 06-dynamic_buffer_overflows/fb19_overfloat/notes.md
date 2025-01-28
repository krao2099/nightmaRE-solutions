`docker build -t overfloat_netcat . && docker run --rm -p 12345:12345 overfloat_netcat`

`docker build -f dockerfile.debug -t gdb-overfloat . && docker run -it --rm gdb-overfloat`

64 bit dynamically linked not stripped
partial relro, no canary, NX, no pie

Need to get past chart_course to get to ret

Can write done after a lat long paur