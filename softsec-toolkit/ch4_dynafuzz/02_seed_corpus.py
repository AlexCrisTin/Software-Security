"""
Bai tap: Xay dung Seed Corpus (Chuong4_Phan1, slide 324)
Fuzzing mot ham phan tich cu phap JSON tu viet bang C. De xuat 4 loai input
nen co trong seed corpus ban dau.

Ngoai viec liet ke (nhu dap an slide), file nay TAO RA cac seed that duoi
dang file, mo phong buoc chuan bi corpus truoc khi chay fuzzer (vd AFL/libFuzzer).
"""
import json
import os

SEED_DIR = "/tmp/json_fuzz_corpus"


def build_seed_corpus():
    seeds = {
        "01_simple_valid.json": '{"key": "value"}',
        "02_nested_deep.json": json.dumps({"a": {"b": {"c": {"d": [1, 2, [3, 4]]}}}}),
        "03_mixed_types.json": json.dumps({
            "num": 42, "str": "hello", "bool": True, "null": None,
            "empty_array": [], "empty_object": {}
        }),
        "04_unicode_escape.json": '{"text": "\\u0041 \\"quoted\\" \\u00e9moji"}',
    }
    os.makedirs(SEED_DIR, exist_ok=True)
    for filename, content in seeds.items():
        path = os.path.join(SEED_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return seeds


if __name__ == "__main__":
    print("== Bai tap: Xay dung Seed Corpus cho fuzzing JSON parser (C) ==\n")
    seeds = build_seed_corpus()
    for i, (name, content) in enumerate(seeds.items(), start=1):
        print(f"{i}. {name}")
        print(f"   noi dung: {content[:80]}")
    print(f"\nDa ghi {len(seeds)} seed file vao {SEED_DIR}/")
    print("(dung lam corpus ban dau cho: afl-fuzz -i", SEED_DIR, "-o output -- ./json_parser @@)")
