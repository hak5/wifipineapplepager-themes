# Darkseclabz Hadal Station

An underwater research station with six selectable rooms. The airlock opens Pager Portal, the beacon opens Alerts, the vault opens Payloads, sonar opens Recon, the antenna bay opens PineAP, and the control room opens Settings.

Extract the ZIP. Copy the darkseclabz-hadal folder to /mmc/root/themes/ and select darkseclabz-hadal under Settings → General → Theme. Confirm the UI reload.

Built for Pager 2.0.0-stable using Hak5 Wargames 2.0 supporting layouts. Original station artwork generated with ImageGen. File references, image decoding, and ZIP integrity were checked offline. Device testing is pending.

## Changelog

### 1.0.2

- `components/lock_screen.json`: `windowed_canvas` is now `false`. The lock
  screen background is a full-screen opaque image, so the windowed canvas was
  keeping an unused copy of the previous screen without ever caching it.
- `components/os_licenses.json`: both pages now use `back` instead of
  targeting `dashboard`, which had pushed a fresh copy of the boot dashboard
  onto the navigation stack each time the licenses screen was dismissed.
