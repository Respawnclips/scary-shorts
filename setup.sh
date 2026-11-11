#!/bin/bash
# One-time setup per session: voice model + Python packages.
set -e
cd "$(dirname "$0")"
pip install kokoro-onnx soundfile --break-system-packages -q 2>&1 | grep -v WARNING || true
mkdir -p voices
for f in kokoro-v1.0.int8.onnx voices-v1.0.bin; do
  [ -s "voices/$f" ] || curl -sSL -o "voices/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
ls -la voices
