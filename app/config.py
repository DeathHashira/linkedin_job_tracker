import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("PRIMERY_CLIENT_SECRET")
redirect_uri = 'https://oauth.pstmn.io/v1/browser-callback'
scope = 'w_member_social openid profile email'