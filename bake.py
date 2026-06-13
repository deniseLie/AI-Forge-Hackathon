"""Bake a golden_run.json with the live (or fixture) sponsor pipeline.

The dashboard always replays golden_run.json. This script PRODUCES it:
  load agent specs  ->  per-agent grounding (Bright Data)  ->  Kimi panel  ->  reduce  ->  write.

  python bake.py --mode fixture            # reproduce the baked run, no network (testable now)
  python bake.py --mode live --mini 6      # cheap smoke test: 6 real agents, does not write
  python bake.py --mode live               # full 60-agent live bake -> golden/golden_run.json

"build real, demo baked": run this ONCE offline to make a real golden run; the demo replays it.
Dev against --mode fixture; spend Kimi/Bright Data credit only on deliberate live bakes.
"""
import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from app.pipeline import reduce_aggregate  # noqa: E402
from app.sponsors import brightdata, kimi  # noqa: E402


def load_dotenv(path):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fixture", "live"], default="fixture")
    ap.add_argument("--mini", type=int, default=0, help="only the first N agents; does not write")
    ap.add_argument("--src", default=os.path.join(ROOT, "golden", "golden_run.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "golden", "golden_run.json"))
    args = ap.parse_args()
    load_dotenv(os.path.join(ROOT, ".env"))

    golden = json.load(open(args.src, encoding="utf-8"))
    agents = golden["reactions"]
    if args.mini:
        agents = agents[: args.mini]
    scenario, creative = golden["scenario"], golden["creative_manifest"]
    print(f"baking mode={args.mode} agents={len(agents)} brand={scenario['brand']}")

    # 1) per-agent grounding (each agent runs its own query)
    for a in agents:
        a["grounding"] = brightdata.ground(a, scenario, mode=args.mode)

    # 2) Kimi panel (fan-out, shared cached prefix + per-agent block)
    reactions = await kimi.run_panel(agents, scenario, creative, mode=args.mode)

    # 3) reduce -> aggregate
    aggregate, grounding_index = reduce_aggregate(reactions, creative)
    golden["reactions"] = reactions
    golden["aggregate"] = aggregate
    golden["grounding_index"] = grounding_index
    golden["mode"] = args.mode

    print(f"  blast={aggregate['blast_score']} decision={aggregate['decision']} "
          f"responders={aggregate['responders']} top={aggregate['clusters'][0]['label'] if aggregate['clusters'] else '-'}")

    if args.mini:
        print("  (mini smoke test: not writing)")
        return
    json.dump(golden, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
