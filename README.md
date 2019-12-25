# Extra cppcheck addons

## Installation & usage

1. Install latest cppcheck from sources:
```bash
git clone https://github.com/danmar/cppcheck.git
cd cppcheck
make install
```

2. Create dump files:
```bash
cppcheck --dump test/test-depsize.c
```

3. Run addons:
```bash
python3 depsize.py test/test-depsize.c.dump
```
