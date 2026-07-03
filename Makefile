# NES Wordle build
# Usage:
#   make        -> build build/hello.nes
#   make run    -> build and launch in FCEUX
#   make clean  -> remove build artifacts

ROM   = build/wordle.nes
SRC   = src/wordle.s
CFG   = src/nrom.cfg
CHR   = build/wordle.chr
WORDS = build/words.bin
ANSW  = build/answers.bin
WINC  = src/words_gen.inc
FCEUX = /usr/local/bin/fceux

all: $(ROM)

$(CHR): tools/make_chr.py
	python3 tools/make_chr.py

$(WORDS) $(ANSW) $(WINC): tools/make_words.py
	python3 tools/make_words.py

$(ROM): $(SRC) $(CFG) $(CHR) $(WORDS) $(ANSW) $(WINC)
	ca65 $(SRC) -o build/wordle.o
	ld65 -C $(CFG) build/wordle.o -o $(ROM)
	@echo "Built $(ROM)"

run: $(ROM)
	$(FCEUX) $(ROM)

clean:
	rm -f build/*.o build/*.nes $(CHR)

.PHONY: all run clean
