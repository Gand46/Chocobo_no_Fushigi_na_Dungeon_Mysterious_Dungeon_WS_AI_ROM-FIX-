# Original English translation: source and credits

The HF20 cumulative translation and fixes are based on the earlier **Chocobo's Dungeon for WonderSwan English v1.1** fan translation. Its public listing is [Romhacking.net, translation no. 5525](https://www.romhacking.net/translations/5525/). The linked site returned an access error during this export, so its live revision and download bytes were not reverified. The names and roles below come directly from the original readme already preserved in this project: [`LEGACY_README.txt`](LEGACY_README.txt).

| Original readme credit | Role |
| --- | --- |
| SpecialAgentApe | Hacking, menu translation, graphics editing |
| Higsby | Translation |
| ShinxHijinx | Testing |
| wowjinxy | Special thanks |

The repository preserves the legacy v1.1 IPS at [`src/legacy_v1.1_original.ips`](../src/legacy_v1.1_original.ips), SHA-256 `46408bc9842ed235ce9d20fae9118e231557563bedb7e329ca9abd1007c2ea0c`, and the readme, SHA-256 `0fcfa97734064e72d65c9b2474bcb555df70d0ebce4e8b792df70350405a352a`. These are inherited translation materials, not newly authored HF20 work. The exact identity of the site's current download against this preserved IPS was not checked.

The editable [`src/legacy_translation_ranges.json`](../src/legacy_translation_ranges.json) reproduces the normalized English baseline from user-provided Japanese and English v1.1 binaries. It includes legacy IPS edits and a normalized checksum, but it was **reconstructed by this project**; it must not be described as the original team's source code. HF1–HF20 corrections and new validation are tracked in [`HISTORY_HF1_HF20.md`](HISTORY_HF1_HF20.md) and [`SOURCE_PROVENANCE.md`](SOURCE_PROVENANCE.md). The HF20 BPS is applied directly to the clean Japanese ROM; the old IPS is retained for provenance and is not an extra installation step.
