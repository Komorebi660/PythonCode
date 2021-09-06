## 基于百度翻译的本地化中英翻译器

**代码介绍见[我的Blog](https://komorebi660.github.io/2021/08/22/BaiduTranslator/)**

### 代码使用

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

安装`tkinter`

接下来，进入源码`BaiduTranslator.py`，修改参数(**必选**)：

- **USER_AGENT**：位于`Request Headers`中的`User-Agent`;
- **COOKIE**：位于`Request Headers`中的`Cookie`;
- **TOKEN**：位于`From Data`中的`token`.

进入[百度翻译](https://fanyi.baidu.com/), 打开浏览器的开发者工具，在`Request URL`为`https://fanyi.baidu.com/v2transapi`处获取.

### 使用示例

运行结果如下：

![运行结果1](result1.png)

![运行结果2](result2.png)

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