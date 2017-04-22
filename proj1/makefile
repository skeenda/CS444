LATEX	= latex -shell-escape
BIBTEX	= bibtex
DVIPS	= dvips
DVIPDF  = dvipdft
XDVI	= xdvi -gamma 4
GH		= gv
CC = gcc

EXAMPLES = $(wildcard *.h)
SRC	:= $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
TRG	= $(SRC:%.tex=%.dvi)
PSF	= $(SRC:%.tex=%.ps)
PDF	= $(SRC:%.tex=%.pdf)

pdf: $(PDF)

ps: $(PSF)

$(TRG): %.dvi: %.tex $(EXAMPLES)
	$(LATEX) $<
	$(LATEX) $<
	$(LATEX) $<

$(PSF):%.ps: %.dvi
	$(DVIPS) -R -Poutline -t letter $< -o $@

$(PDF): %.pdf: %.ps
#	$(DVIPDF) -o $@ $<
	ps2pdf $<

homework1: homework1.o
	$(CC) homework1.c -o homework1 -pthread -lpthread -std=c99

homework1.o:
	$(CC) -c  homework1.c $(CFLAGS) 


all: pdf
	 gcc -o hw1 homework1.c -lpthread

clean:
	rm -f *.pdf *.ps *.dvi *.out *.log *.aux *.bbl *.blg *.pyg *.o homework1

.PHONY: all show clean ps pdf showps