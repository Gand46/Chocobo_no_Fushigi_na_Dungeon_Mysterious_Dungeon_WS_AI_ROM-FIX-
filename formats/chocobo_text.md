# Recovered text and fixture format (bounded findings)

Text uses little-endian 16-bit glyph/control words, not ASCII or Shift-JIS. Existing English glyphs frequently contain digraphs. `FFFF` terminates the observed common copy loops at ROM 0x187AD3 and 0x187B15; source getter is at 0x187E0C. Consumer pointers are near 16-bit offsets in the table's own ROM bank. Runtime CPU CS=3000 in the observed bank mapping.

Getter descriptor array: ROM 0x18D930, four bytes per family (near table offset and segment). SRAM 0x6427 selects family, 0x6428 index, 0x642A returned word. The getter doubles the word/index registers before reading; the Lua observer accounts for this. At CPU 3000:7E1D, AX contains the returned word. In the common copy consumer the returned FFFF is tested before writing; bit 0x2000 selects skipped control words; bit 0x8000 affects output stride. These are observations of this consumer, not a universal complete definition of all dialogue controls. The restored Walking resource preserves its original FFFE/FFFF suffix. FFF2 is NOT changed blindly.

The exact new Walking sequence is `00C3 02BD 01D7 8000 0367 000D 0180 01DE FFFE FFFF`. It reuses existing English glyphs; no glyph bitmap is added or redesigned. Exact IDs, locations and other sequences are in the localization JSON. Stored words are the source of intent; screenshots supply evidence of actual rendering.

Player bag fixture: capacity byte SRAM 0x6C9E; records at 0x6C9F, five bytes each: quantity, item ID, level, auxiliary byte, flags. The test writes only one record into an initially empty bag. This does not prove all arbitrary bit combinations are valid. The game also has another item pool at 0x670A; these are not interchangeable.

Observed IDs: 0x65 TanTalon, 0x9D TanSaddle, 0xDE Whistle, 0xFF Lafoss (description Lafoss pearls), 0x59 DispelDrink. Object names: table 0x16E7F0; descriptions: table 0x15AD00. Identifying a name/description does not prove its usable context or effect.

Text output buffer is based at SRAM 0x6057; watcher logs DI >= 0x23C at CPU stores 3000:7AFF and 3000:7B7D because 0x6293 contains a subsequent control pointer. These two watches are not a global bounds checker. In the recorded tests they report no crossings. Reads past a text slot are distinct from writes out of a destination buffer; this distinction is preserved in the report.
