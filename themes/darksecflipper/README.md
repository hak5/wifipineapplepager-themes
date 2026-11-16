# Darksec Flipper

An orange LCD theme for the WiFi Pineapple Pager on firmware 2.0.0-stable. The
dashboard adapts the Flipper Zero's monochrome menu to the Pager's display and
controls. The dashboard, lock screen and startup sequence use artwork from
Flipper Devices' stock L1_Tv dolphin animation. This theme includes the Pager's
menus, dialogs, status bars, keyboards and screen assets.

## Install

Copy the `darksecflipper` directory into `/mmc/root/themes/` or `/root/themes/`
on the Pager:

```text
/root/themes/darksecflipper/
├── theme.json
├── components/
└── assets/
```

Then select **Darksec Flipper** under **Settings → General → Theme**.

The artwork source and GPL-3.0 license are in the `artwork-source` directory.
The Pager LCD base is Pocket Pager by Korben.

- [Flipper Devices stock animation](https://github.com/flipperdevices/flipperzero-firmware/tree/dev/assets/dolphin/internal/L1_Tv_128x47)
- [Hak5 Pocket Pager](https://github.com/hak5/wifipineapplepager-themes)
