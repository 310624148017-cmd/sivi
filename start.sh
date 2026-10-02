#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "[SIVI] Autonomous Agent for Everyday Apps"
echo "   AI Build Challenge 2026 - Track 01 Prototype"
echo "=========================================================="

# 1. Check for python virtual environment
PYTHON_CMD="python3"
if [ -f "$DIR/../.venv/bin/python" ]; then
    PYTHON_CMD="$DIR/../.venv/bin/python"
elif [ -f "$DIR/backend/venv/bin/python" ]; then
    PYTHON_CMD="$DIR/backend/venv/bin/python"
fi

echo "[PYTHON] Using Python: $($PYTHON_CMD --version)"

# 2. Check or generate resume.pdf
if [ ! -f "data/resume.pdf" ]; then
    echo "[DATA] Generating sample candidate resume.pdf..."
    "$PYTHON_CMD" data/generate_resume.py || true
fi

PORT="${PORT:-8888}"
export PORT

# 3. Start Backend in Background
echo "[START] Starting SIVI Backend on http://localhost:$PORT ..."
cd backend
"$PYTHON_CMD" app.py &
BACKEND_PID=$!
cd "$DIR"

trap "echo 'Stopping SIVI...'; kill $BACKEND_PID 2>/dev/null || true; exit" INT TERM EXIT

echo "[STATUS] Backend running (PID: $BACKEND_PID)"
echo ""
echo "=========================================================="
echo "[READY] SIVI IS LIVE!"
echo "   • Main Interactive Dashboard: http://localhost:$PORT"
echo "   • Mock TechCorp Portal:      http://localhost:$PORT/mock/techcorp/jobs/swe-intern"
echo "   • WebSocket Endpoint:         ws://localhost:$PORT/ws/agent"
echo "   • Health Check:               http://localhost:$PORT/health"
echo "=========================================================="
echo ""
echo "To also run Next.js development server:"
echo "   cd frontend && npm install && npm run dev"
echo "   (Frontend will run on http://localhost:3000)"
echo ""
echo "Press Ctrl+C to stop the backend."

wait $BACKEND_PID
