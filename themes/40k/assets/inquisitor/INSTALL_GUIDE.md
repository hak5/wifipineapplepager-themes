# INQUISITOR 40K — Pager integration

This pack deliberately matches the supplied Warhammer 40K dashboard image, not a generic red-and-gold theme.

## Asset selection
- `assets/reference_dashboard.png`: unselected skull-wheel screen
- `assets/dashboard_selected_0_recon.png` through `dashboard_selected_5_settings.png`: six selection states
- `assets/screen_*.png`: section-specific backgrounds
- `assets/boot.png`, `lock.png`, `notification.png`, `error.png`, `success.png`, `loading.png`, `keyboard.png`, `dialog.png`, `reboot.png`, `shutdown.png`: system screen treatments
- `assets/icon_*.png`: custom icons

## Safe installation workflow
1. Back up the existing Pager theme.
2. Open the official theme for **your installed firmware** in Hak5 Theme Studio Pro or a compatible theme editor.
3. Import the images from `assets/` and apply them to the matching screens, keeping original actions and component IDs.
4. Map each dashboard selection to its corresponding `dashboard_selected_*` visual state if the editor/firmware supports it.
5. Preview with the emulator and verify readability, menu focus, alert overlays, and A/B/D-pad behavior.
6. Export a firmware-compatible theme folder containing `theme.json`, `components/`, and `assets/` and copy it to `/root/themes/` or `/mmc/root/themes/`.

## Important
These PNGs do not themselves create a working radial menu. The firmware-specific theme schema and menu binding must be implemented in the real theme. The baked-in text must not be confused with actual interactive menu elements. This package is **not** represented as a hardware-tested installable theme.

Official reference: https://github.com/hak5/wifipineapplepager-themes
