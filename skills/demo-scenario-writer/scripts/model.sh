#!/bin/sh
# Cross-platform launcher for model.py (macOS, Linux, Windows/Git Bash).
#
# Two things it takes care of so the caller does not have to:
#   * the interpreter name. `python3` is right on macOS and Linux; on Windows it
#     is usually the Microsoft Store stub, which prints an install advert and
#     exits 49 without running anything. `python` is right on Windows and is
#     absent or Python 2 elsewhere.
#   * the working directory. The snapshots are found relative to this file, so
#     the command works from anywhere.
#
# Arguments are passed straight through:
#   sh scripts/model.sh object Case
#   sh scripts/model.sh lookup CaseStatus --banking

set -e

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# A candidate counts only if it really runs and really is Python 3 — the Store
# stub fails both halves of that test.
PY=""
for candidate in python3 python py; do
    case $candidate in
        py) probe="py -3" ;;
        *)  probe=$candidate ;;
    esac
    if [ "$($probe -c 'import sys;print(sys.version_info[0])' 2>/dev/null)" = "3" ]; then
        PY=$probe
        break
    fi
done

if [ -z "$PY" ]; then
    echo "No Python 3 interpreter found (tried python3, python, py -3)." >&2
    echo "Install Python 3.9 or newer and re-run." >&2
    exit 2
fi

if ! $PY -c 'import openpyxl' 2>/dev/null; then
    echo "openpyxl is required to read the object-model snapshot." >&2
    echo "Install it with:  $PY -m pip install openpyxl" >&2
    echo "On a Homebrew or system Python that refuses this, add --user or" >&2
    echo "--break-system-packages, or run the skill inside a virtualenv." >&2
    exit 2
fi

exec $PY "$HERE/model.py" "$@"
