# Sprite Guide

This is a simple sprite guide to build a sprite for Pymodoro. The default "tomato" sprite is built using the **aseprite** software. You are free to modify and redistribute this sprite, but remind to put credits to "Blendify Games" and link to the original repository on [Github](https://github.com/Blendify-Games/Pymodoro).

The sprite consists of two files. One of them is the image containing the frames of the animation. The sprite image sheet can be "unique row", or "multiple rows", format. The frame index count begin as 0 at topleft to N at bottomright. The other file is a JSON containing the description of a simple Finite State Machine for the animation. Both JSON and sheet must have the same name.

## JSON Setup

The JSON describe how the sprite animations will work.

### A JSON Example:

This is an example of JSON use for the tomato animation.

```json
{
    "name": "tomato",
    "frame_size": [32, 32],
    "boing": {
        "frames": [0, 1],
        "delta": [500, 500],
        "repeat": [3, 10],
        "next_state": "idle"
    },
    "blink": {
        "frames": [2, 0],
        "delta": [250, 3000],
        "repeat": 2,
        "next_state": "boing"
    }
}
```

### Key and description relation:

| Keys                                  | Description                                                                                                            |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------|
|**name**                               | a string that identifies the sprite                                                                                    |
| **frame_size**                        | a two-value list containing the sprite frame size (width x height)                                                     |
| ***animation key***                   | a JSON containing at least "frames", "delta" and "repeat" keys. The "next_state" isn't mandatory.                      |
| ***animation key* &rarr; frames**     | a list containing the frame index sequence to play on animation accordingly to the sheet orientation.                  |
| ***animation key* &rarr; delta**      | a list containing each frame time following the "frames" sequence. "delta"s lenght must be equal to "frame"s.          |
| ***animation key* &rarr; repeat**     | an integer or a two-value list. This represents how much this anim state must loop itself. If the value is < 0 it will loop forever. If the value is a list containing two values, this determine a range of random integer values possible to repeat the animation.                    |
| ***animation key* &rarr; next_state** | a string with a corresponding ***animation key*** to jump when the animation repetitions end.                          |