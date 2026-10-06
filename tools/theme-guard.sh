#!/bin/sh
# theme-guard.sh: interim protection for theme development (no UI server changes needed).
#
# - Every time the pager UI server (/pineapple/pineapple) dies, its crash output
#   (Go panic / fatal error + stack trace) is copied from logread into $LOG.
# - If it crash-loops (MAX_STARTS restarts within WINDOW seconds) while a custom
#   theme is selected, the default theme is restored in UCI; procd's next respawn
#   then comes up on the default theme from ROM.
#
# Install (from your computer):
#   scp theme-guard.sh root@172.16.52.1:/root/
#
# Start (on the pager; keeps running after you log out, won't start a second copy):
#   pgrep -f '^sh /root/theme-guard.sh$' >/dev/null || ( sh /root/theme-guard.sh </dev/null >/dev/null 2>&1 & )
#
# Stop:
#   kill $(pgrep -f '^sh /root/theme-guard.sh$')
#
# Crash log:
#   cat /root/theme-guard.log

DEFAULT_NAME='[wargames]'
DEFAULT_PATH='/rom/lib/pager/themes/wargames'
WINDOW=120          # seconds
MAX_STARTS=3        # this many new UI processes within WINDOW = crash loop
LOG=/root/theme-guard.log
LOG_MAX=524288      # rotate the log at 512 KB

# keep running when the SSH session that started us ends (busybox here has no nohup)
trap '' HUP

starts=""
last_pid=""

log() {
	if [ -f "$LOG" ] && [ "$(wc -c < "$LOG")" -gt "$LOG_MAX" ]; then
		mv "$LOG" "$LOG.old"
	fi
	cat >> "$LOG"
}

# Copy the crash output (panic/fatal error and the stack trace after it) of a
# UI server process that has exited, identified by its PID in logread.
save_crash() {
	old_pid=$1
	trace=$(logread | grep "pineapple\[$old_pid\]: " | sed 's/^.*pineapple\[[0-9]*\]: //' |
		grep -A300 -E "^(panic:|fatal error:|unexpected signal|SIGSEGV)")
	[ -n "$trace" ] || return
	{
		echo "=== $(date) UI server (pid $old_pid) crashed, theme: $(uci -q get system.@pager[0].theme_path)"
		echo "$trace"
		echo
	} | log
}

logger -t theme-guard "started, logging UI crashes to $LOG"

while :; do
	pid=$(pidof pineapple)
	if [ -n "$pid" ] && [ "$pid" != "$last_pid" ]; then
		[ -n "$last_pid" ] && save_crash "$last_pid"
		last_pid=$pid

		now=$(cut -d. -f1 /proc/uptime)
		keep=""
		for s in $starts; do [ $((now - s)) -le $WINDOW ] && keep="$keep $s"; done
		starts="$keep $now"

		theme=$(uci -q get system.@pager[0].theme_path)
		if [ "$(echo $starts | wc -w)" -ge "$MAX_STARTS" ] &&
		   [ -n "$theme" ] && [ "$theme" != "$DEFAULT_PATH" ]; then
			echo "=== $(date) UI crash loop with theme $theme, default theme restored" | log
			uci set system.@pager[0].theme_name="$DEFAULT_NAME"
			uci set system.@pager[0].theme_path="$DEFAULT_PATH"
			uci commit system
			logger -t theme-guard "UI crash loop with theme $theme, default theme restored (see $LOG)"
			starts=""
		fi
	fi
	sleep 2
done
