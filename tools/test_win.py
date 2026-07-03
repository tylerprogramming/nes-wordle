#!/usr/bin/env python3
"""Read the randomly-chosen answer from RAM, type it, and submit -> should win.
Verifies the answer/RNG/validation/win path end to end."""
import sys
from PIL import Image
from nes_py import NESEnv

ANSWER_ADDR = 0x2A
UP, A, START, LEFT = 0x10, 0x01, 0x08, 0x40

env = NESEnv(sys.argv[1]); env.reset()
out = sys.argv[2]
last = [None]

def tap(action, press=4, release=8):
    for _ in range(press): last[0] = env.step(action)[0]
    for _ in range(release): last[0] = env.step(0)[0]

def wait(n):
    for _ in range(n): last[0] = env.step(0)[0]

wait(40)
tap(LEFT)                       # no-op press: seeds the answer without typing
wait(5)
answer = [int(env.ram[ANSWER_ADDR + i]) for i in range(5)]
word = "".join(chr(ord('A') + a) for a in answer)
print("answer chosen by RNG:", word)

for i, a in enumerate(answer):
    for _ in range(a):          # cycle A -> target letter
        tap(UP)
    if i < 4:
        tap(A)
tap(START)
wait(20)

Image.fromarray(last[0][:, :, :3]).save(out)
env.close()
print("typed the answer + submit ->", out)
