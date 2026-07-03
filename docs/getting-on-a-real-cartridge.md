# Getting NES Wordle onto a Real Cartridge

This game is **NROM / mapper 0** (32KB PRG + 8KB CHR, a 40,976-byte `.nes`) —
the simplest, most cartridge-friendly config there is. No mapper chip, **no bus
conflicts** ([NESdev NROM](https://www.nesdev.org/wiki/NROM)). Every path below
works cleanly for it.

## Verify first (do this before spending money)
1. **Emulator** — confirm it runs in [Mesen](https://www.mesen.ca/) (cycle-accurate).
   Double-check the **mirroring bit** in the iNES header — wrong mirroring is the
   #1 NROM homebrew bug and only shows on hardware.
2. **Flash cart on real hardware** — run the exact `.nes` on an EverDrive to prove
   it works on a genuine NES before burning any chips.

## Path A — Fast: flash cartridge
- **EverDrive-N8 Pro** (Krikzz) ~$205, or the standard **EverDrive-N8** ~$110–130.
  Copy the `.nes` to a microSD, pick it from an on-screen menu, play.
- Includes a **CIC clone**, so it boots on a stock front-loader NES, NTSC or PAL.
- Buy from [Krikzz](https://krikzz.com/) or [Stone Age Gamer](https://stoneagegamer.com/) (avoid clones).
- Great for the instant "it runs on a real NES" reveal; not a "build."

## Path B — Authentic: build a dedicated cartridge
**Shopping list**
- EPROM programmer: **XGecu TL866II Plus** (~$50) or **T48** (~$65). *(Avoid the old TL866CS.)*
- **27C256** EPROM for PRG (32KB, exact fit) + **27C64** for CHR (8KB, exact fit).
  Or rewritable **SST 39SF010** flash. (~$2–8 total.)
- Either a **common NROM donor cart** (Donkey Kong, Duck Hunt, Excitebike, Ice
  Climber, Mario Bros., Gyromite…) **or** a blank repro NROM PCB
  ([Mouse Bite Labs](https://mousebitelabs.com/2017/06/25/how-to-make-an-nes-reproduction-cartridge/),
  [game-tech ReproX](https://www.game-tech.us/product/reprox/), Muramasa, AliExpress).
- **3.8mm security bit**, soldering/desoldering gear, repro shell + printable label.

**Steps**
1. Split the `.nes` into `PRG.bin` (32KB) + `CHR.bin` (8KB) with **FamiROM** or
   **ReadNES3** (strips the 16-byte header). Pad to chip size if needed.
2. Burn `PRG.bin` → 27C256 and `CHR.bin` → 27C64 with the TL866II/T48.
3. Drop the chips into a repro board, **or** desolder the donor's two mask ROMs
   and socket the EPROMs in. Set the mirroring jumper to match the header.
4. Handle the **CIC lockout** (see below).
5. Reshell, apply a printed label, boot it.

Cost ~$70–120 incl. the reusable programmer; moderate difficulty (soldering + burning).

## The CIC lockout gotcha (important)
A front-loader NES has a **10NES lockout chip**. A repro board with **no CIC** will
make it blink the red light and refuse to boot. Fixes
([ConsoleMods](https://consolemods.org/wiki/NES:Disabling_CIC_Chip)):
- **Use a donor cart** — it already has a working CIC, so your cart boots on a stock
  NES with **zero console mods**. ← best for a video.
- Add a **CIC clone chip** to a repro board.
- **Disable the console lockout**: cut pin 4 of the 10NES chip and tie it to ground
  (also makes it region-free).
- **Use a top-loader NES (NES-101)** — it has no lockout chip at all.

## Path C — Turnkey (someone builds it for you)
- **Broke Studio / [Homebrew Factory](https://www.homebrew-factory.com/)** — configurator + pre-order runs, ~€39–60/cart.
- **[Mega Cat Studios](https://megacatstudios.com/)**, **RetroUSB**, **Infinite NES Lives** — homebrew cart production.

## Recommended arc for the YouTube video
1. Verify in **Mesen** → run on an **EverDrive** (early "real hardware" beat, de-risks everything).
2. **Build the real cartridge**: burn a **27C256 + 27C64** on a **TL866II Plus**, drop
   them into a **gutted Donkey Kong / Duck Hunt donor** (its CIC makes it boot on a
   stock front-loader — no console surgery on camera), reshell, print a label, film the
   first boot. That's the money shot.
3. Mention **Broke Studio / Homebrew Factory** as the "how you'd sell these" outro.
