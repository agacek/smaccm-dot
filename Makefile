.PHONY: all
all:
	./simplify.py >output.dot
	dot output.dot -Tpdf -ooutput.pdf
	cat output.dot
	xdg-open output.pdf
