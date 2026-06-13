# 60's Pulse

**See tomorrow's backlash before you launch today.**

60's Pulse is an AI premortem for advertising campaigns. Paste a campaign or run a film through
the system, and it simulates a 60-member Singaporean reaction panel before the public gets to it.
The output is not a generic sentiment score. It is a launch decision, a blast map, the objections
that will spread, and the cheapest fix path.

## The Problem

Brands usually discover ad backlash after the media cycle starts:

- The campaign is already live.
- The apology is already being drafted.
- The production budget is already sunk.
- The issue is not always the copy; sometimes it is the casting, the premise, the timing, or the
  stakeholder who can turn a bad comment into a headline.

Focus groups are slow, expensive, and often too polite. Social listening only works after the
damage is public. 60's Pulse moves that backlash test to before launch.

## What It Does

60's Pulse takes an ad campaign and returns a campaign premortem:

1. **Blast Score**
   The share of the simulated panel likely to object strongly enough to go public, boycott, report,
   or generate negative coverage.

2. **60-Agent Reaction Panel**
   A grid of Singaporean personas, issue lenses, and stakeholder roles reacting to the same creative.
   Each response includes a quote, severity, trigger moment, fix tier, and press-conference question.

3. **Timeline Blast Map**
   For video campaigns, it identifies which scene or second detonates the panel. This turns
   "people may dislike it" into "0:12 is the shot that causes the issue."

4. **Top Objection Clusters**
   The system groups reactions into categories like privacy, PDPA/consent, representation, pricing,
   accessibility, child safety, religious sensitivity, or trust.

5. **Three-Tier Fix Triage**
   It separates objections by what kind of intervention can actually fix them:
   - **Copy**: rewrite the line, claim, tagline, or voiceover.
   - **Production**: cut/recast/reshoot imagery that wording cannot repair.
   - **Decision**: the concept itself is the risk; this is a launch call, not a copy edit.

6. **Tomorrow's Headline**
   A fictional front page shows the likely public narrative if the campaign ships unchanged.

## The Core Insight

Most brand-safety tools answer:

> Is this campaign positive or negative?

60's Pulse answers:

> What exactly will people attack, who will amplify it, which second caused it, and what is the
> cheapest fix before launch?

That is the selling point: **from vibe check to launch decision.**

## Why 60 Agents

The panel is designed for risk coverage, not census polling.

- **35 public personas** capture consumer reactions and social-sharing behavior.
- **15 concern lenses** inspect sensitive risk areas in third person, such as PDPA, accessibility,
  child data, religious sensitivity, racial representation, and low-income impact.
- **10 stakeholder agents** represent the groups that can escalate a problem: journalists,
  regulators, ad standards, opposition MPs, competitor PR, employees, activist groups, and consumer
  associations.

Identity-sensitive perspectives are not roleplayed in first person. They are handled as third-person
concern lenses, which is safer and more defensible.

## Demo Story

The baked demo uses a fictional telco campaign:

> MerlionTel launches "We're Listening", an AI that listens to customer calls to personalize ads.

60's Pulse catches three different failure modes:

- **Copy risk**: "we listen to your calls" creates immediate privacy panic.
- **Production risk**: a scene reads as tone-deaf representation and cannot be fixed by rewriting.
- **Decision risk**: the surveillance premise may be fundamentally unsellable.

The demo turns this into a concrete fix sequence:

```text
Blast Score 84
  -> rewrite the privacy line
Score drops to 55
  -> cut or reshoot the problematic scene
Score drops to 28
  -> remaining risk is the product premise
```

That final 28 is the client decision. The tool does not pretend copy can save a bad premise.

## Product Differentiators

### It Is Creative-Specific

The output is tied to campaign scenes, lines, and moments. It does not just say "privacy risk";
it points to the line or shot that causes the reaction.

### It Is Fix-Oriented

Every objection is tagged by the cheapest fix tier. This makes the output useful to marketers,
creatives, legal, and leadership in the same meeting.

### It Models Escalation

The panel includes not only consumers, but also the people who turn backlash into consequences:
press, regulators, opposition voices, competitors, staff, and advocacy groups.

### It Is Demo-Safe

The live-capable system bakes a golden run offline. The stage demo replays a single JSON artifact,
so the presentation does not depend on Wi-Fi, sponsor latency, or 60 live calls.

### It Uses Sponsors With A Clear Role

- **Kimi / Moonshot**: 60-agent structured reaction panel.
- **Bright Data**: per-agent public-discourse grounding.
- **Daytona**: sandbox isolation and agent execution receipts.
- **VideoDB**: video transcript, scene extraction, and creative manifest.
- **SenseNova**: fictional scandal-front-page image concept.

Each sponsor maps to a production concern: reasoning, grounding, isolation, video understanding,
and future-artifact generation.

## What The User Gets

The final dashboard is a war-room broadsheet:

- a giant Blast Score,
- the fake tomorrow headline,
- the 60-agent panel,
- top objection clusters,
- a timeline blast map,
- stakeholder escalation badges,
- and a fix triage showing what to rewrite, reshoot, or cancel.

It is built for the meeting where a brand asks:

> Should we launch this?

## Current Demo Surface

The repository currently supports:

- a static dashboard served by FastAPI,
- a baked MerlionTel golden run,
- a live typed-campaign path through `/api/analyze`,
- a live/fixture bake script,
- Kimi or OpenAI-compatible panel generation,
- optional Daytona sandbox receipts,
- optional VideoDB creative ingest,
- Bright Data grounding hooks with parser work still pending.

The dashboard intentionally renders one JSON object. That keeps the product story simple: live work
produces the premortem artifact; the user-facing surface explains the decision.

## Run It

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Run the no-network fixture smoke:

```bash
python bake.py --mode fixture --mini 2
```

Run a cheap live smoke:

```bash
python bake.py --mode live --mini 6
```

Attach Daytona sandbox receipts:

```bash
python bake.py --mode live --mini 3 --sandbox daytona --sandbox-mini 3
```

Ingest a video through VideoDB:

```bash
python bake.py --mode live --video-source "https://example.com/ad.mp4" --mini 6
```

## Environment

Fixture mode needs no keys. Live mode uses the keys relevant to the provider path:

```env
KIMI_API_KEY=
KIMI_BASE_URL=https://api.moonshot.ai/v1
KIMI_MODEL=moonshot-v1-8k

BRIGHTDATA_API_KEY=
BRIGHTDATA_SERP_ZONE=
BRIGHTDATA_UNLOCKER_ZONE=

DAYTONA_API_KEY=
DAYTONA_API_URL=https://app.daytona.io/api

VIDEODB_API_KEY=

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## One-Line Pitch

**60's Pulse is a campaign premortem that shows the backlash, the blast moment, and the fix path
before the campaign becomes tomorrow's apology.**
