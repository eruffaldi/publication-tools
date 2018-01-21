from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjectNotFound
import sys
def extract(objid, obj,pages,anno,marked):
    if isinstance(obj, dict):
        # 'Type' is PDFObjRef type
        if obj.has_key('Type') and obj['Type'].name == 'Page':
            pages.append(objid)
        elif obj.has_key('C'):
            pr = obj['P']
            try:
                pi = pages.index(pr.objid)+1
            except:
                pi = -1
                tgt = obj.get("IRT",None)
                if tgt is not None:
                    #print obj["Type"],obj["State"]
                    if str(obj["Type"]) == "/Annot" and str(obj["State"]) == "Marked":
                        marked.add(tgt.objid)
                        #print "noname",objid,[(x,obj[x]) for x in obj.keys()]
                return
            rc = obj["Rect"]
            anno.append(dict(page=pi,id=objid,content=obj.get('Contents',"highlight"),x=rc[0],y=rc[1]))
            print(objid,pi, obj['Subj'],obj['T'],obj.get('Contents'),obj.keys(),obj["Rect"])


def main():
    pages = []
    fp = file(sys.argv[1], 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser, "")
    visited = set()
    marked = set()
    allannotations = []
    for xref in doc.xrefs:
        for objid in xref.get_objids():
            if objid in visited: continue
            visited.add(objid)
            try:
                obj = doc.getobj(objid)
                if obj is None: continue
                extract(objid,obj,pages,allannotations,marked)
            except PDFObjectNotFound, e:
                print >>sys.stderr, 'not found: %r' % e

    allannotations.sort(key=lambda x: (x["page"],x["x"] < 200,x["y"]))

    print "All ordered:"
    for x in allannotations:            
        if x["content"] != "highlight":
            print "Page %d: %s" % (x["page"],x["content"])

    print "Not addressed:"
    for x in allannotations:            
        if x["content"] != "highlight":
            if not x["id"] in marked:
                print  "TODO Page %d: %s" % (x["page"],x["content"])

if __name__ == '__main__':
    main()