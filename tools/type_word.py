#!/usr/bin/env python3
"""Type a 5-letter word into the Wordle ROM and optionally submit it.
Usage: python3 tools/type_word.py build/wordle.nes build/out.png MARIO [submit]
Each box starts at 'A'; we press Up (index) times then A to advance.
"""
import sys
from PIL import Image
from nes_py import NESEnv

rom, out, word = sys.argv[1], sys.argv[2], sys.argv[3].upper()
submit = len(sys.argv) > 4 and sys.argv[4] == "submit"

UP, A, START = 0x10, 0x01, 0x08
env = NESEnv(rom); env.reset()
last = [None]

def tap(action, press=4, release=8):
    for _ in range(press):
        last[0] = env.step(action)[0]
    for _ in range(release):
        last[0] = env.step(0)[0]

def wait(n=20):
    for _ in range(n):
        last[0] = env.step(0)[0]

wait(30)
tap(START)                                # leave the title screen
wait(10)
for i, ch in enumerate(word):
    for _ in range(ord(ch) - ord('A')):   # cycle A -> target letter
        tap(UP)
    if i < 4:                             # advance to next box (not after last)
        tap(A)
if submit:
    tap(START)
wait(20)

Image.fromarray(last[0][:, :, :3]).save(out)
env.close()
print(f"typed {word}{' + submit' if submit else ''} -> {out}")
