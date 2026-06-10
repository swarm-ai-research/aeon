// AGI Tracker — data model
// Updated by the `agi-tracker` skill. Hand-edits welcome; keep the shape stable.
//
// points[].horizonMinutes = METR 50% time horizon (length of software task,
// measured in human-expert time, that the agent completes 50% of the time).
// reliability: "measured" (METR official), "estimate" (third-party / extrapolated),
//              "saturating" (above the suite's reliable range, treat as fuzzy).
window.AGI_TRACKER = {
  meta: {
    lastUpdated: "2026-06-10",
    maintainer: "aeon agi-tracker skill",
    primarySources: [
      { label: "METR Time Horizons", url: "https://metr.org/time-horizons/" },
      { label: "METR TH1.1 update (Jan 2026)", url: "https://metr.org/blog/2026-1-29-time-horizon-1-1/" },
      { label: "METR: limitations of time horizon", url: "https://metr.org/notes/2026-01-22-time-horizon-limitations/" },
      { label: "Situational Awareness (Aschenbrenner, June 2024)", url: "https://situational-awareness.ai/" },
      { label: "Epoch AI: METR Time Horizons", url: "https://epoch.ai/benchmarks/metr-time-horizons" }
    ],
    notes: [
      "Doubling times per METR TH1.1: ~7 months over 2019–2025, 129 days (~4.3 months) post-2023, ~89 days (~3 months) post-2024.",
      "METR flags 50%-horizon estimates above ~16 hours as unreliable with the current task suite (saturation).",
      "Benchmark horizons are clean, well-specified software tasks — real-world messy work lags these numbers."
    ]
  },

  // METR 50% time horizons (TH1/TH1.1 where available)
  points: [
    { model: "GPT-2",                    date: "2019-02-14", horizonMinutes: 0.033,  reliability: "measured" },
    { model: "GPT-3 (davinci-002)",      date: "2020-07-01", horizonMinutes: 0.15,   reliability: "measured" },
    { model: "GPT-3.5 Turbo",            date: "2023-03-01", horizonMinutes: 0.6,    reliability: "measured" },
    { model: "GPT-4",                    date: "2023-03-14", horizonMinutes: 5,      reliability: "measured" },
    { model: "Claude 3 Opus",            date: "2024-03-04", horizonMinutes: 6,      reliability: "measured" },
    { model: "GPT-4o",                   date: "2024-05-13", horizonMinutes: 9,      reliability: "measured" },
    { model: "Claude 3.5 Sonnet",        date: "2024-06-20", horizonMinutes: 18,     reliability: "measured" },
    { model: "o1-preview",               date: "2024-09-12", horizonMinutes: 22,     reliability: "measured" },
    { model: "Claude 3.5 Sonnet (new)",  date: "2024-10-22", horizonMinutes: 28,     reliability: "measured" },
    { model: "o1",                       date: "2024-12-05", horizonMinutes: 39,     reliability: "measured" },
    { model: "Claude 3.7 Sonnet",        date: "2025-02-24", horizonMinutes: 59,     reliability: "measured" },
    { model: "o3",                       date: "2025-04-16", horizonMinutes: 90,     reliability: "measured" },
    { model: "Claude Opus 4",            date: "2025-05-22", horizonMinutes: 80,     reliability: "measured" },
    { model: "Grok 4",                   date: "2025-07-09", horizonMinutes: 110,    reliability: "estimate" },
    { model: "GPT-5",                    date: "2025-08-07", horizonMinutes: 137,    reliability: "measured" },
    { model: "Claude Sonnet 4.5",        date: "2025-09-29", horizonMinutes: 113,    reliability: "measured" },
    { model: "Claude Opus 4.5",          date: "2025-11-24", horizonMinutes: 289,    reliability: "measured" },
    { model: "Gemini 3 Pro",             date: "2025-11-18", horizonMinutes: 390,    reliability: "estimate" },
    { model: "GPT-5.3 Codex",            date: "2026-03-01", horizonMinutes: 390,    reliability: "estimate" },
    { model: "Claude Opus 4.6",          date: "2026-02-05", horizonMinutes: 870,    reliability: "saturating" }
  ],

  // Capability milestones expressed as human-expert task length.
  // hours are working-time equivalents (day=8h, week=40h, month=167h, year=2000h).
  milestones: [
    { label: "Full workday tasks",   hours: 8,    meaning: "Agent reliably owns a day-sized ticket end to end." },
    { label: "Week-long projects",   hours: 40,   meaning: "Sprint-sized feature work; junior-engineer replacement on clean tasks." },
    { label: "Month-long projects",  hours: 167,  meaning: "Substantial deliverables; Aschenbrenner's proto-agent regime." },
    { label: "Year-long programs",   hours: 2000, meaning: "≈ automated AI researcher / drop-in remote worker — the AGI threshold in Situational Awareness." }
  ],

  // Projection scenarios (doubling time of the 50% horizon, in months)
  scenarios: {
    default: 4.3,
    fast: { label: "Post-2023 trend (METR TH1.1)", months: 4.3 },
    faster: { label: "Post-2024 trend", months: 3.0 },
    slow: { label: "Long-run 2019–2025 trend", months: 7.0 },
    sliderRange: { min: 2.5, max: 10, step: 0.1 }
  },

  // Situational Awareness scorecard — Aschenbrenner's June 2024 claims vs. observed reality.
  // status: "ahead" | "on-track" | "partial" | "behind" | "open"
  scorecard: [
    {
      claim: "Compute buildout: ~0.5 OOM/yr, $100B–$1T clusters, national mobilization of capital",
      status: "ahead",
      evidence: "Stargate at $500B / 10 GW; hyperscaler data-center capex approaching ~$700B planned for 2026; Anthropic's $50B US buildout."
    },
    {
      claim: "Models outpace many college graduates by 2025/26",
      status: "on-track",
      evidence: "Frontier models exceed graduate-level performance on most exam-style and reasoning benchmarks; widely deployed for knowledge work."
    },
    {
      claim: "Unhobbling: chatbots become agents",
      status: "ahead",
      evidence: "METR 50%-horizon doubling every ~4.3 months post-2023 (vs ~7-month long-run); frontier agents at multi-workday horizons by early 2026, saturating the task suite."
    },
    {
      claim: "Drop-in remote worker by ~2027",
      status: "partial",
      evidence: "Benchmark horizons say yes; real-world reliability, messy context, and long-tail failure modes still gate deployment. Self-reported practitioner uplift ~1.4–2x, well below benchmark implication."
    },
    {
      claim: "AGI (automated AI researcher) by 2027",
      status: "open",
      evidence: "At the 4.3-month doubling, year-long-task capability lands ~2028–29; at 7 months, early 2030s. No longer consensus, no longer dismissible."
    },
    {
      claim: "Intelligence explosion 2027–28 (automated AI research → superintelligence)",
      status: "open",
      evidence: "Premise (AI accelerating AI R&D) partially visible — labs report large internal coding/automation gains — but no runaway dynamics observed."
    },
    {
      claim: "The Project: USG-led national AGI effort by 2027/28",
      status: "behind",
      evidence: "Heavy government engagement (export controls, compute diplomacy, defense contracts) but no nationalization; labs remain private and commercially driven."
    },
    {
      claim: "Lab security hardened to state-actor level",
      status: "behind",
      evidence: "Security improved (weights custody, insider-threat programs) but independent assessments still rate frontier labs below state-actor-proof; the gap Aschenbrenner flagged remains."
    }
  ]
};
