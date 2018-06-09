.. config_dbconfig:

DBconfig
========

Overview
--------

This config contains database operaction.It's compatible with flask.

IsCreated
-----

This package debug module.If start debug module,SDK will start some useful infos.

JSON_AS_ASCII
-----

Default is false.It supports your web server appears at chinese,not a string of utf-8 code.

SECRET_KEY
-------

It's a common private key.

SQLALCHEMY_COMMIT_ON_TEARDOWN
-------

Flask-sqlalchemy setting.It will make your session commit automatically.


SQLALCHEMY_DATABASE_URI
-------

Database URI.It's compatible with sqlalchemy's syntax.

.. code-block:: bash
    Example:
    sqlite:////tmp/test.db
    mysql://username:password@server/db

SQLALCHEMY_TRACK_MODIFICATIONS
-------

If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None, which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed.


