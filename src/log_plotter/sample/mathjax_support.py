#!/usr/bin/env python

import sys
from PyQt4.QtCore import QFile, QFileInfo, QTextStream, QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView

pageSource = r"""<html><head>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
</head><body>
<p><mathjax>$$
\frac{1}{2} x = 3
$$</mathjax></p>
</body></html>"""

app = QApplication(sys.argv)

# tempFile = QFile('mathjax.html')
# tempFile.open(QFile.WriteOnly)
# stream = QTextStream(tempFile)
# stream << pageSource
# tempFile.close()
# fileUrl = QUrl.fromLocalFile(QFileInfo(tempFile).canonicalFilePath())

webView = QWebView()
# webView.load(fileUrl)
webView.setHtml(pageSource)
webView.show()

sys.exit(app.exec_())
