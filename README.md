# OB64 Animations

Combat sprite sequences for the Lordly Caliber editor are organized by class. Open a class folder, choose a numbered animation sequence, then select the camera view and artwork layer you want to import. The number at the start of each sequence folder is its editor selector.

## Import a sequence

- **Use the supplied timing.** Import the layer's `Timed.zip` to load its frames, durations, and anchor together.
- **Set your own timing.** Select the numbered PNGs in the layer folder and import them together. Set the anchor to the coordinates listed in the class notes or in the ZIP's `animation.json`.

Use matching views, anchors, and timing when combining body and equipment layers. Frame holds in the ZIP are measured at 60 Hz. The editor rounds them to 30 Hz preview steps and can merge identical neighboring frames.
