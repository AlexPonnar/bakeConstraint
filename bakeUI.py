import sys
import bake
reload(bake)
from pprint import pprint
from maya import cmds

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets

except:
    from PySide2 import QtGui, QtCore, QtWidgets

startFrame = cmds.playbackOptions(query=True, animationStartTime=True)
endFrame = cmds.playbackOptions(query=True, animationEndTime=True)



tableHeader = ['Parent', 'Child', 'Constraint Name']


class constraintBakeUi(QtWidgets.QDialog):

    def __init__(self, parent = None):
        super(constraintBakeUi, self).__init__(parent)
        self.setWindowTitle('Bake Constraint UI')
        self.resize(500, 300)
        self.__initLayout()

    def __initLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        vLayout = QtWidgets.QHBoxLayout()

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(len(tableHeader))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setHorizontalHeaderLabels(tableHeader)

        self.refreshButton = QtWidgets.QPushButton('Refresh')
        self.refreshButton.setIcon(QtGui.QIcon('circular-arrow.png'))
        self.bakeButton = QtWidgets.QPushButton('Bake')
        self.bakeButton.setIcon(QtGui.QIcon('bread.png'))
        vLayout.addWidget(self.refreshButton)
        vLayout.addWidget(self.bakeButton)


        mainLayout.addWidget(self.tableWidget)
        mainLayout.addLayout(vLayout)
        self.setLayout(mainLayout)

        self.refreshButton.clicked.connect(self.refreshList)
        self.bakeButton.clicked.connect(self.bakeConstraint)

    def refreshList(self):
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)
        shotListDummy = bake.QueryConstraints()
        if not shotListDummy:
            return
        for each_key in shotListDummy:
            conName = each_key
            parent = shotListDummy[each_key].get('driver')[0]
            child = shotListDummy[each_key].get('child')[0]
            num_rows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(num_rows)
            self.tableWidget.setItem(num_rows, 0, QtWidgets.QTableWidgetItem(
                parent))
            self.tableWidget.setItem(num_rows, 1, QtWidgets.QTableWidgetItem(
                child))
            self.tableWidget.setItem(num_rows, 2, QtWidgets.QTableWidgetItem(
                conName))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.itemClicked.connect(self.select_controller)


    def bakeConstraint(self):
        row = self.tableWidget.currentItem().row()
        column = self.tableWidget.currentItem().column()
        controllerName = self.tableWidget.item(row, column).text()
        bake.smartBake(startFrame, endFrame, controllerName)

    def select_controller(self):
        row = self.tableWidget.currentItem().row()
        column = self.tableWidget.currentItem().column()

        controllerName = self.tableWidget.item(row, column).text()
        cmds.select(controllerName)


def main():
    #app = QtGui.QApplication(sys.argv)
    myWindow = constraintBakeUi()
    myWindow.show()
    #sys.exit(app.exec_())


if __name__ == '__main__':
    main()
