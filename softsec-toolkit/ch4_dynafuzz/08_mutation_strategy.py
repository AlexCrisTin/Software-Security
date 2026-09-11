"""
Bai tap: Thiet ke chien luoc Dot bien (Mutation) (Chuong4_Phan2, slide 603)

Dinh dang file: 4 byte "magic number" co dinh + 4 byte do dai + payload.
De xuat to hop mutation operators phu hop.

File nay TRIEN KHAI cac mutation operator da de xuat (giu nguyen magic,
arithmetic mutation cho truong do dai, bit/byte flip tu do cho payload) va
chay thu tren mot seed mau de minh hoa ket qua cu the.
"""
import random
import struct

MAGIC = b"SFTP"  # 4 byte magic number co dinh (gia lap)


def make_seed(payload: bytes) -> bytes:
    return MAGIC + struct.pack("<I", len(payload)) + payload


def mutate(data: bytes, seed: int = 0) -> bytes:
    """Ap dung chien luoc dot bien da de xuat trong dap an slide:
      1) GIU NGUYEN 4 byte magic number (khong dot bien vung nay)
      2) Arithmetic mutation cho truong do dai (4 byte tiep theo): +-1, hoac gia tri rat lon
      3) Bit/byte flip TU DO cho phan payload con lai
    """
    rng = random.Random(seed)
    magic = data[:4]                      # (1) giu nguyen
    length_bytes = bytearray(data[4:8])
    payload = bytearray(data[8:])

    # (2) Arithmetic mutation cho truong do dai
    length_val = struct.unpack("<I", length_bytes)[0]
    op = rng.choice(["+1", "-1", "huge"])
    if op == "+1":
        length_val = (length_val + 1) & 0xFFFFFFFF
    elif op == "-1":
        length_val = (length_val - 1) & 0xFFFFFFFF
    else:
        length_val = 0xFFFFFFFF  # gia tri rat lon -> kiem tra xu ly do dai sai lech
    new_length_bytes = struct.pack("<I", length_val)

    # (3) Bit/byte flip tu do cho payload
    if payload:
        idx = rng.randrange(len(payload))
        payload[idx] ^= 1 << rng.randrange(8)  # flip 1 bit ngau nhien

    return bytes(magic) + new_length_bytes + bytes(payload), op


if __name__ == "__main__":
    seed_data = make_seed(b"hello world")
    print("== Bai tap: Thiet ke chien luoc dot bien cho dinh dang [magic4][len4][payload] ==\n")
    print(f"Seed goc: magic={seed_data[:4]}, len_field={seed_data[4:8].hex()}, "
          f"payload={seed_data[8:]}")

    for i in range(3):
        mutated, op = mutate(seed_data, seed=i)
        print(f"\nLan dot bien #{i+1} (arithmetic op tren truong do dai = '{op}'):")
        print(f"  magic (GIU NGUYEN)   = {mutated[:4]}")
        print(f"  length field (moi)   = {mutated[4:8].hex()} "
              f"(gia tri = {struct.unpack('<I', mutated[4:8])[0]})")
        print(f"  payload (bit-flipped)= {mutated[8:]}")
