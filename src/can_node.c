#include "can_node.h"

/* F1 - ASIL B */
bool can_frame_is_valid(uint32_t id, uint8_t dlc, bool extended)
{
    uint32_t max_id = CAN_STD_ID_MAX;

    if (extended) {
        max_id = CAN_EXT_ID_MAX;
    }
    if (dlc > CAN_MAX_DLC) {
        return false;
    }
    if (id > max_id) {
        return false;
    }
    return true;
}

/* F2 - ASIL B */
bool sensor_value_plausible(int16_t value, int16_t previous, bool first_sample)
{
    int32_t delta = (int32_t)value - (int32_t)previous;

    if (delta < 0) {
        delta = -delta;
    }
    if ((value >= SENSOR_MIN) && (value <= SENSOR_MAX) &&
        (first_sample || (delta <= SENSOR_MAX_STEP))) {
        return true;
    }
    return false;
}

/* F3 - ASIL B */
can_err_state_t can_error_state(uint16_t tec, uint16_t rec)
{
    if (tec > CAN_BUSOFF_LIMIT) {
        return CAN_STATE_BUS_OFF;
    }
    if ((tec > CAN_PASSIVE_LIMIT) || (rec > CAN_PASSIVE_LIMIT)) {
        return CAN_STATE_ERROR_PASSIVE;
    }
    return CAN_STATE_ERROR_ACTIVE;
}

/* Integration */
rx_result_t can_rx_handler(const can_msg_t *msg, const sensor_ctx_t *ctx,
                           uint16_t tec, uint16_t rec)
{
    rx_result_t result = RX_REJECTED;
    can_err_state_t state = can_error_state(tec, rec);

    switch (state) {
    case CAN_STATE_ERROR_ACTIVE:
    case CAN_STATE_ERROR_PASSIVE:
        if (can_frame_is_valid(msg->id, msg->dlc, msg->extended) &&
            sensor_value_plausible(msg->value, ctx->previous, ctx->first_sample)) {
            result = RX_ACCEPTED;
        }
        break;
    case CAN_STATE_BUS_OFF:
        result = RX_BUS_OFF;
        break;
    default:
        /* Defensive: unreachable for the states returned by can_error_state() */
        result = RX_FAULT;
        break;
    }
    return result;
}
