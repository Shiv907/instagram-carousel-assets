LiteLLM PyPI compromise - Security #02 overlays (Tue 27 Oct 2026, 7:00 PM IST)

Canvas: 1080x1920 transparent PNGs. Face stays in the top third; overlays sit in the lower two-thirds. Nothing below y=1536.
Each overlay also has a -1080x1350.png crop. Cover: cover.jpg (title 'Signed release mein malware'). Contact sheet: contact-sheet.png.
Fonts: Archivo Black, Poppins, IBM Plex Mono. Accent #FFC800. Same brand look as 2026-10-23-security-01. No logos, no real people.
Generator: generate.py-style generate_overlays.py (python3 generate_overlays.py <outdir>).
Raw URL pattern: https://raw.githubusercontent.com/Shiv907/instagram-carousel-assets/main/reels/2026/10/2026-10-27-security-02-litellm-pypi/overlays/<file>.png

01-hook-signed-malware.png  Hook - "Signed release, phir bhi malware"  bbox (90, 1080, 991, 1441)
  01-hook-signed-malware-1080x1350.png
02-trust-chain.png  Trust chain: Signed / Attested / Trusted Publisher (green checks), then red "source: lookalike repo"; caption "Provenance ≠ sahi source"  bbox (90, 720, 991, 1481)
  02-trust-chain-1080x1350.png
03-pip-pth-drop.png  Terminal mock: pip install litellm, cook.pth drops into site-packages; caption ".pth har Python start pe"  bbox (90, 740, 991, 1420)
  03-pip-pth-drop-1080x1350.png
04-cook-pth-zoom.png  cook.pth zoom: "import cook" highlighted + "runs at every Python start"; caption "Import kiya? Zarurat nahi"  bbox (65, 740, 1017, 1430)
  04-cook-pth-zoom-1080x1350.png
05-master-key.png  Building + master key + burglar copy; caption "Master key pe burglar copy"  bbox (90, 720, 991, 1488)
  05-master-key-1080x1350.png
06-tokens-keys-lock.png  AWS / GCP / Azure / LLM API keys -> lock; title "Tokens se pipeline hijack"  bbox (90, 740, 991, 1468)
  06-tokens-keys-lock-1080x1350.png
07-fix-checklist.png  Fix checklist: Pin + hash · CodeArtifact Upstream BLOCK · IAM roles · Rotate all; caption "Pin + hash, roles, rotate"  bbox (90, 720, 991, 1481)
  07-fix-checklist-1080x1350.png
08-end-card.png  End card "Provenance ≠ trust" + @shivanshu_builds  bbox (90, 900, 991, 1421)
  08-end-card-1080x1350.png
