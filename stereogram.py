#!/usr/bin/env python3
"""
ASCII Stereogram Generator
Creates Magic Eye style 3D images using text characters.
Words and numbers you type will appear to float in 3D!
"""

import random
import sys

# ─── 5×7 Bitmap Font ───────────────────────────────────────────────────────────
# Each entry: 7 strings of 5 chars, '1' = pixel on, '0' = pixel off
FONT = {
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10011","10001","10001","01110"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10001","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01110","10001","10000","01110","00001","10001","01110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10001","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","10000","11110","00001","00001","11110"],
    '6': ["01110","10000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
    '?': ["01110","10001","00001","00010","00100","00000","00100"],
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    ',': ["00000","00000","00000","00000","00110","00100","01000"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '*': ["00000","10101","01110","11111","01110","10101","00000"],
    '#': ["01010","01010","11111","01010","11111","01010","01010"],
    '@': ["01110","10001","10101","10111","10100","10001","01110"],
    '"': ["01010","01010","00000","00000","00000","00000","00000"],
    "'": ["00100","00100","00000","00000","00000","00000","00000"],
    '/': ["00001","00001","00010","00100","01000","10000","10000"],
    '\\':["10000","10000","01000","00100","00010","00001","00001"],
    '[': ["01110","01000","01000","01000","01000","01000","01110"],
    ']': ["01110","00010","00010","00010","00010","00010","01110"],
    '{': ["00110","01000","01000","11000","01000","01000","00110"],
    '}': ["11000","00100","00100","00110","00100","00100","11000"],
    '_': ["00000","00000","00000","00000","00000","00000","11111"],
    '`': ["01000","00100","00000","00000","00000","00000","00000"],
    '~': ["00000","00000","01101","10010","00000","00000","00000"],
    '<': ["00001","00010","00100","01000","00100","00010","00001"],
    '>': ["10000","01000","00100","00010","00100","01000","10000"],
    ';': ["00000","00110","00110","00000","00110","00100","01000"],
    ':': ["00000","00110","00110","00000","00110","00110","00000"],
    '|': ["00100","00100","00100","00100","00100","00100","00100"],
    '^': ["00100","01010","10001","00000","00000","00000","00000"],
    '%': ["11001","11010","00100","01000","01011","10011","00000"],
    '$': ["00100","01111","10100","01110","00101","11110","00100"],
    '&': ["01100","10010","10100","01100","10101","10010","01101"],
}

TEXTURE = (
    "!@#$%&*+-~`|:;<>,.?"
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


def render_text_to_depthmap(text, width, height):
    """Render text into a binary depth map. 1 = elevated (the 3D shape)."""
    text = text.upper()
    chars = [c for c in text if c in FONT]
    if not chars:
        print("  (no supported characters found, using HELLO)")
        chars = list("HELLO")

    GLYPH_W, GLYPH_H, GAP = 5, 7, 1

    n = len(chars)
    text_base_w = n * GLYPH_W + (n - 1) * GAP

    # Scale to fill as much of the grid as possible
    available_w = width - 4
    available_h = height - 4

    scale_w = available_w // text_base_w if text_base_w > 0 else 1
    scale_h = available_h // GLYPH_H
    scale = max(1, min(scale_w, scale_h))

    glyph_w  = GLYPH_W * scale
    glyph_h  = GLYPH_H * scale
    gap_w    = GAP * scale

    text_pixel_w = n * glyph_w + (n - 1) * gap_w
    start_x = (width  - text_pixel_w) // 2
    start_y = (height - glyph_h)      // 2

    depth = [[0] * width for _ in range(height)]

    for ci, ch in enumerate(chars):
        glyph  = FONT[ch]
        char_x = start_x + ci * (glyph_w + gap_w)
        for row_i, row_str in enumerate(glyph):
            for col_i, bit in enumerate(row_str):
                if bit == '1':
                    for sy in range(scale):
                        for sx in range(scale):
                            px = char_x + col_i * scale + sx
                            py = start_y + row_i * scale + sy
                            if 0 <= px < width and 0 <= py < height:
                                depth[py][px] = 1

    return depth


def generate_stereogram(depth_map, width, height):
    """Generate ASCII stereogram rows from a depth map."""
    period    = max(8, width // 6)   # ~1/6 of width works well
    max_shift = max(1, period // 6)  # subtle shift keeps it readable

    lines = []
    for y in range(height):
        row = [''] * width

        # Seed first period columns with random texture
        for x in range(period):
            row[x] = random.choice(TEXTURE)

        # Each subsequent column copies back by `period`, shifted by depth
        for x in range(period, width):
            shift = depth_map[y][x] * max_shift
            src   = max(0, x - period + shift)
            row[x] = row[src]

        lines.append(''.join(row))

    return lines, period, max_shift


def ask_int(prompt, default, lo, hi):
    """Prompt for an integer with a default and range."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
            print(f"  Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Please enter a whole number.")


def viewing_instructions():
    print("""
HOW TO VIEW:
  Parallel (look "through" the screen) — text floats IN FRONT
    • Relax eyes as if staring far behind the screen (~40 cm away)
    • The random noise will "lock" and the text pops out in 3D

  Cross-eyed (easier for some) — text sinks behind the surface
    • Cross your eyes very slightly
    • Give it 10–30 seconds; start at the left edge
""")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║      ASCII STEREOGRAM GENERATOR          ║")
    print("║  Type words/numbers — see them in 3D!   ║")
    print("╚══════════════════════════════════════════╝")
    print(f"  Supported: A-Z  0-9  and most printable ASCII symbols")
    print()

    # Grid size
    width  = ask_int("Grid width  (columns)", 80, 20, 200)
    height = ask_int("Grid height (rows)",    40, 10, 200)
    print()

    while True:
        try:
            text = input("Enter text (or 'q' to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not text:
            continue
        if text.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            return

        depth_map = render_text_to_depthmap(text, width, height)
        lines, period, shift = generate_stereogram(depth_map, width, height)

        print(f"\n  Generating {width}×{height} stereogram "
              f"(period={period}, depth-shift={shift}) for: {text!r}\n")
        print("┌" + "─" * width + "┐")
        for line in lines:
            print("│" + line + "│")
        print("└" + "─" * width + "┘")
        viewing_instructions()


if __name__ == "__main__":
    main()
