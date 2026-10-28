# SW TCA demo: build with coverage, run one test set, produce an HTML report.
#
#   make report SET=f1_statement        statement coverage only
#   make report SET=f1_branch           statement + branch coverage
#   make report SET=f1_branch BUG=1     100% coverage, planted bug not found
#   make report SET=f1_limits BUG=1     boundary tests from the requirements find it
#   make report SET=f2_branch           every decision covered, MC/DC not
#   make report SET=int_one             function / call coverage
#
# The HTML report is written to coverage/index.html.

CC      := gcc-14
GCOV    := gcov-14
GCOVR   ?= $(shell command -v gcovr 2>/dev/null || echo $(HOME)/.local/bin/gcovr)
CFLAGS  := -std=c99 -Wall -Wextra -O0 --coverage -fcondition-coverage
SET     ?= all
BUG     ?= 0

ifeq ($(BUG),1)
SRCDIR := build
else
SRCDIR := src
endif

.PHONY: report clean

report: clean
	mkdir -p build coverage
	cp src/can_node.h build/
	sed 's/if (id > max_id)/if (id >= max_id)/' src/can_node.c > build/can_node.c
	$(CC) $(CFLAGS) -I$(SRCDIR) $(SRCDIR)/can_node.c test/test_demo.c -o build/test_demo
	./build/test_demo $(SET)
	$(GCOVR) --root . --filter '$(SRCDIR)/can_node.c' --gcov-executable $(GCOV) \
	         --txt-metric branch --txt - \
	         --html-details coverage/index.html --html-title "SW TCA demo: $(SET)"
	@echo
	@echo "HTML report: coverage/index.html"

clean:
	rm -rf build coverage
