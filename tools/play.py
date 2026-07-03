#!/usr/bin/env python3
"""Drive a .nes ROM with a scripted button sequence and save the final frame.
Usage: python3 tools/play.py build/wordle.nes build/out.png u u u a u d b ...
Tokens: a b sel st u d l r  (- = no input / wait)
Each token is pressed ~4 frames then released ~6 frames (so edge-detection sees it).
"""
import sys
from PIL import Image
from nes_py import NESEnv

rom = sys.argv[1]
out = sys.argv[2]
seq = sys.argv[3:]

# nes-py action byte bit order (from nes_env.py): A=0, B=1, select=2,
# start=3, up=4, down=5, left=6, right=7.
BTN = {'a': 0x01, 'b': 0x02, 'sel': 0x04, 'st': 0x08,
       'u': 0x10, 'd': 0x20, 'l': 0x40, 'r': 0x80, '-': 0x00}

env = NESEnv(rom)
env.reset()
last = None

def hold(action, frames):
    global last
    for _ in range(frames):
        last = env.step(action)[0]

hold(0x00, 30)                 # warm up / let init run
hold(0x08, 4)                  # Start -> leave the title screen
hold(0x00, 10)
for tok in seq:
    hold(BTN[tok], 4)          # press
    hold(0x00, 8)              # release (edge detect needs the release)
hold(0x00, 10)

Image.fromarray(last[:, :, :3]).save(out)
env.close()
print("saved", out, "after sequence:", " ".join(seq) if seq else "(none)")
