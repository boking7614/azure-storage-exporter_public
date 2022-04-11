import os
from dotenv import load_dotenv
from exporter.auth import az_authentication
from azure.mgmt.resource import ResourceManagementClient

load_dotenv()

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

# Get resource group list
def rsg_list():
    rsg = []
    resource_client = ResourceManagementClient(az_authentication(), os.environ["AZURE_SUBSCRIPTION_ID"])
    group_list = list(resource_client.resource_groups.list())
    for rg in group_list:
        rsg.append(rg.name)
    return rsg

# Get resource list
def rs_list():
    resource_client = ResourceManagementClient(az_authentication(), os.environ["AZURE_SUBSCRIPTION_ID"])
    resource_list = list(resource_client.resources.list())
    for rs in resource_list:
        print(rs.name)



if __name__ == "__main__":
    print(rs_list())
