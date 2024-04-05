# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'documentwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Doc_Window(object):
    def setupUi(self, Doc_Window):
        if not Doc_Window.objectName():
            Doc_Window.setObjectName(u"Doc_Window")
        Doc_Window.resize(1179, 758)
        self.verticalLayout = QVBoxLayout(Doc_Window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(Doc_Window)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)


        self.retranslateUi(Doc_Window)

        QMetaObject.connectSlotsByName(Doc_Window)
    # setupUi

    def retranslateUi(self, Doc_Window):
        Doc_Window.setWindowTitle(QCoreApplication.translate("Doc_Window", u"Untitled", None))
    # retranslateUi

