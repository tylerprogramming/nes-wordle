#!/usr/bin/env python3
"""Headlessly run a .nes ROM for N frames and save a PNG. No window needed.
Usage: python3 tools/render.py build/wordle.nes build/render.png [frames]
"""
import sys
from PIL import Image
from nes_py import NESEnv

rom = sys.argv[1] if len(sys.argv) > 1 else "build/wordle.nes"
out = sys.argv[2] if len(sys.argv) > 2 else "build/render.png"
frames = int(sys.argv[3]) if len(sys.argv) > 3 else 60

env = NESEnv(rom)
screen = env.reset()
for _ in range(frames):
    result = env.step(0)          # action 0 = no buttons pressed
    screen = result[0]
img = Image.fromarray(screen[:, :, :3])
img.save(out)
env.close()

# Quick summary so we can reason about it from the terminal.
colors = sorted(img.convert("RGB").getcolors(maxcolors=100000), reverse=True)
print(f"Saved {out}  ({img.size[0]}x{img.size[1]}), {len(colors)} distinct colors")
print("Top colors:", colors[:5])
