import smtplib
import os
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def markdown_to_html(text):
    html_body = markdown.markdown(text, extensions=["extra", "nl2br"])

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
            blockquote {{
                border-left: 3px solid #e85d04;
                padding-left: 16px;
                color: #666;
                margin: 16px 0;
            }}
            code {{
                background: #f0f0f0;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }}
            pre {{
                background: #f0f0f0;
                padding: 12px;
                border-left: 3px solid #e85d04;
                overflow-x: auto;
            }}
            pre code {{
                background: none;
                padding: 0;
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
        {html_body}
        <div class="footer">Signal Digest — running locally on your machine</div>
    </body>
    </html>
    """

def save_to_archive(digest_text):
    archive_dir = "archive"
    os.makedirs(archive_dir, exist_ok=True)

    week_label = datetime.now().strftime("%Y-%m-%d")
    filename = f"{archive_dir}/digest_{week_label}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Signal Digest — Week of {week_label}\n\n")
        f.write(digest_text)

    print(f"Digest saved to {filename}")
    return filename

def send_digest(digest_text):
    try:
        save_to_archive(digest_text)
    except Exception as e:
        print(f"  WARNING: Could not save to archive: {e}")

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_ADDRESS")

    if not sender or not password:
        print("  ERROR: EMAIL_ADDRESS or EMAIL_PASSWORD not set in .env — skipping email send.")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📡 Signal Digest — {datetime.now().strftime('%b %d, %Y')}"
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
    except smtplib.SMTPAuthenticationError:
        print("  ERROR: Gmail authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD in .env.")
    except smtplib.SMTPException as e:
        print(f"  ERROR: SMTP error — {e}")
    except Exception as e:
        print(f"  ERROR: Failed to send email — {e}")