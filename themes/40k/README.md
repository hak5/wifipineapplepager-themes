# 40k

A Warhammer 40K / Inquisition-inspired skin for the WiFi Pineapple Pager. It
combines the original INQUISITOR wheel states with the component-ready artwork
from `INQUISITOR_40K_FW2_BUILD_KIT.zip` and maps them onto a complete Hak5
**Wargames 2.0** theme. Every menu, toggle, wizard, dialog, status bar and
keyboard is still a live Pager component - no screenshot-style menu image is
placed behind the real UI.

## Install

Copy the folder to the Pager and select the theme:

```sh
cp -r 40k /root/themes/
# or: cp -r 40k /mmc/root/themes/
```

Then choose **40k** under **Settings -> General -> Theme** and
confirm the UI reload.

```text
40k/
├── theme.json
├── components/          # Wargames 2.0 layouts, retained so all actions work
├── ringtones/           # bundled RTTTL ringtone (machine_spirit.rtttl)
└── assets/
    ├── inquisitor/      # original 37-image reference pack
    ├── inquisitor_fw2/  # FW2 build-kit backgrounds, panels, icons, frames
    └── ...              # reskinned Wargames support artwork
```

### Boot ringtone

`ringtones/machine_spirit.rtttl` is the INQUISITOR "Machine Spirit" boot
melody shipped with the theme. Themes cannot change device settings, so to make
it play at startup copy it into `/root/ringtones/` once and select
**Machine Spirit** under **Settings -> General -> Ringtone -> Boot**.

```sh
mkdir -p /root/ringtones
cp ringtones/machine_spirit.rtttl /root/ringtones/
```

## What is themed

- **Main dashboard** - the `reference_dashboard.png` skull wheel with all six
  transparent gold-arc and underline selection states. Selection order: RECON,
  PINEAP, PAYLOADS, Portal, ALERTS, SETTINGS.
- **Section screens** - Recon, PineAP, Payloads, Pager Portal, Alerts and
  Settings keep their live Wargames component layouts. Their backgrounds,
  icons and list panels are reskinned from the FW2 build kit; all labels,
  values and selections are drawn by the Pager.
- **Payload selection** - the left column of the payload lists carries
  INQUISITOR side art, scaled to the original aspect ratio and kept clear of
  every option and its selection indicator.
- **Dialogs and keyboards** - FW2 dialog/list/keyboard backgrounds and panel
  art are applied, while every message, input and option remains live. The
  confirmation dialog uses dedicated yes/no button artwork.
- **System screens** - retained 12-frame FW2 boot animation and spinner timing,
  with continuous dim cathedral backdrops replacing flat center blocks.
- **Support artwork** - the remaining INQUISITOR icon set is applied to
  checkboxes, radios, toggles, arrows, status-bar glyphs, alert screens,
  payload-log indicators and the launch-payload animation.
- **Palette** - gold, amber and rust values derived from the original pack,
  applied to all text/UI colours.
- **Status bar** - an FW2 panel sits behind the live indicators. Baked headers
  and fake batteries were cleared from the top strip of every full-screen
  background, so the real status bar no longer draws a second battery. The
  live battery indicator is red on every status bar variant.
- **Selection pickers** - the outlined selection boxes have been removed from
  option pickers and edit/launch dialogs. Selection is shown by highlighted
  text/icon colour only.

## Notes and limitations

- The original `screen_*.png` mockups and the build kit's `screen_*.png` files
  are kept only as source art; they are not wired behind live menus.
- The **Portal** wheel selection opens **Pager Portal** through the unchanged
  `pager_portal_dashboard` target. Historical `wardrive` filenames are retained
  to preserve references. Unused legacy mockups may retain their original captions.
- Target firmware: **Pager 2.0.0-stable**, theme framework 0.9. Layouts and
  component definitions are from Hak5's Wargames theme.

## Credits

Wargames layout and retained components: Hak5. Original INQUISITOR 40K wheel
artwork: the supplied reference pack. Component-ready backgrounds, panels,
icons and animation frames: the supplied FW2 build kit.
