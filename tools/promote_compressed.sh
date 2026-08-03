#!/usr/bin/env bash

set -u

parent="${1:-}"

if [[ -z "$parent" ]]; then
    echo "Usage: $0 <parent-directory>"
    echo "Example: $0 ./images"
    exit 1
fi

if [[ ! -d "$parent" ]]; then
    echo "Error: directory does not exist: $parent" >&2
    exit 1
fi

renamed=0
failed=0

while IFS= read -r -d '' compressed; do
    original="${compressed%-compressed.png}.png"

    if mv -f -- "$compressed" "$original"; then
        printf '%s -> %s\n' "$compressed" "$original"
        ((renamed++))
    else
        echo "Failed to rename: $compressed" >&2
        ((failed++))
    fi
done < <(
    find "$parent" -type f -iname '*-compressed.png' -print0
)

printf '\nRenamed: %d\n' "$renamed"
printf 'Failed:  %d\n' "$failed"
