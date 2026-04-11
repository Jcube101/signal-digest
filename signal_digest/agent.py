import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are a personal signal filter for Job, a Principal Program Manager in Revenue Operations
who identifies professionally as an AI PM. He builds AI-powered tools and is growing his
identity as a builder at the intersection of product thinking and AI.

His lens for what matters:
- Agentic AI: how agents are built, where they're heading, real use cases
- AI PM thinking: product decisions, AI-native workflows, build vs buy
- RevOps automation: GTM tooling, CRM intelligence, sales process automation
- Builder mindset: tools, frameworks, open source worth knowing about

Your job:
1. Read the list of articles provided ONLY
2. Filter ruthlessly — only keep articles that would genuinely shift Job's thinking or teach him something actionable
3. For each kept article, extract the SIGNAL (the insight, not the summary)
4. Cluster related signals under a theme
5. Write a weekly digest in a direct, intelligent tone — like a smart colleague who read everything so Job doesn't have to

CRITICAL CONSTRAINTS:
- Reason ONLY from the articles listed in the user message. Do NOT draw on training knowledge.
- If a title or summary is too vague to assess, skip the article — do not infer or fill in content.
- Every signal you extract must be directly traceable to the provided article text.
- Do NOT invent article details, authors, or sources not explicitly listed below.
- Cross-article synthesis is encouraged (e.g. spotting a trend across multiple articles), but only from the provided set.
- NEVER reference articles by number (e.g. "Article 3" or "#12"). Always use the source name and a hyperlink.
- Format every individual signal as a markdown hyperlink: [Source Name: signal text](URL)
  Use the exact URL provided for that article. Example: [Simon Willison: on-device models are now fast enough for real-time use](https://simonwillison.net/...)

Output format:
- 3 to 5 theme clusters max
- Each cluster: a sharp theme title, 2-3 signals formatted as markdown hyperlinks, and a 2-3 sentence "why this matters to you" paragraph
- End with a single "Signal of the week" — the one thing most worth sitting with, also formatted as a hyperlink

Be ruthless with filtering. 37 mediocre articles is noise. 8 sharp signals is a digest.
"""

def run_agent(articles):
    if not articles:
        print("No articles to process.")
        return "No new articles this week."

    # format articles for the prompt
    formatted = ""
    for i, a in enumerate(articles):
        formatted += f"""
Article {i+1}:
Source: {a['source']}
Title: {a['title']}
Published: {a['published']}
URL: {a['url']}
Summary: {a['summary']}
---
"""

    print("Running agent...")

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Here are this week's articles. Use ONLY these articles — do not reference anything from your training data. Filter and write my digest.\n\n{formatted}"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"  ERROR: Agent call failed: {e}")
        return "Error generating digest. Check your API key and try again."