import feedparser
from html import escape
from datetime import datetime

FEEDS = {
    "Nature Medicine": "https://www.nature.com/nm.rss",
    "npj Digital Medicine": "https://www.nature.com/npjdigitalmed.rss",
    "Nature Addiction": "https://www.nature.com/subjects/addiction.rss",
}

items = []

for source, url in FEEDS.items():
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:6]:
            title = entry.get("title", "无标题")
            link = entry.get("link", "#")
            published = entry.get("published") or entry.get("updated") or ""
            items.append((source, title, link, published))
    except Exception as e:
        print(f"跳过 {source}: {e}")

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

html = f"""<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>我的 AI 医疗资讯雷达</title>
<style>
body {{ font-family: -apple-system, Arial, sans-serif; max-width: 900px; margin: 30px auto; padding: 0 16px; line-height: 1.6; }}
h1 {{ font-size: 26px; }}
.item {{ border-bottom: 1px solid #ddd; padding: 14px 0; }}
.source {{ color: #666; font-size: 13px; }}
a {{ color: #0969da; }}
.notice {{ background: #f6f8fa; padding: 12px; border-radius: 6px; color: #555; }}
</style>
</head>
<body>
<h1>我的 AI 医疗资讯雷达</h1>
<p class="notice">自动更新，信息整理，不构成医疗建议。更新时间：{now}</p>
"""

if not items:
    html += "<p>今天没有抓到内容。请检查信息源。</p>"

for source, title, link, published in items:
    html += f"""
    <div class="item">
      <div><b>{escape(title)}</b></div>
      <div class="source">{escape(source)} {escape(published)}</div>
      <div><a href="{escape(link)}">读原文</a></div>
    </div>
    """

html += """
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"生成完成，共 {len(items)} 条")
