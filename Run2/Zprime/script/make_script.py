import math
import datetime

import ROOT
import os
path_script="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/script/sub_script/"
path_exc   ="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/script/"
#Year = "2016"
#Year = "2017"
Year = "2018"
Run = "Run_all"
uncertainty=["nominal"]
uncertainty.append("PU_scale_up"          )             
uncertainty.append("PU_scale_down"        )           
uncertainty.append("BB_mass_scale_up"     )  
uncertainty.append("BB_mass_scale_down"   )
uncertainty.append("BE_mass_scale_up"     )  
uncertainty.append("BE_mass_scale_down"   )
uncertainty.append("Barrel_SF_scale_up"   )  
uncertainty.append("Barrel_SF_scale_down" )
uncertainty.append("Endcap_SF_scale_up"   )  
uncertainty.append("Endcap_SF_scale_down" )
uncertainty.append("pdf_scale_up"         )
uncertainty.append("pdf_scale_down"       )
if Year=="2016" or Year=="2017":
    uncertainty.append("pf_scale_up"          )
    uncertainty.append("pf_scale_down"        )


for uncer in uncertainty:
    f1 = open(path_script+"script_"+uncer+"_"+Year+".py",'w') 
    f1.write("import os \n")
    f1.write("import ROOT \n")
    f1.write('ROOT.gSystem.Load("'+path_exc+'select_and_save_C.so") \n')
    f1.write("ROOT.gROOT.ProcessLine('select_and_save("+'"'+Year+'"'+","+'"'+uncer+'"'+","+'"'+Run+'"'+")') \n")
    f1.write("print 'Done!'")
    f1.close()

    f2 = open(path_script+"script_"+uncer+"_"+Year+".sh",'w') 
    f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_10_2_13/src")
    f2.write("\n")
    f2.write("eval `scramv1 runtime -sh`")
    f2.write("\n")
    f2.write("python "+path_script+"script_"+uncer+"_"+Year+".py")
    f2.close()
print "done"
