"""Live analyze: turn a typed campaign into a full premortem result (the /api/analyze path).

Reuses the agent roster (the 60 personas/lenses/stakeholders by label + kind) but regenerates
their reactions for the NEW campaign via the LLM. This is the 'paste your own ad' flow. Heavier
than the baked replay (60 real LLM calls), so the input screen falls back to the baked golden run
if it fails.
"""
from __future__ import annotations

import re

from app.pipeline import reduce_aggregate
from app.sponsors import kimi


def _scenes_from_text(campaign: str):
    """Split the campaign into sentence 'scenes' so the timeline / trigger index works on text."""
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+|\n+", campaign) if p.strip()]
    parts = parts[:12] or [campaign[:200]]
    return [
        {"scene_id": f"s{i}", "t_start": i, "t_end": i + 1, "keyframe": "",
         "visual_desc": "", "transcript": p, "on_screen_text": ""}
        for i, p in enumerate(parts)
    ]


def _roster(golden):
    """Reuse identity (agent_id/kind/label) but drop the baked reaction + grounding."""
    roster = []
    for r in golden["reactions"]:
        roster.append({
            "agent_id": r["agent_id"], "kind": r["kind"], "emoji": r.get("emoji", ""),
            "label": r["label"], "status": "responded", "verdict": r.get("verdict"),
            "objections": [], "quote": "", "severity": 0, "fix_tier": "copy",
            "grounding_query": "", "grounding": [],
        })
    return roster


def _headline(brand, clusters):
    top = clusters[0] if clusters else {"label": "PUBLIC", "pct": 0}
    label = top["label"].title()
    return {
        "masthead": "THE SIGNAL", "dateline": "TOMORROW",
        "title": f"{brand}’s Launch Sparks {label} Backlash",
        "subtitle": f"A simulated global public-and-press panel flags {label.lower()} concerns within hours of the announcement",
        "byline": "By Staff Correspondent",
        "body": f"{brand} faced swift criticism after its announcement, with a large share of a simulated public-and-press panel raising {label.lower()} and related concerns.",
        "page12_title": f"{brand} revises the launch; analysts shrug",
        "page12_body": "A revised, lower-key version of the launch drew little attention.",
    }


def _fix(reactions, blast):
    severe = [r for r in reactions if r.get("status", "responded") == "responded" and r["severity"] >= 2]
    n = len(severe) or 1
    frac = {t: sum(1 for r in severe if r.get("fix_tier") == t) / n for t in ("copy", "production", "decision")}
    after_copy = max(0, round(blast * (1 - frac["copy"])))
    after_prod = max(0, round(after_copy - blast * frac["production"]))
    residual = max(0, round(blast * frac["decision"]))
    return {
        "stages": [
            {"id": "baseline", "label": "As submitted", "score": blast, "detail": "The campaign as written."},
            {"id": "copy", "label": "Rewrite copy-fixable lines", "score": max(after_copy, residual),
             "tier": "copy", "detail": "Wording-level objections resolved."},
            {"id": "production", "label": "Fix production-level issues", "score": max(after_prod, residual),
             "tier": "production", "detail": "Casting / imagery / tone. Unfixable by wording."},
        ],
        "residual": {"score": residual, "tier": "decision",
                     "label": "The concept itself. A launch call, not a copy edit."},
    }


async def analyze(campaign, brand, golden, provider="kimi", mode="live"):
    brand = brand or "the brand"
    campaign = (campaign or "").strip()[:2500]  # cap pasted walls of text (tokens + layout)
    scenario = {"brand": brand, "category": "Campaign", "campaign": campaign,
                "date": golden.get("scenario", {}).get("date", "")}
    creative = _scenes_from_text(campaign)
    roster = _roster(golden)

    reactions = await kimi.run_panel(roster, scenario, creative, mode=mode, provider=provider)
    aggregate, grounding_index = reduce_aggregate(reactions, creative)

    badges = [
        {"emoji": r.get("emoji", ""), "role": r["label"], "verdict": r.get("verdict", ""), "note": r.get("quote", "")}
        for r in reactions if r["kind"] == "stakeholder"
    ]
    return {
        "run_id": "live", "mode": "live", "scenario": scenario, "creative_manifest": creative,
        "grounding_index": grounding_index, "reactions": reactions, "aggregate": aggregate,
        "fix": _fix(reactions, aggregate["blast_score"]),
        "stakeholder_badges": badges, "headline": _headline(brand, aggregate["clusters"]),
        "sponsor_trace": golden.get("sponsor_trace", []),
    }
