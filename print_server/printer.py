# -*- coding: UTF-8 -*-

"""Script that contains Printer class."""

import win32ui
import win32print
from PIL import ImageWin, ImageOps


class Printer:
    """Class for printing PIL images."""

    def __init__(self):
        """Initialize constants & necessary variables."""
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

    def print(self, pil_img, filename):
        """Print PIL image."""
        # Rotate the image if it's wider than it is high, and work out
        # how much to multiply each pixel by to get it as big
        # as possible on the page without distorting.
        pil_img = ImageOps.exif_transpose(pil_img)

        if (self.printable_area[0] > self.printable_area[1]
                and pil_img.size[0] < pil_img.size[1]
                or self.printable_area[0] < self.printable_area[1]
                and pil_img.size[0] > pil_img.size[1]):
            pil_img = pil_img.rotate(90, expand=True)

        if (pil_img.size[0] / pil_img.size[1]
                > self.printable_area[0] / self.printable_area[1]):
            k = self.printable_area[1] / pil_img.size[1]
            w = int(k * pil_img.size[0] + 0.5)
            h = self.printable_area[1]
            pil_img = pil_img.resize((w, h))
            if pil_img.size[0] > self.printable_area[0]:
                left = (pil_img.size[0] - self.printable_area[0]) // 2
                right = left + self.printable_area[0]
                upper = 0
                lower = self.printable_area[1]
                pil_img = pil_img.crop((left, upper, right, lower))
        else:
            k = self.printable_area[0] / pil_img.size[0]
            w = self.printable_area[0]
            h = int(k * pil_img.size[1] + 0.5)
            pil_img = pil_img.resize((w, h))
            if pil_img.size[1] > self.printable_area[1]:
                upper = (pil_img.size[1] - self.printable_area[1]) // 2
                lower = upper + self.printable_area[1]
                left = 0
                right = self.printable_area[0]
                pil_img = pil_img.crop((left, upper, right, lower))

        # Start the print job, and draw the bitmap to
        # the printer device at the scaled size.
        self.hDC.StartDoc(filename)
        self.hDC.StartPage()

        dib = ImageWin.Dib(pil_img)
        dib.draw(self.hDC.GetHandleOutput(),
                 (0, 0, self.printer_size[0], self.printer_size[1]))

        self.hDC.EndPage()
        self.hDC.EndDoc()

    def __del__(self):
        """Release context."""
        self.hDC.DeleteDC()
