from googleapiclient.discovery import build
from email.message import EmailMessage
from auth import get_creds
import base64


def gmail_create_draft(to, subject, content = None):
  creds = get_creds()
  content = "<h1>Message body in <i>html</i> format!</h1>" 

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
  gmail_create_draft()
