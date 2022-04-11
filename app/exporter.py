import os, time, logging
from dotenv import load_dotenv
from storage import disk_list, blob_list
from prometheus_client import start_http_server, Gauge

load_dotenv()

# Create logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

metric_azure_disk_size = Gauge('azure_disk_size', 'Size of disk', ['resource_group','disk_name','vm'])
metric_azure_blob_total_size = Gauge('azure_blob_total_size', 'Approximate total size of all blob in the container', ['resource_group','container','storage_account'])

if __name__ == "__main__":
    start_http_server(8092)
    logger.info("Start Azure Storage exporter server at http://0.0.0.0:8092")
    
    if os.environ.get("INTERVAl_TIME") != None:
        interval = int(os.environ['INTERVAl_TIME'])
    else:
        interval = 10

    while True:
        start_time = time.time()   
    
        for disk in disk_list():
            metric_azure_disk_size.labels(resource_group=disk["rsg"], disk_name=disk["name"], vm=disk["use_vm"]).set(disk["size"])

        for blob in blob_list():
            metric_azure_blob_total_size.labels(resource_group=blob["rsg"], container=blob["container"], storage_account=blob["storage_account"]).set(blob["size"])

        process_time = time.time() - start_time
        logger.info(f"Updated {len(disk_list()) + len(blob_list())} metrics in {process_time:.3f} seconds")

        time.sleep(interval)