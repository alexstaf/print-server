import cv2
import win32ui
import win32print
import numpy as np
from PIL import Image, ImageWin


class Printer:
    def __init__(self):
        # HORZRES / VERTRES = printable area
        self.HORZRES = 8
        self.VERTRES = 10

        # LOGPIXELS = dots per inch
        self.LOGPIXELSX = 88
        self.LOGPIXELSY = 90

        # PHYSICALWIDTH/HEIGHT = total area
        self.PHYSICALWIDTH = 110
        self.PHYSICALHEIGHT = 111

        # PHYSICALOFFSETX/Y = left / top margin
        self.PHYSICALOFFSETX = 112
        self.PHYSICALOFFSETY = 113

        self.printer_name = win32print.GetDefaultPrinter()

        # You can only write a Device-independent bitmap directly to
        # a Windows device context; therefore we need (for ease) to use
        # the Python Imaging Library to manipulate the image.

        # Create a device context from a named printer
        # and assess the printable size of the paper.
        self.hDC = win32ui.CreateDC()
        self.hDC.CreatePrinterDC(self.printer_name)
        self.printable_area = (self.hDC.GetDeviceCaps(self.HORZRES),
                               self.hDC.GetDeviceCaps(self.VERTRES))
        self.printer_size = (self.hDC.GetDeviceCaps(self.PHYSICALWIDTH),
                             self.hDC.GetDeviceCaps(self.PHYSICALHEIGHT))
        self.printer_margins = (self.hDC.GetDeviceCaps(self.PHYSICALOFFSETX),
                                self.hDC.GetDeviceCaps(self.PHYSICALOFFSETY))

    def print(self, path):
        # Open the image, rotate it if it's wider than it is high, and
        # work out how much to multiply each pixel by to get it as big
        # as possible on the page without distorting.
        pil_img = Image.open(path)
        if pil_img.size[0] < pil_img.size[1]:
            pil_img = pil_img.rotate(90)

        img = np.array(pil_img)[:, :, ::-1]
        cond = (img.shape[1] / img.shape[0] >
                self.printable_area[0] / self.printable_area[1])

        if cond:
            k = self.printable_area[1] / img.shape[0]
        else:
            k = self.printable_area[0] / img.shape[1]

        resized_img = cv2.resize(img, (0, 0), fx=k, fy=k)

        if cond:
            if resized_img.shape[1] > self.printable_area[0]:
                k = (resized_img.shape[1] - self.printable_area[0]) // 2
                resized_img = resized_img[:, k:k + self.printable_area[0]]
        else:
            if resized_img.shape[0] > self.printable_area[1]:
                k = (resized_img.shape[0] - self.printable_area[1]) // 2
                resized_img = resized_img[k:k + self.printable_area[1], :]

        img_to_print = Image.fromarray(resized_img[:, :, ::-1])

        # Start the print job, and draw the bitmap to
        # the printer device at the scaled size.
        self.hDC.StartDoc(path)
        self.hDC.StartPage()

        dib = ImageWin.Dib(img_to_print)
        dib.draw(self.hDC.GetHandleOutput(),
                 (0, 0, self.printer_size[0], self.printer_size[1]))

        self.hDC.EndPage()
        self.hDC.EndDoc()

    def __del__(self):
        self.hDC.DeleteDC()
