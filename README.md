# Premortem: Ad-Campaign Edition

> Paste a campaign (copy + key visual + ad film). 60 grounded Singaporean AI agents,
> each isolated in its own Daytona sandbox and self-grounded in this week's live discourse,
> tear it apart in a baked 90-second run. You get a **Blast Score**, a **timeline blast map**
> (which second of the film detonated the panel), tomorrow's fictional front page, and a
> **3-tier fix triage** that separates what a rewrite can save, from what needs a re-shoot,
> from what is simply a no-go. Before the real public does it for free.

**Event:** Agent Forge AI Hackathon (AI Builders x SMU AI Club), 2026-06-13, SMU.
**Theme fit:** Build Production AI Systems. **Status:** plan locked, build pending.

---

## 1. Governing principle

**Build it real, demo it baked.** The architecture is live-capable, but the on-stage 2 minutes
is pure replay of a single pre-produced **golden run**. Every sponsor is used to *produce that one
golden run offline, with receipts*, not to run robustly on stage. This is the only shape that
survives a heavy multi-sponsor architecture in a 4-hour window.

## 2. Architecture

```
INPUT: campaign copy + key visual + ad film + brand/category
        |
        v
[VideoDB] creative ingestion (ONCE, offline)
   -> manifest: {scene_id, t_start, t_end, keyframe, visual_desc, transcript, on_screen_text}
        |
        v
[Daytona] 60 sandboxes, one per agent (baked offline, receipts captured)
   each sandbox:  [Bright Data] self-ground (3 buckets, injection-fenced)
                  [Kimi K2.6 multimodal] react to copy + keyframes + transcript + its grounding
        |
        v
AGGREGATE: Blast Score % + objection clusters + TIMELINE heatmap + 3-run stability band
        |
        +--> [SenseNova] degrade a keyframe -> scandal photo -> Tomorrow's Headline
        |                (fictional masthead + SIMULATED watermark)
        +--> report JSON -> static dashboard (tile grid + timeline scrubber + clusters + fix triage)
        |
        v
FIX TRIAGE (3 tiers) -> two-stage re-sim -> measured delta
```

**Why each agent is sandboxed (defensible, not theater):** each agent self-grounds in untrusted
public text (r/singapore, news), which is a prompt-injection vector. Daytona contains the blast
radius **per agent**, so live grounding becomes 60 isolated sandboxes instead of 60 injection paths.
Honest caveat: sandboxing is isolation, not intelligence, and 60 cold-starts is a stage killer, so
the 60 sandboxed agents run **once in the morning** to bake the golden run.

## 3. Sponsor map (5 core, all architecturally justified)

| Tool | Role | Depth | Bakes golden run by |
|------|------|-------|---------------------|
| **Kimi K2.6** | 60-agent multimodal panel (fan-out, prefix cache, JSON mode, sees keyframes) | CORE | reacting to copy + keyframes + transcript |
| **Bright Data** | per-agent self-grounding, 3 buckets, injection-fenced | CORE | landmine radar / brand baggage / comparable-campaign graveyard |
| **Daytona** | per-agent sandbox isolation (injection containment) + pipeline execution | CORE | running the 60 agents once, transcripts = receipts |
| **VideoDB** | creative ingestion: transcript, OCR, scenes, keyframes, timestamps | CORE | ingesting the one golden ad film |
| **SenseNova U1** | degrade a keyframe into the scandal front-page photo | MED | one image |
| Terminal 3 | audit trail over the 60 sandboxed agent actions (verifiable agent identity) | ADD-ON | in only if ahead of schedule |
| TokenRouter / Nosana | skip / booth-only | SKIP | roadmap line |

Q&A receipt slide: "Kimi 60 multimodal calls (90% cache) | Bright Data 3 sources, N quotes |
Daytona 60 sandboxes, transcripts attached | VideoDB 1 film, M scenes | SenseNova 1 frame."

## 4. The 60-agent panel (N=60, tunable; pitch line "same harness runs 300")

| Block | Count | Voice | Notes for ads |
|-------|-------|-------|---------------|
| Public personas | 35 | first-person (the laugh + the public reaction) | age/race/income/subculture variants via trait jitter |
| Concern lenses | 15 | third-person risk register only | halal, racial-rep (CMIO), accessibility, PDPA, low-income, gender, religious, ageism, disability, LGBTQ-sensitivity |
| Stakeholders | 10 | role-based | CNA/ST journalist, **ASAS** (Advertising Standards Authority of SG), IMDA, opposition MP, competitor brand head, the talent/celebrity fanbase, activist group, own employees |

Identity-sensitive perspectives stay **concern lenses** (third person, evidence-cited), never
first-person roleplay. ASAS is the ad-accurate regulator.

### 4.1 How the 60 agents are created

Two senses: design-time generation and run-time instantiation.

**Design-time: ~37 seeds -> 60 agents.** Hand-author archetype seed cards (the IP), then expand
deterministically:
- ~12 persona seeds x trait-jitter variants -> 35 persona agents
- 15 concern-lens seeds (1:1, no jitter) -> 15 lens agents
- 10 stakeholder seeds (1:1) -> 10 stakeholder agents

Lenses and stakeholders are not jittered (a lens is one fixed analytical perspective). Only personas
multiply, because within-archetype diversity is the point.

A seed card:
```yaml
id: toa_payoh_auntie
kind: persona            # persona | lens | stakeholder
voice: first_person      # personas=1st; lenses & stakeholders=3rd (anti-stereotype rule)
emoji: "elderly_woman"
label: Toa Payoh retiree auntie
concern_axes: [price, privacy, font_size, family_safety]
register: "Singlish, WhatsApp-forward cadence, wary of new tech"
grounding_query: "r/singapore (elderly OR auntie) (scam OR privacy OR price)"
jitter: { age: [58, 72], optimism: [-0.6, 0.0], tech_savvy: [0.1, 0.4] }
```

**Anti-stereotype rule, enforced at creation:** lifestyle/age/occupation -> first-person persona;
race/religion/identity -> third-person concern LENS. The system never roleplays an identity in the
first person.

**Trait jitter is deterministic,** keyed by `(seed_id, variant_index)` on a fixed grid, not random,
so the golden run is reproducible and cache-stable:
`auntie -> {auntie_1 age60/pessimist, auntie_2 age68/mid, auntie_3 age72/low-tech}`.
Output: `personas.json`, 60 concrete records.

**Run-time: each record -> one sandboxed, self-grounding Kimi call,** assembled as:
- **SHARED PREFIX (identical for all 60 -> prefix-cache hit):** task + severity rubric (0-3) + JSON
  schema + the creative manifest (copy + keyframes + transcript + `[scene@t]` indices) + fence rules
  + SIMULATED framing. The big creative payload is cached ONCE, not 60x.
- **PER-AGENT BLOCK (the only varying part):** the agent's persona card + its own Bright Data
  grounding pack (quote-fenced), executed inside the agent's Daytona sandbox.

That split is why 60 agents is affordable: the expensive context is one cached prefix; only a small
persona+grounding block differs per agent. Seeds are hand-written (highest-leverage content work) and
may be LLM-bootstrapped then curated.

## 5. Golden-run scenario

Reuse the **MerlionTel** fiction as a 30-second ad film with three deliberately layered landmines,
one per fix tier:

- **Copy landmine:** the "we listen to your calls to personalise" line (privacy).
- **Visual landmine:** a tone-deaf CMIO casting/representation moment at ~0:12.
- **Concept landmine:** the surveillance premise itself.

Produced safely and cheaply: SenseNova-generated keyframes + a written script/transcript + a scene
list, run through VideoDB once. **No real ad footage ingested or shown.** E-Pay 2019 and Pepsi stay
as **text-level smoke tests** for calibration only. Fictional brand for the video, real disasters for
the text controls: keeps POFMA / real-masthead discipline clean.

## 6. The 3-tier fix triage (the sharpest differentiator)

Every objection is tagged with the cheapest fix that resolves it:

1. **Copy-fixable** (script/tagline/voiceover): rewrite, re-sim.
2. **Production-fixable** / "unfixable by wording" (casting, lighting, imagery, music): cut / recast / re-track.
3. **Decision-level / no-go** (the concept): not a copy edit, a launch call.

Demo shows a **two-stage drop**: rewrite copy 84 to 55, cut the 0:12 scene 55 to 28, then "the
residual 28 is the premise, that is your call." This is also the clean kill for the Goodhart question
("couldn't the rewrite game your personas?"): wording only moves the wording tier, by construction.

## 7. Data contracts (freeze before any UI work)

```jsonc
// creative manifest (VideoDB output)
{ "scene_id": "s12", "t_start": 12.0, "t_end": 14.5,
  "keyframe": "frames/s12.jpg", "visual_desc": "...", "transcript": "...", "on_screen_text": "..." }

// agent reaction (Kimi, JSON mode, per sandbox)
{ "agent_id": "auntie_1", "kind": "persona|lens|stakeholder",
  "sentiment": -2, "severity": 3, "objection_category": "privacy",
  "quote": "first-person for personas / third-person finding for lenses",
  "trigger_moments": [{"scene_id": "s12", "t": 12.4}],   // timeline blast map
  "fix_tier": "copy|production|decision",
  "would_share": {"yes": true, "where": "whatsapp"},
  "evidence_id": "gp_reddit_014 | null",                  // self-grounded, injection-fenced
  "sandbox_id": "dt_a17", "question": "one press-conference question" }

// golden run (the single artifact the stage replays AND the dashboard renders)
{ "run_id": "...", "creative_manifest": [ /* ... */ ], "grounding_packs": { /* ... */ },
  "reactions": [ /* 60 */ ],
  "aggregate": {"blast_score": 84, "clusters": [], "timeline_heatmap": [], "stability": "84 +/- 3"},
  "artifacts": {"front_page_html": "...", "keyframe_img": "..."},
  "fix": {"stage1_copy": {"score": 55}, "stage2_scene": {"score": 28}, "residual": 28},
  "sponsor_trace": [] }
```

## 8. Dashboard: the final result

The 60 agent reactions are summarized into ONE object (`golden_run.json`) and the dashboard is a
**pure render of that object**. This is the final result the user gets and the on-stage surface.

### 8.1 The reduce (60 -> 1)

```
reduce(reactions[60], runs=3) -> dashboard_state:
  responders   = reactions where status != "abstain"        # gray tiles, excluded from denominator
  blast_score  = round(100 * count(r.severity >= 2) / |responders|)   # median across 3 runs
  band         = spread across the 3 runs                   # "84 +/- 3"
  decision     = DELAY if blast>=70 : REVISE if blast>=40 : LAUNCH
  clusters     = groupby(objection_category):
                   pct = members/|responders|
                   pull_quote = pick(max severity AND has evidence_id)
                   badge = evidence-chip if evidence_id else "model speculation"
                 -> sort desc, take top 5
  timeline[scene] = count(r where scene in r.trigger_moments)/|responders| ; peak = argmax
  panel_tiles  = 60 x {id, kind, emoji, sentiment, severity, quote, fix_tier, evidence_id}
  fix_rollup   = groupby(fix_tier): share of blast each tier explains   # drives 84 -> 55 -> 28
  stakeholders = reactions where kind=="stakeholder" -> verdict badges
  headline     = generate(top_cluster, brand)               # the future-artifact text
```

Because the UI is a pure function of `golden_run.json`, **Rung 0** = hand-author that JSON and the
dashboard renders fully; later swap in the real reduce output, renderer unchanged.

### 8.2 Aesthetic: War Room Broadsheet

A live broadsheet front page of a situation room. Layout uses the newspaper "above the fold / below
the fold" metaphor: above is the verdict, below is the forensics.

| Axis | Choice |
|------|--------|
| Display type | **Fraunces** (editorial serif; black weight for the giant number, italic for the headline) |
| Data type | **IBM Plex Mono** (every number, %, agent id, timestamp, ticker, stability band) |
| Artifact nameplate | a blackletter face (e.g. **UnifrakturCook**) only for "THE STRAITS STANDARD" |
| Base | newsprint-on-ink: `--ink #0B0C10`, `--paper #F3EFE3` (warm white, projector-safe) |
| Severity heat | `--calm #2E4A45` -> `--rising #E8A317` -> `--severe #F5402C` -> `--blast #FF2D55`, FILL + white text, never red text on black |
| Signature motion | the panel ignites in a staggered cascade while the Blast number rolls up and its heat meter fills |

### 8.3 Layout

```
+---------------------------------------------------------------------------+
| PREMORTEM | THE STRAITS STANDARD          SIMULATED . MerlionTel . 13 Jun  |  MASTHEAD
| <ticker> KIMI 60 . BRIGHT DATA 3 src . DAYTONA 60 sandboxes . VIDEODB 1    |
+-----------------------------------------------+---------------------------+
|  BLAST SCORE                                  |     [ AD KEYFRAME ]       |  ABOVE
|  +-----------+                                |      under test           |  THE
|  |    84     |  +/- 3   median of 3 runs      |                           |  FOLD
|  +-----------+                                |    [ DECISION: DELAY ]    |  (verdict)
|  % of the panel that would go public          |                           |
|                                                                           |
|  "MerlionTel's 'We're Listening' Ad Sparks Privacy Backlash"  (headline)  |
+-------------------- BELOW THE FOLD . THE FORENSICS ------------------------+  FOLD RULE
| THE KOPITIAM PANEL    | TOP OBJECTIONS         | BLAST MAP (timeline)       |
| [][][][][][][] 60     | # PRIVACY      78% [E] |  .::|##|::.  0:00---0:30   |
| [][][][][][][] ignite | # RACE / CMIO  61% [E] |  peak ^ 0:12 = 71%         |
| [][][][][][][] click  | # SURVEILLANCE 55% [E] |  click bar = who + frame   |
| sq=persona <>=lens    | # PRICING      22%     |  [news]YES [scales]ASAS HI |
+-----------------------+------------------------+----------------------------+
| THE FIX   84 --> 55 --> 28   (residual 28 = your call)                     |
| COPY rewrite 2 lines | PRODUCTION cut 0:12 scene | DECISION the premise     |
+---------------------------------------------------------------------------+
| TOMORROW'S HEADLINE  [ full fake front page . SIMULATED ]  <-> page-12     |
+---------------------------------------------------------------------------+
```

### 8.4 Component format

- **Blast Score banner (hero):** number 120pt+ Fraunces Black on a heat meter that fills to the
  score and shifts hue along the ramp; count-up 0 -> 84 on reveal; `+/- 3` in mono; a DECISION chip
  (LAUNCH / REVISE / DELAY, fill + white text) from the thresholds.
- **Kopitiam Panel (60 tiles):** shape-coded by `kind` (square=persona, diamond=lens, tab=stakeholder),
  fill = severity heat, abstain = flat gray (excluded from the denominator). Click -> quote card
  (36pt+ quote, the agent's `question`, a `fix_tier` tag, evidence chip if `evidence_id`). Tiles flip
  neutral -> heat in a staggered ignition cascade on reveal.
- **Top objections:** up to 5 ranked horizontal bars; category (serif), `%` (mono), width = share,
  fill = heat, a newspaper pull quote (italic serif), evidence chip or muted "model speculation".
- **Blast map (timeline):** ad runtime on X; one bar per scene, height + heat = agents triggered; the
  peak flies a callout ("0:12 . 71%") with a keyframe thumbnail; click a bar -> enlarged frame + the
  agents who triggered there + their fix tiers.
- **Stakeholder badges:** a strip from the 10 stakeholder agents -> journalist would-run YES, ASAS
  interest HIGH, opposition angle, competitor would pounce, staff morale risk.
- **The Fix:** a step-down chart 84 -> 55 -> 28 (residual stamped "DECISION . your call") + three tier
  cards: COPY (the 2 rewritten lines, before/after), PRODUCTION (cut scene 0:12 / recast, "unfixable
  by wording"), DECISION (the surveillance premise).
- **Tomorrow's Headline:** the full fake front page (blackletter nameplate, SenseNova-degraded
  keyframe, headline + subhead + fake byline, diagonal SIMULATED watermark) with a page-12 toggle.

### 8.5 Projector / presentation mode

Font floor 28pt, Blast 120pt+, quotes 36pt+, the peak callout 40-60pt solo. Dark base, paper-white
text, heat as fill not text. Test the light-theme toggle on the real projector at lunch. A
presentation mode walks the six demo beats by key/line cue over the static `golden_run.json`, kiosk,
zero tabs, hotkey to the backup recording within 5 seconds. Nothing live, nothing to break.

## 9. Build plan (unified repo, no lanes, golden-run first)

**Stack (locked):** Python **FastAPI** backend + single static HTML/CSS/JS dashboard served by
FastAPI (no build step, instant SSE, matches the VideoDB/Daytona Python SDKs). Leaner than Next.js
for a replay-focused unified build.

Working dir `C:\hack\AI-Forge-Hackathon`. `PYTHONIOENCODING=utf-8`. Single saved network = hotspot.
One **merge owner** even with no lanes; everyone sequences on the critical path and pairs on the
current rung.

**Rung ladder (each rung is already a shippable demo):**

| Rung | Deliverable | Guarantees |
|------|-------------|-----------|
| **0 = CUT B (sacred)** | replay harness + report UI driven by a golden JSON (hand-authored if needed) | a demo exists no matter what |
| 1 | real Kimi panel, copy-only, 60 agents async + prefix cache -> real text-tier golden JSON + Blast Score + clusters | robust demo from real reactions |
| 2 (hero) | VideoDB ingest of the MerlionTel film -> manifest; multimodal reactions with `trigger_moments`; timeline scrubber; SenseNova front page; two-stage fix | the full-creative wow |
| 3 (production story) | wrap agent in Daytona sandbox + self-grounding; run 60 sandboxed agents ONCE to bake the authentic golden run + capture transcripts | Daytona core + injection story real |
| 4 (booth, post-demo) | general "paste your own ad" live path | product, not just a video |

**Timeline (hacking 11:30 to 16:30):**

| Time | Output |
|------|--------|
| 11:30-11:45 | scaffold FastAPI + static, `.env`, smoke every API over hotspot. **11:35: Kimi 60-burst test + Daytona sandbox spin-up timing** (decides live N + sandbox-offline-only) |
| 11:45-12:30 | golden JSON schema frozen + replay harness + 6-section report UI on a hand-authored golden JSON **[Rung 0 / CUT B]** |
| 12:30-13:10 | real Kimi 60-agent copy-only panel -> real text golden JSON + Blast Score + clusters **[Rung 1]**. Lunch at keyboard |
| 13:10-14:00 | VideoDB ingest MerlionTel film + multimodal reactions + timeline scrubber **[Rung 2 starts]** |
| 14:00-14:40 | 3-tier fix triage + two-stage drop + SenseNova front page + page-12 callback **[Rung 2 done]** |
| 14:40-15:20 | Daytona sandbox + self-grounding, run 60 ONCE to bake authentic golden run + receipts **[Rung 3]**. Fallback: keep 13:10 JSON + a few real sandbox screenshots |
| 15:20-15:40 | 3-bucket grounding wired + 3-run stability + calibration runs (E-Pay text smoke / entity-swap / boring control) |
| 15:40-16:25 | **FREEZE.** Wi-Fi off acceptance test, 2 rehearsals (timer), backup recording, P0 only |

**Sacrifice ladder:** 30 min behind -> cut Rung 3 live (keep text golden JSON + sandbox screenshots)
+ Terminal 3. 60 min -> cut VideoDB live ingest, hand-author the manifest from keyframes, 60->40
agents. 90 min -> demo = Rung 0 replay of the best golden JSON + report. **Never cut:** the replay
harness, 2 rehearsals, backup recording.

## 10. Demo script (2 min, ad-film edition)

| Time | Screen | Line |
|------|--------|------|
| 0:00-0:08 | scandal front page (degraded keyframe) | "This is tomorrow's front page. The ad that causes it hasn't aired yet. We have 90 seconds to stop it." |
| 0:08-0:20 | 5s of the MerlionTel ad + RUN | "MerlionTel's new ad: an AI that speaks every Singaporean's language by listening to your calls. Their agency loved it. Let's ask Singapore first." |
| 0:20-0:45 | 60 tiles ignite, counter to 84 | "Sixty agents, each in its own sandbox, grounded in this week's discourse. Blast Score 84: that many would go public against you." |
| 0:45-1:10 | timeline scrubber spike at 0:12 -> keyframe zoom + "78% PRIVACY" | "One shot did most of the damage. 71% triggered on the casting at 0:12." |
| 1:10-1:35 | two-stage fix: 84 -> 55 -> 28 | "Rewrite the privacy line: 84 to 55. The casting is unfixable by wording, so cut that scene: 55 to 28. The last 28 is the surveillance premise. That is your call, not our copy edit." |
| 1:35-2:00 | front page -> page-12 | "We caught it before the shoot wrapped. We smoke-tested on E-Pay 2019: it catches what Singapore actually caught. Ninety seconds. Cheaper than one apology." |

Naming pass: "each agent sandboxed in **Daytona**, self-grounding via **Bright Data**, seeing the film
through **VideoDB**, reasoning on **Kimi K2.6**, scandal frame by **SenseNova**."

## 11. Risk register

| Risk | Mitigation |
|------|-----------|
| VideoDB ingest latency (async, minutes) | bake offline, never on stage |
| 60 Daytona cold-starts | bake offline; live shows few or pure replay; burst test at 11:35 |
| Multimodal JSON flakiness | transcript-only fallback (agents read scene descriptions instead of keyframes) |
| 5 sponsors = wide integration surface | each used only to bake the golden run + capture receipts, not robust live |
| Unified repo, 3+ devs | one merge owner, sequence rungs, CUT B sacred |
| Real-ad legal / POFMA | golden run is fictional MerlionTel; real disasters stay text smoke tests; fictional masthead + SIMULATED watermark |
| Identity-persona ethics | concern-lens design (third person, evidence-cited) + dogfood-our-own-script backup slide |

## 12. Judging-criteria mapping

| Criterion | Our card |
|-----------|----------|
| Completeness | golden-run replay guarantees a working end-to-end demo; rung ladder + sacrifice ladder |
| Innovation | full-creative timeline blast map + 3-tier fix triage (copy/production/decision) + future-artifact front page |
| Real-Life Problem | ad backlash is a real budget line (focus groups $5-15k) and named disasters (E-Pay, Pepsi, Bud Light) |
| Sponsored Usage | 5 core sponsors, each architecturally load-bearing, with a quantified receipts slide |

## 13. Repo layout (planned)

```
/app           FastAPI app + the broadsheet dashboard (index.html, app.js, styles.css), renders golden_run.json
/agents        seed cards (~37) + the jitter expander -> personas.json (60) + prompt-assembly templates
/sponsors      kimi.py, brightdata.py, daytona.py, videodb.py, sensenova.py (+ terminal3.py add-on)
/pipeline      creative ingest, grounding (3 buckets), reduce (60 -> dashboard_state), fix triage
/golden        golden_run.json + creative manifest + keyframes (the demo replays this)
/fixtures      MerlionTel ad assets, E-Pay/Pepsi text smoke tests, entity-swap, boring control
/docs          demo script, runbook, sponsor receipts
```

## 14. Decisions locked

1. Vertical: **ad / marketing campaign**.
2. Input: **full creative** (copy + key visual + ad film).
3. Grounding: **per-scenario self-grounding**, 3 buckets, built live, demo cached.
4. Agents: **60, each in a Daytona sandbox** (injection containment), baked once offline.
5. Build: **unified repo, no lane split**, golden-run carries the demo.
6. Stack: **Python FastAPI + static dashboard**.
7. Golden-run brand: **MerlionTel** (fictional).
8. Terminal 3: **conditional add-on** (only if ahead of CUT B).
9. Live N: **decided by the 11:35 Kimi burst + Daytona spin-up test.**
