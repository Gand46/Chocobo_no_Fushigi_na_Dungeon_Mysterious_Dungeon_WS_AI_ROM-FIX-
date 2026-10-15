# Whistle source repair

Generate the four current WHISTLE_* entries with tools/generate_whistle_fix.py using the pinned HF2 ROM. The generated JSON matches src/corrections.json. Original compressed resources and their decompression codec are parsed from the user's private ROM; the output contains only editable replacement bytes and metadata.

Source 105B76: 37 tiles. Source 130C48: 18 cells reference missing index37, using palettes0/1/2. Native palettes observed before 5000:4935: [5,1,3,6], [5,6,1,3], [5,3,6,1]. Solid pixel2 in palette1/2 equals pixel1/3 in palette0. Native animation overwrites the map palette. Appending solid pixel2/1/3 tiles and baking the aliases into indices37/38/39 preserves that mapping under palette animation. All other map words and all original tiles remain unchanged.

Resource relocation: tiles10C800, map13FC60; pointers100078 and130040. Both caves are verified FF padding in their original banks; no executable or font bytes changed by HF3.

Evidence: docs/whistle_asset_check.json, docs/whistle_comparison.json, evidence/qa4/q4_whistle_resource_trace2, q4_whistle_palette_trace and q4_whistle_hf3_validation. Source generation and runtime evidence are separate checks.
