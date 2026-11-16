# GS Yellow Theme v1.6.1 — WiFi Pineapple Pager

Author: GhostStrats

## Description
A black-and-yellow theme with custom swipe dashboard panels, faded GS backgrounds,
reworked keyboards, matching spinner and boot animation, and custom low/critical battery screens.

## Important installation fix
This release corrects the ZIP exported with an uppercase versioned folder name and
indexed-color assets with missing transparency. The folder must be named `gs-yellow-theme`.

1. Extract this ZIP on your computer; do not place the ZIP itself in the Pager themes directory.
2. Copy the **gs-yellow-theme** folder directly to `/root/themes/` or `/mmc/root/themes/`.
3. Confirm the file is at `/root/themes/gs-yellow-theme/theme.json` (or the matching `/mmc/root/themes/...` path).
4. Remove/rename the older broken folder `GS_Yellow_Theme_WiFi_Pineapple_Pager_v1_6` from the Pager themes directory, if present.
5. On the Pager choose **Settings → Display → Theme** and select the new theme.
6. If the theme doesn't appear, return to the default theme and check the folder location, firmware support, and that the assets copied completely.

## Compatibility
Designed from an existing Pager theme using `theme_framework_version: 0.5`.
Firmware/hardware: not independently tested on a physical Pager. Actual supported firmware version not verified.
Known limitations: theme compatibility may depend on firmware changes. Keep a working backup theme.
This is an unofficial custom theme, not an official Hak5 product.

## Troubleshooting
If the interface becomes inaccessible, connect with a supported device management method/SSH
and remove the faulty folder from `/root/themes/` or `/mmc/root/themes/`, then restart UI/device
and choose a known-good theme. Do not overwrite the built-in default theme.
