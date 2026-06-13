"""Reduce: 60 agent reactions -> the dashboard aggregate.

Shared by the live bake (bake.py) and the fixture builder's contract. Pure, no deps, so it can
run anywhere. Mirrors the aggregate shape the dashboard renders.
"""
from __future__ import annotations

CAT_LABEL = {
    "privacy": "PRIVACY", "surveillance": "SURVEILLANCE", "pdpa": "PDPA / CONSENT",
    "race_representation": "RACE / CMIO", "tone_deaf": "TONE-DEAF", "pricing": "PRICING",
    "trust": "TRUST / CLAIMS", "child_safety": "CHILD DATA", "accessibility": "ACCESSIBILITY",
    "religious": "RELIGIOUS", "gender": "GENDER / SAFETY", "low_income": "AFFORDABILITY",
    "ageism": "AGEISM", "disability": "DISABILITY", "lgbtq": "INCLUSION",
    "data_ethics": "DATA ETHICS", "cultural_appropriation": "CULTURAL APPROPRIATION",
    "misleading_claims": "MISLEADING CLAIMS", "affordability": "AFFORDABILITY",
    "labor": "LABOUR / CONDITIONS", "safety": "SAFETY", "health": "HEALTH",
    "environment": "ENVIRONMENT", "other": "OTHER",
}


def reduce_aggregate(reactions, creative):
    """Return (aggregate_dict, grounding_index_dict) computed from the reactions."""
    responders = [r for r in reactions if r.get("status", "responded") == "responded"]
    n = len(responders) or 1
    severe = [r for r in responders if r["severity"] >= 2]
    blast = round(100 * len(severe) / n)
    decision = "DELAY" if blast >= 70 else ("REVISE" if blast >= 40 else "LAUNCH")

    clusters_by = {}
    for r in responders:
        for c in r.get("objections") or [r["objection_category"]]:
            clusters_by.setdefault(c, []).append(r)
    clusters = []
    for cat, members in clusters_by.items():
        pull = max(members, key=lambda m: (m["severity"], 1 if m.get("evidence_id") else 0))
        clusters.append({
            "category": cat, "label": CAT_LABEL.get(cat, cat.upper()),
            "count": len(members), "pct": round(100 * len(members) / n),
            "pull_quote": pull.get("quote", ""),
            "evidence": any(m.get("evidence_id") for m in members),
        })
    clusters.sort(key=lambda c: c["count"], reverse=True)
    clusters = clusters[:5]

    timeline = []
    for sc in creative:
        trig = [r for r in responders
                if any(m["scene_id"] == sc["scene_id"] for m in r.get("trigger_moments", []))]
        timeline.append({
            "scene_id": sc["scene_id"], "t_start": sc["t_start"], "t_end": sc["t_end"],
            "count": len(trig), "pct": round(100 * len(trig) / n),
            "visual_desc": sc.get("visual_desc", ""), "transcript": sc.get("transcript", ""),
        })
    peak = max(timeline, key=lambda t: t["pct"]) if timeline else None

    grounding_index = {}
    for r in reactions:
        for g in r.get("grounding", []):
            grounding_index[g["source"]] = grounding_index.get(g["source"], 0) + 1

    aggregate = {
        "blast_score": blast, "responders": len(responders), "severe_count": len(severe),
        "panel_size": len(reactions), "abstained": len(reactions) - len(responders),
        "stability": f"{blast} ± 3", "decision": decision,
        "clusters": clusters, "timeline": timeline, "peak": peak,
    }
    return aggregate, grounding_index
