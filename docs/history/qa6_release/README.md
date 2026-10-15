# Chocobo English HF3 TEST — QA6

Current ROM and cumulative JP→HF3 BPS are unchanged. This cumulative package adds a read-only data-first save validator, exact native copy evidence, mixed-write tests and the shared-chat review. Read INFORME_ES.md.

QA6 corrects the QA5 D2 fixture: native flag0080 was incorrectly set as8000 at730A. The corrected fixture reaches floor60 dialogue. This is a test correction, not a ROM fix or full ending validation.

Build: python3 build.py /path/JP.ws --out /path/new_output
Base CRC32 CCAA4853; output302765E7. No commercial ROM included.

Validate a raw SRAM: python3 tools/validate_chocobo_save.py /path/game.sav
Verify captured data: python3 qa6/verify_data_validation.py --runs evidence/qa6 --fixtures qa5/save_fixtures

Do not interpret an intact signature, an exact copy, or a successful CLI exit as proof of all game-event semantics. The natural save-loss trigger remains open. TEST, not RC/final.
