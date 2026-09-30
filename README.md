# The Real Transport Toolbox: web holding page and social operations

This repository holds the placeholder page for the old GitHub Pages address and the working material for TRTT social media.

## Contents

- `index.html`: a holding page that redirects to https://therealtransporttoolbox.vip/. The earlier template landing page was removed because it made claims TRTT cannot support and its content did not match Australian requirements.
- `privacy.html` and `terms.html`: kept because social platform app settings may link to them. They are generic templates. Review them against the Privacy Act 1988 and the Australian Consumer Law before relying on them.
- `docs/social-media-plan.md`: the social and branding review, the decisions made, the plan and the restore log for paused posts.
- `tools/voice_lint.py`: a heuristic check of draft posts against the TRTT brand voice brief.

## Checking a draft

```
python3 tools/voice_lint.py draft.txt --platform linkedin
```

Put several drafts in one file, separated by a line containing only `---`. The script exits with status 1 if it finds an ERROR. WARN lines need a human decision.
