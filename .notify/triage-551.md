**Triage:** DEFER — size 1017 lines exceeds the 500-line rubric ceiling and no `large-ok` label is set.

This PR is sound (dedicated scenario + 16 tests + writeup, mypy/ruff clean per the summary) but needs a maintainer signoff on the size before it can move. Leaving open and labelling `triage:deferred`; @rsavitt will pick it up on the next review pass — either land as-is behind a `large-ok` tag or split the sweep script + docs from the handler diff so each piece lands under the ceiling.
