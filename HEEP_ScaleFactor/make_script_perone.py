import math
import datetime

import ROOT
import os


#ROOT.gSystem.Load("./reskim_MC_C.so")
#
#
#ch_WW = ROOT.TChain("IIHEAnalysis") 
#ch_WW.Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/crab_WW/161121_151603/0000/outfile_1.root") 
#
#reskim_WW=ROOT.reskim(ch_WW, False, False, False, False) 
#reskim_WW.Loop("ntuples/reskim/MC_newTrkIso/WW_test_1.root") 


str_import=["import os","import ROOT"]

#str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_so/reskim_C.so'"')"
#str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_so/reskim_C_ACLiC_dict_rdict.pcm'"')"
#
str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_FR_so/reskim_C.so'"')"
str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_FR_so/reskim_C_ACLiC_dict_rdict.pcm'"')"

#dir_out_put="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/reMiniAOD/"
#path_script="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/script_perone/"
dir_out_put="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_FR_out_perone/reMiniAOD/"
path_script="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/script_perone_FR/"

Ele27WPloose_trigger={}
Ele27WPloose_trigger["v2"]=["273158","273730"]
Ele27WPloose_trigger["v3"]=["274094","275066"]
Ele27WPloose_trigger["v4"]=["275067","275311"]
Ele27WPloose_trigger["v5"]=["275319","276834"]
Ele27WPloose_trigger["v6"]=["276870","278240"]
Ele27WPloose_trigger["v7"]=["278273","280385"]
Ele27WPloose_trigger["v8"]=["281613","284044"]#prescaled 250

Ele27WPtight_trigger={}
Ele27WPtight_trigger["Ele27WPTight_v2to8"]=["273158" , "284044"]


data_run_range={}
data_run_range["RunB"]=["273150","275376"]
data_run_range["RunC"]=["275656","276283"]
data_run_range["RunD"]=["276315","276811"]
data_run_range["RunE"]=["276831","277420"]
data_run_range["RunF"]=["277932","278808"]
data_run_range["RunG"]=["278820","280385"]
data_run_range["RunHv2"]=["281207","284035"]
data_run_range["RunHv3"]=["284036","284068"]




class run_obj:
    def __init__(self, name, isData,isZToTT, run, file_path, trigger, use_trigger, do_FR, is_file_path_txt):
        self.name=name
        self.isData=isData
        self.isZToTT=isZToTT
        self.run=run
        self.file_path=file_path
        self.trigger=trigger
        self.trigger_used={}
        self.use_trigger=use_trigger
        self.do_FR=do_FR
        self.is_file_path_txt=is_file_path_txt
    #def get_version(self, self.isData, self.run, self.trigger, self.trigger_use):
    def get_version(self):
        if self.use_trigger == False:
            return
        run_min=data_run_range[self.run][0]
        run_max=data_run_range[self.run][1]
        for i in self.trigger:
            run_range_min=0
            run_range_max=0
            trigger_min=self.trigger[i][0]
            trigger_max=self.trigger[i][1]
            #if (int(trigger_max) < int(run_min)) || (int(run_max) < int(trigger_min)):
            if (int(trigger_max) < int(run_min)) or (int(run_max) < int(trigger_min)):
                continue
            else:
                if int(trigger_max) <= int(run_max) and int(trigger_min) >= int(run_min):
                    run_range_min=int(trigger_min)
                    run_range_max=int(trigger_max)
                elif int(trigger_max) <= int(run_max) and int(trigger_min) < int(run_min):
                    run_range_min=int(run_min)
                    run_range_max=int(trigger_max)
                elif int(trigger_max) > int(run_max) and int(trigger_min) >= int(run_min):
                    run_range_min=int(trigger_min)
                    run_range_max=int(run_max)
                else :
                    run_range_min=int(run_min)
                    run_range_max=int(run_max)

                self.trigger_used[i]=[run_range_min,run_range_max]  

    #def creat_script(self, self.name, self.isData, self.run, self.file_path, self.trigger_use, self.use_trigger):
    def creat_script(self):
    
        if self.use_trigger==0:
            self.trigger_used["noTrig"]=[0,9999999] 
        for tr in self.trigger_used:
            if self.is_file_path_txt==1:
                    f_tmp = open(self.file_path,'r') 
                    lines=f_tmp.readlines()
                    for line_i in lines:
                        line=line_i[:-1]
                        num_1=line.split(".root")[0]
                        num=num_1.split("outfile")[-1]
                        f1 = open(path_script+self.run+"/"+"script_"+self.name+"_"+num+"_"+tr+".py",'w') 
                        for im in range(0,len(str_import)):
                            f1.write(str_import[im]) 
                            f1.write("\n")
                        f1.write(str_import_so)
                        f1.write("\n")
                        f1.write(str_import_aclic)
                        f1.write("\n")
                        f1.write("ch_"+self.name+"= ROOT.TChain('"'IIHEAnalysis'"')")
                        f1.write("\n")
                        f1.write("ch_"+self.name+".Add("'"'+line+'"'")")        
                        f1.write("\n")
                        f1.write("print '"'add file done'"'")
                        f1.write("\n")
                        f1.write("reskim_"+self.name+"=ROOT.reskim(ch_"+self.name+", True, False, False, False," +'"'+tr+'"'+","+str(self.trigger_used[tr][0])+","+ str(self.trigger_used[tr][1])+")")
                        f1.write("\n")
                        f1.write("reskim_"+self.name+".Loop("'"'+dir_out_put+self.run+"/"+self.name+"_"+num+"_"+tr+".root"'"'")") 
                        f1.write("\n")
                        f1.close()
                        
                        f2 = open(path_script+self.run+"/"+"script_"+self.name+"_"+num+"_"+tr+".sh",'w') 
                        f2.write("cd /user/wenxing/HEEP/CMSSW_7_4_10_patch2/src")
                        f2.write("\n")
                        f2.write("eval `scramv1 runtime -sh`")
                        f2.write("\n")
                        f2.write("python "+path_script+self.run+"/"+"script_"+self.name+"_"+num+"_"+tr+".py")
                        f2.close()



    def run(self):
        self.get_version()
        self.creat_script()
  
#run_data={}
Run_data=[]
########################### Data ########################################
#runB_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunB.txt"
#runB=run_obj("runB",1, 0, "RunB", runB_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runB)
#runC_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunC.txt"
#runC=run_obj("runC",1, 0, "RunC", runC_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runC)
#runD_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunD.txt"
#runD=run_obj("runD",1, 0, "RunD", runD_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runD)
#runE_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunE.txt"
#runE=run_obj("runE",1, 0, "RunE", runE_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runE)
#runF_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunF.txt"
#runF=run_obj("runF",1, 0, "RunF", runF_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runF)
#runG_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunG.txt"
#runG=run_obj("runG",1, 0, "RunG", runG_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runG)
#runHv2_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunHv2.txt"
#runHv2=run_obj("runHv2",1, 0, "RunHv2", runHv2_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runHv2)
#runHv3_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunHv3.txt"
#runHv3=run_obj("runHv3",1, 0, "RunHv3", runHv3_path,Ele27WPtight_trigger,1 ,0 ,1 )     
#Run_data.append(runHv3)



########################## Data FR ########################################
runB_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunB.txt"
runB=run_obj("runB_FR",1, 0, "RunB", runB_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runB)
runC_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunC.txt"
runC=run_obj("runC_FR",1, 0, "RunC", runC_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runC)
runD_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunD.txt"
runD=run_obj("runD_FR",1, 0, "RunD", runD_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runD)
runE_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunE.txt"
runE=run_obj("runE_FR",1, 0, "RunE", runE_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runE)
runF_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunF.txt"
runF=run_obj("runF_FR",1, 0, "RunF", runF_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runF)
runG_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunG.txt"
runG=run_obj("runG_FR",1, 0, "RunG", runG_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runG)
runHv2_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunHv2.txt"
runHv2=run_obj("runHv2_FR",1, 0, "RunHv2", runHv2_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runHv2)
runHv3_path="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/reMiniAOD/RunHv3.txt"
runHv3=run_obj("runHv3_FR",1, 0, "RunHv3", runHv3_path,Ele27WPtight_trigger,0 ,1 ,1)     
Run_data.append(runHv3)







for i_data in Run_data:
    i_data.get_version()
    i_data.creat_script()
    print "create script for %s"%(i_data.name)
    
 
