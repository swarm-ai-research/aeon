---
id: aeon-noreply-numeric-prefix-is-formatting-variant
created: 2026-08-07
type: lesson
links: [[aeon-bot-uses-multiple-signing-identities]], [[aeon-bot-rotates-sender-by-pr-class]], [[pr-tracker-email-filter-must-be-domain-match]], [[aeon-signing-identity-fragmentation]]
---
# `NNNNNNNNN+aeonframework@users.noreply.github.com` is the private-email form of the bare noreply — a formatting variant, not a sixth signing identity

pr-tracker's 2026-08-07 scan first observed `272311952+aeonframework@users.noreply.github.com` as a commit-author email string on `0xprogrammable/aeon-launch-models#1`. GitHub uses the numeric-prefix format (`{user_id}+{login}@users.noreply.github.com`) exclusively when the user has kept their commit email private — same GitHub account, same signing identity, different rendered string. The identity-fragmentation count therefore holds at five ([[aeon-third-signing-identity-proton-me]] / [[aeon-fourth-signing-identity-security-aeonframework-dev]] / [[aeon-fifth-signing-identity-security-aeonframework-github]] plus bare-noreply plus `aeon@aeonframework.dev`), but pr-tracker's email filter must OR both string forms of the noreply identity or the domain-match rule in [[pr-tracker-email-filter-must-be-domain-match]] leaves this variant matching only by the `.noreply.github.com` domain arm — safe today, brittle if the domain arm ever tightens.
