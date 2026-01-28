"""
问题1：
pytest调用fixture时，里面有对django代码进行操作的动作时，如果没有pytest-django包，pytest不认识django的项目结构，所以找不到django的models。
如果没有配置pytest.ini，就会报ModuleNotFoundError，因为pytest找不到student模块

问题2：
pytest调用fixture时，django服务连接的数据库是本地配置的sqllite数据库，但是安装了pytest-django插件后，这个插件启动时会自动创建一个独立的测试数据库(通常叫 test_db.sqlite3 或内存库)，
所以在fixture 里写的 Student.objects...delete()是在删除test_db.sqlite3库里执行的，情况就会变成在test_db.sqlite3里删除了要删除的数据，但是真实的sqllite库里面的数据并没有执行删除，
pytest的fixture就会返回报错，提示数据已存在，返回400，pytest执行也会停止，

"""