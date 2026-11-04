# Wildhaven Hearth

Your own AI, at home on your computer, that looks after itself. By Wildhaven Homes.

```bash
curl -fsSL https://wildhaven-homes-llc.github.io/hearth/install.sh | bash
```

Or ask any AI that can run commands (GitHub Copilot in Agent mode by default), with the
[RAR Easy Mode skill](https://kody-w.github.io/grail-layers/skills/rar-easy-mode/SKILL.md):
*"Give me wildhaven-hearth using RAR Easy Mode and test it for me."*

## What you get
- **It never drops the conversation.** Adding, removing or updating anything happens while it keeps answering.
- **Add what you need, take out what you don't.** Every pack installs and uninstalls cleanly; nothing else breaks.
- **It looks after its computer, keeps private topics at home, and knows who inherits it.**
- **Your data stays yours, on your computer.**

## How it is built
Hearth is a distribution, like Ubuntu is to Linux. It runs the Brainstem engine exactly as published (pinned by its
sha256 in [`release.json`](release.json), never edited) and adds everything around it from
[grail-layers](https://github.com/kody-w/grail-layers) and the [RAR catalog](https://kody-w.github.io/RAR/), each pinned
to one commit. Machine-readable: [`registry.json`](registry.json), [`llms.txt`](llms.txt).

Wildhaven Homes LLC. All rights reserved unless a license file says otherwise.
