#!/bin/bash
# One-time setup per session: voice models + Python packages (English + Dutch narrators).
set -e
cd "$(dirname "$0")"
pip install kokoro-onnx soundfile piper-tts --break-system-packages -q 2>&1 | grep -v WARNING || true
mkdir -p voices/nl
for f in kokoro-v1.0.int8.onnx voices-v1.0.bin; do
  [ -s "voices/$f" ] || curl -sSL -o "voices/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
if [ ! -s voices/nl/nl-rdh-medium.onnx ]; then
  curl -sSL -o voices/nl/nl.tar.gz "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-nl-rdh-medium.tar.gz"
  tar xzf voices/nl/nl.tar.gz -C voices/nl && rm voices/nl/nl.tar.gz
fi
ls -la voices voices/nl
