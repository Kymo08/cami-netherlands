#!/data/data/com.termux/files/usr/bin/bash
# ── CAMI Netherlands – Start dev server ───────────────────────────────────────
cd "$(dirname "$0")/backend"

# Kill any leftover Flask on port 5000
fuser -k 5000/tcp 2>/dev/null || true

echo ""
echo "Starting CAMI Netherlands dev server..."
echo ""
python app.py
