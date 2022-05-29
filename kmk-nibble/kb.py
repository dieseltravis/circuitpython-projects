# SPDX-FileCopyrightText: 2022 Travis Hardiman
# SPDX-License-Identifier: Hippocratic v3.0
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

class KMKKeyboard(_KMKKeyboard):
    # These are the pro micro pins that QMK uses for the nibble
    # define MATRIX_ROW_PINS { B1, B3, B2, B6, D4 }
    # These are the equivalent pins on the KB2040
    row_pins = (
        board.SCK,
        board.MISO,
    	board.MOSI,
    	board.D10,
    	board.D4,
    )
    # does something special have to be done for the mux?
    # define MATRIX_COL_MUX_PINS { F4, F5, F6, F7 }
    col_pins = (
        board.A3,
        board.A2,
        board.A1,
        board.A0,
    )
    # TODO: verify that this is correct
    diode_orientation = DiodeOrientation.COL2ROW
    i2c = board.I2C
