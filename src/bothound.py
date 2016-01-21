import logging
import optparse
import sys
import yaml

from bothound_live_sniffer import BothoundLiveSniffer
from bothound_tools import BothoundTools

from os.path import dirname, abspath
from os import getcwd
try:
    src_dir = dirname(dirname(abspath(__file__)))
except NameError:
    #the best we can do to hope that we are in the test dir
    src_dir = dirname(getcwd())

sys.path.append(src_dir)

def main():

    parser = optparse.OptionParser()
    
    parser.add_option("-v", "--verbose", dest="verbose",
            help="Be verbose in output, don't daemonise",
            default=False,
            action="store_true")

    parser.add_option("-c", "--conf",
                      action="store", dest="conffile",
                      default=src_dir+'/conf/bothound.yaml',
                      help="Path to config file")

    (parsed_options, args) = parser.parse_args()
    conf_options = {'verbose': parsed_options.verbose, 'conffile': parsed_options.conffile}

    stram = open(conf_options ['conffile'], "r")
    conf = yaml.load(stram)
    conf_options['sniffers'] = conf["sniffers"];

    if conf_options['verbose']:
        mainlogger = logging.getLogger()
        logging.basicConfig(level=logging.DEBUG)
        log_stream = logging.StreamHandler(sys.stdout)
        log_stream.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_stream.setFormatter(formatter)
        mainlogger.addHandler(log_stream)
    else:
        for sniffer in conf_options['sniffers']:
            logger = logging.getLogger('logfetcher')
            hdlr = logging.FileHandler(sniffer["logfile"])
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
            logger.setLevel(logging.DEBUG)

    tools = BothoundTools(conf["database"])
    tools.connect_to_db()

    #
    #print "Processed incidents:"
    #print tools.get_processed_incidents()

    # Create a test incident
    id_incident = tools.create_test_incident()
    tools.disconnect_from_db


    lfetcher = BothoundLiveSniffer(conf_options)
    lfetcher.run()

if __name__ == "__main__":
    main()
