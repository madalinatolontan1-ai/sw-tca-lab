/*
 * Demo test driver for the SW TCA course.
 * Each test set is selected on the command line, so the coverage of
 * different test sets can be compared:  make report SET=f1_statement
 */
#include <stdio.h>
#include <string.h>
#include "can_node.h"

static int failed = 0;

static void check(const char *id, int got, int expected)
{
    printf("%-7s %s  (got %d, expected %d)\n", id,
           (got == expected) ? "PASS" : "FAIL", got, expected);
    if (got != expected) {
        failed++;
    }
}

static int is(const char *set, const char *name)
{
    return strcmp(set, name) == 0 || strcmp(set, "all") == 0;
}

int main(int argc, char **argv)
{
    const char *set = (argc > 1) ? argv[1] : "all";

    /* F1: statement coverage only (all frames are extended) */
    if (is(set, "f1_statement") || is(set, "f1_branch")) {
        check("F1-T1", can_frame_is_valid(0x100, 9, true), false);
        check("F1-T2", can_frame_is_valid(0x20000000u, 8, true), false);
        check("F1-T3", can_frame_is_valid(0x100, 8, true), true);
    }
    /* F1: one more test (standard frame) for branch coverage.
       Run it with BUG=1: coverage stays 100% and every test still passes. */
    if (is(set, "f1_branch")) {
        check("F1-T4", can_frame_is_valid(0x800, 8, false), false);
    }

    /* F1: boundary values taken from the requirements (finds the planted bug) */
    if (is(set, "f1_limits")) {
        check("F1-L1", can_frame_is_valid(0x7FF, 8, false), true);
        check("F1-L2", can_frame_is_valid(0x800, 8, false), false);
        check("F1-L3", can_frame_is_valid(0x1FFFFFFFu, 8, true), true);
        check("F1-L4", can_frame_is_valid(0x100, 8, false), true);
    }

    /* F2: every decision true and false, but no MC/DC */
    if (is(set, "f2_branch")) {
        check("F2-B1", sensor_value_plausible(1000, 1050, false), true);
        check("F2-B2", sensor_value_plausible(2501, 0, true), false);
    }

    /* Integration: function and call coverage */
    if (is(set, "int_one")) {
        can_msg_t msg = {0x100, 8, false, 1000};
        sensor_ctx_t ctx = {990, false};
        check("I-T1", can_rx_handler(&msg, &ctx, 300, 0), RX_BUS_OFF);
    }

    printf("\n%d test(s) failed\n", failed);
    return 0;
}
