import hashlib

# Test prior fingerprint scheme
for s, exp in [
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Early_checkout", "9fb519eb4fdb"),
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Early checkout", None),
    ("unpinned-uses|.github/workflows/aeon.yml|Early_checkout", None),
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Setup_Node.js", "920a2c40af77"),
    ("zizmor/artipacked|.github/workflows/aeon.yml|Early_checkout", "d42af71c10f4"),
]:
    h = hashlib.sha256(s.encode()).hexdigest()[:12]
    print(f"exp={exp} got={h}   input={s!r}")
