.. config_logconfig:

LogConfig
========

Overview
--------

This config contains log config.It's compatible with python log module setting.

format
-----

Log's display form.Default is [%(asctime)s] %(levelname)-8s %(name)s %(message)s,like this:

.. code-block:: bash

    [2018-06-06 10:02:28,609] INFO     Udfs: Current os is Windows

level
-----

Log level.Default is info,including CRITICAL,ERROR,WARNING,IFNO,DEBUG,NOTSET.Becaful with capitalization.

log_file_path
-------

Log file path.The log path you want to save.Default is your project root directory.Name is upapi.log.
