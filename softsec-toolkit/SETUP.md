# Cai dat moi truong (chi can lam 1 lan)

## Python
```bash
pip install -r requirements.txt --break-system-packages
```

## Cong cu he thong (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y gcc cppcheck valgrind cbmc
```
Tat ca cong cu tren da duoc cai dat va kiem chung trong moi truong tao ra
bo code nay: gcc 13 (ho tro -fsanitize=address/undefined), cppcheck 2.13.0,
valgrind, cbmc (Ubuntu 24.04 repo).
