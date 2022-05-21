# SPDX-FileCopyrightText: 2022 Eva Herrada for Adafruit Industries
# SPDX-License-Identifier: MIT
import board

from kb import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes

print("starting...")

keyboard = KMKKeyboard()
media = MediaKeys()
layers_ext = Layers()
rgb_ext = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_default=5,
    val_limit=25,
    val_step=10,
    hue_step=1,
    hue_default=128,
    animation_speed=5,
    refresh_rate=60,
    animation_mode=AnimationModes.BREATHING
    )

keyboard.extensions = [media, rgb_ext]
keyboard.modules = [layers_ext]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

keyboard.keymap = [
    [
        KC.NLCK, KC.PSLS, KC.PAST, KC.PMNS,
        KC.P7,   KC.P8,   KC.P9,   _______,
        KC.P4,   KC.P5,   KC.P6,   KC.PPLS,
        KC.P1,   KC.P2,   KC.P3,   _______,
        _______, KC.P0, KC.PDOT,   KC.PENT,
    ]
]

print(__name__)
if __name__ == '__main__':
    print("kb...")
    keyboard.go()
    print("end.")
