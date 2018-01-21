from PyPDF2 import PdfFileWriter, PdfFileReader
import sys

in1,out = sys.argv[1:]

output = PdfFileWriter()
input1 = PdfFileReader(file(in1, "rb"))

for i in range(0,input1.getNumPages()):
    p1 = input1.getPage(i)
    output.addPage(p1)
output.addBlankPage()

# finally, write "output" to document-output.pdf
outputStream = file(out, "wb")
output.write(outputStream)
outputStream.close()