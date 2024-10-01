// This file is generated by apc_parsers.py do not edit!

#pragma once

#include "base64.h"
static inline void parse_graphics_code(PS *self, uint8_t *parser_buf,
                                       const size_t parser_buf_pos) {
  unsigned int pos = 1;
  enum PARSER_STATES { KEY, EQUAL, UINT, INT, FLAG, AFTER_VALUE, PAYLOAD };
  enum PARSER_STATES state = KEY, value_state = FLAG;
  static GraphicsCommand g;
  unsigned int i, code;
  uint64_t lcode;
  int64_t accumulator;
  bool is_negative;
  memset(&g, 0, sizeof(g));
  size_t sz;

  enum KEYS {
    action = 'a',
    delete_action = 'd',
    transmission_type = 't',
    compressed = 'o',
    format = 'f',
    more = 'm',
    id = 'i',
    image_number = 'I',
    placement_id = 'p',
    quiet = 'q',
    width = 'w',
    height = 'h',
    x_offset = 'x',
    y_offset = 'y',
    data_height = 'v',
    data_width = 's',
    data_sz = 'S',
    data_offset = 'O',
    num_cells = 'c',
    num_lines = 'r',
    cell_x_offset = 'X',
    cell_y_offset = 'Y',
    z_index = 'z',
    cursor_movement = 'C',
    unicode_placement = 'U',
    parent_id = 'P',
    parent_placement_id = 'Q',
    offset_from_parent_x = 'H',
    offset_from_parent_y = 'V'
  };

  enum KEYS key = 'a';
  if (parser_buf[pos] == ';')
    state = AFTER_VALUE;

  while (pos < parser_buf_pos) {
    switch (state) {
    case KEY:
      key = parser_buf[pos++];
      state = EQUAL;
      switch (key) {
      case action:
        value_state = FLAG;
        break;
      case delete_action:
        value_state = FLAG;
        break;
      case transmission_type:
        value_state = FLAG;
        break;
      case compressed:
        value_state = FLAG;
        break;
      case format:
        value_state = UINT;
        break;
      case more:
        value_state = UINT;
        break;
      case id:
        value_state = UINT;
        break;
      case image_number:
        value_state = UINT;
        break;
      case placement_id:
        value_state = UINT;
        break;
      case quiet:
        value_state = UINT;
        break;
      case width:
        value_state = UINT;
        break;
      case height:
        value_state = UINT;
        break;
      case x_offset:
        value_state = UINT;
        break;
      case y_offset:
        value_state = UINT;
        break;
      case data_height:
        value_state = UINT;
        break;
      case data_width:
        value_state = UINT;
        break;
      case data_sz:
        value_state = UINT;
        break;
      case data_offset:
        value_state = UINT;
        break;
      case num_cells:
        value_state = UINT;
        break;
      case num_lines:
        value_state = UINT;
        break;
      case cell_x_offset:
        value_state = UINT;
        break;
      case cell_y_offset:
        value_state = UINT;
        break;
      case z_index:
        value_state = INT;
        break;
      case cursor_movement:
        value_state = UINT;
        break;
      case unicode_placement:
        value_state = UINT;
        break;
      case parent_id:
        value_state = UINT;
        break;
      case parent_placement_id:
        value_state = UINT;
        break;
      case offset_from_parent_x:
        value_state = INT;
        break;
      case offset_from_parent_y:
        value_state = INT;
        break;
      default:
        REPORT_ERROR("Malformed GraphicsCommand control block, invalid key "
                     "character: 0x%x",
                     key);
        return;
      }
      break;

    case EQUAL:
      if (parser_buf[pos++] != '=') {
        REPORT_ERROR("Malformed GraphicsCommand control block, no = after key, "
                     "found: 0x%x instead",
                     parser_buf[pos - 1]);
        return;
      }
      state = value_state;
      break;

    case FLAG:
      switch (key) {

      case action: {
        g.action = parser_buf[pos++];
        if (g.action != 'T' && g.action != 'a' && g.action != 'c' &&
            g.action != 'd' && g.action != 'f' && g.action != 'p' &&
            g.action != 'q' && g.action != 't') {
          REPORT_ERROR("Malformed GraphicsCommand control block, unknown flag "
                       "value for action: 0x%x",
                       g.action);
          return;
        };
      } break;

      case delete_action: {
        g.delete_action = parser_buf[pos++];
        if (g.delete_action != 'A' && g.delete_action != 'C' &&
            g.delete_action != 'F' && g.delete_action != 'I' &&
            g.delete_action != 'N' && g.delete_action != 'P' &&
            g.delete_action != 'Q' && g.delete_action != 'R' &&
            g.delete_action != 'X' && g.delete_action != 'Y' &&
            g.delete_action != 'Z' && g.delete_action != 'a' &&
            g.delete_action != 'c' && g.delete_action != 'f' &&
            g.delete_action != 'i' && g.delete_action != 'n' &&
            g.delete_action != 'p' && g.delete_action != 'q' &&
            g.delete_action != 'r' && g.delete_action != 'x' &&
            g.delete_action != 'y' && g.delete_action != 'z') {
          REPORT_ERROR("Malformed GraphicsCommand control block, unknown flag "
                       "value for delete_action: 0x%x",
                       g.delete_action);
          return;
        };
      } break;

      case transmission_type: {
        g.transmission_type = parser_buf[pos++];
        if (g.transmission_type != 'd' && g.transmission_type != 'f' &&
            g.transmission_type != 's' && g.transmission_type != 't') {
          REPORT_ERROR("Malformed GraphicsCommand control block, unknown flag "
                       "value for transmission_type: 0x%x",
                       g.transmission_type);
          return;
        };
      } break;

      case compressed: {
        g.compressed = parser_buf[pos++];
        if (g.compressed != 'z') {
          REPORT_ERROR("Malformed GraphicsCommand control block, unknown flag "
                       "value for compressed: 0x%x",
                       g.compressed);
          return;
        };
      } break;

      default:
        break;
      }
      state = AFTER_VALUE;
      break;

    case INT:
#define READ_UINT                                                              \
  for (i = pos, accumulator = 0; i < MIN(parser_buf_pos, pos + 10); i++) {     \
    int64_t n = parser_buf[i] - '0';                                           \
    if (n < 0 || n > 9)                                                        \
      break;                                                                   \
    accumulator += n * digit_multipliers[i - pos];                             \
  }                                                                            \
  if (i == pos) {                                                              \
    REPORT_ERROR("Malformed GraphicsCommand control block, expecting an "      \
                 "integer value for key: %c",                                  \
                 key & 0xFF);                                                  \
    return;                                                                    \
  }                                                                            \
  lcode = accumulator / digit_multipliers[i - pos - 1];                        \
  pos = i;                                                                     \
  if (lcode > UINT32_MAX) {                                                    \
    REPORT_ERROR(                                                              \
        "Malformed GraphicsCommand control block, number is too large");       \
    return;                                                                    \
  }                                                                            \
  code = lcode;

      is_negative = false;
      if (parser_buf[pos] == '-') {
        is_negative = true;
        pos++;
      }
#define I(x)                                                                   \
  case x:                                                                      \
    g.x = is_negative ? 0 - (int32_t)code : (int32_t)code;                     \
    break
      READ_UINT;
      switch (key) {
        I(z_index);
        I(offset_from_parent_x);
        I(offset_from_parent_y);
      default:
        break;
      }
      state = AFTER_VALUE;
      break;
#undef I
    case UINT:
      READ_UINT;
#define U(x)                                                                   \
  case x:                                                                      \
    g.x = code;                                                                \
    break
      switch (key) {
        U(format);
        U(more);
        U(id);
        U(image_number);
        U(placement_id);
        U(quiet);
        U(width);
        U(height);
        U(x_offset);
        U(y_offset);
        U(data_height);
        U(data_width);
        U(data_sz);
        U(data_offset);
        U(num_cells);
        U(num_lines);
        U(cell_x_offset);
        U(cell_y_offset);
        U(cursor_movement);
        U(unicode_placement);
        U(parent_id);
        U(parent_placement_id);
      default:
        break;
      }
      state = AFTER_VALUE;
      break;
#undef U
#undef READ_UINT

    case AFTER_VALUE:
      switch (parser_buf[pos++]) {
      default:
        REPORT_ERROR("Malformed GraphicsCommand control block, expecting a "
                     "comma or semi-colon after a value, found: 0x%x",
                     parser_buf[pos - 1]);
        return;
      case ',':
        state = KEY;
        break;
      case ';':
        state = PAYLOAD;
        break;
      }
      break;

    case PAYLOAD: {
      sz = parser_buf_pos - pos;
      g.payload_sz = MAX(BUF_EXTRA, sz);
      if (!base64_decode8(parser_buf + pos, sz, parser_buf, &g.payload_sz)) {
        g.payload_sz = MAX(BUF_EXTRA, sz);
        REPORT_ERROR("Failed to parse GraphicsCommand command payload with "
                     "error: invalid base64 data in chunk of size: %zu with "
                     "output buffer size: %zu",
                     sz, g.payload_sz);
        return;
      }
      pos = parser_buf_pos;
    } break;

    } // end switch
  }   // end while

  switch (state) {
  case EQUAL:
    REPORT_ERROR("Malformed GraphicsCommand control block, no = after key");
    return;
  case INT:
  case UINT:
    REPORT_ERROR(
        "Malformed GraphicsCommand control block, expecting an integer value");
    return;
  case FLAG:
    REPORT_ERROR(
        "Malformed GraphicsCommand control block, expecting a flag value");
    return;
  default:
    break;
  }

  REPORT_VA_COMMAND(
      "K s {sc sc sc sc sI sI sI sI sI sI sI sI sI sI sI sI sI sI sI sI sI sI "
      "sI sI sI sI si si si sI} y#",
      self->window_id, "graphics_command", "action", g.action, "delete_action",
      g.delete_action, "transmission_type", g.transmission_type, "compressed",
      g.compressed, "format", (unsigned int)g.format, "more",
      (unsigned int)g.more, "id", (unsigned int)g.id, "image_number",
      (unsigned int)g.image_number, "placement_id",
      (unsigned int)g.placement_id, "quiet", (unsigned int)g.quiet, "width",
      (unsigned int)g.width, "height", (unsigned int)g.height, "x_offset",
      (unsigned int)g.x_offset, "y_offset", (unsigned int)g.y_offset,
      "data_height", (unsigned int)g.data_height, "data_width",
      (unsigned int)g.data_width, "data_sz", (unsigned int)g.data_sz,
      "data_offset", (unsigned int)g.data_offset, "num_cells",
      (unsigned int)g.num_cells, "num_lines", (unsigned int)g.num_lines,
      "cell_x_offset", (unsigned int)g.cell_x_offset, "cell_y_offset",
      (unsigned int)g.cell_y_offset, "cursor_movement",
      (unsigned int)g.cursor_movement, "unicode_placement",
      (unsigned int)g.unicode_placement, "parent_id", (unsigned int)g.parent_id,
      "parent_placement_id", (unsigned int)g.parent_placement_id, "z_index",
      (int)g.z_index, "offset_from_parent_x", (int)g.offset_from_parent_x,
      "offset_from_parent_y", (int)g.offset_from_parent_y, "payload_sz",
      g.payload_sz, parser_buf, g.payload_sz);

  screen_handle_graphics_command(self->screen, &g, parser_buf);
}
