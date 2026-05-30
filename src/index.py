#!/usr/bin/env python3
"""
video-brief-writer — topic/URL/idea → complete YouTube/TikTok/Reels video brief
Hook formulas, script outline, B-roll list, thumbnail concepts,
title variants, SEO tags, posting schedule, retention tactics
"""
import anthropic, json, re, sys, urllib.request
from pathlib import Path

SYSTEM = """You are a YouTube strategist and viral content director who has helped channels
grow from 0 to 1M+ subscribers. You understand retention psychology deeply.

Create a complete, actionable video production brief.

Return ONLY valid JSON — no markdown, no explanation.

{
  "topic": "refined topic statement",
  "platform": "YouTube|TikTok|Instagram_Reels|YouTube_Shorts|all",
  "video_format": "educational|listicle|story|documentary|how_to|opinion|reaction|challenge",
  "target_length_minutes": number,
  "hook": {
    "primary": "first 5-10 seconds script — the scroll stopper",
    "alternatives": ["3 alternative hooks using different formulas"],
    "hook_formula": "curiosity_gap|pain_point|bold_claim|story_tease|question|shocking_stat"
  },
  "title_variants": [
    {"title":"string","why":"psychological trigger it uses","predicted_ctr":"low|medium|high|very_high"}
  ],
  "thumbnail": {
    "primary_concept": "detailed description of the thumbnail",
    "text_overlay": "3-5 words max",
    "emotion": "curiosity|shock|excitement|fear|hope",
    "color_scheme": "high contrast suggestion",
    "face_expression": "surprised|confident|concerned|excited|null"
  },
  "script_outline": [
    {
      "section": "Hook|Intro|Main|Transition|CTA|Outro",
      "timestamp_start": "0:00",
      "timestamp_end": "0:30",
      "talking_points": ["key points to cover"],
      "retention_tactic": "pattern_interrupt|open_loop|social_proof|callback|cliffhanger",
      "b_roll": ["visuals to cut to during this section"]
    }
  ],
  "three_act_structure": {
    "act_1_hook": "what you promise the viewer",
    "act_2_content": "how you deliver on the promise",
    "act_3_payoff": "the satisfying conclusion and CTA"
  },
  "seo": {
    "primary_keyword": "main search term",
    "secondary_keywords": ["list"],
    "tags": ["20 YouTube tags"],
    "description_first_line": "first 125 chars of description (most important for SEO)"
  },
  "engagement_triggers": {
    "comment_bait": "question to ask that drives comments",
    "like_trigger": "moment to ask for like and why they should",
    "subscribe_hook": "what to promise subscribers",
    "community_post_idea": "follow-up community post to keep engagement going"
  },
  "chapters": [
    {"timestamp":"0:00","title":"chapter title"}
  ],
  "production_notes": {
    "tone": "educational|entertaining|inspirational|controversial|conversational",
    "pacing": "fast_cuts|slow_build|mixed",
    "graphics_needed": ["list of graphics or animations"],
    "music_mood": "upbeat|tense|inspiring|chill|dramatic",
    "estimated_edit_hours": number
  },
  "repurposing": {
    "shorts_clip": "which section makes the best Short (timestamp and why)",
    "twitter_thread": "3-tweet thread from the content",
    "linkedin_post": "professional angle from the same content",
    "newsletter_hook": "how to introduce this in a newsletter"
  },
  "upload_strategy": {
    "best_day": "Monday|Tuesday|...|Saturday|Sunday",
    "best_time": "EST time window",
    "first_hour_actions": ["pin comment","reply to early comments","share to community tab"],
    "collaboration_angle": "who you could collab with on this topic"
  }
}"""

def generate(topic: str, platform: str = "YouTube", url: str = "") -> dict:
    client = anthropic.Anthropic()
    context = f"Platform: {platform}\nTopic/Idea: {topic}"
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"video-brief-writer/1.0"})
            html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8",errors="replace")
            text = re.sub(r'<[^>]+>',' ',re.sub(r'<script[^>]*>[\s\S]*?</script>','',html,flags=re.I))
            text = re.sub(r'\s+',' ',text).strip()[:5000]
            context += f"\n\nSource content:\n{text}"
        except Exception as e:
            context += f"\n\nURL: {url} (could not fetch: {e})"

    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Create a complete video brief for:\n\n{context}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def print_brief(r: dict):
    hook = r.get("hook",{})
    thumb = r.get("thumbnail",{})
    seo = r.get("seo",{})
    prod = r.get("production_notes",{})
    upload = r.get("upload_strategy",{})

    print(f"\n{'═'*60}")
    print(f"  VIDEO BRIEF — {r.get('topic','')}")
    print(f"  {r.get('platform','')} | {r.get('video_format','')} | ~{r.get('target_length_minutes','?')} min")
    print(f"{'═'*60}")

    print(f"\n  HOOK")
    print(f"  \"{hook.get('primary','')}\"")
    print(f"  Formula: {hook.get('hook_formula','?')}")
    alts = hook.get("alternatives",[])
    if alts:
        print(f"\n  Alternative hooks:")
        for alt in alts: print(f"  • \"{alt}\"")

    titles = r.get("title_variants",[])
    if titles:
        print(f"\n  TITLES (by predicted CTR)")
        for t in sorted(titles, key=lambda x: ["low","medium","high","very_high"].index(x.get("predicted_ctr","low")), reverse=True):
            ctr_bar = {"low":"○○○○","medium":"●●○○","high":"●●●○","very_high":"●●●●"}.get(t.get("predicted_ctr","low"),"")
            print(f"  {ctr_bar} {t.get('title','')}")
            print(f"       {t.get('why','')}")

    print(f"\n  THUMBNAIL")
    print(f"  Concept: {thumb.get('primary_concept','')}")
    print(f"  Text: \"{thumb.get('text_overlay','')}\" | Emotion: {thumb.get('emotion','?')}")

    outline = r.get("script_outline",[])
    if outline:
        print(f"\n  SCRIPT OUTLINE")
        for section in outline:
            print(f"\n  [{section.get('timestamp_start','?')}–{section.get('timestamp_end','?')}] {section.get('section','?')}")
            for pt in section.get("talking_points",[])[:3]: print(f"  • {pt}")
            tactic = section.get("retention_tactic")
            if tactic: print(f"  🧠 Retention: {tactic}")

    eng = r.get("engagement_triggers",{})
    if eng.get("comment_bait"):
        print(f"\n  ENGAGEMENT")
        print(f"  Comment bait: \"{eng['comment_bait']}\"")
        if eng.get("like_trigger"): print(f"  Like trigger: {eng['like_trigger']}")

    print(f"\n  SEO: {seo.get('primary_keyword','?')}")
    print(f"  Tags: {', '.join(seo.get('tags',[])[:8])}")
    print(f"\n  Upload: {upload.get('best_day','?')} {upload.get('best_time','?')}")
    print(f"  Edit time: ~{prod.get('estimated_edit_hours','?')} hours")

    rep = r.get("repurposing",{})
    if rep.get("shorts_clip"): print(f"\n  Shorts clip: {rep['shorts_clip']}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate complete video production brief")
    p.add_argument("topic", help="Video topic, idea, or description")
    p.add_argument("--platform","-p",default="YouTube",choices=["YouTube","TikTok","Instagram_Reels","YouTube_Shorts","all"])
    p.add_argument("--url","-u",default="",help="Source URL to base the video on")
    p.add_argument("--json",action="store_true")
    a = p.parse_args()
    r = generate(a.topic, a.platform, a.url)
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_brief(r)
