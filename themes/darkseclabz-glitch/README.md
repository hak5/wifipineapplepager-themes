# Darkseclabz Glitch

Darkseclabz design and skull artwork on the official Wargames theme by Hak5.

## Theme details

- **Theme name:** Darkseclabz Glitch
- **Author:** sinXne0 (Darkseclabz)
- **Version:** 1.0.0
- **Firmware:** WiFi Pineapple Pager 2.0.0-stable
- **Theme framework:** 0.9
- **Baseline:** Hak5 Wargames 2.0.0
- **Hardware testing:** tested on a physical WiFi Pineapple Pager running
  2.0.0-stable — boot, theme selection, lock screen, dashboard navigation,
  payload dialogs, and the recon and alerts screens

## Description

A glitch-styled sibling of the Darkseclabz theme: the same dark purple
Wargames re-skin and custom Darkseclabz skull artwork, with corrupted-signal
dashboard icons, a glitched boot animation, and new dashboard, payloads and
lock screen backgrounds. The full Wargames component layout is retained, so
every screen, menu, toggle, wizard and dialog keeps working.

## What changed

- 14 new `glitch-*` dashboard icons (alerts, payloads, PineAP, portal, recon
  and settings — selected and unselected states)
- Glitched boot animation frames
- New dashboard and payloads backgrounds and lock screen artwork
- Dashboard tiles use dedicated glitch icons instead of recoloured Wargames
  assets
- `dsl_*` purple palette entries: focus, tile, icon, selected, rule, white
- `theme.json` author, version and theme name metadata

## Installation

Copy this entire directory to `/root/themes/` or `/mmc/root/themes/`, then
choose **Darkseclabz Glitch** in **Settings → General → Theme**.

```sh
cp -r darkseclabz-glitch /root/themes/
```

## Known limitations

- Layout, component structure and retained original artwork come from Hak5's
  Wargames theme; this is a visual re-skin, not a ground-up theme.
- Validated against the 2.0.0-stable firmware image and the public Wargames
  source. Future firmware or theme-framework changes may require updates.
- Tested at the Pager's native 480 × 222 resolution only.

## Credits

Wargames layout and retained assets are by Hak5. See the
[official theme repository](https://github.com/hak5/wifipineapplepager-themes)
and the [Hak5 Software License Agreement](https://hak5.org/license).
