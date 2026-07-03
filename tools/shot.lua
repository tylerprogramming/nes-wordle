-- Force emulation forward regardless of window focus, then snapshot.
emu.speedmode("turbo")
emu.unpause()
for i = 1, 120 do
  emu.frameadvance()
end
local path = "/Users/tylerreed/ai-nintendo-game/build/shot.png"
gui.savescreenshotas(path)
emu.print("SHOT_SAVED " .. path)
emu.frameadvance()
emu.frameadvance()
emu.exit()
