#!/usr/bin/env bash
# CI smoke test: start Streamlit briefly and verify HTTP responds.
set -euo pipefail

streamlit run app.py \
  --server.headless true \
  --server.port 8501 \
  --server.address 127.0.0.1 &
pid=$!

cleanup() {
  kill "${pid}" 2>/dev/null || true
  wait "${pid}" 2>/dev/null || true
}
trap cleanup EXIT

for _ in $(seq 1 90); do
  if curl -sf --max-time 2 "http://127.0.0.1:8501/_stcore/health" >/dev/null; then
    echo "Streamlit health check passed (/_stcore/health)."
    exit 0
  fi
  if curl -sf --max-time 2 "http://127.0.0.1:8501/" >/dev/null; then
    echo "Streamlit root URL responded."
    exit 0
  fi
  sleep 1
done

echo "Streamlit did not become ready in time." >&2
exit 1
