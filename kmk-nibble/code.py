# SPDX-FileCopyrightText: 2022 Travis Hardiman
# SPDX-License-Identifier: Hippocratic v3.0
import board

from kb import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.keys import KC

print("starting kmk nibble...")
# define VENDOR_ID       0x6E61
# define PRODUCT_ID      0x6060
# define DEVICE_VER      0x0001
# define MANUFACTURER    nullbits
# define PRODUCT         NIBBLE

keyboard = KMKKeyboard()

# init extensions
media = MediaKeys()
rgb_ext = RGB(
    pixel_pin=board.D7,
    num_pixels=10,
    val_default=5,
    val_limit=25,
    val_step=10,
    hue_step=1,
    hue_default=96,
    animation_speed=5,
    refresh_rate=60,
    animation_mode=AnimationModes.BREATHING
)

keyboard.extensions = [media, rgb_ext]

# init modules
layers_ext = Layers()
encoder_handler = EncoderHandler()

keyboard.modules = [layers_ext,encoder_handler]

# Filler keys
_______ = KC.TRNS
xxxxxxx = KC.NO

# Layers
LYR_STD, LYR_EXT = 0, 1

TO_STD = KC.DF(LYR_STD)
MT_EXT = KC.MO(LYR_EXT)

keyboard.keymap = [
    [ # standard
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC, KC.HOME,
        TO_STD,  KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS, KC.DEL,
        MT_EXT,  KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,          KC.ENT,  KC.PGUP,
        KC.UP,   KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,          KC.UP,   KC.PGDN,
        KC.DOWN, KC.LCTL, KC.LGUI, KC.LALT,                   KC.SPC,                    TO_STD,  KC.RALT, KC.RCTL, KC.LEFT,          KC.DOWN, KC.RGHT
    ], 
    [ # fn extra
        KC.GRV,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  _______, KC.END,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,          _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,          _______, _______,
        _______, _______, _______, _______,                   _______,                   _______, _______, _______, _______,          _______, _______
    ]
]

# setup rotary encoder
encoder_handler.pins = ((board.D9, board.D8, board.D7, False),)
encoder_handler.map = ( 
    ((KC.VOLU, KC.VOLD, KC.MUTE),), # standard
    ((_______, _______, _______),), # fn extra
)

print(__name__)
if __name__ == '__main__':
    print("kb...")
    keyboard.go()
    print("end.")
