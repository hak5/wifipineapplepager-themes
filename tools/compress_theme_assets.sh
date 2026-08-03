#!/usr/bin/env bash

set -u

parent="${1:-}"
colors="${2:-64}"

if [[ -z "$parent" ]]; then
    echo "Usage: $0 <parent-directory> [colors]"
    echo "Example: $0 ./images 64"
    exit 1
fi

if [[ ! -d "$parent" ]]; then
    echo "Error: directory does not exist: $parent" >&2
    exit 1
fi

if ! command -v pngquant >/dev/null 2>&1; then
    echo "Error: pngquant is not installed or not in PATH." >&2
    exit 1
fi

total_before=0
total_after=0
processed=0
failed=0

while IFS= read -r -d '' input; do
    # Avoid recompressing files produced by this script.
    if [[ "$input" == *-compressed.png ]]; then
        continue
    fi

    output="${input%.png}-compressed.png"

    before=$(stat -c '%s' "$input") || {
        echo "Failed to read size: $input" >&2
        ((failed++))
        continue
    }

    if pngquant \
        --speed 1 \
        --quality 0-100 \
        --skip-if-larger \
        --nofs \
        --strip \
        --force \
        --output "$output" \
        "$colors" \
        -- \
        "$input"
    then
        after=$(stat -c '%s' "$output")

        saved=$((before - after))

        percent=$(awk -v before="$before" -v after="$after" '
            BEGIN {
                if (before > 0)
                    printf "%.1f", ((before - after) / before) * 100
                else
                    printf "0.0"
            }
        ')

        printf '\n%s\n' "$input"
        printf '  Original:   %10s\n' "$(numfmt --to=iec-i --suffix=B "$before")"
        printf '  Compressed: %10s\n' "$(numfmt --to=iec-i --suffix=B "$after")"

        if (( saved >= 0 )); then
            printf '  Saved:      %10s (%s%%)\n' \
                "$(numfmt --to=iec-i --suffix=B "$saved")" \
                "$percent"
        else
            printf '[!!]  Increased:  %10s (%s%% larger)\n' \
                "$(numfmt --to=iec-i --suffix=B "$((-saved))")" \
                "${percent#-}"
                #todo remove file
        fi

        total_before=$((total_before + before))
        total_after=$((total_after + after))
        ((processed++))
    else
        echo "[!] Failed: $input" >&2
        rm -f -- "$output"
        ((failed++))
    fi
done < <(
    find "$parent" -type f \
        \( -iname '*.png' \) \
        -print0
)

total_saved=$((total_before - total_after))

total_percent=$(awk -v before="$total_before" -v after="$total_after" '
    BEGIN {
        if (before > 0)
            printf "%.1f", ((before - after) / before) * 100
        else
            printf "0.0"
    }
')

printf '\n========================================\n'
printf 'Processed:  %d\n' "$processed"
printf 'Failed:     %d\n' "$failed"
printf 'Original:   %s\n' "$(numfmt --to=iec-i --suffix=B "$total_before")"
printf 'Compressed: %s\n' "$(numfmt --to=iec-i --suffix=B "$total_after")"

if (( total_saved >= 0 )); then
    printf 'Total saved: %s (%s%%)\n' \
        "$(numfmt --to=iec-i --suffix=B "$total_saved")" \
        "$total_percent"
else
    printf 'Total increase: %s (%s%% larger)\n' \
        "$(numfmt --to=iec-i --suffix=B "$((-total_saved))")" \
        "${total_percent#-}"
fi
