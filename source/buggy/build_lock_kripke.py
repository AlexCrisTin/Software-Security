from ch1_models.kripke import KripkeStructure


def build_lock_model(insecure: bool = False) -> KripkeStructure:
    """Xay dung mo hinh Kripke cho khoa cua thong minh.

    insecure=False (mac dinh): mo hinh DUNG, giong lock.py
        - Tu UNLOCKING chi toi UNLOCKED neu PIN dung (nhanh "pin dung")
        - Tu UNLOCKING quay ve LOCKED neu PIN sai (nhanh "pin sai")

    insecure=True: mo hinh CO LOI, giong lock_buggy.py
        - Tu UNLOCKING LUON LUON toi UNLOCKED, du PIN dung hay sai
          (thieu nhanh "pin sai" -> day chinh la lo hong)
    """
    k = KripkeStructure()

    k.add_state("LOCKED", labels=["locked"], initial=True)
    k.add_state("UNLOCKING", labels=["unlocking"])
    k.add_state("UNLOCKED", labels=["unlocked"])
    k.add_state("ALARM", labels=["alarm"])

    # Nhan mot chu so dau tien -> chuyen sang dang nhap (UNLOCKING)
    k.add_transition("LOCKED", "UNLOCKING")

    if insecure:
        # --- MO HINH CO LOI (giong lock_buggy.py) ---
        # Bat ke PIN dung hay sai, he thong deu mo khoa.
        # Day la LY DO DUY NHAT khien mo hinh nay khong an toan.
        k.add_transition("UNLOCKING", "UNLOCKED")
    else:
        # --- MO HINH DUNG (giong lock.py) ---
        # Nhanh 1: PIN dung -> mo khoa that su
        k.add_transition("UNLOCKING", "UNLOCKED")
        # Nhanh 2: PIN sai -> quay ve LOCKED (khong mo khoa)
        k.add_transition("UNLOCKING", "LOCKED")
        # Nhanh 3: PIN sai qua nhieu lan -> ALARM
        k.add_transition("UNLOCKING", "ALARM")

    # Tu UNLOCKED co the khoa lai
    k.add_transition("UNLOCKED", "LOCKED")
    # Tu ALARM, quan tri vien reset ve LOCKED
    k.add_transition("ALARM", "LOCKED")

    return k


if __name__ == "__main__":
    print("=" * 60)
    print("MO HINH 1: Khoa cua AN TOAN (giong lock.py)")
    print("=" * 60)
    safe_model = build_lock_model(insecure=False)
    print("Cac trang thai co the dat toi:", sorted(safe_model.reachable_states()))

    # Trong mo hinh an toan, van co the toi UNLOCKED (qua nhanh PIN dung)
    # -- dieu nay LA BINH THUONG, vi PIN dung thi PHAI mo duoc khoa.
    path = safe_model.find_path("UNLOCKED")
    print("Duong toi UNLOCKED (qua nhanh PIN dung, day la HANH VI DUNG):", path)

    print()
    print("=" * 60)
    print("MO HINH 2: Khoa cua CO LOI (giong lock_buggy.py)")
    print("=" * 60)
    buggy_model = build_lock_model(insecure=True)
    print("Cac trang thai co the dat toi:", sorted(buggy_model.reachable_states()))

    bug_path = buggy_model.find_path("UNLOCKED")
    print("Duong toi UNLOCKED trong mo hinh loi:", bug_path)

    print()
    print("=" * 60)
    print("KET LUAN")
    print("=" * 60)
    print("O mo hinh CO LOI, khong co cach nao phan biet duong di nay voi")
    print("truong hop PIN sai, vi ca 2 truong hop deu chi co 1 canh duy nhat")
    print("UNLOCKING -> UNLOCKED. Day chinh la COUNTEREXAMPLE can dua vao")
    print("muc 'V. Bang chung kiem chung' trong bao cao: he thong mo khoa")
    print("ma khong phan biet duoc PIN dung/sai.")
