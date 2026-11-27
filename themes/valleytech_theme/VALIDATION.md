# Valleytech Terminal 2.4.1 validation

Checked on November 27, 2026 using a WiFi Pineapple Pager running **2.1.0 Stable**, theme framework **0.9**. Device observations used Virtual Pager's live framebuffer and D-pad controls.

| Check | Observation |
| --- | --- |
| Theme Studio Pro | Importing the 2.4.1 package returned 0 errors, 0 warnings and 0 informational findings. |
| Device installation | The archive checksum on the Pager matched the local archive. Selecting the new theme in Settings reloaded the interface. |
| Home | All eight entries fit the 480 × 222 display with the clock and charging percentage visible. Wardriving, Biscuit Node and Quartermaster were each selected on the device to inspect their artwork against gold. |
| All eight focus positions | Local pixel checks covered all eight Home selections. The contrast between the selected label and gold background measured 12.83:1 in the source artwork. |
| Shortcuts | On 2.4.0, both Home shortcuts opened their respective native launch confirmations on the Pager. The checks ended at those prompts. The Home dashboard and shortcut bindings are identical in 2.4.1. |
| Wardriving | Local navigation checks reached all 32 positions across four pages. The 24 existing controls kept their native targets or variables. |

The Home screenshot was saved from the 2.4.1 device framebuffer with Quartermaster selected. [View the capture](previews/device-home.png).

The Wardriving screenshot was captured on the Pager using 2.3. The Capture page and its artwork match the 2.4.1 files. The loading screen displays the two logos and a small activity indicator. It omits the stock spinner text template. [View the Wardriving capture](previews/device-wardriving.png).

Direct outdoor readability, cold boot, lock/unlock, field GPS and radio behavior, payload execution, and live WiGLE acceptance were outside the 2.4.1 device checks.
