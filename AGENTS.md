# Publishing class animation packs

Use [Dragon Rider's index](Dragon-Rider/class-animations.json) as the version 1 example. The repository README covers import for all classes. Put class-specific names, credits, dimensions, and the download link in the class README.

The [Dragon Rider exporter](tools/export_dragon_rider.py) generates numbered PNGs, timed ZIPs, the index, and the class download in one pass. Run it with Python and Pillow. Its inputs are the production art directory, retail catalog JSON, class-route CSV, and donor class. Pass the public class folder containing its README as `--class-dir` and the archive path as `--download`. For a new class, supply its own action and equipment recipe.

## Generate the index with the tracks

Emit `class-animations.json` at the class root from the same phase definitions, export paths, equipment assignments, and timing used to write the tracks. Use `format: "lordly-class-animations"`, `version: 1`, and a `sequences` array. The importer obtains the destination class from the user's editor selection. Keep the index independent of a class ID, descriptor, or installation path.

- Emit one entry per authored action, side, and mode. Set exactly one of `motion` (retail pose selector) or `attack` (gameplay action ID). Confirm attacks against the intended choreography and the class/action route. Folder numbers can identify donor poses. Resolve uncertain assignments before publishing.
- Use `side: "player"` for `Player_Left` and `side: "enemy"` for `Enemy_Right`. On attacks only, set `blocked: true` for a separately authored blocked version. Omit it or use false for normal playback. Give entry and recovery independent timelines. Set `loop` explicitly.
- Set `body` to the weapon-free body ZIP. Each `weapons` entry has a `path` and numeric retail `items`. Resolve every item sharing an equipment appearance slot to the same drawing. Keep item assignments disjoint within an entry. Use class-relative paths with forward slashes.
- Set `behind` explicitly. For false, draw the weapon over the body and remove pixels occluded by the posed body, hand, or mount. Use true when the whole equipment track draws behind the body. Preserve the grip in the body track.
- Retain numbered sequence folders, loose transparent PNGs, and each track's `Timed.zip`. Keep `lordly-frame-sequence` version 1 and exact 60 Hz holds in each ZIP. All tracks for an entry share the canvas, anchor, frame order, and holds. Preserve an occurrence when any layer changes, even if the body repeats.

## Native-resolution WebM previews

Place `Player_Left.webm` and `Enemy_Right.webm` directly in every numbered animation folder and include both in the downloadable class ZIP. Each video shows its own combat camera with the registered body and default equipment composited in game order. Use the track's native canvas, one complete playback, and one frame per 60 Hz tick, including held frames. Decode the archived videos and verify dimensions, frame count, timestamps and pose order against the timed tracks.

## Validate and distribute

Resolve every index path from the class folder. Check the ZIP members and manifest, decode every numbered PNG, and compare the loose and archived images and frame holds against the source. Verify both views, unique action/side/mode assignments, loop flags, item IDs and appearance slots. Composite every weapon in both views during Idle, an attack, and Death when available. Inspect grip, occlusion and registration.

Publish one downloadable ZIP per class with the class folder as its only top-level directory. Check that the extracted index resolves with the original workspace unavailable. Keep authoring scenes, private paths, retail command dumps, and full-size working renders outside the public pack.
