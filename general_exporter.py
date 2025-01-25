from file_exporter import export_peak_xps
#from export_tools import get_proposal_path
from prefect import flow

from tiled.client import from_profile
catalog = from_profile("nsls2")['haxpes']['raw']

@flow
def export_switchboard(uid):
    run = catalog[uid]
    
    if run.start['autoexport']:
        if run.start['scantype'] == "xps":
            export_peak_xps(run)
