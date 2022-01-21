# 基于百度翻译的本地化中英翻译器

**代码介绍见[我的Blog](https://komorebi660.github.io/2021/08/22/Translator/)**

## 代码使用

安装依赖库：

```
pip install requests
pip install js2py
```

`re`、`tkinter`库为`Python`自带库，无需手动安装。

Linux环境可能没有安装`tkinter`库，输入：

```
sudo apt-get install python-tk
或
sudo apt-get install python3-tk
```

即可安装`tkinter`.

接下来，进入源码`BaiduTranslator.py`，修改参数(**必选**)：

- **USER_AGENT**：位于`Request Headers`中的`User-Agent`;
- **COOKIE**：位于`Request Headers`中的`Cookie`;
- **TOKEN**：位于`From Data`中的`token`.

进入[百度翻译](https://fanyi.baidu.com/), 按`F12`打开浏览器的开发者工具，在`Request URL`为`https://fanyi.baidu.com/v2transapi`处可以获取上述参数.

**注意：最新的百度翻译可能需要登录百度账号才可以使用，建议先登录百度账号再抓取有关内容。**

## 使用示例

若运行时出现：

```
ERROR, Can not Translate now!
或
出现异常，暂时无法翻译!
```

原因是翻译结果没有正常返回，可能的原因是参数设置错误，正常的运行结果如下：

<div align="center">
<img src=./result1.png width=80%/>
</div>

<div align="center">
<img src=./result2.png width=80%/>
</div>

在`Windows`环境下，你还可以将其打包为`.exe`文件，这样即使电脑不含`Python`也能运行，方法如下：

安装`pyinstaller`:

```
pip install pyinstaller
```

在源码所在目录执行：

```
pyinstaller -F -w BaiduTranslator.py
```

即可生成`.exe`文件，位于`/dist`目录下