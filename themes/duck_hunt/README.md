Theme name: Duck Hunt  
Author: kernel-kliink  
Version: 2.0.0  
Developed for firmware version 2.0.0 (theme framework 0.9)  

A Duck Hunt–inspired NES theme for the WiFi Pineapple Pager.

## What's new in 2.0.0

Version 1.0 was a reskin of the *Wargames* theme for firmware 1.0.4. Version 2.0.0 rebuilds the theme on the firmware 2.0.0 components and covers the screens that didn't exist when 1.0 was made:

- New main menu with icon tiles (Alerts, Payloads, Recon, PineAP, Portal, Settings)
- Bluetooth recon lists and device details
- Pager Portal (get, update and manage payloads, installed themes)
- Quick Settings, with NES-style brightness and volume pickers
- DuckyScript list picker and payload launch screens
- GPS settings, and WiGLE options under PineAP
- Keyboards, dialogs, alerts, lock screens and update screens
- Duck Hunt title-screen boot animation

## Installation

Copy the `duck_hunt` folder to `/root/themes/` (or `/mmc/root/themes/`), then pick it from **Pager Portal > Themes**.

## Artwork Attribution

Duck Hunt and its characters belong to Nintendo. This theme is a non-commercial fan work.

For 2.0.0 the artwork was redrawn. The character sprites were created with the help of AI image tools and then reworked to fit the Pager's 480x222 screen.

## Known Limitations

- Dynamic text (SSIDs, payload names, descriptions, values) uses the firmware's built-in font, not the NES-style lettering used for titles and labels.
- The Virtual Pager web interface (including the WiGLE map and upload pages) is not part of the on-device theme engine and keeps its default look.
- The early Linux boot screen shown before the Pager UI starts is not themeable.
- Tested on firmware 2.0.0 only. Other firmware versions may not display correctly.
