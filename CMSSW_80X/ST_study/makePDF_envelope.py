import ROOT
import numpy
ROOT.TH1.AddDirectory(ROOT.kFALSE)

Dir   ="./ntuples/saved_hist/Step2_0805/"
Dir_SS="./ntuples/saved_hist/Step2_SameSign_0805/"


f_nominal=ROOT.TFile(Dir+"emu_nominal_.root","read")

hist_list=[]
for ih in range(0,f_nominal.GetListOfKeys().GetSize()):
    hname=f_nominal.GetListOfKeys()[ih].GetName()
    if "TTTo2L2Nu" in hname and type(f_nominal.Get(hname)) == ROOT.TH1D:
        hist_list.append(hname)
f_nominal.Close()
print hist_list
for idir in [Dir,Dir_SS]:
    #for chan in ["ee","emu","mumu"]:
    for chan in ["ee","mumu"]:
        print idir+chan
        f_up  =ROOT.TFile("%s%s_TT_PDF_Up_.root"  %(idir,chan),"RECREATE")
        f_down=ROOT.TFile("%s%s_TT_PDF_Down_.root"%(idir,chan),"RECREATE")
        ############## save TTbar hist ########################
        for hname in hist_list:
            tmp_list=[]
            for i in range(2001,2103):
                f_tmp=ROOT.TFile("%s%s_TT_PDF_%s_.root"%(idir,chan,i),"read")
                tmp_name=hname.replace("nominal","TT_PDF_%s"%str(i))
                tmp_list.append(f_tmp.Get(tmp_name))
                f_tmp.Close()
            hname_up  =hname.replace("nominal","TT_PDF_Up")
            hname_down=hname.replace("nominal","TT_PDF_Down")
            hist_up  =tmp_list[0].Clone(hname_up)
            hist_down=tmp_list[0].Clone(hname_down)
            for ibin in range(1,hist_up.GetNbinsX()+1):
                list_value=[]
                for ihist in tmp_list:
                    list_value.append(ihist.GetBinContent(ibin))
                down_up=numpy.percentile(list_value,[15.865,84.135])
                hist_down.SetBinContent(ibin,down_up[0]) 
                hist_up  .SetBinContent(ibin,down_up[1]) 
            f_up.cd()
            hist_up.Write()
            f_down.cd()
            hist_down.Write()
         #### save other hist #####################3#########
        f_nom=ROOT.TFile("%s%s_nominal_.root"%(idir,chan),"read")
        for ih in range(0,f_nom.GetListOfKeys().GetSize()):
            hname=f_nom.GetListOfKeys()[ih].GetName()
            if "TTTo2L2Nu" in hname:continue
            hist_name=str(hname)
            up_name  =hist_name.replace("nominal","TT_PDF_Up"  )
            down_name=hist_name.replace("nominal","TT_PDF_Down")
            f_up.cd()
            f_nom.Get(hname).Write(up_name)
            f_down.cd()
            f_nom.Get(hname).Write(down_name)
        f_up.Close()
        f_down.Close()

print "created TT PDF up and down file"
