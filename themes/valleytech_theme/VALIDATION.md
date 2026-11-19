# Valleytech Theme 2.1.0 validation

Recorded November 18, 2026 on WiFi Pineapple Pager **2.0.0 Stable**, theme
framework **0.9**. The JSON components match the tested installation with only
CRLF-to-LF line-ending normalization for the repository; runtime artwork is
byte-identical. Contribution documentation and the two screenshots were added
afterward.

## Theme checks

| Check | Observed result |
| --- | --- |
| Structural validation | 139 JSON files parsed; 194 runtime PNGs verified; 1,467 references checked; no errors or warnings. Native names and manifest slots were compared with Hak5 Wargames. |
| Theme Studio Pro | Current runtime ZIP imported with 0 errors, 0 warnings and 0 informational findings; home and loading screens visually reviewed. |
| Installation | Transfer SHA-256 matched on the Pager; theme activated through Settings > General > Theme. |
| Home | All six labeled tiles visible. Right from Wardriving selected Alerts; Down selected PineAP; Left selected Recon; Up returned to Wardriving. |
| Wardriving | All 25 controls visible together. Row/column movement and expanded focus labels worked; Up from the first control wrapped to Upload & Archive without paging. |
| Loading | Both logos, Valleytech Theme lettering, animated gold activity bar and native Getting Categories / Getting Payloads messages displayed. |
| Optional companion shortcut | Wardriving > Upload & Archive > Launch opened all four menu rows with Cancel selected. A on Cancel ended cleanly at Payload Complete. |

These observations used the actual connected device's framebuffer and controls
through Virtual Pager. [Home capture](previews/device-home.png) and
[companion menu capture](previews/device-upload-menu.png) are actual screenshots.

## Separate companion checks

The pinned companion linked from the README has its own source and tests.
Its final host suite ran **39 tests: 38 passed and one Windows symbolic-link
fixture was skipped**. A persistent-fixture run on the actual Pager passed
**23 checks with zero failures**, including native JSON parsing, real process
open-file checks, persistent storage, archive recovery and blocked repeat
attempts. The native run covered the process behavior skipped on Windows.

These tests used synthetic files and stubbed network responses. No real
wardriving log was uploaded, archived or deleted. Native menu launch/cancellation
does not establish WiGLE acceptance, processing or score changes.

## Remaining checks

- Direct physical-panel and outdoor readability.
- Cold boot and lock/unlock acceptance.
- A moving wardrive session and a full pass through other native workflows.
- Live WiGLE upload/archive acceptance for the optional companion.

Structural and editor checks do not replace these practical checks. The compact
Wardriving labels and preserved keyboard/QR layouts are documented in the README.
