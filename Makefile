# SW TCA demo: build with coverage, run one test set, produce an HTML report.
#
#   make report SET=f1_statement        statement coverage only
#   make report SET=f1_branch           statement + branch coverage
#   make report SET=f1_branch BUG=1     100% coverage, planted bug not found
#   make report SET=f1_limits BUG=1     boundary tests from the requirements find it
#   make report SET=f2_branch           every decision covered, MC/DC not
#   make report SET=int_one             function / call coverage
#
# The same functions tested with GoogleTest (test/test_gtest.cpp):
#
#   make gtest                          every suite, report + MC/DC + traceability
#   make gtest FILTER='F1Statement*'    one suite (F1Statement, F1Branch, F1Limits,
#                                       F2Mcdc, F2Limits, F3Limits, Integration)
#   make gtest FILTER='F1Statement*:F1Branch*' BUG=1   100% coverage, bug not found
#   make gtest FILTER='F1Limits*' BUG=1                boundary tests find it
#   make gtest FI=1                     fault injection reaches the default branch
#
# The HTML report is written to coverage/index.html.
# Open it in the browser with:  make serve

CC      := gcc-14
CXX     := g++-14
GCOV    := gcov-14
GCOVR   ?= $(shell command -v gcovr 2>/dev/null || echo $(HOME)/.local/bin/gcovr)
CFLAGS  := -std=c99 -Wall -Wextra -O0 --coverage -fcondition-coverage
SET     ?= all
BUG     ?= 0
FI      ?= 0
FILTER  ?= *

ifeq ($(BUG),1)
SRCDIR := build
else
SRCDIR := src
endif

.PHONY: report gtest trace serve clean

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
	@echo "HTML report: coverage/index.html  (open it with: make serve)"

# GoogleTest build: the C code keeps coverage and condition (MC/DC) instrumentation,
# the C++ test file does not. BUG=1 plants the V0 defect, FI=1 adds the
# fault-injection hook (the call to can_error_state() inside can_rx_handler()
# goes through fi_can_error_state(), defined in the test file).
gtest: clean
	mkdir -p build coverage
	cp src/can_node.h build/
	cp src/can_node.c build/can_node.c
ifeq ($(BUG),1)
	sed -i 's/if (id > max_id)/if (id >= max_id)/' build/can_node.c
endif
ifeq ($(FI),1)
	sed -i 's/= can_error_state(tec, rec);/= fi_can_error_state(tec, rec);/' build/can_node.c
	sed -i '1a can_err_state_t fi_can_error_state(uint16_t tec, uint16_t rec);' build/can_node.c
endif
	$(CC) $(CFLAGS) -Ibuild -c build/can_node.c -o build/can_node.o
	$(CXX) -std=c++17 -Wall -O0 -Ibuild $(if $(filter 1,$(FI)),-DFAULT_INJECTION) \
	       test/test_gtest.cpp build/can_node.o --coverage -lgtest -lgtest_main -pthread -o build/test_gtest
	-./build/test_gtest --gtest_filter='$(FILTER)' --gtest_output=xml:build/results.xml
	$(GCOVR) --root . --filter 'build/can_node.c' --gcov-executable $(GCOV) \
	         --txt-metric line --txt-metric branch --txt-metric condition --txt - \
	         --html-details coverage/index.html --html-title "SW TCA, GoogleTest: $(FILTER)"
	@echo
	@echo "Lines executed, per function:"
	@$(GCOV) -f -n -o build build/can_node.c | awk '/^Function/ {f=$$2; gsub(sprintf("%c",39),"",f)} /^Lines executed/ && f {sub(/executed:/,"",$$2); printf "  %-24s %s of %s lines\n", f, $$2, $$4; f=""}'
	@echo
	@python3 tools/trace.py build/results.xml
	@echo
	@echo "HTML report: coverage/index.html  (open it with: make serve)"

trace:
	python3 tools/trace.py build/results.xml

serve:
	python3 -m http.server 8080 --directory coverage

clean:
	rm -rf build coverage
