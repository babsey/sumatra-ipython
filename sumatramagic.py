# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)

import time
import os
import numpy as np

from sumatra.projects import load_project
from sumatra.parameters import build_parameters

# The class MUST call this class decorator at creation time
@magics_class
class SumatraMagic(Magics):

    @magic_arguments()
    @argument('parameters', default=None, help='a param file to be imported.')
    @argument('--record', '-r', default=False, action='store_true',
              help='recording the script')
    @argument('--save', '-s', default=False, action='store_true',
              help='save output to file')
    @argument('--main_file', '-m', metavar="main_file", 
              help='select a main_file')

    @line_magic
    def smt_run(self, line):
        args = parse_argstring(self.smt_run, line)

        global parameters
        parameters = globals().get('parameters',build_parameters(args.parameters))
        print(10*"-" + " Parameters " + 10*"-")
        print(parameters)
        print(32*"-", end="\n\n")
        print(12*"-" + " Script " + 12*"-")
        with open(args.main_file, 'r') as f:
            script = f.readlines()
        f.closed
        print(''.join(script), end='')
        print(32*"-", end="\n\n")

        if args.record is True:
            project = load_project()
            record = project.new_record(main_file=os.path.relpath(args.main_file),parameters=parameters)
            print("Record label for this run: '%s'" %record.label)

        start_time = time.time()
        execfile(args.main_file, globals(), parameters.as_dict())
        duration = time.time() - start_time

        if args.record is True:
            fname = "%s.dat"%record.label
            np.savetxt("Data/%s"%fname, data)                                            # Save data
            record.duration = duration
            record.output_data = record.datastore.find_new_data(record.timestamp)
            project.add_record(record)
            project.save()
            print("Data keys are [%s(%s [%s])"%(record.label, record.version, record.timestamp))

        elif args.save is True:
            np.savetxt("%s_%s.dat"%(time.strftime("%y%m%d-%H%M%S", time.gmtime(start_time)), 
                os.path.splitext(os.path.basename(args.main_file))[0]), data)                           # Save data

        print("Duration: %.2fs" %duration)

# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(SumatraMagic)
