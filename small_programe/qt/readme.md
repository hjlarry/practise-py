1. 使用Qt Designer([下载](https://build-system.fman.io/qt-designer-download))软件绘制GUI界面，保存后得到*.ui文件
2. `pyuic5 -o login.py login.ui`，PyQt5的该命令将UI文件转换为Py文件
3. 最好是通过其他文件调用的方式将业务逻辑和界面分离开