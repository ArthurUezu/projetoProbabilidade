from PyQt5 import QtCore, QtGui, QtWidgets
import efarsas
import filtragem
import fato_fake
from datetime import datetime


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(451, 343)

        self.verticalLayout = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Texto = QtWidgets.QLabel(Widget)
        
        font = QtGui.QFont()
        font.setPointSize(26)

        self.Texto.setFont(font)
        self.Texto.setStyleSheet("color:rgb(74, 74, 74);")
        self.Texto.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Texto.setObjectName("Texto")
        self.verticalLayout.addWidget(self.Texto, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.RbFarsas = QtWidgets.QRadioButton(Widget)
        self.RbFarsas.setStyleSheet("color:rgb(74, 74, 74);")
        self.RbFarsas.setChecked(True)
        self.RbFarsas.setObjectName("RbFarsas")

        self.buttonGroup = QtWidgets.QButtonGroup(Widget)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.RbFarsas,1)

        self.horizontalLayout.addWidget(self.RbFarsas, 0, QtCore.Qt.AlignHCenter)

        self.RbG1 = QtWidgets.QRadioButton(Widget)
        self.RbG1.setStyleSheet("color:rgb(74, 74, 74);")
        self.RbG1.setObjectName("RbG1")
        self.buttonGroup.addButton(self.RbG1,2)
        self.horizontalLayout.addWidget(self.RbG1, 0, QtCore.Qt.AlignHCenter)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.Tag = QtWidgets.QLineEdit(Widget)
        self.Tag.setStyleSheet("background-color:rgb(248,248,248);\n" "border-color: rgb(136, 136, 136);")
        self.Tag.setObjectName("Tag")
        self.verticalLayout.addWidget(self.Tag)

        self.deate = QtWidgets.QHBoxLayout()
        self.deate.setObjectName("deate")

        self.de = QtWidgets.QLabel(Widget)
        self.de.setObjectName("de")
        self.deate.addWidget(self.de)

        self.ate = QtWidgets.QLabel(Widget)
        self.ate.setObjectName("ate")
        self.deate.addWidget(self.ate)
        self.verticalLayout.addLayout(self.deate)

        self.datas = QtWidgets.QHBoxLayout()
        self.datas.setObjectName("datas")
        self.data1 = QtWidgets.QDateEdit(Widget)
        self.data1.setObjectName("data1")
        self.datas.addWidget(self.data1)
        self.data2 = QtWidgets.QDateEdit(Widget)
        self.data2.setObjectName("data2")
        self.datas.addWidget(self.data2)
        self.verticalLayout.addLayout(self.datas)

        self.Bpesquisa = QtWidgets.QPushButton(Widget)
        self.Bpesquisa.setStyleSheet("color: rgb(64, 65, 66);\n" "border-color: rgb(136, 136, 136);")
        self.Bpesquisa.setObjectName("Bpesquisa")
        self.verticalLayout.addWidget(self.Bpesquisa)

        self.Edtexto = QtWidgets.QTextEdit(Widget)
        self.Edtexto.setStyleSheet("background-color:rgb(248,248,248);\n" "border-color: rgb(136, 136, 136);")
        self.Edtexto.setReadOnly(True)
        self.Edtexto.setObjectName("Edtexto")
        self.verticalLayout.addWidget(self.Edtexto)

        

        

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        self.Bpesquisa.clicked.connect(self.cleanAndSet)

    def cleanAndSet(self):
        Texto=self.Tag.text()
        if Texto=="":
            self.Edtexto.setText("Nenhuma Tag Selecionada!")
        elif (self.data1.date()>self.data2.date()):
            self.Edtexto.setText("Data Inicial Maior que a Data Final!")
        else:
            self.Tag.setText("")
            if (self.buttonGroup.checkedId() == 1):
                self.Edtexto.append("Selecionado E-Farsas\n")
                self.Edtexto.append("Tag: "+Texto)
                efarsas.startEFarsas(Texto)
                filtragem.startFiltragem(True,self.data1.date().toPyDate().strftime("%Y-%m-%d"),self.data2.date().toPyDate().strftime("%Y-%m-%d"))

            elif (self.buttonGroup.checkedId() == 2):
                self.Edtexto.append("Selecionado G1\n")
                self.Edtexto.append("Tag: "+Texto)
                fato_fake.startFato_fake(Texto)
                filtragem.startFiltragem(False,self.data1.date().toPyDate().strftime("%Y-%m-%d"),self.data2.date().toPyDate().strftime("%Y-%m-%d"))



    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Compilador de Fake News"))
        self.Texto.setText(_translate("Widget", "Compilador de Fake News"))
        self.RbFarsas.setText(_translate("Widget", "E-Farsas"))
        self.RbG1.setText(_translate("Widget", "G1 Fato ou Fake"))
        self.de.setText(_translate("Widget", "De"))
        self.ate.setText(_translate("Widget", "Ate"))
        self.Bpesquisa.setText(_translate("Widget", "Pesquisa"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
