#!/usr/bin/env python3
"""
Generate an 8KB NES CHR-ROM containing an 8x8 font.
Each glyph is placed at the tile index equal to its ASCII code, so in
assembly you can write  .byte "HELLO"  and the right tiles appear.

NES tile format: 16 bytes per tile = 8 bytes (bit plane 0) + 8 bytes (plane 1).
We use a 2-color font, so plane 1 is left as zeros (color index 1 = "on").
"""

# Each glyph: 8 rows of 8 chars. '#' = pixel on, anything else = off.
GLYPHS = {
    'A': ["..###...",".#...#..","#.....#.","#.....#.","#######.","#.....#.","#.....#.","........"],
    'B': ["######..","#.....#.","#.....#.","######..","#.....#.","#.....#.","######..","........"],
    'C': [".#####..","#.....#.","#.......","#.......","#.......","#.....#.",".#####..","........"],
    'D': ["#####...","#....#..","#.....#.","#.....#.","#.....#.","#....#..","#####...","........"],
    'E': ["#######.","#.......","#.......","#####...","#.......","#.......","#######.","........"],
    'F': ["#######.","#.......","#.......","#####...","#.......","#.......","#.......","........"],
    'G': [".#####..","#.....#.","#.......","#..####.","#.....#.","#.....#.",".#####..","........"],
    'H': ["#.....#.","#.....#.","#.....#.","#######.","#.....#.","#.....#.","#.....#.","........"],
    'I': [".#####..","...#....","...#....","...#....","...#....","...#....",".#####..","........"],
    'J': ["..#####.","....#...","....#...","....#...","#...#...","#...#...",".###....","........"],
    'K': ["#....#..","#...#...","#..#....","###.....","#..#....","#...#...","#....#..","........"],
    'L': ["#.......","#.......","#.......","#.......","#.......","#.......","#######.","........"],
    'M': ["#.....#.","##...##.","#.#.#.#.","#..#..#.","#.....#.","#.....#.","#.....#.","........"],
    'N': ["#.....#.","##....#.","#.#...#.","#..#..#.","#...#.#.","#....##.","#.....#.","........"],
    'O': [".#####..","#.....#.","#.....#.","#.....#.","#.....#.","#.....#.",".#####..","........"],
    'P': ["######..","#.....#.","#.....#.","######..","#.......","#.......","#.......","........"],
    'Q': [".#####..","#.....#.","#.....#.","#.....#.","#...#.#.","#....#..",".####.#.","........"],
    'R': ["######..","#.....#.","#.....#.","######..","#..#....","#...#...","#....#..","........"],
    'S': [".#####..","#.....#.","#.......",".#####..","......#.","#.....#.",".#####..","........"],
    'T': ["#######.","...#....","...#....","...#....","...#....","...#....","...#....","........"],
    'U': ["#.....#.","#.....#.","#.....#.","#.....#.","#.....#.","#.....#.",".#####..","........"],
    'V': ["#.....#.","#.....#.","#.....#.",".#...#..",".#...#..","..#.#...","...#....","........"],
    'W': ["#.....#.","#.....#.","#.....#.","#..#..#.","#.#.#.#.","##...##.","#.....#.","........"],
    'X': ["#.....#.",".#...#..","..#.#...","...#....","..#.#...",".#...#..","#.....#.","........"],
    'Y': ["#.....#.",".#...#..","..#.#...","...#....","...#....","...#....","...#....","........"],
    'Z': ["#######.","......#.",".....#..","...##...","..#.....",".#......","#######.","........"],
    '?': [".#####..","#.....#.","......#.","...###..","...#....","........","...#....","........"],
    '!': ["...#....","...#....","...#....","...#....","...#....","........","...#....","........"],
    '0': [".#####..","#.....#.","#....##.","#.#..#..","##...#..","#.....#.",".#####..","........"],
    '1': ["...#....","..##....","...#....","...#....","...#....","...#....",".#####..","........"],
    '2': [".#####..","#.....#.","......#.","...###..",".##.....","#.......","#######.","........"],
    '3': ["#######.","....#...","...#....","..###...","......#.","#.....#.",".#####..","........"],
    '4': ["....##..","...#.#..","..#..#..",".#...#..","#######.",".....#..",".....#..","........"],
    '5': ["#######.","#.......","######..","......#.","......#.","#.....#.",".#####..","........"],
    '6': [".#####..","#.......","#.......","######..","#.....#.","#.....#.",".#####..","........"],
    '7': ["#######.","......#.",".....#..","....#...","...#....","..#.....","..#.....","........"],
    '8': [".#####..","#.....#.","#.....#.",".#####..","#.....#.","#.....#.",".#####..","........"],
    '9': [".#####..","#.....#.","#.....#.",".######.","......#.","......#.",".#####..","........"],
}

def glyph_to_tile(rows):
    """Return 16 bytes for one tile from 8 rows of '#'/'.' text."""
    plane0 = []
    for r in rows:
        byte = 0
        for x in range(8):
            if x < len(r) and r[x] == '#':
                byte |= (1 << (7 - x))
        plane0.append(byte)
    # Put the glyph in BOTH bit planes so its pixels are color index 3,
    # which we keep white in every palette (title text, box outlines).
    return bytes(plane0 + plane0)

def main():
    chr_rom = bytearray(8192)  # 8KB = pattern table 0 (4KB) + table 1 (4KB)
    # Tile $DB: a solid filled 8x8 block (used later for Wordle color squares)
    solid = bytes([0xFF] * 8 + [0x00] * 8)
    chr_rom[0xDB * 16 : 0xDB * 16 + 16] = solid

    # Box-outline corner tiles ($5B-$5E). Four tile together into one hollow
    # 16x16 empty cell:   5B 5C
    #                     5D 5E
    def tile_from_plane0(plane0):
        return bytes(list(plane0) + list(plane0))   # color index 3 (white)
    box_tiles = {
        0x5B: [0xFF, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80],  # top-left
        0x5C: [0xFF, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],  # top-right
        0x5D: [0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0xFF],  # bottom-left
        0x5E: [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0xFF],  # bottom-right
    }
    for idx, plane0 in box_tiles.items():
        chr_rom[idx * 16 : idx * 16 + 16] = tile_from_plane0(plane0)

    # Big 16x16 letters A-Z, made by scaling each 8x8 glyph 2x and splitting
    # into four tiles. Letter L lives at tiles $60+L*4 .. +3 (TL,TR,BL,BR),
    # so a filled cell shows a large, readable letter.
    def big_letter_tiles(rows):
        big = [[0] * 16 for _ in range(16)]
        for y in range(16):
            src = rows[y // 2]
            for x in range(16):
                sx = x // 2
                big[y][x] = 1 if (sx < len(src) and src[sx] == '#') else 0
        def quad(oy, ox):
            # Filled cell: every pixel is color 1 (the "fill"), and the letter
            # pixels are color 3 (white). Palette 0 -> fill black = white letter
            # on black; palettes 1/2/3 -> fill green/yellow/gray after submit.
            plane0 = [0xFF] * 8          # whole tile filled
            plane1 = []
            for y in range(8):
                b = 0
                for x in range(8):
                    if big[oy + y][ox + x]:
                        b |= (1 << (7 - x))
                plane1.append(b)
            return bytes(plane0 + plane1)
        return quad(0, 0), quad(0, 8), quad(8, 0), quad(8, 8)  # TL, TR, BL, BR

    BIG_BASE = 0x60
    for L in range(26):
        ch = chr(ord('A') + L)
        tl, tr, bl, br = big_letter_tiles(GLYPHS[ch])
        for q, tile in enumerate((tl, tr, bl, br)):
            idx = BIG_BASE + L * 4 + q
            chr_rom[idx * 16 : idx * 16 + 16] = tile

    # Small (8x8) FILLED letters for the on-screen keyboard: whole tile is
    # color 1 (the key background) with the letter glyph in color 3 (white),
    # so a key tints green/yellow/gray via its palette while staying readable.
    SMALL_FILLED_BASE = 0xDC
    for L in range(26):
        rows = GLYPHS[chr(ord('A') + L)]
        plane1 = []
        for r in rows:
            b = 0
            for x in range(8):
                if x < len(r) and r[x] == '#':
                    b |= (1 << (7 - x))
            plane1.append(b)
        idx = SMALL_FILLED_BASE + L
        chr_rom[idx * 16 : idx * 16 + 16] = bytes([0xFF] * 8 + plane1)
    for ch, rows in GLYPHS.items():
        idx = ord(ch)          # tile index == ASCII code
        chr_rom[idx * 16 : idx * 16 + 16] = glyph_to_tile(rows)
    with open("build/wordle.chr", "wb") as f:
        f.write(chr_rom)
    print("Wrote build/wordle.chr (%d bytes)" % len(chr_rom))

if __name__ == "__main__":
    main()
