from PyQt5.QtWidgets import QPushButton

class Blocks():

    form = 0
    btn = 0
    actualColor = 0

    #imutable colors, this should be dynamic an controlled from the widget
    COLORS = ("grey", "red", "yellow", "black", "blue")

    def __init__(self, day, hour, form, color, hboxTable):

        self.form = form
        self.btn = QPushButton( str(hour), self.form)
        if color < len(self.COLORS):
            self.actualColor = color
        else:
            self.actualColor = 0
        self.btn.setStyleSheet("color: pink; background-color: " + self.COLORS[self.actualColor])
        self.btn.setToolTip(str(day*24 + hour))
        hboxTable.addWidget(self.btn)
        self.btn.setFixedWidth(30)
        self.btn.clicked.connect( self.on_click )

    def on_click(self):
        self.actualColor += 1
        if self.actualColor >= len(self.COLORS):
            self.actualColor = 0
        self.btn.setStyleSheet("color: pink; background-color: " + self.COLORS[self.actualColor])
        self.form.show()

    def getColor(self):
        return self.actualColor
