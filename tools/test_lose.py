#!/usr/bin/env python3
"""Submit 6 valid guesses that are NOT the answer -> should show YOU LOSE."""
import sys
from PIL import Image
from nes_py import NESEnv

ANSWER_ADDR = 0x2A
UP, A, START, LEFT = 0x10, 0x01, 0x08, 0x40
CANDIDATES = ["TABLE", "EARTH", "MUSIC", "RIVER", "GHOST", "PLANT", "SNAKE", "BREAD"]

env = NESEnv(sys.argv[1]); env.reset()
out = sys.argv[2]
last = [None]

def tap(action, press=4, release=8):
    for _ in range(press): last[0] = env.step(action)[0]
    for _ in range(release): last[0] = env.step(0)[0]

def wait(n):
    for _ in range(n): last[0] = env.step(0)[0]

def type_word(word, submit=True):
    for i, ch in enumerate(word):
        for _ in range(ord(ch) - ord('A')):
            tap(UP)
        if i < 4:
            tap(A)
    if submit:
        tap(START)
    wait(6)

wait(40)
tap(LEFT)                       # seed the answer
wait(5)
answer = "".join(chr(ord('A') + int(env.ram[ANSWER_ADDR + i])) for i in range(5))
print("answer:", answer)
guesses = [w for w in CANDIDATES if w != answer][:6]
print("guessing:", guesses)
for w in guesses:
    type_word(w)
wait(20)

Image.fromarray(last[0][:, :, :3]).save(out)
env.close()
print("submitted 6 guesses ->", out)
