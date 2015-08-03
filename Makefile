.PHONY: all
all:
	./simplify.py >arch.dot
	dot arch.dot -Tpdf -oarch.pdf
	cat arch.dot
	xdg-open arch.pdf

.PHONY: clean
clean:
	rm -f arch.dot arch.pdf
