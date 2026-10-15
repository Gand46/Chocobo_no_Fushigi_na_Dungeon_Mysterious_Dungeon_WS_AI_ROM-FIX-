"""Compile QA14's small subtitle from explicit native-grid glyph definitions.

The supplied main wordmark and original masters remain untouched. This is a
title-specific 2bpp font, not a replacement for the game's shared font.
"""
import json
import numpy as np


def render_subtitle(path):
    cfg = json.loads(path.read_text())
    width, height = cfg['canvas']
    ink = np.zeros((height, width), dtype=bool)
    x, y = cfg['origin']
    layout = []
    for position, char in enumerate(cfg['text']):
        rows = cfg['glyphs'][char]
        h, w = len(rows), len(rows[0])
        assert h == 7 and all(len(row) == w for row in rows)
        assert all(set(row) <= {'0', '1'} for row in rows)
        assert 1 <= x and x + w < width and 1 <= y and y + h < height
        for j, row in enumerate(rows):
            for i, value in enumerate(row):
                ink[y+j, x+i] = value == '1'
        layout.append({'position': position, 'character': char,
                       'ink_box': [x, y, x+w, y+h]})
        x += w + cfg['advance_gap']
    outline = ink.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            outline |= np.roll(np.roll(ink, dy, axis=0), dx, axis=1)
    pixels = np.full((height, width), cfg['background_index'], dtype='uint8')
    pixels[outline] = cfg['outline_index']
    pixels[ink] = cfg['foreground_index']
    return pixels, {'font': path.name, 'size': [width, height], 'glyphs': layout}
