import os
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter
from PIL import Image


def main():
    front = input("Site front dimension (unit meter/minimum 7m): ")
    f = site_front(front)

    depth = input("Site depth dimension (unit meter/minimum 30m): ")
    d = site_depth(depth)

    house = select(f)
    house_img = str(house + ".png")

    name = input("Type your name: ")
    info = house_info(house, house_img)

    px_mm = 0.2645833333
    dim = info[0] * px_mm
    dim2 = info[1] * px_mm
    pname = info[3]

    page1 = "Page1.pdf"
    paths = [page1, info[2]]

    pdf_name = str(name + "_" + str(f) + "x" + str(d) + "_" + pname + ".pdf")

    create_pdf(paths, pdf_name)
    print("PDF", pdf_name, "created")


def site_front(front):
    front = float(front)
    while True:
        try:
            if front < 7:
                print("Site front must be larger than 7 meters")
                front = float(input("Site front dimension (unit meter/minimum 7m): "))
            else:
                return front
        except ValueError:
            pass


def site_depth(depth):
    depth = float(depth)
    while True:
        try:
            if depth < 30:
                print("Site depth must be larger than 30 meters")
                depth = float(input("Site depth dimension (unit meter/minimum 30m): "))
            else:
                return depth
        except ValueError:
            pass


def select(f):
    folk = "Folk"
    acacia = "Acacia"
    banksia = "Banksia"
    telopea = "Telopea"
    lada = "Lada"

    if 7 <= f < 12:
        return folk
    elif 12 <= f < 15:
        nbed = int(input("Type the number of bedrooms (1, 2, or 3): "))
        if nbed == 1:
            return lada
        elif nbed == 2:
            floor = int(input("Type the number of floors (1 or 2): "))
            if floor == 1:
                return acacia
            elif floor == 2:
                return folk
            else:
                print("Number of floors must be 1 or 2")
                return None
        elif nbed == 3:
            return banksia
        else:
            print("Number of bedrooms must be 1, 2, or 3")
            return None
    elif f >= 15:
        nbed = int(input("Type the number of bedrooms (1, 2, 3, or 4): "))
        if nbed == 1:
            return lada
        elif nbed == 2:
            floor = int(input("Type the number of floors (1 or 2): "))
            if floor == 1:
                return acacia
            elif floor == 2:
                return folk
            else:
                print("Number of floors must be 1 or 2")
                return None
        elif nbed == 3:
            return banksia
        elif nbed == 4:
            return telopea

        else:
            print("Number of bedrooms must be between 1 and 4")
            return None


def house_info(house, house_img):
    image = Image.open(house_img)
    width, height = image.size
    draw = str("Drawings_" + house + ".pdf")
    hname = str(house + "House")
    info = [width, height, draw, hname]
    return info


class PDF:
    def __init__(self, house_img, f, d, dim, dim2, pname, page1):
        self.pdf = FPDF(unit='mm', format=(420, 297))
        self.pdf.add_page()
        self.pdf.set_line_width(0.4)
        self.pdf.set_draw_color(0)
        self.pdf.set_fill_color(r=255, g=255, b=255)
        self.pdf.image(house_img, x=40, y=30 + (((f * 10) - (dim2)) / 2), w=dim, h=0)
        self.pdf.rect(30, 30, d * 10, f * 10, round_corners=False, style="D")
        self.pdf.image("scale_bar.png", x=260, y=260, w=130, h=0)
        self.pdf.set_font("Helvetica", size=11)
        self.pdf.cell(0, 30, str(d), ln=True, align='C')
        self.pdf.cell(25, 30 + (f * 5), str(f), ln=True, align='C')
        self.pdf.set_font("Helvetica", size=30)
        self.pdf.text(x=30, y=280, txt=pname.upper())
        self.pdf.set_line_width(0.3)
        self.pdf.set_draw_color(0)
        self.pdf.line(x1=0, y1=250, x2=420, y2=250)
        self.pdf.output(page1)


def create_pdf(paths, output):
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(path)
        writer.addpages(reader.pages)  # Use lowercase "p" in addpages
    writer.write(output)



if __name__ == "__main__":
    main()
