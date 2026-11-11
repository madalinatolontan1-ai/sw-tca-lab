/*
 * SW TCA lab: the same tests as in the web app, written with GoogleTest.
 *
 * Every test records the requirement it verifies (RecordProperty), so the
 * XML report can be traced back to the requirements:  make trace
 *
 * Test suites (select them with FILTER, see the Makefile):
 *   F1Statement  three extended frames: 100% statement, branch not complete
 *   F1Branch     + the standard frame: 100% statement and branch
 *   F1Limits     boundary values at and beyond each limit (finds the BUG=1 defect)
 *   F2Mcdc       five tests for four conditions (unique-cause MC/DC)
 *   F2Limits     boundary values for min, max and the step
 *   F3Limits     TEC 127/128, 255/256 and REC 127/128
 *   Integration  function and call coverage of can_rx_handler
 *   FaultInjection  forces a corrupted CAN state (only with FI=1)
 */
extern "C" {
#include "can_node.h"
}
#include <gtest/gtest.h>
#include <ostream>
#include <string>

/* Turns "SWR-F1-02" and an index into a valid GoogleTest name: SWR_F1_02_3 */
static std::string case_name(const char *req, size_t index)
{
    std::string s(req);
    for (char &c : s) {
        if (c == '-') c = '_';
    }
    return s + "_" + std::to_string(index);
}

/* ------------------------------------------------------------------ F1 */
struct F1Case {
    const char *req;
    uint32_t id;
    uint8_t dlc;
    bool extended;
    bool expected;  /* true = frame accepted, false = frame rejected */
};

/* readable test parameters in the failure messages */
void PrintTo(const F1Case &c, std::ostream *os)
{
    *os << c.req << ": id=0x" << std::hex << c.id << std::dec << " dlc=" << int(c.dlc)
        << " extended=" << (c.extended ? "true" : "false") << " expected=" << (c.expected ? "true" : "false");
}

class F1 : public ::testing::TestWithParam<F1Case> {};

TEST_P(F1, CanFrameIsValid)
{
    const F1Case &c = GetParam();
    RecordProperty("requirement", c.req);
    EXPECT_EQ(can_frame_is_valid(c.id, c.dlc, c.extended), c.expected)
        << "id=0x" << std::hex << c.id << std::dec << " dlc=" << int(c.dlc)
        << " extended=" << c.extended << " (" << c.req << ")";
}

#define F1_NAME [](const ::testing::TestParamInfo<F1Case> &i) { return case_name(i.param.req, i.index); }

INSTANTIATE_TEST_SUITE_P(F1Statement, F1, ::testing::Values(
    F1Case{"SWR-F1-01", 0x100, 9, true, false},
    F1Case{"SWR-F1-03", 0x20000000u, 8, true, false},
    F1Case{"SWR-F1-04", 0x100, 8, true, true}), F1_NAME);

INSTANTIATE_TEST_SUITE_P(F1Branch, F1, ::testing::Values(
    F1Case{"SWR-F1-02", 0x800, 8, false, false}), F1_NAME);

INSTANTIATE_TEST_SUITE_P(F1Limits, F1, ::testing::Values(
    F1Case{"SWR-F1-01", 0x100, 8, false, true},           /* DLC exactly at the limit */
    F1Case{"SWR-F1-01", 0x100, 9, false, false},          /* DLC just beyond */
    F1Case{"SWR-F1-02", 0x7FF, 8, false, true},           /* standard ID at the limit */
    F1Case{"SWR-F1-02", 0x800, 8, false, false},          /* standard ID just beyond */
    F1Case{"SWR-F1-03", 0x1FFFFFFFu, 8, true, true},      /* extended ID at the limit */
    F1Case{"SWR-F1-03", 0x20000000u, 8, true, false}),    /* extended ID just beyond */
    F1_NAME);

/* ------------------------------------------------------------------ F2 */
struct F2Case {
    const char *req;
    int16_t value;
    int16_t previous;
    bool first_sample;
    bool expected;  /* true = value accepted (plausible), false = rejected */
};

void PrintTo(const F2Case &c, std::ostream *os)
{
    *os << c.req << ": value=" << c.value << " previous=" << c.previous
        << " first_sample=" << (c.first_sample ? "true" : "false") << " expected=" << (c.expected ? "true" : "false");
}

class F2 : public ::testing::TestWithParam<F2Case> {};

TEST_P(F2, SensorValuePlausible)
{
    const F2Case &c = GetParam();
    RecordProperty("requirement", c.req);
    EXPECT_EQ(sensor_value_plausible(c.value, c.previous, c.first_sample), c.expected)
        << "value=" << c.value << " previous=" << c.previous
        << " first_sample=" << c.first_sample << " (" << c.req << ")";
}

#define F2_NAME [](const ::testing::TestParamInfo<F2Case> &i) { return case_name(i.param.req, i.index); }

/* Decision at line 28: A && B && (C || D). Pairs: D T1-T2, C T2-T3, A T1-T4, B T1-T5 */
INSTANTIATE_TEST_SUITE_P(F2Mcdc, F2, ::testing::Values(
    F2Case{"SWR-F2-04", 1000, 1050, false, true},    /* T1 base: A B D true          */
    F2Case{"SWR-F2-04", 1000, 1100, false, false},   /* T2 only D false              */
    F2Case{"SWR-F2-03", 1000, 2000, true, true},     /* T3 C true, D not evaluated   */
    F2Case{"SWR-F2-01", 1, 0, true, false},          /* T4 A false                   */
    F2Case{"SWR-F2-02", 2501, 2500, true, false}),   /* T5 B false                   */
    F2_NAME);

INSTANTIATE_TEST_SUITE_P(F2Limits, F2, ::testing::Values(
    F2Case{"SWR-F2-01", 2, 2, true, true},           /* min exactly       */
    F2Case{"SWR-F2-02", 2500, 2500, false, true},    /* max exactly       */
    F2Case{"SWR-F2-04", 1080, 1000, false, true},    /* step = 80         */
    F2Case{"SWR-F2-04", 1081, 1000, false, false}),  /* step = 81         */
    F2_NAME);

/* ------------------------------------------------------------------ F3 */
struct F3Case {
    const char *req;
    uint16_t tec;
    uint16_t rec;
    can_err_state_t expected;
};

void PrintTo(const F3Case &c, std::ostream *os)
{
    static const char *names[] = {"ERROR_ACTIVE", "ERROR_PASSIVE", "BUS_OFF"};
    *os << c.req << ": tec=" << c.tec << " rec=" << c.rec << " expected=" << names[c.expected];
}

class F3 : public ::testing::TestWithParam<F3Case> {};

TEST_P(F3, CanErrorState)
{
    const F3Case &c = GetParam();
    RecordProperty("requirement", c.req);
    EXPECT_EQ(can_error_state(c.tec, c.rec), c.expected)
        << "tec=" << c.tec << " rec=" << c.rec << " (" << c.req << ")";
}

#define F3_NAME [](const ::testing::TestParamInfo<F3Case> &i) { return case_name(i.param.req, i.index); }

INSTANTIATE_TEST_SUITE_P(F3Limits, F3, ::testing::Values(
    F3Case{"SWR-F3-01", 256, 0, CAN_STATE_BUS_OFF},
    F3Case{"SWR-F3-02", 255, 0, CAN_STATE_ERROR_PASSIVE},
    F3Case{"SWR-F3-02", 128, 0, CAN_STATE_ERROR_PASSIVE},
    F3Case{"SWR-F3-03", 127, 0, CAN_STATE_ERROR_ACTIVE},
    F3Case{"SWR-F3-02", 0, 128, CAN_STATE_ERROR_PASSIVE},
    F3Case{"SWR-F3-03", 0, 127, CAN_STATE_ERROR_ACTIVE}), F3_NAME);

/* ------------------------------------------------------------------ Integration */
static rx_result_t rx(uint32_t id, uint8_t dlc, int16_t value, uint16_t tec)
{
    can_msg_t msg = {id, dlc, false, value};
    sensor_ctx_t ctx = {1050, false};
    return can_rx_handler(&msg, &ctx, tec, 0);
}

TEST(Integration, AcceptsValidFrame)
{
    RecordProperty("requirement", "SWR-INT-02");
    EXPECT_EQ(rx(0x100, 8, 1000, 0), RX_ACCEPTED);
}

TEST(Integration, DiscardsFrameWhenBusOff)
{
    RecordProperty("requirement", "SWR-INT-01");
    EXPECT_EQ(rx(0x100, 8, 1000, 300), RX_BUS_OFF);
}

TEST(Integration, RejectsInvalidFrame)
{
    RecordProperty("requirement", "SWR-INT-03");
    EXPECT_EQ(rx(0x100, 9, 1000, 0), RX_REJECTED);
}

TEST(Integration, RejectsImplausibleValue)
{
    RecordProperty("requirement", "SWR-INT-03");
    EXPECT_EQ(rx(0x100, 8, 3000, 0), RX_REJECTED);
}

/* ------------------------------------------------------------------ Fault injection
 * Built only with FI=1. The Makefile redirects the call to can_error_state()
 * inside can_rx_handler() to this stub, which can return a corrupted state.
 * This reaches the defensive default branch (ISO 26262-6, Table 7, 1l).
 */
#ifdef FAULT_INJECTION
static bool inject_corrupted_state = false;

extern "C" can_err_state_t fi_can_error_state(uint16_t tec, uint16_t rec)
{
    if (inject_corrupted_state) {
        return (can_err_state_t)0xFF;
    }
    return can_error_state(tec, rec);
}

TEST(FaultInjection, CorruptedStateGivesRxFault)
{
    RecordProperty("requirement", "defensive code (MISRA C:2012 rule 16.4)");
    inject_corrupted_state = true;
    EXPECT_EQ(rx(0x100, 8, 1000, 0), RX_FAULT);
    inject_corrupted_state = false;
}
#endif
