import ROOT as R
import os

diodelist = ["FZ200P_04_DiodeL_8"]
annlist = [0,1,2,3,4,5,6,7]
h0 = []
h1 = []
h2 = []
h3 = []

tfile = R.TFile("PAIRS.root")   #R.TFile("CVIV.root")
tree = tfile.Get("pair")
tree.Draw("biasdut>>hv")
hv2 = R.gPad.GetPrimitive("hv")
for diode in diodelist:
	for ann in annlist:
		cut0 = "pair==0 && temp==0 && ann==" + str(ann) + " && diode==\"" + diode + "\"" # 0==redLaserFront
		cut1 = "pair==0 && temp==-20 && ann==" + str(ann) + " && diode==\"" + diode + "\""
		#cut2 = "cviv==1 && temp==0 && ann==" + str(ann) + " && diode==\"" + diode + "\""
		#cut3 = "cviv==1 && temp==-20 && ann==" + str(ann) + " && diode==\"" + diode + "\""
		plot0 = "redfront_t0_a" + str(ann) 
		plot1 = "redfront_t-20_a" + str(ann) 
		#plot2 = "cv_t0_a" + str(ann) 
		#plot3 = "cv_t-20_a" + str(ann)
		print cut0, plot0
		tree.Draw("pairdut:biasdut>>" + plot0, cut0, "box") 
		###h0 =  R.gPad.GetPrimitive("test") 
		h0.append(R.gPad.GetPrimitive(plot0)) 
		tree.Draw("pairdut:biasdut>>" + plot1, cut1, "box") 
		h1.append(R.gPad.GetPrimitive(plot1)) 
		#tree.Draw("c1k:v>>" + plot2, cut2, "box") 
		#h2.append(R.gPad.GetPrimitive(plot2)) 
		#tree.Draw("c1k:v>>" + plot3, cut3, "box")
		#h3.append(R.gPad.GetPrimitive(plot3)) 
		h0[len(h0)-1].SetMarkerColor(ann+1)
		h1[len(h0)-1].SetMarkerColor(ann+1)
		#h2[len(h0)-1].SetMarkerColor(ann+1)
		#h3[len(h0)-1].SetMarkerColor(ann+1)
		###h1 =  R.gPad.GetPrimitive(plot1) 
		###h2 =  R.gPad.GetPrimitive(plot2) 
		###h3 =  R.gPad.GetPrimitive(plot3) 
		###print h0.GetBinEntries()
	name = "test2"
	cut = "pair==0 && ann==0 && temp==0 && diode==\"FZ200P_04_DiodeL_8\""
	tree.Draw("pairdut:biasdut>>"+name,cut,"box")
	hiv2 = R.gPad.GetPrimitive(name)
###tree.Draw("bias:v>>hiv3","cviv==0 && ann==0 && temp==-20 && diode==\"FZ320Y_06_DiodeS_153\"","box")
###hiv4 = R.gPad.GetPrimitive("hiv3")

if os.path.isfile("plots.root"): hFile = R.TFile("plots.root",'UPDATE')
else: hFile = R.TFile("plots.root",'RECREATE')
hv2.Write("",R.TObject.kOverwrite)
for i in xrange(len(h0)):
	h0[i].Write("",R.TObject.kOverwrite)
	h1[i].Write("",R.TObject.kOverwrite)
	#h2[i].Write("",R.TObject.kOverwrite)
	#h3[i].Write("",R.TObject.kOverwrite)
###h0.Write("",R.TObject.kOverwrite)
###h1.Write("",R.TObject.kOverwrite)
###h2.Write("",R.TObject.kOverwrite)
###h3.Write("",R.TObject.kOverwrite)
###hiv4.Write("",R.TObject.kOverwrite)
hFile.Close()
