# OB64 Animations

Combat sprite packs for the Lordly Caliber editor are organized by class. Choose the destination class in the editor. A pack can supply artwork for a new class or an existing one.

## Import a class pack

Choose your class ZIP from [downloads](downloads/) and extract it. The optional `class-animations.json` sits beside the numbered sequence folders. It describes the action, side, body track, equipment mappings, and playback flags for a class-pack importer. Keep the extracted folders together so the relative paths resolve.

## Preview an animation

In the Ronin pack, open `Player_Left.webm` or `Enemy_Right.webm` directly inside any numbered animation folder. Each video shows the body and katana together at 112 × 104 and 60 frames per second. One video frame equals one game tick. Enable repeat in your player to inspect a walk cycle.

## Import one track by hand

1. Open the desired sequence, choose `Player_Left` or `Enemy_Right`, then choose the body or one equipment track.
2. Import that track's `Timed.zip` to load its frames, durations, and anchor. To set durations yourself, select its numbered PNGs together and use the anchor in the class notes.
3. Use matching anchors and timing for the body and equipment. The supplied frame ZIPs store exact 60 Hz holds. The editor's individual-image import path can round holds to 30 Hz preview steps and merge adjacent identical images.

Sequence folder numbers identify donor pose selectors. The class index uses gameplay action IDs for attacks. Pack authors can follow the [class-pack conventions](AGENTS.md).

## Editable Blender scenes

| Class | Source |
| --- | --- |
| Ronin | [Ronin r05](Blender-Sources/Ronin/Ironclad-Ronin-r05.blend) includes the alternating walk, corrected lead-hand grip, and both armor palettes. |
| Crone | [Crone r05](Blender-Sources/Crone/Griselda-Crone-r05.blend) includes the silver hair and revised shoulder cloak. |
| Dragon Rider | [Eleven action scenes](Blender-Sources/Dragon-Rider/) cover the 17 published sequences. |

The scenes are stored with Git LFS. After cloning with Git LFS installed, run `git lfs pull` from the repository root to download them. The class ZIPs in [downloads](downloads/) contain the editor import assets.
