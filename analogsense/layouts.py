from .keymaps import *


def layout_rows(layout):    return layout[0]
def layout_cols(layout):    return layout[1]
def layout_size(layout):    return layout[0] * layout[1]
def layout_key(layout, i):  return layout[2 + i]
def layout_index_to_row(layout, i): return i // layout_cols(layout)
def layout_index_to_col(layout, i): return i % layout_cols(layout)


LAYOUT_KEYCHRON_Q1_HE = (6, 15,
    KEY_ESCAPE,    KEY_F1,    KEY_F2,   KEY_F3,   KEY_F4,   KEY_F5,   KEY_F6,    KEY_F7,   KEY_F8,   KEY_F9,    KEY_F10,       KEY_F11,          KEY_F12,           KEY_DEL,        KEY_NONE,
    KEY_BACKQUOTE, KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,  KEY_PAGE_UP,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,  KEY_PAGE_DOWN,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_ENTER,         KEY_HOME,       KEY_NONE,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_NONE,         KEY_SLASH,         KEY_RSHIFT,     KEY_ARROW_UP,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RMETA, KEY_FN,        KEY_RCTRL,        KEY_ARROW_LEFT,    KEY_ARROW_DOWN, KEY_ARROW_RIGHT,
)

LAYOUT_KEYCHRON_Q3_HE = (6, 16,
    KEY_ESCAPE,    KEY_F1,    KEY_F2,   KEY_F3,   KEY_F4,   KEY_F5,   KEY_F6,    KEY_F7,   KEY_F8,   KEY_F9,    KEY_F10,       KEY_F11,          KEY_F12,           KEY_PRINT_SCREEN, KEY_OEM_1,      KEY_OEM_2,
    KEY_BACKQUOTE, KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,    KEY_INSERT,     KEY_HOME,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,    KEY_DEL,        KEY_END,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_NONE,          KEY_ENTER,        KEY_PAGE_UP,    KEY_PAGE_DOWN,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_NONE,         KEY_SLASH,         KEY_RSHIFT,       KEY_NONE,       KEY_ARROW_UP,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RALT,  KEY_RMETA,     KEY_FN,           KEY_RCTRL,         KEY_ARROW_LEFT,   KEY_ARROW_DOWN, KEY_ARROW_RIGHT,
)

LAYOUT_KEYCHRON_Q5_HE = (6, 19,
    KEY_ESCAPE,    KEY_NONE,  KEY_F1,   KEY_F2,   KEY_F3,   KEY_F4,   KEY_F5,    KEY_F6,   KEY_F7,   KEY_F8,    KEY_F9,        KEY_F10,          KEY_F11,           KEY_F12,        KEY_DEL,         KEY_OEM_1,     KEY_OEM_2,         KEY_OEM_3,           KEY_NONE,
    KEY_BACKQUOTE, KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,  KEY_PAGE_UP,     KEY_NUM_LOCK,  KEY_NUMPAD_DIVIDE, KEY_NUMPAD_MULTIPLY, KEY_NUMPAD_SUBTRACT,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,  KEY_PAGE_DOWN,   KEY_NUMPAD7,   KEY_NUMPAD8,       KEY_NUMPAD9,         KEY_NUMPAD_ADD,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_ENTER,         KEY_HOME,       KEY_NONE,        KEY_NUMPAD4,   KEY_NUMPAD5,       KEY_NUMPAD6,         KEY_NONE,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_NONE,         KEY_SLASH,         KEY_RSHIFT,     KEY_ARROW_UP,    KEY_NUMPAD1,   KEY_NUMPAD2,       KEY_NUMPAD3,         KEY_NUMPAD_ENTER,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RMETA, KEY_FN,        KEY_RCTRL,        KEY_ARROW_LEFT,    KEY_ARROW_DOWN, KEY_ARROW_RIGHT, KEY_NONE,      KEY_NUMPAD0,       KEY_NUMPAD_DECIMAL,  KEY_NONE,
)

LAYOUT_KEYCHRON_K2_HE = (6, 16,
    KEY_ESCAPE,    KEY_F1,    KEY_F2,   KEY_F3,   KEY_F4,   KEY_F5,   KEY_F6,    KEY_F7,   KEY_F8,   KEY_F9,    KEY_F10,       KEY_F11,          KEY_F12,           KEY_PRINT_SCREEN, KEY_DEL,         KEY_OEM_2,
    KEY_BACKQUOTE, KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,    KEY_PAGE_UP,     KEY_NONE,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,    KEY_PAGE_DOWN,   KEY_NONE,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_ENTER,         KEY_HOME,         KEY_NONE,        KEY_NONE,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_SLASH,        KEY_RSHIFT,        KEY_ARROW_UP,     KEY_END,         KEY_NONE,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RALT,  KEY_FN,        KEY_RCTRL,        KEY_ARROW_LEFT,    KEY_ARROW_DOWN,   KEY_ARROW_RIGHT, KEY_NONE,
)

LAYOUT_LEMOKEY_P1_HE = (6, 15,
    KEY_ESCAPE,    KEY_F1,    KEY_F2,   KEY_F3,   KEY_F4,   KEY_F5,   KEY_F6,    KEY_F7,   KEY_F8,   KEY_F9,    KEY_F10,       KEY_F11,          KEY_F12,           KEY_DEL,        KEY_NONE,
    KEY_BACKQUOTE, KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,  KEY_HOME,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,  KEY_PAGE_UP,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_ENTER,         KEY_PAGE_DOWN,  KEY_NONE,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_NONE,         KEY_SLASH,         KEY_RSHIFT,     KEY_ARROW_UP,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RMETA, KEY_FN,        KEY_RCTRL,        KEY_ARROW_LEFT,    KEY_ARROW_DOWN, KEY_ARROW_RIGHT,
)

LAYOUT_MADLIONS_MAD60HE = [
    KEY_ESCAPE,    KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_NONE,          KEY_ENTER,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_SLASH,        KEY_NONE,          KEY_RSHIFT,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RMETA, KEY_RALT,      KEY_CTX,          KEY_RCTRL,         KEY_FN,
]

LAYOUT_MADLIONS_MAD68HE = [
    KEY_ESCAPE,    KEY_1,     KEY_2,    KEY_3,    KEY_4,    KEY_5,    KEY_6,     KEY_7,    KEY_8,    KEY_9,     KEY_0,         KEY_MINUS,        KEY_EQUALS,        KEY_BACKSPACE,  KEY_INSERT,
    KEY_TAB,       KEY_Q,     KEY_W,    KEY_E,    KEY_R,    KEY_T,    KEY_Y,     KEY_U,    KEY_I,    KEY_O,     KEY_P,         KEY_BRACKET_LEFT, KEY_BRACKET_RIGHT, KEY_BACKSLASH,  KEY_DEL,
    KEY_CAPS_LOCK, KEY_A,     KEY_S,    KEY_D,    KEY_F,    KEY_G,    KEY_H,     KEY_J,    KEY_K,    KEY_L,     KEY_SEMICOLON, KEY_QUOTE,        KEY_NONE,          KEY_ENTER,      KEY_PAGE_UP,
    KEY_LSHIFT,    KEY_NONE,  KEY_Z,    KEY_X,    KEY_C,    KEY_V,    KEY_B,     KEY_N,    KEY_M,    KEY_COMMA, KEY_PERIOD,    KEY_SLASH,        KEY_RSHIFT,        KEY_ARROW_UP,   KEY_PAGE_DOWN,
    KEY_LCTRL,     KEY_LMETA, KEY_LALT, KEY_NONE, KEY_NONE, KEY_NONE, KEY_SPACE, KEY_NONE, KEY_NONE, KEY_RALT,  KEY_FN,        KEY_RCTRL,        KEY_ARROW_LEFT,    KEY_ARROW_DOWN, KEY_ARROW_RIGHT,
]

_DRUNKDEER_MAP = {
    (0*21)+0:  0x29, (0*21)+2:  0x3A, (0*21)+3:  0x3B, (0*21)+4:  0x3C,
    (0*21)+5:  0x3D, (0*21)+6:  0x3E, (0*21)+7:  0x3F, (0*21)+8:  0x40,
    (0*21)+9:  0x41, (0*21)+10: 0x42, (0*21)+11: 0x43, (0*21)+12: 0x44,
    (0*21)+13: 0x45, (0*21)+14: 0x4C,
    (1*21)+0:  0x35, (1*21)+1:  0x1E, (1*21)+2:  0x1F, (1*21)+3:  0x20,
    (1*21)+4:  0x21, (1*21)+5:  0x22, (1*21)+6:  0x23, (1*21)+7:  0x24,
    (1*21)+8:  0x25, (1*21)+9:  0x26, (1*21)+10: 0x27, (1*21)+11: 0x2D,
    (1*21)+12: 0x2E, (1*21)+13: 0x2A, (1*21)+15: 0x4A,
    (2*21)+0:  0x2B, (2*21)+1:  0x14, (2*21)+2:  0x1A, (2*21)+3:  0x08,
    (2*21)+4:  0x15, (2*21)+5:  0x17, (2*21)+6:  0x1C, (2*21)+7:  0x18,
    (2*21)+8:  0x0C, (2*21)+9:  0x12, (2*21)+10: 0x13, (2*21)+11: 0x2F,
    (2*21)+12: 0x30, (2*21)+13: 0x31, (2*21)+15: 0x4B,
    (3*21)+0:  0x39, (3*21)+1:  0x04, (3*21)+2:  0x16, (3*21)+3:  0x07,
    (3*21)+4:  0x09, (3*21)+5:  0x0A, (3*21)+6:  0x0B, (3*21)+7:  0x0D,
    (3*21)+8:  0x0E, (3*21)+9:  0x0F, (3*21)+10: 0x33, (3*21)+11: 0x34,
    (3*21)+13: 0x28, (3*21)+15: 0x4E,
    (4*21)+0:  0xE1, (4*21)+2:  0x1D, (4*21)+3:  0x1B, (4*21)+4:  0x06,
    (4*21)+5:  0x19, (4*21)+6:  0x05, (4*21)+7:  0x11, (4*21)+8:  0x10,
    (4*21)+9:  0x36, (4*21)+10: 0x37, (4*21)+11: 0x38, (4*21)+13: 0xE5,
    (4*21)+14: 0x52, (4*21)+15: 0x4D,
    (5*21)+0:  0xE0, (5*21)+1:  0xE3, (5*21)+2:  0xE2, (5*21)+6:  0x2C,
    (5*21)+10: 0xE6, (5*21)+11: 0x409,(5*21)+12: 0x65,
    (5*21)+14: 0x50, (5*21)+15: 0x51, (5*21)+16: 0x4F,
}

def drunkdeer_index_to_hid_scancode(i):
    import warnings
    sc = _DRUNKDEER_MAP.get(i, 0)
    if sc == 0:
        warnings.warn(f"Failed to map DrunkDeer key to HID scancode: {i}")
    return sc