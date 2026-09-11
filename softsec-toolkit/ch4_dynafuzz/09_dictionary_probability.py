"""
Bai tap: Tinh xac suat sinh tu khoa bang random mutation (Chuong4_Phan2)

Fuzzer can sinh chuoi "BEGIN" (5 ky tu ASCII in hoa) bang random byte-flip
tu du lieu ngau nhien. Neu khong dung dictionary, xac suat sinh dung chuoi
"BEGIN" tai mot vi tri co dinh trong 1 lan thu la bao nhieu? So sanh voi
khi dung dictionary-based mutation (chen thang tu khoa).
"""
import random

KEYWORD = "BEGIN"
ASCII_UPPER_COUNT = 26  # A-Z


def probability_without_dictionary(keyword: str) -> float:
    """Xac suat 5 byte ngau nhien (dong deu trong 256 gia tri) VUA VAN
    dung 5 ky tu ASCII in hoa cua keyword, tai 1 vi tri co dinh."""
    return (1 / 256) ** len(keyword)


def simulate_random_mutation(keyword: str, trials: int = 2_000_000, seed: int = 7) -> int:
    """Mo phong thuc te: random.choice tren 256 gia tri byte, dem so lan
    trung khop CA 5 ky tu tai 1 vi tri co dinh trong so lan thu cho phep."""
    rng = random.Random(seed)
    hits = 0
    target = keyword.encode()
    for _ in range(trials):
        candidate = bytes(rng.randrange(256) for _ in range(len(target)))
        if candidate == target:
            hits += 1
    return hits


def probability_with_dictionary() -> float:
    """Voi dictionary-based mutation: fuzzer CHON tu dictionary (gia su co
    N tu trong dictionary, moi lan mutate chon deu 1 trong N tu de chen).
    Neu dictionary co "BEGIN" va N=20 tu, xac suat chon dung tu do trong
    1 lan mutate la 1/N (thay vi (1/256)^5)."""
    N = 20
    return 1 / N


if __name__ == "__main__":
    p_no_dict = probability_without_dictionary(KEYWORD)
    print("== Bai tap: Xac suat sinh tu khoa 'BEGIN' bang random mutation ==\n")
    print(f"Khong dictionary: P = (1/256)^5 = {p_no_dict:.3e}")
    print(f"  (xap xi 1 tren {int(1/p_no_dict):,} lan thu)")

    print(f"\nMo phong {2_000_000:,} lan thu ngau nhien thuc te:")
    hits = simulate_random_mutation(KEYWORD, trials=2_000_000)
    print(f"  So lan trung khop 'BEGIN': {hits} / 2,000,000")
    print("  (ky vong ly thuyet ~ 2,000,000 * 9.09e-12 ~ 0.0000182 lan -> gan nhu chac chan la 0,")
    print("   khop voi ket qua mo phong.)")

    p_dict = probability_with_dictionary()
    print(f"\nCo dictionary (gia su 20 tu, co san 'BEGIN'): P = 1/20 = {p_dict}")
    print(f"So lan cai thien: {p_dict / p_no_dict:.3e} lan cao hon")
    print("-> ket luan: dictionary-based mutation hieu qua vuot troi cho cac 'magic")
    print("   keyword/token' co dinh ma random mutation gan nhu khong the tim ra.")
