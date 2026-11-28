# BWM-Wardriver 2.4.2 validation

Target hardware is the 480 × 222 WiFi Pineapple Pager running **2.1.0 Stable**, theme framework **0.9**.

| Local check | Result |
| --- | --- |
| GPS port and option lists | Rendered all 64 combinations of choice and focus across the standard, narrow and DuckyScript pickers. Every combination retained a single filled radio mark. Focusing Save or Cancel cleared the green row highlight. |
| Settings | All 127 selectable rows have a green plate and a near-white label. Bounds checks kept each plate on screen. Labels, live values and native actions matched the previous layout. |
| Confirmations and value editors | Both Yes/No choices, Launch/Cancel, and Save/Edit/Cancel in the text, numeric, IP and MAC dialogs retain their original targets. Near-white text on the deep-green fill has an 8.77:1 contrast ratio in the source artwork. |
| Navigation | All eight Home entries and all 32 Wardriving positions are reachable. The 24 Wardriving controls retain their original actions or variables. |
| Native menus and keyboards | Checked 374 entries across 71 screens and 194 key positions across four keyboard layouts. Focus stays inside the display and adjacent choices have separate focus areas. |

## Device checks

During the 2.4.2 device check, all 377 installed files matched the package used for the test. Theme Studio Pro opened that package with zero errors, warnings or information notices. Home displayed all eight entries and the charging percentage. On Wardriving's Capture page the ON/OFF column stayed visible as the green cursor moved. General Settings also showed the green bar on the focused item. [Home](previews/device-home.png) · [Wardriving](previews/device-wardriving.png).

The GPS device list contained one serial port. Moving focus from that row to Cancel left the filled circle on the port. Cancel returned to the GPS page with the existing port setting. [Port focused](previews/device-gps-port.png) · [Cancel focused](previews/device-gps-cancel.png).

The native confirmation dialog displayed its **No** and **Yes** choices. With **No** focused, the green button, pale text and cursor marked it as the active choice.

The Pager froze during a UI reload. Home returned after a power cycle. The cause is unknown.

Outdoor readability, cold boot, lock/unlock, field GPS and radio behavior, payload execution and live WiGLE acceptance remain unverified for 2.4.2.
