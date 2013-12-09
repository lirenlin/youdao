#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

from BeautifulSoup import BeautifulSoup
import urllib2
import signal

view = None
app = None
webpage= None

class Page(QWebPage):
    def __init__(self, url):
        QWebPage.__init__(self)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        #self.connect(self, SIGNAL('loadFinished(bool)'), self._clean_page)
        self.connect(self, SIGNAL('loadStarted(bool)'), self._clean_page)
        self.mainFrame().load(QUrl(url))

    def _clean_page(self, result):
        print 'page: clean page'
        frame = self.mainFrame()
        divList = frame.findAllElements('div')
        cleanID = ['custheme', 'topImgAd', 'c_footer', 'ads', 'result_navigator', 'rel-search'] 
        cleanCLASS = ['c-topbar c-subtopbar', 'c-header', 'c-bsearch'] 
        for div in divList:
            if div.attribute('class') in cleanCLASS:
                div.setAttribute('style', 'display: none');
            if div.attribute('id') in cleanID:
                div.setAttribute('style', 'display: none');
            if div.attribute('id') == 'results-contents':
                div.setAttribute('style', 'margin-left: 10px; margin-right: 10px; position:relative');
            if div.attribute('id') == 'container':
                div.setAttribute('style', 'margin: 0px auto; width: 550px');

        self.contentsChanged.emit()

    def setValue(self, word):
        if word:
            frame = self.mainFrame()
            elementList = frame.findAllElements('input')
            for element in elementList:
                if element.attribute('id') == 'query':
                    element.setAttribute('value', word)
                    break


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)
        #self.loadProgress.connect(self._progress)
        #self.loadStarted.connect(self._result_available)

    def _progress(self, percent):
        if percent == 30:
            print "progress"
            self._result_available(True)

    def _result_available(self, result):
        print "browser: clean page"
        #frame = self.page().mainFrame()
        self.clean_page();
        self.page().contentsChanged.emit()
        #self.update()
        #self.show()
        #print unicode(frame.toHtml()).encode('utf-8')

    def clean_page(self):
        frame = self.page().mainFrame()
        divList = frame.findAllElements('div')
        cleanID = ['custheme', 'topImgAd', 'c_footer', 'ads', 'result_navigator', 'rel-search'] 
        cleanCLASS = ['c-topbar c-subtopbar', 'c-header', 'c-bsearch'] 
        for div in divList:
            if div.attribute('class') in cleanCLASS:
                div.setAttribute('style', 'display: none');
            if div.attribute('id') in cleanID:
                div.setAttribute('style', 'display: none');
            if div.attribute('id') == 'results-contents':
                div.setAttribute('style', 'margin-left: 10px; margin-right: 10px; position:relative');
            if div.attribute('id') == 'container':
                div.setAttribute('style', 'margin: 0px auto; width: 550px');

    def setValue(self, word):
        if word:
            frame = self.page().mainFrame()
            elementList = frame.findAllElements('input')
            for element in elementList:
                if element.attribute('id') == 'query':
                    element.setAttribute('value', word)
                    break


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.cmd = QLineEdit(self)
        self.cmd.returnPressed.connect(self.search)
        self.cmd.hide()
        self.view = Browser()
        self.view.load(QUrl('http://dict.youdao.com/search?q=linux&keyfrom=dict.index'))
        #self.page = Page(QUrl('http://dict.youdao.com/search?q=linux&keyfrom=dict.index'))
        #self.view = QWebView(self)
        #self.view.setPage(self.page)
        self.view.show()
        self.mgr = self.view.page().networkAccessManager();
        self.mgr.finished.connect(self.view.clean_page)

        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)
        layout.addWidget(self.cmd)

    def search(self):
        text = self.cmd.text()
        quit = ('q', 'quit')
        if text in quit:
            self.close()

        if text:
            self.cmd.hide()
            self.cmd.clear()
            self.view.setValue(text)
            self.view.page().mainFrame().evaluateJavaScript('f.submit()')
            self.view.setFocus(Qt.OtherFocusReason)
            #self.page().mainFrame().evaluateJavaScript('f.submit()')


    def keyPressEvent(self, event):
        key = event.key()
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
            
def onLoadFinished(result):
    src = unicode(webpage.mainFrame().toHtml()).encode('utf-8')
    soup = BeautifulSoup(src)

    #cleanID = ['custheme', 'topImgAd', 'c_footer', 'ads'] 
    #cleanCLASS = ['c-topbar c-subtopbar', 'c-header', 'c-bsearch'] 
    #for s in cleanID:
    #    element = soup.find('div', {'id':s})
    #    if element:
    #        element.extract()
    #for s in cleanCLASS:
    #    element = soup.find('div', attrs={'class':s})
    #    if element:
    #        element.extract()

    html = soup.prettify()
    view.setHtml(html)


if __name__ == '__main__':

    #f = urllib2.urlopen('http://dict.youdao.com/search?q=linux&keyfrom=dict.index')
    #s = f.read()
    #src = s.decode('utf-8').encode('utf-8')
    #soup = BeautifulSoup(f)
    #cleanID = ['custheme', 'topImgAd', 'c_footer', 'ads'] 
    #cleanCLASS = ['c-topbar c-subtopbar', 'c-header', 'c-bsearch'] 
    #for s in cleanID:
    #    element = soup.find('div', {'id':s})
    #    if element:
    #        element.extract()
    #for s in cleanCLASS:
    #    element = soup.find('div', attrs={'class':s})
    #    if element:
    #        element.extract()

    #header = soup.findAll('html')
    #header[0]['class'] = 'ua-sf ua-sf ua-wk ua-linux'
    #html = soup.prettify()

    app = QApplication(sys.argv)
    #view = Browser()
    win = Window()
    win.show()

    #view.setHtml(html)
    #print html

    #view.load(QUrl('http://dict.youdao.com/search?q=linux&keyfrom=dict.index'))

    #webpage = QWebPage()
    #webpage.loadFinished.connect(onLoadFinished)
    #webpage.mainFrame().load(QUrl('http://dict.youdao.com/search?q=linux&keyfrom=dict.index'))

    sys.exit(app.exec_())
