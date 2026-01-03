# Tiitle: ColorUI Theme
# Description: Easily edit the theme.json color palette to change the theme colors.
# Author: RootJunky
# Version 1

[![Video Demo](https://img.youtube.com/vi/u66qg6Bg-14/0.jpg)](https://youtu.be/u66qg6Bg-14)

### Demo Video
[Watch on YouTube](https://youtu.be/u66qg6Bg-14)


## Open theme.json and scroll down to the color_palette section. Here you will be able to edit most the the theme text and image colors. Then just push the theme.json file over to the pager and restart the server from developer menu.


Edit the rgb for each item you want to theme.
Example "textheader":{ "r":106, "g":210, "b":249 },
Example "pngstatus":{ "r":106, "g":210, "b":249 },
Example "pngpayloadcaticonselect":{ "r":0, "g":0, "b":0,"a":0 }, adding the a attribute will make it clear or transparent.

## List and location of png files you should edit.
~~~
assets/alerts_dashboard/alerts_bg.png
assets/boot_animation/init-1.png
assets/boot_animation/init-2.png
assets/boot_animation/init-3.png
assets/boot_animation/init-4.png
assets/dashboard/wargames_bg.png
assets/keyboard/keyboard_layout_hex.png
assets/keyboard/keyboard_layout_ip.png
assets/keyboard/keyboard_layout_lower.png
assets/keyboard/keyboard_layout_numeric.png
assets/keyboard/keyboard_layout_symbols.png
assets/keyboard/keyboard_layout_upper.png
assets/keyboard/_hex-bg.png
assets/keyboard/_key-bg.png
assets/keyboard/_spacebar-4x.png
assets/launch_payload_dialog/launch_payload_bg.png
assets/launch_payload_dialog/animation/anim_frame_1.png
assets/launch_payload_dialog/animation/anim_frame_2.png
assets/payloadlog/payload_log_bg.png
assets/payloads_dashboard/arrow.png
assets/payloads_dashboard/payloads_bg.png
assets/payloads_dashboard/recon_payloads_bg.png
assets/recon/ recon_dashboard.png
assets/recon/recon_list_bg.png
assets/blank_recon_bg.png
assets/dialog_bg.png
assets/edit_string_dialog_bg.png
assets/lock_screen.png
assets/payload_log_bg.png
assets/pineap_bg.png
assets/power_menu_bg.png
assets/settings_bg.png
assets/optiondialog/option_dialog_bg_windowed_mask.png This one is a special mask for popup windows and it gives them the circle effect. 
~~~

## List of 2 json file you might want to edit.
~~~
theme.json
components/boot_animation.json
~~~

