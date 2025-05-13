ctf-run:
	docker build -t betstar_ctf -f dockerfile .
	docker run -d --rm --name betstar_ctf -p 5000:5000 betstar_ctf

ctf-debug:
	docker build -t betstar_debug -f dockerfile.debug .
	docker run -d --rm --name betstar_debug -p 5000:5000 betstar_debug

kill-ctf:
	docker kill betstar_ctf

kill-debug:
	docker kill betstar_debug
