import math
import datetime

import ROOT
import os
path_script="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/script_select/script/"
path_exc   ="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/script_select/"
channel=[]
channel.append("ee")
channel.append("emu")
channel.append("mumu")

uncertainty=["nominal"]
uncertainty.append("PU_scale_up")         
uncertainty.append("PU_scale_down")       
uncertainty.append("SmearedJetResUp")     
uncertainty.append("SmearedJetResDown")   
uncertainty.append("JetEnUp")             
uncertainty.append("JetEnDown")           
uncertainty.append("BtagSFbcUp")          
uncertainty.append("BtagSFbcDown")        
uncertainty.append("BtagSFudsgUp")        
uncertainty.append("BtagSFudsgDown")      
uncertainty.append("T1JetEnUp")           
uncertainty.append("T1JetEnDown")         
uncertainty.append("EleSFReco_up")        
uncertainty.append("EleSFReco_down")      
uncertainty.append("EleSFID_up")          
uncertainty.append("EleSFID_down")        
uncertainty.append("MuonSFID_up")         
uncertainty.append("MuonSFID_down")       
uncertainty.append("MuonSFIso_up")        
uncertainty.append("MuonSFIso_down")      
uncertainty.append("MuonSFtrack_up")      
uncertainty.append("MuonSFtrack_down")    
uncertainty.append("TrigSF_up")    
uncertainty.append("TrigSF_down")    
uncertainty.append("UnclusteredEnUp")    
uncertainty.append("UnclusteredEnDown")    
############## TT PDF uncertainty ################
for ip in range(2001,2103):
    uncertainty.append("TT_PDF_%s"%(str(ip)))    

########## Systematic sample ##############
uncertainty.append("TT_TuneEE5C"          )
uncertainty.append("TT_TuneCUETP8M2T4down")
uncertainty.append("TT_TuneCUETP8M2T4up"  )
uncertainty.append("TT_fsrdown"           )
uncertainty.append("TT_fsrup"             )
uncertainty.append("TT_hdampDOWN"         )
uncertainty.append("TT_hdampUP"           )
uncertainty.append("TT_isrdown"           )
uncertainty.append("TT_isrup"             )
uncertainty.append("TT_mtop1695"          )
uncertainty.append("TT_mtop1755"          )
uncertainty.append("TT_QCDbasedCRTune_erdON")
uncertainty.append("TT_GluonMoveCRTune"   )
uncertainty.append("TT_erdON"             )

uncertainty.append("ST_tW_herwigpp"   )
uncertainty.append("ST_tW_DS"         )
uncertainty.append("ST_tW_MEscaledown")
uncertainty.append("ST_tW_MEscaleup"  )
uncertainty.append("ST_tW_PSscaledown")
uncertainty.append("ST_tW_PSscaleup"  )
uncertainty.append("ST_tW_fsrdown"    )
uncertainty.append("ST_tW_fsrup"      )
uncertainty.append("ST_tW_isrdown"    )
uncertainty.append("ST_tW_isrup"      )
uncertainty.append("ST_tW_mtop1695"   )
uncertainty.append("ST_tW_mtop1755"   )


sign_list=["samesign","oppsign"]

for chan in channel:
    for uncer in uncertainty:
        for sname in sign_list:
            f1 = open(path_script+"script_"+chan+"_"+uncer+"_"+sname+".py",'w') 
            f1.write("import os \n")
            f1.write("import ROOT \n")
            #f1.write('ROOT.gROOT.ProcessLine(".L '+path_exc+'select_save_hist_sys.C+") \n')
            f1.write('ROOT.gSystem.Load("'+path_exc+'select_save_hist_sys_C.so") \n')
            f1.write("ROOT.gROOT.ProcessLine('select_save_hist_sys("+'"'+chan+'"'+","+'"'+uncer+'"'+","+'"'+sname+'"'+")') \n")
            f1.write("print 'Done!'")
            f1.close()

            f2 = open(path_script+"script_"+chan+"_"+uncer+"_"+sname+".sh",'w') 
            f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_8_0_25/src")
            f2.write("\n")
            f2.write("eval `scramv1 runtime -sh`")
            f2.write("\n")
            f2.write("python "+path_script+"script_"+chan+"_"+uncer+"_"+sname+".py")
            f2.close()
print "done"
