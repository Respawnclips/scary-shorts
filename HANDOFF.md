# Overdracht: automatisch posten buiten Metricool

Doel van Aimane: de TikToks (NL, Lucas-stem) en YouTube Shorts (EN) automatisch laten plaatsen, 3 per dag (10:00, 15:00, 20:30, Europe/Amsterdam), zonder dat hij iets hoeft te doen. Metricool gratis plan (20 posts/maand) is bijna op.

## Huidige situatie
- Video's staan in `videos/<id>.mp4` (1080x1920, 30 fps). EN = YouTube, `-nl` = TikTok.
- Ze worden gemaakt door een geplande cloud-taak ("Daily scary Shorts (3 legends...)", elke dag 04:47 Amsterdam). Die rendert, commit naar deze repo en plant via Metricool (brand 8026350).
- Metricool-limiet is dus het probleem: 6 posts/dag past niet in 20/maand.
- Video's hebben nog geen "wachtrij": `USED.md` houdt bij welke verhalen gebruikt zijn (007 hookman-nl staat er nog niet in).

## Wat er onderzocht is
- Upload-Post gratis: 10 uploads/maand, TikTok niet inbegrepen. Betaald vanaf ca. $24/maand.
- Postiz (zelf hosten): officieel minimum 2 vCPU / 2 GB, aanbevolen 4 vCPU / 8 GB; vereist PostgreSQL, Redis en Temporal. Te zwaar voor een Pi 4 met 2 GB.
- TikTok Content Posting API: een niet-goedgekeurde app kan alleen privé posten. Voor openbaar posten is een audit nodig (weken). Dit geldt voor elk zelfgehost alternatief.
- YouTube Data API: geen audit nodig voor eigen kanaal, standaardquota is genoeg voor 3 uploads/dag.

## Plan
1. Script `poster/youtube_post.py`: leest `poster/queue.json` (video, titel, beschrijving, tijdstip) en uploadt via YouTube Data API (OAuth, token lokaal bewaren, NIET in git).
2. Draait op de laptop (Taakplanner/cron) of op de Raspberry Pi (WireGuard, 2 GB, externe schijf 1 TB). Laptop moet dan aan staan om te posten; de Pi staat altijd aan.
3. TikTok: eigen ontwikkelaarsapp aanvragen (Content Posting API + audit). Tot goedkeuring: de overgebleven Metricool-posts alleen voor TikTok gebruiken (ca. 1/dag).
4. Cloud-taak aanpassen: schrijft alleen nog video + `queue.json` naar GitHub; het script op laptop/Pi doet het posten.

## Hardware van Aimane
- Pc: GTX 1650 Super (4 GB), laptop: RTX 4050 (waarschijnlijk 6 GB).
- Raspberry Pi 4 (2 GB), 128 GB + 1 TB extern, bereikbaar via WireGuard.

## Voorkeuren
- Spreekt Nederlands, wil weinig handwerk, wil geen vragen waar een redelijke keuze volstaat.
- Wil betere animatie (nu 2D, "rig v2" voorgesteld maar nog niet bevestigd).
