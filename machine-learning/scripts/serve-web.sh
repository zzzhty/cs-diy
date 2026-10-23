#!/usr/bin/env sh
set -eu

usage() {
    cat <<'EOF'
Usage: scripts/serve-web.sh [options]

Serve only explicitly approved static course pages for remote browser access.

Options:
  --host HOST   Address to bind. Defaults to 0.0.0.0.
  --port PORT   TCP port to listen on. Defaults to 8000.
  -h, --help    Show this help.

Examples:
  scripts/serve-web.sh
  scripts/serve-web.sh --port 8080
EOF
}

require_value() {
    option=$1
    value=${2-}
    if [ -z "$value" ]; then
        echo "missing value for $option" >&2
        exit 2
    fi
}

host=${WEB_HOST:-0.0.0.0}
port=${WEB_PORT:-8000}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --host)
            require_value "$1" "${2-}"
            host=$2
            shift 2
            ;;
        --host=*)
            host=${1#*=}
            shift
            ;;
        --port)
            require_value "$1" "${2-}"
            port=$2
            shift 2
            ;;
        --port=*)
            port=${1#*=}
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

case "$port" in
    *[!0-9]*|'')
        echo "port must be a positive integer: $port" >&2
        exit 2
        ;;
esac

if [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
    echo "port must be between 1 and 65535: $port" >&2
    exit 2
fi

if command -v python3 >/dev/null 2>&1; then
    python_bin=$(command -v python3)
elif command -v python >/dev/null 2>&1; then
    python_bin=$(command -v python)
else
    echo "Python is required to serve static pages." >&2
    exit 1
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

echo "Serving $repo_root on http://$host:$port/"
echo "Open /deep-learning/language-modeling-from-scratch/ from a reachable host IP."
exec "$python_bin" "$repo_root/../scripts/serve_web.py" --port "$port" --host "$host" --url-root machine-learning
