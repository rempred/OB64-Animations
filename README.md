# OB64 Animations

Mounted Flarebrass combat sprites for the Lordly Caliber editor. Each of the 17 sequence folders starts with its selector number. Entry and recovery are separate selections, including Sleep (34) and Wake up (35).

## Import a sequence

1. Choose a sequence under `Flarebrass`, then `Player_Left` or `Enemy_Right`.
2. Open `Body` for the mounted rider and dragon. For equipment artwork, open the matching `Leaf_Spear`, `Bronze_Partisan`, or `Tide_Trident` folder.
3. Import the numbered PNGs together to set your own frame durations. Set the anchor to **(50, 75)** from the top left of the **104 × 96** canvas. To load the supplied frame order, timing, and anchor together, import that folder's **Timed.zip** instead.

The editor converts the supplied 60 Hz schedule to 30 Hz preview steps and may merge adjacent identical images. Check odd-length holds on the timeline if exact game timing matters. Use the same timing and anchor for the body and its equipment. The chosen spear draws over the body. Whole-animation replacement flattens the imported artwork, so interchangeable equipment needs a separate equipment layer in the destination unit.

## Art credits

The dragon and rider were rendered from Fiery Dragon King and Dragonwing Adventurer models created with Meshy. The mounted gait adapts the T-Rex run from Quaternius's [Animated LowPoly Dinosaurs](https://quaternius.itch.io/animated-lowpoly-dinosaurs) (CC0).
