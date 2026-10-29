#! /bin/sh
# Build the static site (for GitHub Pages) into _site/
#
# The conversion runs in the browser with Pyodide, which installs the project
# and its dependencies from the wheels in _site/wheels/.
# odfpy has no wheel on PyPI, so all the wheels are built here.
set -eu

SITE=_site
WHEELS=$SITE/wheels

rm -rf "$SITE"
cp -r src/convertor/web/static "$SITE"
mkdir -p "$WHEELS"

uv build --wheel --out-dir "$WHEELS"
uv export --frozen --no-dev --no-hashes --no-emit-project --no-header --no-annotate \
    --output-file "$WHEELS/requirements.txt"
uvx pip wheel --no-deps --wheel-dir "$WHEELS" --requirement "$WHEELS/requirements.txt"
rm "$WHEELS/requirements.txt"

# the list of wheels for worker.js to install, its presence also enables the in-browser conversion
(cd "$WHEELS" && ls *.whl) | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read().split()))' > "$WHEELS/wheels.json"

echo "Built $SITE/, serve it with: python3 -m http.server -d $SITE"
