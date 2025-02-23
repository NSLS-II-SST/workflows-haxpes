from file_exporter import peak_export, xas_export, generic_export
#from export_tools import get_proposal_path
from prefect import flow, get_run_logger
from export_tools import initialize_tiled_client

@flow
def export_switchboard(uid,beamline_acronym="haxpes"):
    logger = get_run_logger()
    c = initialize_tiled_client(beamline_acronym)
    run = c[uid]
#    if run.start['autoexport']:
        #need to add generic exporter
#        return
    if 'scantype' in run.start.keys():
        if run.stop['exit_status'] != "abort":
            if run.start['scantype'] == "xps":
                peak_export(uid)
            elif run.start['scantype'] == "xas":
                xas_export(uid)
    else:
        if run.start['autoexport']:
            generic_export(uid)

