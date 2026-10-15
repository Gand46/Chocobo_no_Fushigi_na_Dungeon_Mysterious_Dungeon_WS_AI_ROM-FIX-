# 1.1-HF2-TEST — 2026-10-13

- Reproduced Lafoss freeze in JP, English v1.1 and HF1 under a controlled dungeon fixture.
- Added a 17-byte invalid-model guard with a six-byte hook, using native bank restoration/return. Animation reconstruction remains open.
- Reproduced whistle tile reuse; no speculative graphic edit shipped.
- Verified synthetic DispelDrink before/after ordering and basic HF1/HF2 cold loading.
- Fixed one-shot savestate capture in the QA driver; retained rejected attempts explicitly.
- Revalidated 30 equipment actions, ten text resources, patch rebuild and independent BPS apply.
- All HF1 changes remain cumulative; historical change log is in docs/HF1_CHANGELOG.md.
