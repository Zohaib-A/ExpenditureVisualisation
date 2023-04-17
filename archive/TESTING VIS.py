import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('My Window')

        # Create a Matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Create a vertical layout and add the canvas to it
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Create a button and connect its clicked signal to the update_plot slot
        self.button = QPushButton('Update Plot')
        self.button.clicked.connect(self.update_plot)
        layout.addWidget(self.button)

        # Create a widget and set the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the window to the widget
        self.setCentralWidget(widget)

        # Create a Matplotlib axes and plot some data
        self.axes = self.figure.add_subplot(111)
        self.axes.plot([1, 2, 3, 4], [1, 4, 2, 3])

        # Show the window
        self.show()

    def update_plot(self):
        # Clear the previous plot
        self.axes.clear()

        # Plot some new data
        self.axes.plot([1, 2, 3, 4], [5, 2, 4, 1])

        # Update the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
