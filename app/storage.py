import os

from dotenv import load_dotenv
from auth import az_authentication
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.blob import BlobServiceClient

load_dotenv()

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

def disk_list():
    disk_info = []
    compute_client = ComputeManagementClient(az_authentication(), subscription_id)
    disk_list = compute_client.disks.list()
    for disk in list(disk_list):
        disk_info.append({
            "name": disk.name,
            "size": disk.disk_size_gb,
            "rsg": disk.id.split("/")[4],
            "use_vm": disk.managed_by.split("/")[-1]
        })
    return disk_info

def blob_list():
    data =[]
    storage_client = StorageManagementClient(az_authentication(), subscription_id)
    # Get storage accounts list
    sa_list = storage_client.storage_accounts.list()
    for sa in sa_list:

        blob_service = BlobServiceClient(f"https://{sa.name}.blob.core.windows.net", az_authentication())

        # Get Container list
        container_list = blob_service.list_containers()
        for container in container_list:
            container_client = blob_service.get_container_client(container)

            # Get Blob list
            blob_list = container_client.list_blobs()
            total_size = 0
            for b in blob_list:
                total_size += b.size
            data.append({
                "rsg": sa.id.split("/")[4],
                "storage_account": sa.name,
                "container": container.name,
                "size": total_size
            })
    return data