from file_exporter import peak_export
#from export_tools import get_proposal_path
from prefect import flow, get_run_logger
from export_tools import initialize_tiled_client

@flow
def export_switchboard(uid,beamline_acronym="haxpes"):
    logger = get_run_logger()
    c = initialize_tiled_client(beamline_acronym)
    run = c[uid]
    if run.start['autoexport']:
        if run.start['scantype'] == "xps":
            peak_export(uid)
