import hashlib

for s, exp in [
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Early checkout", "9fb519eb4fdb"),
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Setup Node.js", "920a2c40af77"),
    ("zizmor/artipacked|.github/workflows/aeon.yml|Early checkout", "d42af71c10f4"),
    ("zizmor/unpinned-uses|.github/workflows/aeon.yml|Checkout repo", "7491c14fbe74"),
]:
    h = hashlib.sha256(s.encode()).hexdigest()[:12]
    print(f"exp={exp} got={h} MATCH={h == exp}   input={s!r}")
