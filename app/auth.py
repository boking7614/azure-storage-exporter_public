import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential

def az_authentication():
    load_dotenv()
    credential = ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"], 
        client_id=os.environ["AZURE_CLIENT_ID"], 
        client_secret= os.environ["AZURE_CLIENT_SECRET"]
        )
    return credential