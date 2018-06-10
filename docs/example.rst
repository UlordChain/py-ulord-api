.. exapmle:

========
Examle
========

This is a tutorial thar uses SDK to develop a blog demo.

Get development permissions
============================

You should regist on the ulord-platform.And then you need to create a application.You will get a appkey and a secret.The two things are important.You mustn't lose them.

Init
====

Create a role according to your ability using your appkey and secret.SDK has two roles.One is junior and the other is senior.Both them have to init using your appkey and secret.

Senior has base API about UDFS and ulord-platform.UDFS is a distributed storge platform.Using it you can upload your resource and download easily.The API about ulord-platform packages fot ulord-platform http interface.

Junior has all API of Senior.And it also has a base database.You can using database whatever you want to use.Default is sqlite.It achieves base on the flask-sqlalchemy.And you can build your own database structure.

.. code-block:: python

    from ulordapi.user import Junior
    junior = Junior(appkey="5d42b27e581c11e88b12f48e3889c8ab", secret="5d42b27f581c11e8bf63f48e3889c8ab")

Config
======

You should make your own config.Reading config module and create your own config.

.. code-block:: python

    blog_config = {
    'baseconfig':{
        'config_file':'E:\ulord\ulord-blog-demo\config'
    },
    'logconfig':{
        'log_file_path': 'E:\ulord\ulord-blog-demo\blogdemo.log'
    }
    }
    junior.config_edit(blog_config)

Create your required interface
==============================

Example regist(This demo is using flask):

.. code-block:: python

    @app.route('/user/regist',methods=['POST'])
    def regist():
        """
        user regist

        :return: user token
        """
        username = request.json.get('username')
        password = request.json.get('password')
        cellphone = request.json.get('cellphone')
        email = request.json.get('email')
        if username is None or password is None:
            # missing arguments
            return jsonify(return_result(60100))
        args = junior.decrypt([username, password, cellphone, email])
        if args:
            result = junior.user_regist(username=args[0],password=args[1],cellphone=args[2],email=args[3])
            return jsonify(result)
        else:
            return jsonify(return_result(60100))


