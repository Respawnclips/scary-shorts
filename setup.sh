#!/bin/bash
# One-time setup per session: voice models + Python packages (English + Dutch narrators).
set -e
cd "$(dirname "$0")"
pip install kokoro-onnx soundfile piper-tts --break-system-packages -q 2>&1 | grep -v WARNING || true
mkdir -p voices/nl
for f in kokoro-v1.0.int8.onnx voices-v1.0.bin; do
  [ -s "voices/$f" ] || curl -sSL -o "voices/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
mkdir -p voices/nl2
if [ ! -s voices/nl2/vits-piper-nl_NL-miro-high/nl_NL-miro-high.onnx ]; then
  curl -sSL -o voices/nl2/miro.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-nl_NL-miro-high.tar.bz2"
  tar xjf voices/nl2/miro.tar.bz2 -C voices/nl2 && rm voices/nl2/miro.tar.bz2
fi
ls -la voices voices/nl2
