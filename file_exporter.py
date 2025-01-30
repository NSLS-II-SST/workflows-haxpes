from export_tools import *
import numpy as np
from os import makedirs
from os.path import exists

from prefect import get_run_logger, task, flow

@task(retries=2, retry_delay_seconds=10)
def export_peak_xps(uid, beamline_acronym="haxpes"):
    logger = get_run_logger()

    catalog = initialize_tiled_client(beamline_acronym)
    run = catalog[uid]

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

@task(retries=2, retry_delay_seconds=10)
def export_xas(uid, beamline_acronym="haxpes"):
    logger = get_run_logger()

    catalog = initialize_tiled_client(beamline_acronym)
    run = catalog[uid]

    metadata = get_general_metadata(run)
    header = make_header(metadata,"xas")
    data = get_xas_data(run)

    export_path = "/home/xf07id1/tmp/XAS_export/"
    if not exists(export_path):
        logger.info(f"Export path does not exist, making {export_path}")
        makedirs(export_path)
    filename = export_path+"XAS_scan"+str(run.start['scan_id'])+".csv"
    logger.info('Exporting XAS Data")
    np.savetxt(filename,data,delimiter=',',header=header)


@flow
def xas_export(uid, beamline_acronym="haxpes"):
    export_xas(uid,beamline_acronym)

@flow
def peak_export(uid, beamline_acronym="haxpes"):
    export_peak_xps(uid, beamline_acronym)


