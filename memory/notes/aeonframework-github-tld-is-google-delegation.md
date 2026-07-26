---
id: aeonframework-github-tld-is-google-delegation
created: 2026-07-26
type: observation
links: [[aeon-fifth-signing-identity-security-aeonframework-github]], [[aeon-signing-identity-fragmentation]]
---
# The `.github` TLD is a real Google delegation, but `aeonframework.github` is not observably in wide public use — likely an internal alias or typo of `aeonframework.dev`

`.github` was delegated to Google as a corporate gTLD; it exists in the DNS root and can serve real MX records. However, no public DNS resolution or GitHub Pages presence has been observed under `aeonframework.github`, and its local-part `security@` matches the `.dev` identity exactly. Most parsimonious hypothesis: the sender was mistyped or an internal SMTP alias, not a second production domain — to be confirmed or refuted by whether the same address repeats on the next same-class PR.
