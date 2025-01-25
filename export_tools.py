from numpy import column_stack, transpose

def get_proposal_path(run):
    proposal = run.start.get("proposal", {}).get("proposal_id", None)
    is_commissioning = "commissioning" in run.start.get("proposal", {}).get("type", "").lower()
    cycle = run.start.get("cycle", None)
    if proposal is None or cycle is None:
        raise ValueError("Proposal Metadata not Loaded")
    if is_commissioning:
        proposal_path = f"/nsls2/data/sst/proposals/commissioning/pass-{proposal}/"
    else:
        proposal_path = f"/nsls2/data/sst/proposals/{cycle}/pass-{proposal}/"
    return proposal_path



def get_md(run,md_key,default="Unknown"):
    if md_key in run.start.keys():
        return str(run.start[md_key])
    else:
        return default


def get_general_metadata(run):

    metadata = {}
    #beamline setup:
        # slit positions, L1 & L2 positions, nBPM position, DCM crystal, harmonic
    #sample info:
        # sample positions, 
    #KE / BE 
    
    try:
        metadata['Proposal'] = str(run.start['proposal']['proposal_id'])
    except: 
        metadata['Proposal'] = unknown 

    metadata['UID'] = get_md(run,'uid')
    metadata['Start Date/Time'] = get_md(run,'start_datetime')
    metadata['Scan ID'] = get_md(run,'scan_id')
    metadata['SAF'] = get_md(run,'saf')
    metadata['Sample Name'] = get_md(run,'sample_name')
    metadata['Sample Description'] = get_md(run,'sample_description')

    return metadata    

def get_metadata_xps(run):

    metadata = get_general_metadata(run)

    peak_config = run.primary.descriptors[0]['configuration']['PeakAnalyzer']['data']
    for peakkey in peak_config.keys():
        out_key = peakkey.replace("_"," ")
        metadata[out_key] = str(peak_config[peakkey])

    metadata['I0 Integration Time'] = str(run.primary.descriptors[0]['configuration']['I0 ADC']['data']['I0 ADC_exposure_time'])
    metadata['I0 Data'] = str(run.primary.read()["I0 ADC"].data)

    metadata['Number of Sweeps'] = str(run.primary.read()['PeakAnalyzer_xaxis'].data.shape[0])

    return metadata

def get_data_xps(run):

    energy_axis = run.primary.read()["PeakAnalyzer_xaxis"].data[0,:]
    imdat = run.primary.read()['PeakAnalyzer_edc'].data

    #add dimension mode should be a metadata key.  If true, keep every sweep individually.  For now force False
    add_dimension = False
    if add_dimension:
        edc = transpose(imdat)
    else:
        edc = imdat.sum(axis=0)

    data_array = column_stack((energy_axis,edc))

    return data_array

def make_header(metadata,datatype):
    """
    compiles metadata into a header for data export.  Datatype should be "xps" or "xas"
    """

    header = ""
    for k in metadata.keys(): 
        header = header + k + ": "+metadata[k]+"\n"

    if datatype == "xps":
        header = header+'\n'
        header = header+'[Data]\n'
        header = header+'Energy'
        for n in range(int(metadata['Number of Sweeps'])):
            header = header+", Dimension"+str(n)
        header = header+"\n"
    elif datatype == "xas":
        pass
    else:
        pass
    
    return header
