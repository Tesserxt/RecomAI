
#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

# Locate Vercel configuration
if [[ -f "$FRONTEND/vercel.json" ]]; then
    VERCEL_JSON="$FRONTEND/vercel.json"
elif [[ -f "$ROOT/vercel.json" ]]; then
    VERCEL_JSON="$ROOT/vercel.json"
else
    echo "ERROR: vercel.json not found"
    exit 1
fi

API_LOG="$ROOT/uvicorn.log"
TUNNEL_LOG="$ROOT/cloudflared.log"

API_PID=""
TUNNEL_PID=""

cleanup() {
    echo
    echo "Stopping FastAPI and Cloudflare Tunnel..."
    [[ -n "$TUNNEL_PID" ]] && kill "$TUNNEL_PID" 2>/dev/null || true
    [[ -n "$API_PID" ]] && kill "$API_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# Check dependencies
for cmd in uv cloudflared curl python git vercel jq; do
    command -v "$cmd" >/dev/null || {
        echo "Missing dependency: $cmd"
        exit 1
    }
done

# Verify Vercel authentication
if ! vercel whoami >/dev/null 2>&1; then
    echo "ERROR: Vercel CLI is not logged in."
    echo "Run: vercel login"
    exit 1
fi

# 1. Start FastAPI
echo "Starting FastAPI..."

(
    cd "$BACKEND"
    uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
) > "$API_LOG" 2>&1 &

API_PID=$!

for i in {1..40}; do
    if curl -fsS http://127.0.0.1:8000/docs >/dev/null; then
        break
    fi
    sleep 1
done

if ! curl -fsS http://127.0.0.1:8000/docs >/dev/null; then
    echo "FastAPI failed to start:"
    tail -30 "$API_LOG"
    exit 1
fi

echo "FastAPI is running."

# 2. Start Cloudflare Tunnel
echo "Starting Cloudflare Tunnel..."

cloudflared tunnel \
    --url http://127.0.0.1:8000 \
    --no-autoupdate > "$TUNNEL_LOG" 2>&1 &

TUNNEL_PID=$!

# 3. Capture tunnel URL
TUNNEL_URL=""

for i in {1..60}; do
    TUNNEL_URL="$(
        grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' \
        "$TUNNEL_LOG" | head -n 1 || true
    )"

    if [[ -n "$TUNNEL_URL" ]]; then
        break
    fi
    sleep 1
done

if [[ -z "$TUNNEL_URL" ]]; then
    echo "Could not obtain Cloudflare URL:"
    tail -30 "$TUNNEL_LOG"
    exit 1
fi

WS_URL="${TUNNEL_URL/https:/wss:}/ws"

echo "Tunnel URL: $TUNNEL_URL"
echo "WebSocket URL: $WS_URL"

# 4. Update Vercel rewrite
export TUNNEL_URL

python - "$VERCEL_JSON" <<'PY'
import json
import os
import sys

path = sys.argv[1]
url = os.environ["TUNNEL_URL"]

with open(path) as f:
    config = json.load(f)

rewrites = config.setdefault("rewrites", [])

api_rule = next(
    (r for r in rewrites if r.get("source") == "/api/:path*"),
    None
)

if api_rule:
    api_rule["destination"] = f"{url}/api/:path*"
else:
    rewrites.insert(0, {
        "source": "/api/:path*",
        "destination": f"{url}/api/:path*"
    })

with open(path, "w") as f:
    json.dump(config, f, indent=2)
    f.write("\n")

print("Updated vercel.json")
PY

# 5. Update production WebSocket URL
ENV_FILE="$FRONTEND/.env.production"

touch "$ENV_FILE"

grep -v '^VITE_WS_URL=' "$ENV_FILE" > "$ENV_FILE.tmp" || true
mv "$ENV_FILE.tmp" "$ENV_FILE"

echo "VITE_WS_URL=$WS_URL" >> "$ENV_FILE"

echo "Updated production WebSocket URL."

# 6. Commit and push configuration changes
cd "$ROOT"

JSON_REL="${VERCEL_JSON#"$ROOT/"}"
ENV_REL="${ENV_FILE#"$ROOT/"}"

git add -- "$JSON_REL"
git add -f -- "$ENV_REL"

if ! git diff --cached --quiet -- "$JSON_REL" "$ENV_REL"; then
    git commit --only -m "chore: update Cloudflare tunnel URL" -- "$JSON_REL" "$ENV_REL"

    git push -u origin "$(git branch --show-current)"

    echo "Configuration changes pushed."
else
    echo "No configuration changes to commit."
fi

# 7. Find, verify, and promote current commit
cd "$FRONTEND"

echo
echo "Checking Vercel deployments..."

COMMIT_SHA="$(git -C "$ROOT" rev-parse HEAD)"
NEW_URL=""
PRODUCTION_PROMOTED=0
LATEST_URL=""

echo "Looking for deployment of commit: $COMMIT_SHA"

# Wait up to 5 minutes for the commit deployment
for i in {1..60}; do
    DEPLOYMENTS="$(vercel ls --format json)"

    NEW_URL="$(echo "$DEPLOYMENTS" | jq -r \
        --arg sha "$COMMIT_SHA" \
        '[.deployments[] | select(.meta.githubCommitSha == $sha)][0].url // empty'
    )"

    if [[ -n "$NEW_URL" ]]; then
        break
    fi

    sleep 5
done

if [[ -n "$NEW_URL" ]]; then
    echo "Found deployment: https://$NEW_URL"

    echo
    echo "Waiting for deployment to finish..."

    if vercel inspect "$NEW_URL" --wait; then
        echo "Deployment is ready!"

        # Promote the deployment to Production
        echo
        echo "Promoting latest commit to Vercel Production..."

        if vercel promote "$NEW_URL" --yes; then
            PRODUCTION_PROMOTED=1
            echo "Successfully promoted to Production!"
        else
            echo "ERROR: Production promotion failed."
            echo "Skipping automatic cleanup for safety."
        fi

        # 8. Clean up old deployments only after successful promotion
        if [[ "$PRODUCTION_PROMOTED" -eq 1 ]]; then
            echo
            echo "Cleaning up old deployments (keeping latest 3)..."

            DEPLOYMENTS="$(vercel ls --format json)"

            OLD_URLS="$(echo "$DEPLOYMENTS" | jq -r '
                .deployments[3:][]
                | select((.aliases // []) | length == 0)
                | .url // empty
            ')"

            if [[ -n "$OLD_URLS" ]]; then
                while IFS= read -r URL; do
                    [[ -z "$URL" ]] && continue
                    echo "Removing: $URL"
                    vercel remove "$URL" --yes || \
                        echo "Could not remove $URL"
                done <<< "$OLD_URLS"
            else
                echo "No eligible old deployments to remove."
            fi
        fi
    else
        echo "Deployment did not become ready."
        echo "Skipping promotion and cleanup."
    fi
else
    echo "Could not find deployment for commit $COMMIT_SHA."
    echo "Skipping promotion and cleanup."
fi

# 9. Final status
echo
echo "========================================"
echo "          RecomAI is running!"
echo "========================================"
echo "API:        $TUNNEL_URL"
echo "WebSocket:  $WS_URL"

if [[ -n "$NEW_URL" ]]; then
    echo "Deployment: https://$NEW_URL"
fi

if [[ "$PRODUCTION_PROMOTED" -eq 1 ]]; then
    echo "Production: Successfully promoted"
else
    echo "Production: Promotion not confirmed"
fi

echo "========================================"
echo "Keep this terminal open."
echo "Press Ctrl+C to stop everything."

# Keep processes alive
wait "$TUNNEL_PID"
