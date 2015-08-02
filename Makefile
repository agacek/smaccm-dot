.PHONY: all
all:
	./simplify.py >output.dot
	dot output.dot -Tpdf -ooutput.pdf
	xdg-open output.pdf
