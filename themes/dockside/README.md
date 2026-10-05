# Dockside

- Author: Jenx
- Version: 0.1.0
- Theme framework: 0.7 (built from the stock `wargames` theme)

## Description

A light, desktop-computer look for the WiFi Pineapple Pager.

- **Desktop:** the main screen is a desktop with a wallpaper, a menu bar (the Pager's status icons
  sit in it like menu bar extras), desktop icons and a dock of six custom app icons. The selected
  icon magnifies, gets an indicator dot, and shows its name in a tooltip above it.
- **Menu bar:** press up (or B) from the dock to reach the pineapple, then left/right along the
  menu bar. The pineapple opens the power menu; **Pager** opens About, and **Display**, **Sound**
  and **Network** open those settings pages. The power menu also has **Settings...** and
  **Pager Portal...** shortcuts. A divider in the dock sets Settings apart.
- **Windows everywhere:** every screen is a window with a title bar and red/yellow/green window
  buttons. Selected rows get a blue highlight bar with white text, dialogs use rounded push
  buttons (the focused one is blue), toggles are green switches, and longer lists and pages show
  a classic scroll bar.
- **Payloads:** browsing user, recon and alert payloads looks like a file browser, with a
  Favorites sidebar, a Name/Kind list and a path bar showing where you are
  (`Pager HD > payloads > user`). Launching a payload drops a sheet from that
  window, where the Terminal icon's cursor blinks.
- **Settings and PineAP:** styled like a system-settings app, with a sidebar of colored category
  icons and grouped rows showing switches, current values and chevrons, previewed live as you
  move through the sidebar. About lists the device info with a scroll bar and a Developer Tools
  row.
- **Pager Portal:** styled like an app store, with Discover tiles, section rows, GET/UPDATE pills
  and payload pages. Its icon shows the Pager itself, drawn like Hak5's Pager character.
- **Recon:** an activity-monitor style graph, results and clients as tables with column headers,
  and access point / client details with an info grid beside an actions card.
- **Everything else:** the power menu drops down from the pineapple, the payload log is a
  Terminal window, confirmations and option/edit dialogs are sheets, alerts slide in as
  notification cards, setup has a sidebar of steps, the lock screen is a login window,
  locked buttons show a small overlay, the keyboards are redrawn as keycaps, and the boot, update,
  battery, heat, license and QR screens all match the look.

## Installation

1. Copy the `dockside` folder to `/root/themes/` (or `/mmc/root/themes/`) on your Pager
2. Go to **Settings > General > Theme**
3. Select **dockside**

## Known limitations

- Status icons and some small glyphs are recolored stock art, not redrawn.
- Text drawn by the firmware uses the Pager's system font, so on-screen labels are monospaced.
