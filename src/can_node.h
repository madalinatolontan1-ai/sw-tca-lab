#ifndef CAN_NODE_H
#define CAN_NODE_H

#include <stdint.h>
#include <stdbool.h>

/* CAN frame limits (ISO 11898-1) */
#define CAN_MAX_DLC        8u
#define CAN_STD_ID_MAX     0x7FFu
#define CAN_EXT_ID_MAX     0x1FFFFFFFu

/* Front radar, object longitudinal distance, unit 0.1 m */
#define SENSOR_MIN         2        /*   0.2 m */
#define SENSOR_MAX         2500     /* 250.0 m */
#define SENSOR_MAX_STEP    80       /*   8.0 m per 72 ms cycle */

/* CAN fault confinement (ISO 11898-1) */
#define CAN_PASSIVE_LIMIT  127u
#define CAN_BUSOFF_LIMIT   255u

typedef enum {
    CAN_STATE_ERROR_ACTIVE,
    CAN_STATE_ERROR_PASSIVE,
    CAN_STATE_BUS_OFF
} can_err_state_t;

typedef enum {
    RX_ACCEPTED,
    RX_REJECTED,
    RX_BUS_OFF,
    RX_FAULT
} rx_result_t;

typedef struct {
    uint32_t id;
    uint8_t  dlc;
    bool     extended;
    int16_t  value;
} can_msg_t;

typedef struct {
    int16_t previous;
    bool    first_sample;
} sensor_ctx_t;

bool can_frame_is_valid(uint32_t id, uint8_t dlc, bool extended);
bool sensor_value_plausible(int16_t value, int16_t previous, bool first_sample);
can_err_state_t can_error_state(uint16_t tec, uint16_t rec);
rx_result_t can_rx_handler(const can_msg_t *msg, const sensor_ctx_t *ctx,
                           uint16_t tec, uint16_t rec);

#endif
