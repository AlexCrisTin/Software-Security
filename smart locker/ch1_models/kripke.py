"""
Chuong 1 - Phan 2, muc 1.5: Cau truc Kripke (Kripke Structure)
================================================================

Cai dat lop `KripkeStructure` duoc nhac toi truc tiep trong slide voi ten
day du `softsec.ch1_models.kripke.KripkeStructure` va duoc dung lai o
Chuong 3 (dac ta thuoc tinh LTL/CTL).

Bai tap duoc hien thuc hoa trong file nay:
  - "Bai tap: Xay dung Kripke Structure" (dem/counter, slide 908)
  - "Bai tap thuc hanh voi module Python" (reachable_states/find_path, slide 935)
  - "Bai tap: Kiem tra thuoc tinh bang tay" (den giao thong, slide 1041)
  - "Bai tap: Reachability tren Vending Machine" (slide 1082)
  - "Bai tap tong hop lon" (ATM, slide 1500)

Ngon ngu: Python 3.
"""
from collections import deque
from typing import Dict, Iterable, List, Optional, Set


class KripkeStructure:
    """Kripke structure M = (S, S0, R, L).

    - S  : tap trang thai (state la string bat ky)
    - S0 : tap trang thai khoi tao (subset cua S)
    - R  : quan he chuyen tiep, bieu dien bang dict state -> set(next_states)
    - L  : ham gan nhan, dict state -> set(propositions dung tai state do)
    """

    def __init__(self) -> None:
        self.states: Set[str] = set()
        self.initial: Set[str] = set()
        self.transitions: Dict[str, Set[str]] = {}
        self.labels: Dict[str, Set[str]] = {}

    # -- xay dung mo hinh ---------------------------------------------------
    def add_state(self, s: str, labels: Optional[Iterable[str]] = None, initial: bool = False) -> None:
        self.states.add(s)
        self.transitions.setdefault(s, set())
        self.labels[s] = set(labels or [])
        if initial:
            self.initial.add(s)

    def add_transition(self, src: str, dst: str) -> None:
        if src not in self.states or dst not in self.states:
            raise ValueError(f"State '{src}' hoac '{dst}' chua duoc khai bao bang add_state()")
        self.transitions[src].add(dst)

    # -- truy van -------------------------------------------------------------
    def reachable_states(self) -> Set[str]:
        """BFS/DFS tu tap trang thai khoi tao, tra ve tat ca trang thai dat toi."""
        visited: Set[str] = set()
        queue = deque(self.initial)
        while queue:
            s = queue.popleft()
            if s in visited:
                continue
            visited.add(s)
            for nxt in self.transitions.get(s, ()):
                if nxt not in visited:
                    queue.append(nxt)
        return visited

    def is_reachable(self, target: str) -> bool:
        return target in self.reachable_states()

    def find_path(self, target: str) -> Optional[List[str]]:
        """Tim mot duong di (counterexample-style) tu mot trang thai khoi tao
        toi `target`. Tra ve None neu khong ton tai (khong reachable)."""
        for s0 in self.initial:
            path = self._bfs_path(s0, target)
            if path is not None:
                return path
        return None

    def _bfs_path(self, start: str, target: str) -> Optional[List[str]]:
        if start == target:
            return [start]
        visited = {start}
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            last = path[-1]
            for nxt in self.transitions.get(last, ()):
                if nxt == target:
                    return path + [nxt]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(path + [nxt])
        return None

    def states_with_label(self, prop: str) -> Set[str]:
        return {s for s, labs in self.labels.items() if prop in labs}

    # -- kiem tra thuoc tinh CTL don gian (EF, AG EF) -----------------------
    def satisfies_EF(self, prop: str, frm: Optional[str] = None) -> bool:
        """EF p tai `frm`: ton tai duong di tu `frm` toi mot trang thai co
        nhan p. Neu frm=None, kiem tra tu MOI trang thai khoi tao."""
        starts = [frm] if frm else list(self.initial)
        target_states = self.states_with_label(prop)
        for start in starts:
            reached = self._reachable_from(start)
            if reached & target_states:
                continue
            return False
        return True

    def satisfies_AG_EF(self, prop: str) -> bool:
        """AG EF p: tu MOI trang thai s trong S, EF p dung tai s.
        Day chinh la thuoc tinh 'luon ton tai duong quay lai p' (vd: den do)."""
        target_states = self.states_with_label(prop)
        for s in self.states:
            reached = self._reachable_from(s)
            if not (reached & target_states):
                return False
        return True

    def _reachable_from(self, s: str) -> Set[str]:
        visited: Set[str] = set()
        queue = deque([s])
        while queue:
            cur = queue.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            for nxt in self.transitions.get(cur, ()):
                if nxt not in visited:
                    queue.append(nxt)
        return visited


# ---------------------------------------------------------------------------
# Bai tap 1: "counter" -- dem tu 0 den max=3 roi reset
#   S = {0,1,2,3}, S0 = {0}
#   R: 0->1, 1->2, 2->3, 3->0 (reset)
#   L: 0={zero}, 1={nonzero}, 2={nonzero}, 3={nonzero,max}
# ---------------------------------------------------------------------------

def build_counter_model(max_value: int = 3) -> KripkeStructure:
    k = KripkeStructure()
    for i in range(max_value + 1):
        labels = ["zero"] if i == 0 else ["nonzero"]
        if i == max_value:
            labels.append("max")
        k.add_state(str(i), labels=labels, initial=(i == 0))
    for i in range(max_value + 1):
        nxt = (i + 1) % (max_value + 1)
        k.add_transition(str(i), str(nxt))
    return k


# ---------------------------------------------------------------------------
# Bai tap 2: Den giao thong Do -> Xanh -> Vang -> Do (chu ky don)
# ---------------------------------------------------------------------------

def build_traffic_light_model() -> KripkeStructure:
    k = KripkeStructure()
    k.add_state("red", labels=["red"], initial=True)
    k.add_state("green", labels=["green"])
    k.add_state("yellow", labels=["yellow"])
    k.add_transition("red", "green")
    k.add_transition("green", "yellow")
    k.add_transition("yellow", "red")
    return k


# ---------------------------------------------------------------------------
# Bai tap 3: Vending Machine -- idle -> selecting -> dispensing -> idle
#   them mot trang thai loi "stuck" KHONG co transition nao tro toi.
# ---------------------------------------------------------------------------

def build_vending_machine_model() -> KripkeStructure:
    k = KripkeStructure()
    k.add_state("idle", labels=["idle"], initial=True)
    k.add_state("selecting", labels=["selecting"])
    k.add_state("dispensing", labels=["dispensing"])
    k.add_state("stuck", labels=["error"])  # khong co canh nao tro toi -> unreachable
    k.add_transition("idle", "selecting")
    k.add_transition("selecting", "dispensing")
    k.add_transition("dispensing", "idle")
    return k


# ---------------------------------------------------------------------------
# Bai tap tong hop: ATM
#   no_card -> card_inserted -> pin_verified -> transaction -> card_ejected -> no_card
#   Mo hinh SAI (co lo hong): card_inserted -> transaction (bo qua pin_verified)
# ---------------------------------------------------------------------------

def build_atm_model(insecure: bool = False) -> KripkeStructure:
    k = KripkeStructure()
    for s in ["no_card", "card_inserted", "pin_verified", "transaction", "card_ejected"]:
        k.add_state(s, labels=[s], initial=(s == "no_card"))
    k.add_transition("no_card", "card_inserted")
    k.add_transition("card_inserted", "pin_verified")
    k.add_transition("pin_verified", "transaction")
    k.add_transition("transaction", "card_ejected")
    k.add_transition("card_ejected", "no_card")
    if insecure:
        # Lo hong STRIDE: Elevation of Privilege / Tampering -- bo qua xac thuc PIN
        k.add_transition("card_inserted", "transaction")
    return k


if __name__ == "__main__":
    print("== Bai tap: Counter (0..3, reset ve 0) ==")
    counter = build_counter_model()
    print("  reachable_states():", sorted(counter.reachable_states(), key=int))
    assert counter.reachable_states() == {"0", "1", "2", "3"}, "phai dung {0,1,2,3} nhu slide yeu cau"
    path = counter.find_path("3")
    print("  find_path('3'):", path)
    print("  -> counterexample nghia la: tu trang thai khoi tao 0, chi can 3 buoc"
          " chuyen tiep (0->1->2->3) la dat duoc trang thai 3.")

    print("\n== Bai tap: Kiem tra thuoc tinh bang tay -- den giao thong ==")
    traffic = build_traffic_light_model()
    result = traffic.satisfies_AG_EF("red")
    print("  AG EF red =", result, "(tu moi trang thai luon co duong quay lai den do)")
    assert result is True

    print("\n== Bai tap: Reachability tren Vending Machine ==")
    vm = build_vending_machine_model()
    print("  is_reachable('dispensing') tu idle:", vm.is_reachable("dispensing"))
    print("  is_reachable('stuck'):", vm.is_reachable("stuck"))
    assert vm.is_reachable("dispensing") is True
    assert vm.is_reachable("stuck") is False

    print("\n== Bai tap tong hop lon: ATM (mo hinh AN TOAN) ==")
    atm_safe = build_atm_model(insecure=False)
    print("  reachable:", sorted(atm_safe.reachable_states()))
    print("  is_reachable('transaction') ma KHONG qua pin_verified?",
          "khong the kiem tra truc tiep bang reachability don gian -- can dac ta LTL/CTL,"
          " xem ch3_verify/ cho vi du dung Z3/CTL.")

    print("\n== Mo hinh ATM KHONG AN TOAN (bo qua pin_verified) ==")
    atm_insecure = build_atm_model(insecure=True)
    bypass_path = atm_insecure.find_path("transaction")
    print("  duong ngan nhat toi 'transaction':", bypass_path)
    if bypass_path == ["no_card", "card_inserted", "transaction"]:
        print("  -> XAC NHAN lo hong: co the vao 'transaction' ma KHONG qua 'pin_verified'!")
