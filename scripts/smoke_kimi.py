"""One-call Kimi smoke test: confirms the key + base_url work and discovers the model id."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_dotenv(p):
    if not os.path.exists(p):
        return
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


load_dotenv(os.path.join(ROOT, ".env"))
from openai import OpenAI  # noqa: E402

base = os.environ.get("KIMI_BASE_URL", "https://api.moonshot.ai/v1")
key = os.environ.get("KIMI_API_KEY", "")
want = os.environ.get("KIMI_MODEL", "kimi-k2.6")
print(f"base={base}  key={'set(' + str(len(key)) + ')' if key else 'MISSING'}  want_model={want}")

client = OpenAI(api_key=key, base_url=base)

# 1) discover available models
models = []
try:
    models = [m.id for m in client.models.list().data]
    print("available models:", models)
except Exception as e:
    print("models.list ERROR:", type(e).__name__, "|", str(e)[:200])

pick = want if want in models else next((m for m in models if "kimi" in m.lower() or "moonshot" in m.lower()), want)
print("using model:", pick)

# 2) one real chat call (JSON mode)
try:
    r = client.chat.completions.create(
        model=pick,
        messages=[
            {"role": "system", "content": "You simulate a Singaporean panellist. Reply ONLY as JSON."},
            {"role": "user", "content": 'React to: a telco that records your phone calls to personalise ads. JSON: {"severity": 0-3, "quote": "one sentence"}'},
        ],
        response_format={"type": "json_object"}, max_tokens=800, temperature=1,
    )
    ch = r.choices[0]
    m = ch.message
    print("CHAT OK  finish_reason:", ch.finish_reason)
    print("content:", repr(m.content))
    print("reasoning:", repr(getattr(m, "reasoning_content", None))[:400])
    if getattr(r, "usage", None):
        print(f"usage: {r.usage.prompt_tokens} in / {r.usage.completion_tokens} out")
except Exception as e:
    print("CHAT ERROR:", type(e).__name__, "|", str(e)[:400])
    sys.exit(1)
