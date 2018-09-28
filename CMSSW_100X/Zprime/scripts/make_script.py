import math
import datetime

import ROOT
import os
path_script="/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/script/"
path_exc   ="/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/"

uncertainty=[]
#uncertainty.append("nominal")
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
#uncertainty.append("pdf_scale_up"         )
#uncertainty.append("pdf_scale_down"       )

pu=[]
pu.append("Rereco_all")
#pu.append("Rereco_B"  )
#pu.append("Rereco_C"  )
#pu.append("Rereco_D"  )
#pu.append("Rereco_E"  )
#pu.append("Rereco_F"  )

for uncer in uncertainty:
    for ipu in pu:
        f1 = open(path_script+"script_"+uncer+"_"+ipu+".py",'w') 
        f1.write("import os \n")
        f1.write("import ROOT \n")
        f1.write('ROOT.gSystem.Load("'+path_exc+'select_and_save_C.so") \n')
        f1.write("ROOT.gROOT.ProcessLine('select_and_save("'"'+uncer+'"'+","+'"'+ipu+'"' ")') \n")
        f1.write("print 'Done!'")
        f1.close()

        f2 = open(path_script+"script_"+uncer+"_"+ipu+".sh",'w') 
        f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_9_4_0/src")
        f2.write("\n")
        f2.write("eval `scramv1 runtime -sh`")
        f2.write("\n")
        f2.write("python "+path_script+"script_"+uncer+"_"+ipu+".py")
        f2.close()
print "done"
