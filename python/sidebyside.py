from PyPDF2 import PdfFileWriter, PdfFileReader
import sys

in1,in2,out = sys.argv[1:]

output = PdfFileWriter()
input1 = PdfFileReader(file(in1, "rb"))
input2 = PdfFileReader(file(in2, "rb"))

m = min(input1.getNumPages(),input2.getNumPages())
print "common pages",m
for i in range(0,m):
    print "adding page common",i
    p1 = input1.getPage(i)
    p2 = input2.getPage(i)
    offset_x = p1.mediaBox[2]
    offset_y = 0
    p1.mergeTranslatedPage(p2, offset_x, offset_y, expand=True)
    output.addPage(p1)

for j in range(i+1,input1.getNumPages()):
    # BUGGY use addblank to balance
    print "adding ",j,"from first"
    output.addPage(input1.getPage(j))
for j in range(i+1,input2.getNumPages()):
    # BUGGY use addblank to balance
    p0 = output.addBlankPage(p1.mediaBox[2],p1.mediaBox[3])
    offset_x = p1.mediaBox[2] # lastg
    offset_y = 0
    p0.mergeTranslatedPage(input2.getPage(j), offset_x, offset_y)

# finally, write "output" to document-output.pdf
outputStream = file(out, "wb")
output.write(outputStream)
outputStream.close()