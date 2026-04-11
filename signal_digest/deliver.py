import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def markdown_to_html(text):
    lines = text.split("\n")
    html_lines = []
    
    for line in lines:
        # h1
        if line.startswith("# "):
            line = f"<h1>{line[2:]}</h1>"
        # h2
        elif line.startswith("## "):
            line = f"<h2>{line[3:]}</h2>"
        # h3
        elif line.startswith("### "):
            line = f"<h3>{line[4:]}</h3>"
        # horizontal rule
        elif line.strip() == "---":
            line = "<hr>"
        # bullet points
        elif line.startswith("- "):
            line = f"<li>{line[2:]}</li>"
        # blank line
        elif line.strip() == "":
            line = "<br>"
        # regular paragraph
        else:
            line = f"<p>{line}</p>"

        # inline bold
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        # inline links
        line = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', line)

        html_lines.append(line)

    body = "\n".join(html_lines)

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Georgia, serif;
                max-width: 680px;
                margin: 0 auto;
                padding: 24px 16px;
                color: #1a1a1a;
                background: #ffffff;
                font-size: 16px;
                line-height: 1.7;
            }}
            h1 {{
                font-size: 24px;
                font-weight: bold;
                border-bottom: 3px solid #e85d04;
                padding-bottom: 8px;
                margin-bottom: 4px;
            }}
            h2 {{
                font-size: 18px;
                font-weight: bold;
                color: #e85d04;
                margin-top: 32px;
                margin-bottom: 8px;
            }}
            h3 {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 4px;
            }}
            p, li {{
                margin: 6px 0;
            }}
            li {{
                margin-left: 16px;
            }}
            hr {{
                border: none;
                border-top: 1px solid #e0e0e0;
                margin: 24px 0;
            }}
            a {{
                color: #e85d04;
                text-decoration: none;
            }}
            strong {{
                font-weight: bold;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 13px;
                color: #999;
                border-top: 1px solid #e0e0e0;
                padding-top: 12px;
            }}
        </style>
    </head>
    <body>
        {body}
        <div class="footer">Weak Signal Tracker — running locally on your machine</div>
    </body>
    </html>
    """

def save_to_archive(digest_text):
    archive_dir = "archive"
    os.makedirs(archive_dir, exist_ok=True)

    week_label = datetime.now().strftime("%Y-%m-%d")
    filename = f"{archive_dir}/digest_{week_label}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Weak Signal Tracker — Week of {week_label}\n\n")
        f.write(digest_text)

    print(f"Digest saved to {filename}")
    return filename

def send_digest(digest_text):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_ADDRESS")

    save_to_archive(digest_text)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📡 Weak Signal Tracker — {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = sender
    msg["To"] = recipient

    text_part = MIMEText(digest_text, "plain")
    html_part = MIMEText(markdown_to_html(digest_text), "html")

    msg.attach(text_part)
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print("Digest sent to your inbox.")