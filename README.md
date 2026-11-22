# OB64 Animations

Combat sprite packs for the Lordly Caliber editor are organized by class. Choose the destination class in the editor. A pack can supply artwork for a new class or an existing one.

## Import a class pack

Choose your class ZIP from [downloads](downloads/) and extract it. The optional `class-animations.json` sits beside the numbered sequence folders. It describes the action, side, body track, equipment mappings, and playback flags for a class-pack importer. Keep the extracted folders together so the relative paths resolve.

## Import one track by hand

1. Open the desired sequence, choose `Player_Left` or `Enemy_Right`, then choose the body or one equipment track.
2. Import that track's `Timed.zip` to load its frames, durations, and anchor. To set durations yourself, select its numbered PNGs together and use the anchor in the class notes.
3. Use matching anchors and timing for the body and equipment. The supplied frame ZIPs store exact 60 Hz holds. The editor's individual-image import path can round holds to 30 Hz preview steps and merge adjacent identical images.

Sequence folder numbers identify donor pose selectors. The class index uses gameplay action IDs for attacks. Pack authors can follow the [class-pack conventions](AGENTS.md).
