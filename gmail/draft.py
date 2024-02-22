from googleapiclient.discovery import build
from email.message import EmailMessage
from auth import get_creds
import base64

def set_content(title, text_1, text_2, text_3):
  with open("gmail/template.html", 'r') as file:
    email_template = file.read()

  email_content = email_template.replace("{{title}}", title) \
                                .replace("{{text_1}}", text_1) \
                                .replace("{{text_2}}", text_2) \
                                .replace("{{text_3}}", text_3)
  
  return email_content

def gmail_create_draft(to, subject, content):
  creds = get_creds()

  # https://stackoverflow.com/a/73480540
  with build('gmail', 'v1', credentials=creds) as service:
    message = EmailMessage()

    message["To"] = to
    message["From"] = "magi.donna@gmail.com"
    message["Subject"] = subject
    message.add_header('Content-Type','text/html')
    message.set_payload(content)

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try: 
      draft = (
          service.users().drafts().create(
            userId="me", 
            body={"message": { "raw": encoded_message }}
          ).execute()
      )
      print(f'\nDraft id: {draft["id"]}\nDraft message: {draft["message"]}\n')
    except Exception as e:
        print('Error:', e)
        draft = None

  return draft


if __name__ == "__main__":
  content = set_content("Hello, World!", "This is the first paragraph.", "This is the second paragraph.", "This is the third paragraph.")
  gmail_create_draft(content=content, to="magi.donna@gmail.com", subject="Hello, World!")
