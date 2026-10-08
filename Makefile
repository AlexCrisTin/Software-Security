PYTHON ?= python
CC := clang
CXX := clang++
ASAN_CXX := clang++

BUILD_DIR := build
BUGGY_EXE := $(BUILD_DIR)/lock2_buggy.exe
FIXED_EXE := $(BUILD_DIR)/lock2_fixed.exe
FIXED_ASAN_EXE := $(BUILD_DIR)/lock2_fixed_asan.exe
SAN_EXE := $(BUILD_DIR)/smart_lock_san.exe

.DEFAULT_GOAL := help
.RECIPEPREFIX := >

.PHONY: help setup dirs build buggy fixed fixed-asan kripke unit bmc smt static san-build \
	overflow double-free use-after-free integer-overflow leak spec framework \
	verify demo clean

help:
>@echo "Smart Lock Formal Verification"
>@echo ""
>@echo "Cai dat:"
>@echo "  make setup             Cai z3-solver"
>@echo ""
>@echo "Mo hinh va kiem chung:"
>@echo "  make buggy             Bien dich va chay phien ban CWE-287"
>@echo "  make fixed             Bien dich va chay phien ban da sua"
>@echo "  make fixed-asan        Chay phien ban v1 voi AddressSanitizer"
>@echo "  make kripke            Chay mo hinh Kripke v0/v1"
>@echo "  make unit              Chay unit test mo hinh Kripke"
>@echo "  make bmc               Chay 6 truy van BMC bang Z3"
>@echo "  make smt               Kiem tra overflow/bounded bang Z3"
>@echo "  make spec              Kiem tra cu phap JSON dac ta"
>@echo ""
>@echo "Phan tich tinh va sanitizer:"
>@echo "  make static            Chay Clang Static Analyzer"
>@echo "  make overflow          ASan: stack-buffer-overflow"
>@echo "  make double-free       ASan: double-free"
>@echo "  make use-after-free    ASan: heap-use-after-free"
>@echo "  make integer-overflow  UBSan: signed integer overflow"
>@echo "  make leak              Chay nhanh leak"
>@echo ""
>@echo "Tong hop:"
>@echo "  make verify            Chay cac kiem tra khong co chu dich crash"
>@echo "  make demo              Chay chuoi trinh dien chinh"
>@echo "  make framework         Mo SecLabFramework de ve CFG"
>@echo "  make clean             Xoa thu muc build"

setup:
>$(PYTHON) -m pip install z3-solver

dirs:
>mkdir -p $(BUILD_DIR)

$(BUGGY_EXE): source/buggy/lock2_buggy.cpp | dirs
>$(CXX) -std=c++17 -Wall -Wextra -O0 $< -o $@

$(FIXED_EXE): source/src/lock2.cpp | dirs
>$(CXX) -std=c++17 -Wall -Wextra -O0 $< -o $@

$(FIXED_ASAN_EXE): source/src/lock2.cpp | dirs
>$(ASAN_CXX) -std=c++17 -g -O0 -fsanitize=address -fno-omit-frame-pointer $< -o $@

$(SAN_EXE): source/ch2_memsafe/smart_lock_cwe_samples.c | dirs
>$(CC) -std=c17 -g -O0 -fsanitize=address,undefined \
>	-fno-omit-frame-pointer $< -o $@

build: $(BUGGY_EXE) $(FIXED_EXE) $(FIXED_ASAN_EXE) $(SAN_EXE)

buggy: $(BUGGY_EXE)
>$(BUGGY_EXE)

fixed: $(FIXED_EXE)
>$(FIXED_EXE)

fixed-asan: $(FIXED_ASAN_EXE)
>$(FIXED_ASAN_EXE)

kripke:
>$(PYTHON) -m source.buggy.build_lock_kripke

unit:
>$(PYTHON) -m unittest source.ch1_models.tests.test_smart_lock_model -v

bmc:
>$(PYTHON) source/ch3_verify/smart_lock_bmc.py

smt:
>$(PYTHON) source/ch3_verify/smart_lock_extended_smt.py

static:
>$(CC) --analyze -Xanalyzer -analyzer-output=text -Wall -Wextra \
>	source/ch2_memsafe/smart_lock_cwe_samples.c

san-build: $(SAN_EXE)

# Cac target nay co chu dich lam sanitizer dung chuong trinh. Dau '-' bao make
# tiep tuc va coi exit code khac 0 la ket qua mong doi cua bai thu loi.
overflow: $(SAN_EXE)
>-$(SAN_EXE) overflow

double-free: $(SAN_EXE)
>-$(SAN_EXE) double-free

use-after-free: $(SAN_EXE)
>-$(SAN_EXE) use-after-free

integer-overflow: $(SAN_EXE)
>-$(SAN_EXE) integer

leak: $(SAN_EXE)
>$(SAN_EXE) leak
>@echo "Neu Windows khong bao leak, chay 'make static' de xem CWE-401."

spec:
>$(PYTHON) -c "import json; p='source/specs/smart_lock_spec.json'; d=json.load(open(p, encoding='utf-8')); print('SPEC OK:', d['name']); print('Requirements:', len(d.get('requirements', []))); print('Test cases:', len(d.get('test_cases', [])))"

framework:
>powershell.exe -NoProfile -Command "Start-Process -FilePath '.\\SecLabFramework.exe'"

verify: fixed fixed-asan kripke unit bmc smt static spec

demo: buggy fixed fixed-asan kripke unit bmc smt static spec

clean:
>powershell.exe -NoProfile -Command "if (Test-Path -LiteralPath '$(BUILD_DIR)') { Remove-Item -LiteralPath '$(BUILD_DIR)' -Recurse -Force }"
