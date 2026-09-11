# softsec-toolkit
### Code cho cac bai tap trong slide "CSE703093 - An toan phan mem" (Chuong 1-4)

Bo code nay hien thuc hoa **tat ca bai tap co the "viet code"** trong 8 file
slide (`Chuong1_Phan1/2`, `Chuong2_Phan1/2`, `Chuong3_Phan1/2`,
`Chuong4_Phan1/2`). Moi bai tap deu da duoc **bien dich/chay that** trong qua
trinh xay dung (khong chi viet ma tren ly thuyet) bang: `gcc` +
`-fsanitize=address/undefined` (ASan/UBSan), `cppcheck`, `valgrind`, `cbmc`,
va `z3-solver` (Python). Ket qua thuc te duoc trich dan trong bang duoi day.

Cai dat moi truong: xem [`SETUP.md`](SETUP.md).

Cac bai tap **thuan khai niem** (khong co "ngon ngu tuong ung" - vd phan
loai STRIDE, ve trust boundary, dien risk matrix, thiet ke test case bang
loi khong kem ham cu the...) **khong** duoc lam thanh file code rieng vi
khong co gi de "chay" - dap an cua chung la mot doan van/bang, khong phai
chuong trinh. Danh sach day du o cuoi file.

---

## Chuong 1 - Gioi thieu An toan Phan mem (`ch1_models/`)

| Bai tap (slide) | File | Lenh chay | Ket qua |
|---|---|---|---|
| EP/BVA tu dong, Cyclomatic Complexity, Branch Coverage f(a,b), Decision Table bao hiem | `ch1_models/testing.py` | `python3 ch1_models/testing.py` | 4 test case bien `[(7,F),(8,T),(20,T),(21,F)]`; **V(G)=3**; coverage 1 test = 60% statement/50% branch, thieu `['a<=0','b<=0_given_a>0']`; 3 test bo sung -> 100%/100% |
| Test Automation (pytest): age validator + password EP/BVA | `ch1_models/tests/test_testing.py` | `pytest ch1_models/tests/test_testing.py -v` | **4 passed** |
| Kripke Structure: counter, den giao thong, vending machine, ATM tong hop | `ch1_models/kripke.py` | `python3 ch1_models/kripke.py` | `reachable_states()={0,1,2,3}`; `AG EF red = True`; vending: `dispensing` reachable, `stuck` KHONG reachable; **ATM khong an toan: phat hien duong `no_card->card_inserted->transaction` bo qua `pin_verified`** |

## Chuong 2 - Loi bo nho & Static Analysis trong C (`ch2_memsafe/`)

| Bai tap (slide) | File | Lenh chay | Ket qua |
|---|---|---|---|
| Tim loi Linked List (Use-After-Free) | `01_linked_list_uaf.c` | `gcc -fsanitize=address -g -DDEMO_BUG -o /tmp/a 01_linked_list_uaf.c && /tmp/a` | **ASan: `heap-use-after-free`** tai dong `printf("Removed: %d\n", old_head->data)` |
| Phat hien Memory Leak | `02_memory_leak.c` | `gcc -g -DDEMO_LEAK -o /tmp/a 02_memory_leak.c && valgrind --leak-check=full /tmp/a` | **Valgrind: "4 bytes in 1 blocks are definitely lost"** |
| Xac dinh UB (tran so co dau) | `03_ub_signed_overflow.c` | `gcc -fsanitize=undefined -g -o /tmp/a 03_ub_signed_overflow.c && /tmp/a` | **UBSan: "signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'"**; `safe_add()` tu choi an toan |
| Sua 3 doan ma khong an toan (greet/make_array/read_line) | `04_unsafe_fixes.c` | `gcc -fsanitize=address -g -o /tmp/a 04_unsafe_fixes.c && /tmp/a` | Ban an toan chay dung; ban loi (`-DDEMO_UNSAFE`) bi **ASan: `heap-buffer-overflow`** |
| Gioi han do sau de quy an toan | `05_recursion_depth.c` | `gcc -g -o /tmp/a 05_recursion_depth.c && /tmp/a` | Voi 1000 dau `(`: **chan tai depth 100, khong stack overflow** |
| Tinh/toi uu kich thuoc Struct (4 bai) | `06_struct_alignment.c` | `gcc -g -o /tmp/a 06_struct_alignment.c && /tmp/a` | `Data`=**24 byte**; `Mixed` 32→**16 byte** (toi uu); `Point`=**12 byte**; Protocol default=8 byte, `__attribute__((packed))`=**5 byte** |
| Chay cppcheck tren ma da hoc | `07_cppcheck_demo.c` | `cppcheck --enable=all --inconclusive 07_cppcheck_demo.c` | Canh bao `strcpy`/`strcat` khong an toan (bufferAccessOutOfBounds tiem an); xac nhan cppcheck **khong** tu phat hien duoc leak (can biet ngu canh caller) |
| Viet Rule tuy chinh (phat hien `system()`) | `pattern_scanner.py` | `python3 ch2_memsafe/pattern_scanner.py` | Quet 3 file, bao cao dung dong/ham vi pham (`strcpy`, `strcat`...) |
| Bai tong hop: module quan ly Sinh vien | `08_student_module.c` | `gcc -fsanitize=address -g -o /tmp/a 08_student_module.c && /tmp/a` roi `valgrind --leak-check=full /tmp/a` (ban khong ASan) | `sizeof(Student)=56 byte`; **Valgrind: "All heap blocks were freed -- no leaks are possible"** |
| Bai thuc hanh mo rong: Product List | `09_product_list_extended.c` | `gcc -fsanitize=address -g -o /tmp/a 09_product_list_extended.c && /tmp/a` | Chay dung voi ca 2 du lieu bien (danh sach rong, xoa id khong ton tai) khong crash; `sizeof(Product)=48 byte` |

## Chuong 3 - Kiem chung hinh thuc: SAT/SMT/BMC (`ch3_verify/`)

| Bai tap (slide) | File | Lenh chay | Ket qua |
|---|---|---|---|
| Giai SAT bang tay: `(a v ~b) ^ (b v c) ^ (~a v ~c)` | `01_sat_manual.py` | `python3 ch3_verify/01_sat_manual.py` | Brute-force + Z3 deu xac nhan **SAT**, 2/8 phep gan thoa man, vd `a=F,b=F,c=T` |
| Viet rang buoc SMT (age/license) | `02_smt_examples.py` | `python3 ch3_verify/02_smt_examples.py` | **sat**, vd `age=18, has_license=True` |
| Phan tich CNF `(a^b)vc` | (cung file, muc 2) | " | **unsat** khi so sanh voi `(avc)^(bvc)` -> xac nhan **tuong duong** |
| Bit-vector: `unsigned char 250+10` | (cung file, muc 3) | " | `simplify(...) = 4` (260 mod 256) |
| Tu ma nguon toi SMT: `a+b==c && a>0 && b>0` | (cung file, muc 4) | " | **sat**, vd `a=1,b=1,c=2` |
| Ma hoa BMC bang tay (k=1) | `03_bmc_manual.py` | `python3 ch3_verify/03_bmc_manual.py` | **sat**, `s0=0, s1=1` -> trang thai xau dat duoc sau 1 buoc |
| Xac dinh gia tri Unwind (mang tinh, n<=15) | `04_cbmc_unwind_demo.c` | `cbmc 04_cbmc_unwind_demo.c --bounds-check --unwind 10/16 --function main` | `--unwind 10`: **VERIFICATION SUCCESSFUL (sai, khong du bao phu)**; `--unwind 16`: **VERIFICATION FAILED** - phat hien dung `array_bounds` loi |
| BMC voi vong lap `sum_array` (n<=50) | `05_bmc_loop_demo.c` | `cbmc 05_bmc_loop_demo.c --unwind 30/51 --unwinding-assertions --function main` | `--unwind 30`: **`unwinding assertion: FAILURE`** (khong du); `--unwind 51`: **VERIFICATION SUCCESSFUL** |
| Mo hinh hoa Double-Free bang `valid_map` | `06_memory_model_doublefree.py` | `python3 ch3_verify/06_memory_model_doublefree.py` | Khong kiem tra: **sat** (double-free co the xay ra); co kiem tra: **unsat** (da chan) |
| Kiem chung Alignment bang Z3 (allocator boi so 4) | `07_alignment_z3.py` | `python3 ch3_verify/07_alignment_z3.py` | **sat**, vd `addr=4` vi pham yeu cau align-8 |
| Chung minh tinh chat Alignment (`arr[2]`) | (cung file, muc 2) | " | **unsat** (khong co phan vi du) -> tinh chat **dung** |
| Bai tong hop: CBMC packet parser (buffer overflow) | `08_cbmc_packet_parser.c` | `cbmc 08_cbmc_packet_parser.c [-DDEMO_BUGGY] --bounds-check --pointer-check --unwind 301 --function main` | Ban loi: **VERIFICATION FAILED** - `pointer outside object bounds in out_buf`; ban sua: **VERIFICATION SUCCESSFUL** (0 of 24 failed) |

## Chuong 4 - Fuzzing & Symbolic/Concolic Execution (`ch4_dynafuzz/`)

| Bai tap (slide) | File | Lenh chay | Ket qua |
|---|---|---|---|
| Xac dinh input "ac y" cho `process_name()` | `01_malicious_input.py` + `01b_malicious_input_harness.c` | `python3 ch4_dynafuzz/01_malicious_input.py` roi `gcc -fsanitize=address -g -o /tmp/a 01b_malicious_input_harness.c && /tmp/a` | Mo phong xac dinh 3 input nguy hiem; xac nhan that: **ASan `stack-buffer-overflow` (WRITE of size 100)** |
| Xay dung Seed Corpus (JSON parser) | `02_seed_corpus.py` | `python3 ch4_dynafuzz/02_seed_corpus.py` | Sinh **4 file seed that** vao `/tmp/json_fuzz_corpus/` (valid/nested/mixed-type/unicode) |
| Tinh Edge Coverage cho `f(a,b)` (4 nhanh A/B/C/D) | `03_edge_coverage.py` | `python3 ch4_dynafuzz/03_edge_coverage.py` | 2 test case -> **2/4 nhanh (50%)**: `A, D`; thieu `B, C` |
| Sinh duong thuc thi (concolic) cho `classify(x,y)` | `04_concolic_execution.py` | `python3 ch4_dynafuzz/04_concolic_execution.py` | Tu `(5,5)`->nhanh 1; phu dinh dieu kien -> **sinh `(1,0)`->nhanh 2** va **`(0,*)`->nhanh 3** (Z3 xac nhan) |
| So sanh DFS vs Coverage-guided (10 dieu kien, ngan sach 50) | `05_dfs_vs_coverage_guided.py` | `python3 ch4_dynafuzz/05_dfs_vs_coverage_guided.py` | DFS: chi **2 duong phan biet**, 11/20 (55%) to hop kham pha; Coverage-guided: **50 duong phan biet**, 20/20 (100%) |
| Thiet ke White-box Fuzzing cho `check(code)==0x1337` | `06_white_box_fuzzing.py` | `python3 ch4_dynafuzz/06_white_box_fuzzing.py` | Z3: **sat, code=4919 (0x1337)** ngay lap tuc; black-box: **0/2,000,000 lan thu ngau nhien** trung |
| Xac dinh Infeasible Path (`unsigned x`, `x<0`) | `07_infeasible_path.py` | `python3 ch4_dynafuzz/07_infeasible_path.py` | **unsat** -> nhanh `crash()` khong bao gio dat duoc |
| Thiet ke chien luoc Dot bien (magic+len+payload) | `08_mutation_strategy.py` | `python3 ch4_dynafuzz/08_mutation_strategy.py` | 3 lan dot bien mau: magic giu nguyen, truong do dai bi bien doi arithmetic, payload bi bit-flip |
| Tinh xac suat sinh tu khoa "BEGIN" bang random mutation | `09_dictionary_probability.py` | `python3 ch4_dynafuzz/09_dictionary_probability.py` | Khong dictionary: **P=9.1e-13**; mo phong 2 trieu lan: **0 lan trung**; co dictionary (20 tu): **P=0.05** (~5.5e10 lan cao hon) |
| Uoc luong chi phi Symbolic Execution (doc lap vs long nhau) | `10_symbolic_cost.py` | `python3 ch4_dynafuzz/10_symbolic_cost.py` | 20 nhanh doc lap: **~20 lan goi solver**; 10 tang long nhau: **2^10 = 1,024 lan** (path explosion) |

---

## Bai tap THUAN KHAI NIEM (khong lam file code - khong co "ngon ngu tuong ung")

Cac bai duoi day yeu cau tra loi bang loi/bang/so do (STRIDE classification,
ve trust boundary diagram, dien risk matrix, liet ke checklist code review,
mo ta quy trinh SDLC, so sanh SAST/DAST bang van ban, thiet ke test case
"tren giay" khong kem ham C/Python cu the, v.v.) - day la dac diem cua mon
hoc ly thuyet an toan phan mem, KHONG phai loi thieu sot cua bo code nay.

---

## Cau truc thu muc

```
softsec-toolkit/
├── README.md              <- file nay
├── SETUP.md                <- huong dan cai dat
├── requirements.txt
├── ch1_models/              (testing.py, kripke.py, tests/)
├── ch2_memsafe/              (9 file .c + pattern_scanner.py)
├── ch3_verify/                (4 file .py + 3 file .c cho CBMC)
└── ch4_dynafuzz/                (10 file, .py + 1 harness .c)
```
