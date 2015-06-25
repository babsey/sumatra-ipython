# sumatra_ipython
Sumatra implementation for IPython magic function. Sumatra works with IPython interactively.

Requirement
-----------
or which I have already tested:
- Sumatra 0.7.0rc
- IPython 3.0.0

How to install it
-----------------
- Download the zip file, then unzip 
- Copy `cp sumatramagic.py  ~/.ipython/profile_default/startup/` (recommended with specific profile)
- Run `ipython` (or `ipython --profile=<profile_name>`)

How to use it
-------------
- use the magic key `%smt_run` with options:
  - -m select the main_file (neccessary)
  - -r enable sumatra recording
  - -s only save output data to file

Examples
--------
- run without recordings `%smt_run -m myscript.py default.param`
- run with recordings `%smt_run -m myscript.py default.param -r`
- run without recordings but save the data to file `%smt_run -m myscript.py default.param -s`
- run without recordings, change parameter set and then run with recording
  1. `%smt_run -m myscript.py default.param`
  2. `parameters.update({'key':value})`
  3. `%smt_run -m myscript.py default.param -r`
