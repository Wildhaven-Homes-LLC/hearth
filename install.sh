#!/usr/bin/env bash
# Wildhaven Hearth: your own AI at home, that looks after itself.
#   curl -fsSL https://wildhaven-homes-llc.github.io/hearth/install.sh | bash
# Every piece is pinned to one exact release (release.json): the Brainstem engine by its sha256, the layers and the
# catalog by their commits. Already have a Brainstem? Hearth is added around it while it keeps answering.
set -euo pipefail
HEARTH="${HEARTH_URL:-https://wildhaven-homes-llc.github.io/hearth}"
GL_REV="7e035a4aa5ca234b5cb0111de981b77a622a3a4e"
RAR_REV="f86f847951640fc99337b69c81f2baf2273d0cd7"
KERNEL_SHA="35618683ebc3d1c2bfaff47f60182fd756f3a8de53c53dd907ec1099d631930a"
GL="https://raw.githubusercontent.com/kody-w/grail-layers/$GL_REV"
RAR="https://raw.githubusercontent.com/kody-w/RAR/$RAR_REV"
BS="${BRAINSTEM_HOME:-$HOME/.brainstem}"
KERNEL="$BS/src/rapp_brainstem/brainstem.py"
say(){ printf '\033[1m%s\033[0m\n' "$*"; }
case "$(uname)" in Darwin|Linux) ;; *) echo "Wildhaven Hearth needs macOS or Linux (on Windows, use WSL)."; exit 1;; esac

say "Wildhaven Hearth 1.0.0"
say "Step 1 of 2: the Brainstem and its safety net"
curl -fsSL "$GL/install.sh" | GRAIL_LAYERS_URL="$GL" GRAIL_LAYERS_RAR="$RAR/stacks/grail-layers" bash

have="$(shasum -a 256 "$KERNEL" 2>/dev/null | cut -c1-64 || true)"
if [ "$have" != "$KERNEL_SHA" ]; then
  echo "Your Brainstem engine is a different version (${have:0:12}) from the one Hearth 1.0.0 is built for (${KERNEL_SHA:0:12})."
  echo "Your Brainstem keeps working as it is; Hearth's packs will be offered when a matching Hearth release is out."
  exit 2
fi

say "Step 2 of 2: Hearth's packs"
curl -fsSL "$GL/add.sh" | RAR_PAGES="$RAR" GRAIL_LAYERS_URL="$GL" bash -s -- wildhaven-hearth
say "Done. Talk to your Brainstem at http://localhost:7071 — or just ask it 'what am I running'."
