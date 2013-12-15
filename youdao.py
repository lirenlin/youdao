#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

class Browser(QWebView):
    unameAvailable = pyqtSignal(['QString'])

    def __init__(self):
        self.baseUrl = 'http://dict.youdao.com/search?q=%s&keyfrom=dict.index'
        self.uname = ''
        self.wordbook = None 
        self.login = None
        self.opWB = None
        self.navigate = list()
        QWebView.__init__(self)
        self._showStartPage()
        #self.loadFinished.connect(self._result_available)

    def _showStartPage(self):
        startPage = u'''
        <html>
        <body>
        <h1 align="center">有道词典</h1>

        <p align="center">搜索：word</p>
        <p align="center">登陆：login</p>
        <p align="center">添加：add</p>
        <p align="center">退出：quit</p>

        <p align="center">下一页：Ctrl-f</p>
        <p align="center">上一页：Ctrl-b</p>
        <p align="center">i，j：next/previous line</p>
        <p align="center">0：释义,  1：权威词典</p>
        <p align="center">2：例句,  3：百科</p>
        </body>
        </html>'''
        self.setHtml(startPage)
        self.start = True

    def _result_available(self, result):
        print "browser: clean page"
        self.clean_page();
        self.page().contentsChanged.emit()
        self.wordbook = self.page().mainFrame().findFirstElement("span[class='wordbook']")
        #self.update()
        #self.show()

    def clean_page(self):
        currentURL = self.url().toString()
        frame = self.page().mainFrame()
        #print unicode(frame.toHtml()).encode('utf-8')
        if 'account.youdao.com/login' in currentURL:
            cleanID = ['b', 't', 'login']
            cleanCLASS = ['link', 'login_left', 'hr', 'clr'] 
            for ID in cleanID:
                element = frame.findFirstElement("div[id='%s']"%ID)
                if element.attribute('id') == 'login':
                    element.setAttribute('style', 'margin: 0px auto; width: 290px');
                else:
                    element.setAttribute('style', 'display: none');
            for CLASS in cleanCLASS:
                element = frame.findFirstElement("div[class='%s']"%CLASS)
                element.setAttribute('style', 'display: none');
        elif 'dict.youdao.com' in currentURL:
            cleanID = ['custheme', 'topImgAd', 'c_footer', 'ads', \
                    'result_navigator', 'rel-search', 'container', 'results-contents'] 
            cleanCLASS = ['c-topbar c-subtopbar', 'c-header', 'c-bsearch'] 
            for ID in cleanID:
                element = frame.findFirstElement("div[id='%s']"%ID)
                if element.attribute('id') == 'results-contents':
                    element.setAttribute('style', 'margin-left: 10px; margin-right: 10px; position:relative');
                elif element.attribute('id') == 'container':
                    element.setAttribute('style', 'margin: 0px auto; width: 560px');
                else:
                    element.setAttribute('style', 'display: none');
            for CLASS in cleanCLASS:
                element = frame.findFirstElement("div[class='%s']"%CLASS)
                element.setAttribute('style', 'display: none');

            element = frame.findFirstElement("div[class=c-sust]")
            if element:
                ele = element.firstChild()
                if ele.attribute('href'):
                    self.login = ele
                elif ele.attribute('id') == 'uname':
                    self.uname = ele.toPlainText()
                    self.unameAvailable.emit(self.uname)
                            
            element = frame.findFirstElement("a[id=wordbook]")
            if element:
                if element.attribute('class') == 'add_to_wordbook':
                    self.opWB = element
                elif element.attribute('class') == 'remove_from_wordbook':
                    self.opWB = element

            navHref = ['#', '#authTrans', '#examples', '#eBaike']
            self.navigate = list()
            for href in navHref:
                element = frame.findFirstElement("a[href='%s']"%href)
                self.navigate.append(element)

    def _setValue(self, word):
        if word:
            frame = self.page().mainFrame()
            elementList = frame.findAllElements('input')
            for element in elementList:
                if element.attribute('id') == 'query':
                    element.setAttribute('value', word)
                    break

    def searchWord(self, word):
        if word:
            if self.start:
                self.load(QUrl(self.baseUrl%word))
                self.start = False
            else:
                self._setValue(word)
                self.page().mainFrame().evaluateJavaScript('f.submit()')

    def navigateTo(self, num):
        if 0 <= num < 4:
            self.navigate[num].evaluateJavaScript("var evObj = document.createEvent('MouseEvents'); \
                    evObj.initEvent( 'click', true, true ); \
                    this.dispatchEvent(evObj);")


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.cmd = QLineEdit(self)
        self.cmd.returnPressed.connect(self.search)
        self.cmd.hide()
        self.view = Browser()
        self.view.unameAvailable.connect(self.getUserName)
        self.view.show()
        self.mgr = self.view.page().networkAccessManager();
        self.mgr.finished.connect(self.view.clean_page)

        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)
        layout.addWidget(self.cmd)
        self.setWindowTitle(u'有道词典')

    def getUserName(self, uname):
        if uname:
            title = u'%s @ 有道词典' % uname
            self.setWindowTitle(title)

    def search(self):
        text = self.cmd.text()
        quit = ('q', 'quit')
        if text in quit:
            self.close()

        if text == 'login':
            if not self.view.uname:
                self.view.login.evaluateJavaScript("var evObj = document.createEvent('MouseEvents'); \
                        evObj.initEvent( 'click', true, true ); \
                        this.dispatchEvent(evObj);")
            else:
                print 'Already loged in'
            self.cmd.hide()
            return
            
        if text == 'add':
            self.view.opWB.evaluateJavaScript("var evObj = document.createEvent('MouseEvents'); \
                    evObj.initEvent( 'click', true, true ); \
                    this.dispatchEvent(evObj);")

            self.cmd.hide()
            return
            
        if text == 'wordbook':
            if self.view.uname:
                import webbrowser
                url = self.view.wordbook.parent().attribute('href')
                print url
                webbrowser.open_new_tab(url)
            else:
                print 'Not login yet!'
            
            self.cmd.hide()
            return

        if text:
            self.cmd.hide()
            self.cmd.clear()
            self.view.searchWord(text)
            self.view.setFocus(Qt.OtherFocusReason)

    def keyPressEvent(self, event):
        key = event.key()
        if event.modifiers() == Qt.ControlModifier:
            if key == Qt.Key_F:
                nextPage = QKeyEvent(QEvent.KeyPress, Qt.Key_PageDown, Qt.NoModifier)
                QCoreApplication.sendEvent(self.view.page(), nextPage)
            if key == Qt.Key_B:
                prevPage = QKeyEvent(QEvent.KeyPress, Qt.Key_PageUp, Qt.NoModifier)
                QCoreApplication.sendEvent(self.view, prevPage)
        else:
            if key == Qt.Key_J:
                self.view.page().mainFrame().scroll(0,15)
            if key == Qt.Key_K:
                self.view.page().mainFrame().scroll(0,-15)
            if key == Qt.Key_H:
                self.view.page().mainFrame().scroll(-15,0)
            if key == Qt.Key_L:
                self.view.page().mainFrame().scroll(15,0)
            if key == Qt.Key_Colon:
                self.cmd.clear()
                self.cmd.show()
                self.cmd.setFocus(Qt.OtherFocusReason)
            if key == Qt.Key_Escape:
                self.cmd.hide()
                self.view.setFocus(Qt.OtherFocusReason)
            if key == Qt.Key_0:
                self.view.navigateTo(0)
            if key == Qt.Key_1:
                self.view.navigateTo(1)
            if key == Qt.Key_2:
                self.view.navigateTo(2)
            if key == Qt.Key_3:
                self.view.navigateTo(3)
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = Window()
    win.show()


    sys.exit(app.exec_())
