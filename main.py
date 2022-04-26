from PySide2.QtWidgets import QApplication, QMessageBox, QListWidget, QTreeWidgetItem, QMdiSubWindow, QDockWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from lib.share import SI
from threading import Thread

from PySide2.QtCore import Signal, QObject


class Win_Login:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('login.ui')
        self.ui.btn_lg.clicked.connect(self.onSignIn)
        self.ui.pwd.returnPressed.connect(self.onSignIn)  # 回车

    def onSignIn(self):
        username = self.ui.usr.text().strip()
        password = self.ui.pwd.text().strip()
        # if username == '' or password == '':
        #     QMessageBox.warning(self.ui, '警告', '密码或账号为空!')
        #     return
        self.ui.pwd.setText('')
        print(username, password)
        SI.mainWin = Win_Main()
        SI.mainWin.ui.show()
        self.ui.hide()
        SI.mainWin.treeWidget()
        SI.mainWin.dockWidget()
        SI.mainWin.subArea()


class Win_Main:
    def __init__(self):
        self.ui = QUiLoader().load('main.ui')
        self.subui = QUiLoader().load('subWidget.ui')
        # 实例化signal
        self.ms = MySignals()
        self.ui.actionExit.triggered.connect(self.onSignOut)
        self.ui.actionDataTest.triggered.connect(self.subArea)  # MDI窗口
        self.ui.menu.addAction(self.ui.dockWidget.toggleViewAction())  # 显示或者关闭dockwidget
        self.ui.actionThread.triggered.connect(self.onSendThread)  # 发送线程
        self.ms.message_print.connect(self.onSendThread)
        # self.ui.treeWidget.setHeaderLabel('数据环境创建') #指定列标签
        self.ui.treeWidget.header().setVisible(False)  # 隐藏表头
        # 绑定节点点击事件
        self.ui.treeWidget.clicked.connect(self.onClickTree)  # 树控件
        self.listWidget = QListWidget()  # 列表框
        self.listWidget.itemClicked.connect(self.onClickListWidget)  # DockWidget中QListWidget
        self.ui.btnFile.clicked.connect(self.onTextBrowser)

    def onTextBrowser(self):
        self.ui.textBrowser.append('123\n')  # 在指定的区域显示提示信息
        # 一边执行耗时程序，一边刷新界面的功能，给人的感觉就是程序运行很流畅
        QApplication.processEvents()  # 一定加上这个功能，不然有卡顿
    # 发送线程信号
    def onSendThread(self):
        # Qt建议： 只在主线程中操作界面 。
        #
        # 在另外一个线程直接操作界面，可能会导致意想不到的问题
        # 因此通过发送信号的方式操作主界面
        if self.ui.actionThread.isChecked:
            def run():
                self.ms.message_print.emit('我是多线程')

            t = Thread(target=run)
            t.start()  # 启动线程

        QMessageBox.information(self.ui, '提示', '请不要反复启动')
        return
    def onSendThread(self):
        QMessageBox.warning(self.ui, '警告', '我是多线程')

    def onSignOut(self):
        SI.mainWin.ui.hide()
        SI.loginWin.ui.show()

    def treeWidget(self):
        # 根节点
        root = QTreeWidgetItem(self.ui.treeWidget)
        root.setText(0, '数据环境创建')
        root.setIcon(0, QIcon('images/file.png'))

        # 子节点
        item1 = QTreeWidgetItem(root)
        item1.setText(0, '创建分类')
        item1.setIcon(0, QIcon('images/file.png'))

        item2 = QTreeWidgetItem(root)
        item2.setText(0, '创建标签')
        item2.setIcon(0, QIcon('images/file.png'))

    def onClickTree(self, index):
        item = self.ui.treeWidget.currentItem()
        print(index.row())
        print(item.text(0))  # 获取标签

    def dockWidget(self):
        # labels = ['导航', '搜索']
        # self.listWidget.addItems(labels)
        # self.ui.dockWidget.setWidget(self.listWidget)
        self.ui.dockWidget.setWidget(self.ui.textBrowser)

    def onClickListWidget(self, index):
        item = self.listWidget.currentItem()
        print(item.text())  # 获取标签

    def subArea(self):
        # 实例化多文档界面对象
        sub = QMdiSubWindow()
        # 向sub内添加内部控件
        sub.setWidget(QUiLoader().load('subWidget.ui'))
        sub.setWindowTitle('subWindow')
        # 将子窗口添加到Mdi区域
        self.ui.mdiArea.addSubWindow(sub)
        # 子窗口显示
        sub.show()
        # 安排子窗口在Mdi区域平铺显示
        self.ui.mdiArea.tileSubWindows()


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    message_print = Signal(str)

    # 还可以定义其他种类的信号
    update_table = Signal(str)


app = QApplication([])
loginWin = Win_Login()
SI.loginWin = Win_Login()
SI.loginWin.ui.show()
app.exec_()
