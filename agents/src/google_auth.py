import os,pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES =  [
    'https://www.googleapis.com/auth/calendar.events',
]

AUTH_FILE = r"D:\llmora\googleAuth.json"

def get_auth_service(api_name,api_version):

    #check if any existed tokens are available
    creds = None
    if os.path.exists('token.pickle'):
        print("Load existing credential token")
        try:
            with open('token.pickle') as token:
                creds = pickle.load(token)
            print("Successfully loaded credentials")
        except Exception as e:
            print(f"Error loading token : {e}")
            creds = None
    
    #if not available , make user login
    if not creds or not creds.valid:
        print("No credential available,check and refresh")

        #again check credential and check whether it is expired or try to refresh 
        if creds and creds.expired and creds.refresh_token:
            print("Credential are expired. refreshing")
            try:
                creds.refresh(Request()) #get new access token by refresh
                print("Succesfully refresh")
            except Exception as e:
                print(f"Refresh failed: {e}.")
                creds = None #reset if refresh fails
        else:
            print("No valid credentials, starting new A0uth")
            creds=None

    #if no credentail and refresh failed, start new authentication
    if not creds:
        print("starting 0Auth 2.0 authentication flow...")

        try:
            #check if auth file exist first
            if not os.path.exists(AUTH_FILE):
                raise FileNotFoundError(f"Auth file not found : {AUTH_FILE}")
                
            #load client configuration from json file
            flow = InstalledAppFlow.from_client_secrets_file(
                AUTH_FILE,
                SCOPES
            )

            #this opens a browser window for user to log and grant permission
            creds = flow.run_local_server(
                port=5000,
                authorization_prompt_message='please athorize access to your Google services.',
                success_message='Authentication successful! You can close this window',
                open_browser=True #auto open browser
            )
            print("0Auth flow completed successfully!")
        
            #save credential for future use
            print("Saving credential to token.pickle")
            with open('token.pickle','wb') as token:
                pickle.dump(creds,token)
            print("Credential saved")
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
    try:
        service = build(api_name,api_version,credentials=creds)
        print("service build successess")
        return service
    except Exception as e:
        print(f"Failed to build services : {e}")
        return None



print("init..lization google service")
calender_service = get_auth_service('calendar','v3')
if calender_service:
    print("calender service init...lization success") 
else:
    print("calender service init...lization failed")
