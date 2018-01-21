#Emanuele Ruffaldi 2014-2016
#
#TODO: keep bib explicit and not replace with bbl
#TODO: add frontiersSCNS.cls frontiersinSCNS_ENG_HUMS.bst in replicable
#TODO: add logo1
#TODO: don't merge
#TODO: respect folders
import os,sys,re,argparse

def checkpaths(f,paths):
	if os.path.isfile(f):
		return f
	for p in paths:
		fp = os.path.join(p,f)
		if os.path.isfile(fp):
			return fp
	return None
def startmerge(infile,figures,args,rootfile):
	print "processing",infile
	o = open(infile,"r")
	output = []
	xr = re.compile('\\includegraphics(\[[^\]]+\])?\{([^\}]+)\}')
	yr = re.compile('\\bibliography\{([^}]+)\}')
	gp = re.compile('\\\graphicspath\{([^}]+)\}')
	paths= []
	for line in o:
		sline = line.strip()
		if len(sline) == 0 or sline[0] == "%":
			continue
		if line.startswith("\\input"):
			pre,rest = line.split("{")
			sub = rest.strip().replace("}","")
			if not sub.endswith(".tex"):
				sub = sub+".tex"
			suboutput,subpaths = startmerge(sub,figures,args,rootfile)
			paths.extend(subpaths)
			output.extend(suboutput)
		elif line.find("\\graphicspath") >= 0:
			g = gp.search(line)
			if g:
				print "graphicspath",g.group(1)
				paths = [x.strip("{}") for x in g.group(1).split("{")]
		elif sline.startswith("\\bibliography{"):
			if args.keepbib:
				k = sline[len("\\bibliography{"):]
				k2 = k.find("}")
				k = k[0:k2]
				for y in k.split(","):
					if os.path.isfile(y):
						figures.append(y)
					elif os.path.isfile(y+".bib"):
						figures.append(y+".bib")
				output.append(sline)
			else:
				sub = os.path.splitext(os.path.split(rootfile)[1])[0]+".bbl"
				suboutput,subpaths = startmerge(sub,figures,args,rootfile)
				paths.extend(subpaths)
				output.extend(suboutput)
				#r.append("\\input{%s.bbl}" % (sub)
		else:
			w = line.strip()
			g = xr.search(w)
			if g:
				print "figure",g.group(1),g.group(2)
				figures.append(g.group(2))
			output.append(w)
	return (output,paths)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Merges files for Publishing in ZIP')
	parser.add_argument('--target', default="merged.tex")
	parser.add_argument('file', default="main.tex")
	parser.add_argument('--keepbib',action="store_true",help="keeps bib files instead of replacing them with the bbl")
	parser.add_argument('--list', action="store_true",help="lists only")
	parser.add_argument('--removefolders', type=bool,default=True)

	args = parser.parse_args()

	figures = []
	target = args.target
	rootfile = args.file


	content,paths = startmerge(rootfile,figures,args,rootfile)
	extensions = ["pdf","png","jpg","eps"]
	xfigures = []
	good = True
	for f in set(figures):
		founds = f
		found = checkpaths(f,paths)
		if not found:
			for e in extensions:
				ff = f+"."+e
				founds = ff
				found = checkpaths(ff,paths)
				if found:
					break
		if found:
			if args.removefolders:
				a = os.path.split(founds)
				if a[0] != "":
					print "manually remove folder for",found,founds
					good = False
			xfigures.append((founds,found))
	if good:

		if os.path.isfile("llncs.cls"):
			xfigures.append("llncs.cls","llncs.cls")
		print "\n\nExtra Files"
		print "\n".join(["%s %dKB" % (x,os.stat(x).st_size/1.0E3) for q,x in xfigures])

		if not args.list:
			o = open(target,"wb")
			o.write("\n".join(content))
			o.close()
			o = open("merged.lst","w")
			o.write("\n".join([target]+[x for q,x in xfigures]))
			o.close()
			print "\nAssemble using:\nzip merged.zip %s $(cat merged.lst)" % ("-j" if args.removefolders else "")
