from ..io import lcmodel

import os
import subprocess

def process(data, wref=None,file_base = "/tmp/temp", options={}):
    """
    Runs the LCModel basis set fitting program to determine metabolite
    concentrations.


    Parameters
    ----------
    data : MRSData
        The water suppressed FID data to be fitted.
    wref : MRSData
        Optional water reference file for concentration scaling.
    file_base : string
        Pattern for input and output files written.
    options : dict
        Set of LCModel parameters to override.

    Returns
    -------
    dict
        Output from running LCModel on the data
    """

    # Generate control file and .raw files
    lcmodel.write_all_files(file_base,data,wref,options)
    control_file = file_base+'_sl0.CONTROL' # why are multiple control files written by write_all_files?

    # Run LCModel
    result = subprocess.run("lcmodel < {}".format(control_file
    ), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8")
    if result.returncode != 0:
        raise Exception("Error doing quantification with LCModel: {}".format(result.stderr))
    
    # Read output
    out_file = file_base+".COORD"
    if os.path.isfile(out_file):
        result = lcmodel.read_coord(out_file)
    else:
        raise FileNotFoundError("Could not find LCModel output file at {}".format(out_file))
    return result