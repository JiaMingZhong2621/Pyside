# Pyside2
Pyside2 GUI demo
## 如何将程序打包成APP？
```
pip install pyinstaller  
pyinstaller --noconsole main.py
```
程序将在当前根目录下生成一个dist文件夹，里面包含了可执行文件。
##注意，请把用到的资源文件复制到可执行文件所在目录！！！
--noconsole 表示不要控制台 main.py主窗口所在的py文件，如果缺少依赖，打包时通过--import xxx解决。  
前期调试建议显示控制台，方便查找错误。若运行程序闪退，可通过命令./main.exe执行程序。

