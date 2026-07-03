#!/usr/bin/env python3
"""Win a game, then press Right to restart, and capture the fresh board."""
import sys
from PIL import Image
from nes_py import NESEnv

ANSWER_ADDR = 0x2A
UP, A, START, RIGHT, LEFT = 0x10, 0x01, 0x08, 0x80, 0x40
env = NESEnv(sys.argv[1]); env.reset()
out = sys.argv[2]
last = [None]

def tap(action, press=4, release=8):
    for _ in range(press): last[0] = env.step(action)[0]
    for _ in range(release): last[0] = env.step(0)[0]
def wait(n):
    for _ in range(n): last[0] = env.step(0)[0]

wait(40)
tap(LEFT)                              # seed
wait(5)
answer = [int(env.ram[ANSWER_ADDR + i]) for i in range(5)]
print("first answer:", "".join(chr(65 + a) for a in answer))
for i, a in enumerate(answer):
    for _ in range(a): tap(UP)
    if i < 4: tap(A)
tap(START)                              # win
wait(15)
tap(RIGHT)                              # restart
wait(15)
new_answer = "".join(chr(65 + int(env.ram[ANSWER_ADDR + i])) for i in range(5))
print("after-restart answer (changes on first press of new game):", new_answer)

Image.fromarray(last[0][:, :, :3]).save(out)
env.close()
print("saved", out)
