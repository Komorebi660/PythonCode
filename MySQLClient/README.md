# MySQL客户端框架

这是一个`C/S`架构的`MySQL`客户端框架, 它实现了`MySQL`与`Python`的基本交互功能, 支持登录与展示表格信息, 可在此基础上进行扩展。

各个模块之间的连接图如下:

<div align="center">
<img src=./figure/module.png width=40%/>
</div>

## Getting Started

### 安装MySQL Server

官网下载并安装: `https://dev.mysql.com/downloads/mysql/`, 安装完成后需要进行初始化(可能需要管理员权限):

```bash
mysqld.exe --initialize --user=mysql --console
```

在`MySQL`的安装目录下找到`my.ini`文件(没有则直接新建一个), 在此文件中添加如下内容:

```ini
[mysqld]
#设置3306端口号
port=3306
#设置MySQL的安装目录
basedir=
#设置MySQL数据库的数据存放目录
datadir=
#运行最大连接数
max_connections=200
#运行连接失败的次数。这也是为了防止有人从该主机试图攻击数据库系统
max_connect_errors=10
#服务端使用的字符集默认为utf-8
character-set-server=utf8
#设置可以读入读出文件
secure_file_priv=''
[mysql]
#客户端使用的字符集默认为utf8
default-character-set=utf8
[client]
#客户端默认端口号为3306
port=3306
```

保存后就可以启动`MySQL`服务了:

```bash
mysqld.exe --install mysql --defaults-file="my.ini"
net start mysql
```

尝试登录`MySQL`服务器:

```bash
mysql -u root -p
```

若出现:

```
Welcome to the MySQL monitor.
```

则表明成功登录。若要关闭连接, 请输入`exit`; 若要关闭`MySQL`服务, 请使用`net stop mysql`.

### 安装MySQL Client

```bash
pip install mysqlclient
```

这样在`Python`中就可以通过`import MySQLdb`来导入`Python--MySQL`接口模块。

### 运行

```bash
python main.py
```

在左上角选择登录后即可看到数据库中存在的三张表格数据(`Book`， `Reader`, `Borrow`), 这是`MainWindow.py`函数在登录成功后插入到数据库中的, 具体的SQL语句见`SQL.py`.

## Advanced

进一步我们可以在此框架上添加更多的功能, 如:数据的增、删、改、查等。该过程主要分为以下几步:

### Step 1

利用`Qt Designer`创建`ui`文件, 然后使用`pyuic5`将生成的`.ui`文件转变为`.py`文件(放在`ui`文件夹内), 如:

```bash
pyuic5 -o ./ui/UiLogin.py ./ui/PyQt_UI/login.ui
pyuic5 -o ./ui/UiMainWindow.py ./ui/PyQt_UI/mainwindow.ui
```

### Step 2

编写相应功能的`SQL`代码并进行测试, 以验证其功能性。

### Step 3

在`src`文件夹中创建控制模块, 导入先前转换的`ui`文件, 并在控制模块中调用经过测试的`SQL`语句以实现相应的功能, 将结果以图形化的形式展现出来。