
"""
paramsCORRXFM.py

set up a params class to read/store the input parameters for correlating diffraction data from teh XFM beamline, Australian Synchrotron

Classes:
    paramsCORRXFM - calculated angular correlations from the xfm beamline
"""

from params.paramsCORR import paramsCORR
import os
import numpy as np

#
# class to set up the PADF parameters
#


class paramsCORRXFM(paramsCORR):

    """
    params class instance with diffraction input parameters  

    Parameters
    ----------
    xfmconfig : str
   	sets up fluxfm beamline parameters (different from pypadf configs) 
    
    xfmgroup : str
	group name used for xfm scan

    run_limit : int
        limit number of h5 files to use
    """

    def __init__(self):

        ch = ["CORRXFM"]
        paramsCORR.__init__(self)


        self.add_parameter("xfmconfig", "None", cmdline="--xfmconfig",cmdline2="-xfmc", help="XFM beamline parameters",
                        nargs=1,header=ch[0],pathflag=False)

        self.add_parameter("xfmgroup", "None", cmdline="--xfmgroup",cmdline2="-xg", help="Group name used for xfm scan",
                        nargs=1,header=ch[0],pathflag=False)

        self.add_parameter("run", 1, cmdline="--run",cmdline2="-rn", help="Run number to analyse",
                        nargs=1,header=ch[0],pathflag=False)
        
        self.add_parameter("run_limit", 1, cmdline="--run_limit",cmdline2="-runl", help="Max number of h5 files to load",
                        nargs=1,header=ch[0],pathflag=False)

        self.add_parameter("npatsum", 1, cmdline="--npatsum",cmdline2="-nps", help="Number of frames to sum before correlating",
                        nargs=1,header=ch[0],pathflag=False)
                        
        self.add_parameter("dlistflag", True, cmdline="--dlistflag",cmdline2="-dlf", help="if True then use the list to select frames to correlate",
                        nargs=1,header=ch[0],pathflag=False)
                       
        self.add_parameter("dlistfile", "None", cmdline="--dlistfile",cmdline2="-dlfile", help="Text file containing list of h5 file and frames indices",
                        nargs=1,header=ch[0],pathflag=False)
                        
        self.add_parameter("filtertype", "None", cmdline="--filtertype",cmdline2="-ftype", help="Text to state which filtering is being used",
                        nargs=1,header=ch[0],pathflag=False)
                        
        self.add_parameter("filterlabel", "None", cmdline="--filterlabel",cmdline2="-flabel", help="Text to label the filtering range",
                        nargs=1,header=ch[0],pathflag=False)

    def read_diff_parameters_from_file(self):
        """Read the values of the input parameters from a text (config) file.
        
        All parameters are written to a log file in the outpath.
        """

        #cwd = os.getcwd()+"/"
        #self.read_parameters_from_file(cwd+self.parser.parse_args().config[0] )
        #abspath = os.path.abspath(self.parser.parse_args().config[0])
        #self.parse_config_file( abspath )
        #self.parse_commandline_args()
#        self.read_config_file(cwd+self.parser.parse_args().config[0] )
        #print("config file name:", abspath )

        self.parse_all_parameters()
        outname = self.makefname( self.outpath, self.tag, "_diffraction_batch_parameter_log", ".txt")
        #self.write_params_to_file( outname )

