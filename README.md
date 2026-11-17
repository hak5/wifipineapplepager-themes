# Themes Library for the [WiFi Pineapple Pager](https://hak5.org/products/wifi-pineapple-pager) by [Hak5](https://hak5.org)

This repository contains **community-developed themes** for the Hak5 **WiFi Pineapple Pager**.  
Themes define the **visual appearance, layout, colors, fonts, icons, and UI components** used by the device.

Developers and designers are encouraged to submit Pull Requests to add new themes or improve existing ones.

**Themes here are written for the official WiFi Pineapple Pager theming system.  
Hak5 does NOT guarantee theme compatibility across firmware versions.**  
See [Legal and Disclaimers](#legal).

---
<div align="center">
<img src="https://img.shields.io/github/forks/hak5/wifipineapplepager-themes?style=for-the-badge"/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://img.shields.io/github/stars/hak5/wifipineapplepager-themes?style=for-the-badge"/>
<br/>
<img src="https://img.shields.io/github/commit-activity/y/hak5/wifipineapplepager-themes?style=for-the-badge">
<img src="https://img.shields.io/github/contributors/hak5/wifipineapplepager-themes?style=for-the-badge">
</div>
<br/>



<div align="center">
<a href="https://hak5.org/discord"><img src="https://img.shields.io/discord/506629366659153951?label=Hak5%20Discord&style=for-the-badge"></a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://twitter.com/hak5"><img src="https://img.shields.io/badge/follow-%40hak5-1DA1F2?logo=twitter&style=for-the-badge"/></a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://instagram.com/hak5gear"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"/></a>
<br/><br/>

</div>


Join the community on **[Hak5 Discord](https://hak5.org/discord)**

---

## Table of Contents

- [About the WiFi Pineapple Pager](#about-the-wifi-pineapple-pager)
- [About Pager Themes](#about-pager-themes)
- [Build Your Themes with Theme Studio Pro](#build-your-themes-with-theme-studio-pro)
- [Installing Pager Themes](#installing-pager-themes)
- [Contributing Themes](#contributing-themes)
- [Theme Guidelines](#theme-guidelines)
- [Legal](#legal)
- [Disclaimer](#disclaimer)

---

## Shop

- [WiFi Pineapple Pager](https://hak5.org/products/wifi-pineapple-pager)
- [Theme Studio Pro](https://shop.hak5.org/products/theme-studio-pro)
- [PayloadStudio Pro](https://hak5.org/products/payload-studio-pro)
- [Shop All Hak5 Tools](https://shop.hak5.org)

## Documentation / Learn More

- [WiFi Pineapple Pager Documentation](https://docs.hak5.org)
- [Theme Studio Pro Documentation](https://documentation.hak5.org/theme-studio)

## Community

Got questions or want feedback on your theme?

- [Hak5 Discord](https://hak5.org/discord)

---

## Additional Links

**Follow the creators**

- [Korben on Twitter](https://twitter.com/notkorben) | [Instagram](https://instagram.com/hak5korben)
- [Dragorn on Mastodon](https://infosec.exchange/@kismetwireless)
- [Darren on Twitter](https://twitter.com/hak5darren) | [Instagram](https://instagram.com/hak5darren)

---

## About the WiFi Pineapple Pager

A WiFi Pineapple built for hackers who don’t stay put.

The **WiFi Pineapple Pager** combines the power of Hak5’s PineAP engine with a fast, highly optimized embedded UI. Themes allow creators to reshape the look and feel of the device — from subtle visual refinements to bold, stylized interfaces inspired by retro, tactical, or modern aesthetics.

Themes affect **visuals only**. They do not alter payload behavior, system configuration, or wireless operations.

---

## About Pager Themes

Pager themes are **UI composition and UX behavior definitions**, typically composed of:

- Component layout and composition definitions
- Icons and Image Assets
- Color palette

Themes are loaded dynamically by the Pager UI framework and can be switched at runtime.

Themes in this repository are the **source assets** used directly by the device — **no compilation required**.

---

## Build Your Themes with [Theme Studio Pro](https://themestudio.hak5.org)

<p align="center">
Make designing your own WiFi Pineapple Pager themes 10x easier, right in your browser. (Runs offline)
<br/><br/>
<a href="https://themestudio.hak5.org"><img src="https://shop.hak5.org/cdn/shop/files/wifi-pineapple-pager-theme-studio-pro-icon_180x.jpg?v=1793480335" alt="Theme Studio Pro"></a>
<br/>
<i>Theme Studio Pro is the theme editor for the WiFi Pineapple Pager. It draws every screen exactly as the Pager draws it, so what you see in the editor is what your Pager shows.
<br/><br/>
There's nothing to install. Sign in, start a theme, and edit it on the screen: click anything to select it, drag it into place, change its text and colors, and paint its images. When you're done, export the theme and copy it to your Pager.
<br/><br/></i>
<a href="https://shop.hak5.org/products/theme-studio-pro">Get Theme Studio Pro</a> and <b>make your Pager unmistakably yours!</b>
<br/>
<a href="https://documentation.hak5.org/theme-studio">Read the Theme Studio Pro documentation</a>
<br/><br/>
<a href="https://documentation.hak5.org/theme-studio"><img src="https://1168486578-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FYUw5FdwX3RNc9Yxd0SzQ%2Fuploads%2Fgit-blob-2e866e6ae9783e776c38a3a02de1a7046b2a2eb8%2Feditor-overview.png?alt=media" width="800" alt="Theme Studio Pro with the default theme's dashboard open"></a>
<br/>
<i>Theme Studio Pro with the default theme's dashboard open</i>
<br/><br/>
<a href="https://documentation.hak5.org/theme-studio/getting-started/your-first-theme"><img src="https://1168486578-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FYUw5FdwX3RNc9Yxd0SzQ%2Fuploads%2Fgit-blob-b7d4d146ce816ffb456baf54169e5c02bf149f48%2Femulate.png?alt=media" width="800" alt="Trying a menu with the Pager's buttons in Emulate"></a>
<br/>
<i>Trying a menu with the Pager's buttons in Emulate</i>
</p>

With Theme Studio Pro you can:

- **Start a theme** from a copy of the default theme, open one you already have, or browse the community themes
- **Edit screens visually**: select text, images, variables and menu items, then move, align, restyle or edit them, with undo for every change
- **Change it once, everywhere**: move, recolor or swap an image, and its copies on other screens can follow after you review each one
- **Line things up** with ruler guides, smart guides and a measure tool
- **Paint your images** in the built-in asset editor, with layers, pixel-art tools and the Pager's own fonts
- **Try your menus** with the Pager's buttons in Emulate
- **Check your theme** for anything that would stop it loading or look wrong on the Pager
- **Keep up with the firmware**: see what each firmware release changed for themes and add it to yours
- **Optimize images** so your theme stays small
- **Export** the theme as a zip, or save it straight to a folder on your computer

---

## Installing Pager Themes

To install a new theme, simply copy it to `/root/themes/`, or `/mmc/root/themes/` (Create the `themes` directory if it doesn't exist yet).

## Contributing Themes

Once you have created or modified a theme, you are encouraged to contribute it by submitting a **Pull Request**.

Reviewed and approved Pull Requests will add your theme to this repository, where it may be publicly available to Pager users.

Please ensure your theme:

- Is tested on real hardware
- Loads and operates fully without errors
- Does not rely on undocumented or internal APIs
- Does not break usability or readability

If your theme is inspired by or based on someone else’s work, **credit the original author**.

---

## Theme Guidelines

### Naming Conventions

- Each theme must live in its **own directory**
- Directory names must be lowercase
- Use `-` or `_` instead of spaces if required
- Theme names should be unique, descriptive, and appropriate

Example directory structure:
```
wargames/
├── assets/
├── components/
├── theme.json
└── README.md
```

### Required Files

Each theme must include:

- A primary theme definition file, `theme.json`, in the root of its directory
- All referenced assets (fonts, icons, images)
- A `README.md` containing:
    - Theme name
    - Author
    - Description or inspiration
    - Known limitations
    - Firmware version developed for

> Reference the default theme (wargames) as an example. The theme file format is documented in the [Theme Files reference](https://documentation.hak5.org/theme-studio/reference/theme-files).
---

### Design Best Practices

- Maintain sufficient contrast for readability
- Ensure UI elements remain usable in outdoor lighting
- Avoid excessive asset size or visual noise
- Crop images to the smallest possible size, even when transparent
- Test with real Pager workflows (alerts, recon, payload execution)

Themes that significantly degrade usability may be rejected.

---

### Prohibited Content

The following will **not** be accepted:

- Malicious or deceptive UI intended to mislead users
- Content that violates Hak5 community standards
- Copyrighted material without permission
- Branding that impersonates other products or companies

---

## Legal

Themes from this repository are provided for **educational and customization purposes only**.

Hak5 gear is intended for authorized auditing and security analysis purposes only where permitted by local and international law. Users are solely responsible for compliance.

WiFi Pineapple and DuckyScript are trademarks of Hak5 LLC.  
Copyright © 2010 Hak5 LLC. All rights reserved.

Themes are subject to the Hak5 Software License Agreement:  
https://hak5.org/license

Hak5 LLC products and technology are only available to BIS recognized license exception ENC favorable treatment countries pursuant to US 15 CFR Supplement No 3 to Part 740.

---

## Disclaimer

**Themes are provided AS-IS without warranty.**

While Hak5 makes a best effort to review submitted themes, there is no guarantee of compatibility, performance, or visual correctness across firmware versions or hardware revisions.

Use at your own risk.
