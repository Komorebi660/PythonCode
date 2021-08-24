## 肥科自动健康打卡脚本

**代码介绍见[我的Blog](https://komorebi660.github.io/2021/08/20/USTCHealthPunch/)**

### 安装依赖

安装`OCR`模块：

**Windows**：

访问[这里](`https://digi.bib.uni-mannheim.de/tesseract/`)，下载`.exe`文件安装.

**Ubuntu**：

```
sudo apt install tesseract
```

安装代码所需库：

```
pip install requests
pip install Image
pip install pytesseract
```

`re`、`io`库为`Python`自带库，无需手动安装。

### 修改参数

接下来，进入源码文件`USTCHealthPunch.py`，修改如下参数(**必选**):

- **USR**：学号
- **PWD**：密码
- **LOCATION**：所在校区
- **EMERGENCY_CONTACT**：紧急联系人姓名
- **RELATIONSHIP**：本人与紧急联系人关系
- **PHONE_NUMBER**：紧急联系人电话

然后运行代码，可能会出现以下几种情况：

若出现

```
上报成功
```

则表明成功打卡。

若出现

```
UserName or Password ERROR!
```

则表明用户名或密码输入错误，或者验证码识别错误，此时可多尝试几次。

若出现

```
Health Punch ERROR!
```

则表明上报失败，原因可能是打卡网站进行了更新，需要重新修改代码。

### 上传至`Vlab`定时执行

以`Ubuntu20.04`版本的`Vlab`为例，要实现自动运行脚本需要进行如下设置：

**第一步：上传源码**

将源码上传至`Vlab`虚拟机，你可以使用`ftp`传输。

**第二步：编辑`crontab`**

```
sudo crontab -e
```

使用`vim`进行设置，设置格式如下：

```
* * * * * command
分 时 日 月 周 命令
```

例如：
```
* 21 * * * /usr/bin/python3 /home/ubuntu/USTCHealthPunc.py
```

就是每天`21：00`执行位于`/home/ubuntu/`下的`USTCHealthPunch.py`文件

**第三步：重启`cron`服务**

```
service cron restart
```

接下来就能解放双手自动打卡了~

