# Darkseclabz Desktop

A macOS Tahoe-inspired Pager theme with a translucent dock, a magnified selection, six dashboard cards, and custom wallpaper, startup, lock, Settings, Recon, Alerts, Pager Portal, PineAP, payload menu, and payload log. The glass effect is rendered into the assets. Supporting screens use Hak5 Wargames 2.0 layouts.

Extract this ZIP and copy darkseclabz-desktop into /mmc/root/themes/. Select darkseclabz-desktop under Settings → General → Theme and confirm the reload.

Target firmware is Pager 2.0.0-stable. Includes frosted confirmation dialogs, option pickers, Quick Settings and Power menus, a 16-frame startup animation, a rotating wait indicator, and an animated launch confirmation icon. Files checked offline. On-device testing is pending.

## Changelog

### 11.0.2

- `components/lock_screen.json`: `windowed_canvas` is now `false`. The lock
  screen background is a full-screen opaque image, so the windowed canvas was
  keeping an unused copy of the previous screen without ever caching it.
- `components/os_licenses.json`: both pages now use `back` instead of
  targeting `dashboard`, which had pushed a fresh copy of the boot dashboard
  onto the navigation stack each time the licenses screen was dismissed.
