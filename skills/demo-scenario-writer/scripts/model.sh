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
# The script needs nothing outside the standard library, so there is no
# dependency to probe for and one interpreter check is the whole of the startup
# cost. Arguments are passed straight through:
#   sh scripts/model.sh object Case
#   sh scripts/model.sh lookup CaseStatus --banking

set -e

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# Probe order matters for speed, not just correctness. Launching the Windows
# Store stub costs about a quarter of a second before it fails, so on Windows
# `python` is tried first; everywhere else `python3` is both the right answer
# and the first guess. The stub is installed under BOTH names, so the probe
# below still has to run - the order only decides how often it wastes 250 ms.
case $(uname -s 2>/dev/null) in
    MINGW*|MSYS*|CYGWIN*|Windows*) CANDIDATES="python py python3" ;;
    *)                             CANDIDATES="python3 python py" ;;
esac

# A candidate counts only if it really runs and really is Python 3 - the Store
# stub fails both halves of that test.
PY=""
for candidate in $CANDIDATES; do
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
    echo "No Python 3 interpreter found (tried: $CANDIDATES)." >&2
    echo "Install Python 3.9 or newer and re-run." >&2
    exit 2
fi

exec $PY "$HERE/model.py" "$@"
