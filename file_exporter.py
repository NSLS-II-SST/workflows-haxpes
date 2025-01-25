from export_tools import *
import numpy as np
from os import makedirs
from os.path import exists

from prefect import get_run_logger, task

@task(retries=2, retry_delay_seconds=10)
def export_peak_xps(run):
    logger = get_run_logger()
    metadata = get_metadata_xps(run)
    header = make_header(metadata,"xps")
    data = get_data_xps(run)
    export_path = get_proposal_path(run)+"XPS_export/"
    #export_path = "/home/xf07id1/Documents/UserFiles/live/LiveData/XPS_export/"
    #export filename key in md ???
    if not exists(export_path):
        logger.info(f"Export path does not exist, making {export_path}")
        makedirs(export_path)
    filename = export_path+"XPS_scan"+str(run.start['scan_id'])+".csv"
    logger.info("Exporting Peak XPS Data")
    np.savetxt(filename,data,delimiter=',',header=header)
