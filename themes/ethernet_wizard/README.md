# ethernet_wizard

- **Theme name:** ethernet_wizard (EthernetWizard)
- **Author:** EthernetWizard ([GitHub](https://github.com/EthernetWizard), [ethernetwizard.com](https://ethernetwizard.com))
- **Theme version:** 2.0.0
- **Firmware:** WiFi Pineapple Pager firmware **2.0.0** (`theme_framework_version` **0.9**)

## Description

A wizard-themed reskin of the whole WiFi Pineapple Pager interface. What's new in v2:

- **New main menu rail:** six pixel-art icons (Pager Portal, Alerts, Payloads, Recon,
  PineAP, Settings) evenly spaced, with the name of the selected icon shown beside it and
  a glowing green rune marking where you are.
- **Pager Portal scenes:** a PC with a green portal pouring out of the screen, the wizard
  brewing a potion for Payloads, and the wizard browsing on a crystal-screen PC for Themes.
- **Original art remastered:** all the v1 wizard scenes keep their look but are redrawn
  crisper and tuned for the Pager screen so dark scenes don't band.
- **Mana Flask switch:** on/off toggles are a glass flask that fills with glowing green
  mana when on and sits empty when off.
- **Arcane eye launch animation:** a 10-frame eye that opens over 5 frames and closes over
  the next 5, looping while a payload launches.
- **New markers and icons:** green gem list cursor, green potion payload marker,
  crystal-ball folder icon, flame, info, checkbox and menu icons all redrawn to match.
- **Orb loading spinner:** a silver-teal orb with mist swirling counter-clockwise.
- **Rune-stone keyboards:** every keyboard rebuilt with carved stone keys and a green
  selection frame.
- **Candlelit Recon list** background with a glowing crystal ball.
- **Green glow** on selected alerts.
- **Solid lock screens** so the lock and buttons-locked screens are easy to see.
- **EthernetWizard Lab QR:** under **Settings → Help**, page 2 (press Down on the last
  Help item), linking to <https://ethernetwizard.com/lab-pager-theme>.
- **Firmware 2.0.0 screens styled to match:** Bluetooth recon, quick settings, Bluetooth
  and GPS settings, the help screens, the scan submenu and the DuckyScript picker.

**Inspiration:** EthernetWizard's own branding at [ethernetwizard.com](https://ethernetwizard.com).

## Install

Copy this whole `ethernet_wizard` folder into `/root/themes/` on the Pager, so that
`theme.json` ends up at `/root/themes/ethernet_wizard/theme.json`. Then pick it under
**Settings → General → Theme**.

Upgrading from v1: switch to the built-in **wargames** theme, delete the old
`EthernetWizard` folder, then install this one. v2 uses the lowercase folder name
`ethernet_wizard`.

## Known limitations

- Made for firmware 2.0.0 only. On firmware 1.0.x, use v1.
- About 5 MB installed, since every screen has a full-colour scene.
- Some Pager Portal lists show fewer characters than the main Payloads list, so very long
  payload names may be cut off.

## Credits

Theme design and art by EthernetWizard. Layouts are based on Hak5's default **wargames**
theme.
