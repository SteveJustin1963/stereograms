# ASCII Stereogram Generator — How-To Guide

## What Is a Stereogram?

A stereogram (also called a Magic Eye image) hides a 3D shape inside a flat
repeating pattern. Your two eyes see the pattern at slightly different positions;
when you relax your eyes the brain fuses those two views and perceives depth —
the hidden shape appears to float in front of (or behind) the surface.

This tool does the same thing entirely in text characters.

---

## Running the Program

```
python3 stereogram.py
```

Requires Python 3.9 or newer. No third-party packages needed.

---

## Step-by-Step Usage

### 1. Set the grid size

```
Grid width  (columns) [80]: 120
Grid height (rows)    [40]: 60
```

- Press **Enter** to accept the default shown in brackets.
- Width: 20–200 columns. Heights below 20 rows produce very small results.
- Wider grids give the eyes more repeating pattern to lock onto — easier to view.
- Taller grids make the hidden text larger and more impressive.

### 2. Enter your text

```
Enter text (or 'q' to quit): HELLO
Enter text (or 'q' to quit): 2026
Enter text (or 'q' to quit): 42
```

- Supported characters: `A–Z  0–9  ! ? . , - + = ( ) * #`
- Lowercase is accepted and converted to uppercase automatically.
- Unknown characters are silently skipped.
- Short inputs (1–3 chars) are scaled up to fill the grid nicely.
- Long inputs are scaled down to fit.

### 3. Read the output

The stereogram is printed immediately, surrounded by a border:

```
┌────────── ... ──────────┐
│ ... random noise ... │
│ ... noise with hidden depth distortions ... │
│ ... random noise ... │
└────────── ... ──────────┘
```

- Rows **without** depth look like a perfectly repeating tile.
- Rows **with** depth have tiny rhythm breaks — those encode the 3D shape.

### 4. Type another word or press `q` to quit

The grid size stays the same for the whole session. Restart the program to
change it.

---

## How to View the Stereogram

This is the tricky part. Give yourself a quiet moment and 30–60 seconds to
adapt. Most people get it on the second or third try.

### Method 1 — Parallel / Diverge (recommended)

The text will appear to **float in front** of the surface.

1. Hold the screen 30–40 cm from your face.
2. Relax your eyes completely — imagine staring at something far behind the
   screen, like a distant wall.
3. Your focus will go blurry. That is normal and correct.
4. Keep staring softly. After a few seconds the repeating pattern will
   "click" into a stable 3D image and the letters pop out.
5. Once you see it, you can move slightly closer or further without losing it.

### Method 2 — Cross-eyed (easier for some people)

The text will appear to sink **behind** the surface.

1. Hold one finger between your eyes and the screen, about 15 cm from your face.
2. Focus on your fingertip until you see two copies of the screen behind it.
3. Slowly remove your finger while keeping that crossed-eye focus.
4. The two copies will overlap and the depth image will appear.

### Tips for Stubborn Cases

| Problem | Try this |
|---|---|
| Can't get eyes to diverge | Press your nose against the screen, then slowly pull back while keeping eyes relaxed |
| Image keeps snapping back | Blink slowly instead of staring hard |
| Seeing double but no depth | The two copies aren't lined up — shift left or right slightly |
| Text too small to see clearly | Re-run with a larger grid (e.g. 160×80) or enter fewer characters |
| Terminal wraps lines | Make sure your terminal window is at least as wide as the grid |

---

## How It Works (Technical)

### Depth map

Each character you type is rendered using a built-in **5×7 bitmap font**,
scaled up to fill roughly 45% of the grid height and centered. The result is
a 2D grid of 0s (background, far) and 1s (foreground, close).

### Stereogram generation

For each row the algorithm:

1. Fills the first `period` columns with random characters from the texture set.
2. For every subsequent column `x`:
   - Reads the depth value at that position.
   - Copies the character from column `x − period + shift`, where `shift` is
     0 for background and a small positive integer (typically 2) for foreground.

This makes the effective period slightly shorter over the elevated shape.
When your eyes are diverged by exactly `period` columns, background regions
match perfectly but foreground regions appear to come forward because their
period is shorter — that mismatch is depth.

```
period = width ÷ 6      (e.g. 13 for an 80-wide grid)
shift  = period ÷ 6     (e.g. 2)
```

### Texture

The background noise is drawn randomly from printable ASCII characters
(letters, digits, punctuation). More visual variety in the texture makes it
harder for the eye to track individual characters and easier to see the 3D
shape.

---

## Example Sessions

### Large single digit

```
Grid width  (columns) [80]: 80
Grid height (rows)    [40]: 60
Enter text: 7
```

The `7` will be scaled to fill most of the grid — very striking in 3D.

### Short word

```
Grid width  (columns) [80]: 120
Grid height (rows)    [40]: 50
Enter text: HI
```

Two large letters, easy to see once your eyes lock in.

### Year or number

```
Grid width  (columns) [80]: 160
Grid height (rows)    [40]: 40
Enter text: 2026
```

Use a wide grid for longer text so the font can be a reasonable size.

---

## Supported Characters

```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
0 1 2 3 4 5 6 7 8 9
! ? . , - + = ( ) * #
```

Space is supported (produces a gap between words).
