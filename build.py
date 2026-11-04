"""One hand-authored input (release.json + the served files) -> one idempotent build -> registry.json,
api/v1/status.json, api/v1/badge.json, llms.txt, append-only versions/. rapp-static-api/1.1."""
import hashlib, json, pathlib
from datetime import datetime, timezone

R = pathlib.Path(__file__).resolve().parent
PAGES = "https://wildhaven-homes-llc.github.io/hearth"
RAW = "https://raw.githubusercontent.com/Wildhaven-Homes-LLC/hearth/main"
SERVED = ["install.sh", "release.json", "README.md", "llms.txt"]
rel = json.loads((R / "release.json").read_text())
(R / "llms.txt").write_text(f"""# Wildhaven Hearth
> Your own AI at home on your computer that looks after itself: it never drops the conversation, every pack installs and
> uninstalls cleanly, and the Brainstem engine runs exactly as published. By Wildhaven Homes.

Release: {rel['version']} (engine sha256 {rel['kernel']['sha256'][:12]}, grail-layers {rel['grail_layers']['revision'][:7]}, RAR {rel['catalog']['revision'][:7]})
Install: curl -fsSL {PAGES}/install.sh | bash
Any AI (GitHub Copilot Agent mode by default): https://kody-w.github.io/grail-layers/skills/rar-easy-mode/SKILL.md
Index (JSON): {PAGES}/registry.json
Release pins: {PAGES}/release.json
Rules for any AI: https://kody-w.github.io/RAR/RAPP.md
""")
entries = []
for n in SERVED:
    b = (R / n).read_bytes(); sha = hashlib.sha256(b).hexdigest()
    ext = pathlib.Path(n).suffix
    v = R / "versions" / pathlib.Path(n).stem / f"{sha[:8]}{ext}"
    if not v.exists():  # append-only: a published version is never rewritten
        v.parent.mkdir(parents=True, exist_ok=True); v.write_bytes(b)
    entries.append({"name": n, "sha256": sha, "url": f"{PAGES}/{n}", "raw": f"{RAW}/{n}",
                    "version_url": f"{PAGES}/versions/{pathlib.Path(n).stem}/{sha[:8]}{ext}"})
reg = {"schema": "hearth-registry/1.0", "spec": "rapp-static-api/1.1", "generated": None, "pages": PAGES + "/", "raw": RAW + "/",
       "release": rel, "summary": {"files": len(entries), "version": rel["version"]}, "entries": entries}
old = R / "registry.json"; prev = json.loads(old.read_text()) if old.is_file() else {}
reg["generated"] = prev.get("generated") if prev and {**prev, "generated": None} == reg else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
old.write_text(json.dumps(reg, indent=2) + "\n")
(R / "api/v1").mkdir(parents=True, exist_ok=True)
(R / "api/v1/status.json").write_text(json.dumps({"schema": "hearth-status/1.0", "generated": reg["generated"], "ok": True, **reg["summary"]}, indent=2) + "\n")
(R / "api/v1/badge.json").write_text(json.dumps({"schemaVersion": 1, "label": "hearth", "message": rel["version"], "color": "orange"}) + "\n")
print("built", rel["version"])
