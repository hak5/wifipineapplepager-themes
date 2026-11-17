# GS Yellow Theme — WiFi Pineapple Pager

**Author:** GhostStrats (@Ghoststrats)  
**Theme version:** 1.6.1  
**Theme framework version:** 0.5  
**Firmware developed/tested for:** WiFi Pineapple Pager firmware (exact firmware build not recorded; confirm on your device before use)

## Description

GS Yellow Theme is a high-contrast black-and-yellow community theme for the Hak5 WiFi Pineapple Pager. It features custom swipe-through dashboard art for Alerts, Payloads, Recon, PineAP, and Settings; yellow status icons; redesigned menus and keyboards; GS artwork on the lock screen; a frame-based boot animation; and customized low/critical battery alerts. The payload confirmation uses a minimal dark-to-yellow-eyes animation.

## Installation

Copy the `gs-yellow-theme` directory to `/root/themes/` or `/mmc/root/themes/` on the Pager. Confirm that `theme.json` is directly inside that directory. On the Pager, select the theme from **Settings > Display > Theme**. Keep the built-in theme available as a fallback.

## Testing and known limitations

- The author has confirmed that the repaired v1.6.1 theme loads on a physical WiFi Pineapple Pager. This does not establish compatibility with all firmware builds or exhaustively test every UI screen.
- The exact firmware version used for the reported successful test was not recorded.
- Some animations and layouts may be affected by future Pager firmware/theme-framework changes.
- If the theme causes an error, switch back to a known-good theme and remove or replace the custom theme folder.

## Credits and disclaimer

Custom theme design: **GhostStrats**. Based on the WiFi Pineapple Pager theme framework and existing Pager theme structures. WiFi Pineapple and associated Hak5 product names and marks belong to Hak5 LLC. This is an independent, **unofficial community theme**, not an official Hak5 product or firmware.

All theme assets are supplied for the Pager UI; this theme does not change wireless or payload behavior.
