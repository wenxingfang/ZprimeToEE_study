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
str_import_so=["ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/MC_so/reskim_C.so'"')", "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_so/reskim_C.so'"')","ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_FR_so/reskim_C.so'"')"]
str_import_aclic=["ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/MC_so/reskim_C_ACLiC_dict_rdict.pcm'"')", "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_so/reskim_C_ACLiC_dict_rdict.pcm'"')","ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_FR_so/reskim_C_ACLiC_dict_rdict.pcm'"')"]
dir_out_put="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/"
#dir_out_put="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out/"
path_script="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/script/"
#path_script="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/script_FR/"
#dir_out_put="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_FR_out/"

Ele27WPloose_trigger={}
Ele27WPloose_trigger["v2"]=["273158","273730"]
Ele27WPloose_trigger["v3"]=["274094","275066"]
Ele27WPloose_trigger["v4"]=["275067","275311"]
Ele27WPloose_trigger["v5"]=["275319","276834"]
Ele27WPloose_trigger["v6"]=["276870","278240"]
Ele27WPloose_trigger["v7"]=["278273","280385"]
Ele27WPloose_trigger["v8"]=["281613","284044"]#prescaled 250

Ele27WPtight_trigger={}
Ele27WPtight_trigger["v2"]=["273158" , "274442"]
Ele27WPtight_trigger["v3"]=["274954" , "275066"]
Ele27WPtight_trigger["v4"]=["275067" , "275311"]
Ele27WPtight_trigger["v5"]=["275319" , "276834"]
Ele27WPtight_trigger["v6"]=["276870" , "278240"]
Ele27WPtight_trigger["v7"]=["278273" , "280385"]
Ele27WPtight_trigger["v8"]=["281613" , "284044"] 


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
    def __init__(self, name, isData, isZToEE, isZToTT, isWJet, run, file_path, trigger, use_trigger, do_FR, is_file_path_txt):
        self.name=name
        self.isData=isData
        self.isZToTT=isZToTT
        self.isWJet=isWJet
        self.isZToEE=isZToEE
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
            f1 = open(path_script+"script_"+self.name+".py",'w') 
            for im in range(0,len(str_import)):
                f1.write(str_import[im]) 
                f1.write("\n")
            if self.do_FR==1:
                f1.write(str_import_so[2])
                f1.write("\n")
                f1.write(str_import_aclic[2])
                f1.write("\n")
            else:
                f1.write(str_import_so[self.isData])
                f1.write("\n")
                f1.write(str_import_aclic[self.isData])
                f1.write("\n")
                
            f1.write("ch_"+self.name+"= ROOT.TChain('"'IIHEAnalysis'"')")
            f1.write("\n")
            if self.is_file_path_txt ==0:
                for pa in range(0,len(self.file_path)):
                    f1.write("ch_"+self.name+".Add("'"'+self.file_path[pa]+'"'")")        
                    f1.write("\n")
            else:
                f1.write("tmp = open("+'"'+self.file_path+'"'+",'"'r'"')")
                f1.write("\n")
                f1.write("lines = tmp.readlines()")
                f1.write("\n")
                f1.write("for fi in lines:")
                f1.write("\n")
                f1.write("    fi=fi[:-1]")
                f1.write("\n")
                f1.write("    ch_"+self.name+".Add(fi)")
                f1.write("\n")
            f1.write("print '"'add file done'"'")
            f1.write("\n")
 
            reskim_list=["reskim_",self.name,"=ROOT.reskim(ch_",self.name,", False",", False",", False",", False)"]
            if self.isData==1 or self.do_FR==1:
                reskim_list[4]=", True"
            if self.isZToTT==1:
                reskim_list[6]=", True"
            if self.isWJet==1:
                reskim_list[7]=", True)"
            if self.isZToEE==1:
                reskim_list[5]=", True"
            f1.write(reskim_list[0]+reskim_list[1]+reskim_list[2]+reskim_list[3]+reskim_list[4]+reskim_list[5]+reskim_list[6]+reskim_list[7])
            f1.write("\n")
            f1.write(reskim_list[0]+self.name+".Loop("'"'+dir_out_put+self.name+".root"'"'")")
            f1.close()
             
            f2 = open(path_script+"script_"+self.name+".sh",'w') 
            f2.write("cd /user/wenxing/HEEP/CMSSW_7_4_10_patch2/src")
            f2.write("\n")
            f2.write("eval `scramv1 runtime -sh`")
            f2.write("\n")
            f2.write("python "+path_script+"script_"+self.name+".py")
            f2.close()
        if self.use_trigger==1:  ##only for data
            for tr in self.trigger_used:
                f1 = open(path_script+"script_"+self.name+tr+".py",'w') 
                for im in range(0,len(str_import)):
                    f1.write(str_import[im]) 
                    f1.write("\n")
                if self.do_FR==1:
                    f1.write(str_import_so[2])
                    f1.write("\n")
                    f1.write(str_import_aclic[2])
                    f1.write("\n")
                else:
                    f1.write(str_import_so[self.isData])
                    f1.write("\n")
                    f1.write(str_import_aclic[self.isData])
                    f1.write("\n")
                f1.write("ch_"+self.name+"= ROOT.TChain('"'IIHEAnalysis'"')")
                f1.write("\n")
                if self.is_file_path_txt==0:
                    for pa in range(0,len(self.file_path)):
                        f1.write("ch_"+self.name+".Add("'"'+self.file_path[pa]+'"'")")    
                        f1.write("\n")
                else:
                    f1.write("tmp = open("+'"'+self.file_path+'"'+",'"'r'"')")
                    f1.write("\n")
                    f1.write("lines = tmp.readlines()")
                    f1.write("\n")
                    f1.write("for fi in lines:")
                    f1.write("\n")
                    f1.write("    fi=fi[:-1]")
                    f1.write("\n")
                    f1.write("    ch_"+self.name+".Add(fi)")
                    f1.write("\n")
                f1.write("print '"'add file done'"'")
                f1.write("\n")
                tr_tmp=tr.split("v") ## [v, 8]
                f1.write("reskim_"+self.name+"=ROOT.reskim(ch_"+self.name+", True, False, False, False," +tr_tmp[-1]+","+str(self.trigger_used[tr][0])+","+ str(self.trigger_used[tr][1])+")")
                f1.write("\n")
                f1.write("reskim_"+self.name+".Loop("'"'+dir_out_put+self.name+tr+".root"'"'")") 
                f1.write("\n")
                f1.close()
                
                f2 = open(path_script+"script_"+self.name+tr+".sh",'w') 
                f2.write("cd /user/wenxing/HEEP/CMSSW_7_4_10_patch2/src")
                f2.write("\n")
                f2.write("eval `scramv1 runtime -sh`")
                f2.write("\n")
                f2.write("python "+path_script+"script_"+self.name+tr+".py")
                f2.close()



    def run(self):
        self.get_version()
        self.creat_script()
  
#run_data={}
Run_data=[]
########################### Data ########################################
#runB1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunB/0000_skimed/*.root"]
#runB1=run_obj("runB1",1, 0, 0, "RunB", runB1_path,Ele27WPtight_trigger,1 ,0 ,0 )     
#Run_data.append(runB1)
#runB2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunB/0001_skimed/*.root"]
#runB2=run_obj("runB2",1, 0, 0, "RunB", runB2_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runB2)
#runB3_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunB/0002_skimed/*.root"]
#runB3=run_obj("runB3",1, 0, 0, "RunB", runB3_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runB3)
#runB4_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunB/0003_skimed/*.root"]
#runB4=run_obj("runB4",1, 0, 0, "RunB", runB4_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runB4)
#runC1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunC/0000_skimed/*.root"]
#runC1=run_obj("runC1",1, 0, 0, "RunC", runC1_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runC1)
#runC2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunC/0001_skimed/*.root"]
#runC2=run_obj("runC2",1, 0, 0, "RunC", runC2_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runC2)
#runD1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunD/0000_skimed/*.root"]
#runD1=run_obj("runD1",1, 0, 0, "RunD", runD1_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runD1)
#runD2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunD/0001_skimed/*.root","/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunD/0002_skimed/*.root"]
#runD2=run_obj("runD2",1, 0, 0, "RunD", runD2_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runD2)
#runE1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunE/0000_skimed/*.root"]
#runE1=run_obj("runE1",1, 0, 0, "RunE", runE1_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runE1)
#runE2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunE/0001_skimed/*.root"]
#runE2=run_obj("runE2",1, 0, 0, "RunE", runE2_path,Ele27WPtight_trigger,1 ,0 ,0 )              
#Run_data.append(runE2)
#runF1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunF/0000_skimed/*.root","/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunF/0000_lumi_skimed/*.root"]
#runF1=run_obj("runF1",1, 0, 0, "RunF", runF1_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runF1)
#runF2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunF/0001_skimed/*.root"]
#runF2=run_obj("runF2",1, 0, 0, "RunF", runF2_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runF2)
#runG1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunG/0000_skimed/*.root","/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunG/0000_lumi_skimed/*.root"]
#runG1=run_obj("runG1",1, 0, 0, "RunG", runG1_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runG1)
#runG2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunG/0001_skimed/*.root"]
#runG2=run_obj("runG2",1, 0, 0, "RunG", runG2_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runG2)
#runG3_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunG/0002_skimed/*.root"]
#runG3=run_obj("runG3",1, 0, 0, "RunG", runG3_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runG3)
#runG4_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunG/0003_skimed/*.root"]
#runG4=run_obj("runG4",1, 0, 0, "RunG", runG4_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runG4)
#runHv2_1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunHv2/0000_skimed/*.root"]
#runHv2_1=run_obj("runHv2_1",1, 0, 0, "RunHv2", runHv2_1_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runHv2_1)
#runHv2_2_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunHv2/0001_skimed/*.root"]
#runHv2_2=run_obj("runHv2_2",1, 0, 0, "RunHv2", runHv2_2_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runHv2_2)
#runHv2_3_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunHv2/0002_skimed/*.root"]
#runHv2_3=run_obj("runHv2_3",1, 0, 0, "RunHv2", runHv2_3_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runHv2_3)
#runHv2_4_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunHv2/0003_skimed/*.root"]
#runHv2_4=run_obj("runHv2_4",1, 0, 0, "RunHv2", runHv2_4_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runHv2_4)
#runHv3_1_path=["/pnfs/iihe/cms/store/user/wenxing/SingleElectron_skimed/RunHv3/0000_skimed/*.root"]
#runHv3_1=run_obj("runHv3_1",1, 0, 0, "RunHv3", runHv3_1_path,Ele27WPtight_trigger,1 ,0 ,0 )               
#Run_data.append(runHv3_1)



########################## Data FR ########################################
#runB1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunB_1.txt"
#runB1_FR=run_obj("runB1_FR",1, 0, 0,  "RunB", runB1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )     
#Run_data.append(runB1_FR)
#runB2_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunB_2.txt"
#runB2_FR=run_obj("runB2_FR",1, 0, 0,  "RunB", runB2_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runB2_FR)
#runB3_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunB_3.txt"
#runB3_FR=run_obj("runB3_FR",1, 0, 0,  "RunB", runB3_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runB3_FR)
#runB4_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunB_4.txt"
#runB4_FR=run_obj("runB4_FR",1, 0, 0,  "RunB", runB4_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runB4_FR)
#runC1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunC_1.txt"
#runC1_FR=run_obj("runC1_FR",1, 0, 0,  "RunC", runC1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runC1_FR)
#runD1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunD_1.txt"
#runD1_FR=run_obj("runD1_FR",1, 0, 0,  "RunD", runD1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runD1_FR)
#runD2_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunD_2.txt"
#runD2_FR=run_obj("runD2_FR",1, 0, 0,  "RunD", runD2_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runD2_FR)
#runE1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunE_1.txt"
#runE1_FR=run_obj("runE1_FR",1, 0, 0,  "RunE", runE1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runE1_FR)
#runE2_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunE_2.txt"
#runE2_FR=run_obj("runE2_FR",1, 0, 0,  "RunE", runE2_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )              
#Run_data.append(runE2_FR)
#runF1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunF_1.txt"
#runF1_FR=run_obj("runF1_FR",1, 0, 0,  "RunF", runF1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runF1_FR)
#runG1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunG_1.txt"
#runG1_FR=run_obj("runG1_FR",1, 0, 0,  "RunG", runG1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runG1_FR)
#runG2_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunG_2.txt"
#runG2_FR=run_obj("runG2_FR",1, 0, 0,  "RunG", runG2_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runG2_FR)
#runG3_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunG_3.txt"
#runG3_FR=run_obj("runG3_FR",1, 0, 0,  "RunG", runG3_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runG3_FR)
#runHv2_1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunHv2_1.txt"
#runHv2_1_FR=run_obj("runHv2_1_FR",1, 0, 0,  "RunHv2", runHv2_1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )            
#Run_data.append(runHv2_1_FR)
#runHv2_2_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunHv2_2.txt"
#runHv2_2_FR=run_obj("runHv2_2_FR",1, 0, 0,  "RunHv2", runHv2_2_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )            
#Run_data.append(runHv2_2_FR)
#runHv2_3_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunHv2_3.txt"
#runHv2_3_FR=run_obj("runHv2_3_FR",1, 0, 0,  "RunHv2", runHv2_3_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runHv2_3_FR)
#runHv3_1_path_FR="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/data_list/Double_RunHv3_1.txt"
#runHv3_1_FR=run_obj("runHv3_1_FR",1, 0, 0,  "RunHv3", runHv3_1_path_FR,Ele27WPtight_trigger,0 ,1 ,1 )               
#Run_data.append(runHv3_1_FR)



################################## MC ########################################

#DYToEE_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYToEE_NNPDF30_13TeV-powheg-pythia8/crab_DYToEE_NNPDF30_13TeV-powheg_MiniAOD/170120_105508/0000/*.root"]
#DYToEE_1=run_obj("DYToEE",0, 0, 0, 0, "", DYToEE_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_1)
#DY_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170117_095012/0000/*.root"]
#DY_1=run_obj("DYToLL",0, 0, 1, 0, "", DY_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DY_1)
DYToEE_amc_11_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_122606/0000/*.root"]
DYToEE_amc_11=run_obj("DYToEE_amc_pt100_new_1",0, 1, 1, 0, "", DYToEE_amc_11_path,Ele27WPtight_trigger,0 ,0 ,0 )               
Run_data.append(DYToEE_amc_11)
DYToEE_amc_12_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_122606/0001/*.root"]
DYToEE_amc_12=run_obj("DYToEE_amc_pt100_new_2",0, 1, 1, 0, "", DYToEE_amc_12_path,Ele27WPtight_trigger,0 ,0 ,0 )               
Run_data.append(DYToEE_amc_12)
#DYToEE_amc_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_122606/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_122606/0001/*.root"]
#DYToEE_amc_1=run_obj("DYToEE_amc_pt50_new",0, 1, 1, 0, "", DYToEE_amc_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_1)
#DYToEE_amc_2_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_114013/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext3/170221_122143/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext3/170221_122143/0001/*.root"]
#DYToEE_amc_2=run_obj("DYToEE_amc_pt50_100",0, 0, 1, 0, "", DYToEE_amc_2_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_2)
#DYToEE_amc_3_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_121251/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext1/170221_120413/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext2/170221_120826/0000/*.root"]
#DYToEE_amc_3=run_obj("DYToEE_amc_pt100_250_1",0, 0, 1, 0, "", DYToEE_amc_3_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_3)
#DYToEE_amc_4_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext5/170221_115220/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext5/170221_115220/0001/*.root"]
#DYToEE_amc_4=run_obj("DYToEE_amc_pt100_250_2",0, 0, 1, 0, "", DYToEE_amc_4_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_4)
#DYToEE_amc_5_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_121720/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext1/170221_112625/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext2/170221_112235/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext5/170221_113320/0000/*.root"]
#DYToEE_amc_5=run_obj("DYToEE_amc_pt250_400",0, 0, 1, 0, "", DYToEE_amc_5_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_5)
#DYToEE_amc_6_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_113642/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext1/170221_120020/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext2/170221_114409/0000/*.root"]
#DYToEE_amc_6=run_obj("DYToEE_amc_pt400_650",0, 0, 1, 0, "", DYToEE_amc_6_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_6)
#DYToEE_amc_7_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_115614/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext1/170221_114848/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD_ext2/170221_112957/0000/*.root"]
#DYToEE_amc_7=run_obj("DYToEE_amc_pt650_Inf",0, 0, 1, 0, "", DYToEE_amc_7_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToEE_amc_7)
#DYToLL_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170117_095012/0000/*.root"]
#DYToLL=run_obj("DYToEE_mad_Zpt100_new",0, 1, 1, 0, "", DYToLL_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToLL)
#DYToLL_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170202_110216/0000/*.root"]
#DYToLL_1=run_obj("DYToEE_mad_Zpt100_200",0, 0, 1, 0, "", DYToLL_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToLL_1)
#DYToLL_2_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170202_105926/0000/*.root"]
#DYToLL_2=run_obj("DYToEE_mad_Zpt200_Inf",0, 0, 1, 0, "", DYToLL_2_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(DYToLL_2)
#WJet_amc_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_201901/0000/*.root"]
#WJet_amc_1=run_obj("WJet_amc_pt_100_new",0, 0, 0, 1, "", WJet_amc_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_amc_1)
#WJet_amc_2_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_201529/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext1/170220_200840/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext4/170220_195821/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext4/170220_195821/0001/*.root"]
#WJet_amc_2=run_obj("WJet_amc_pt_100_250",0, 0, 0, 0, "", WJet_amc_2_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_amc_2)
#WJet_amc_3_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_194838/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext1/170220_201202/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext4/170220_200145/0000/*.root"]
#WJet_amc_3=run_obj("WJet_amc_pt_250_400",0, 0, 0, 0, "", WJet_amc_3_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_amc_3)
#WJet_amc_4_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_195159/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext1/170220_194530/0000/*.root"]
#WJet_amc_4=run_obj("WJet_amc_pt_400_600",0, 0, 0, 0, "", WJet_amc_4_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_amc_4)
#WJet_amc_5_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_195510/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD_ext1/170220_200518/0000/*.root"]
#WJet_amc_5=run_obj("WJet_amc_pt_600_Inf",0, 0, 0, 0, "", WJet_amc_5_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_amc_5)
#WJet_mad_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170117_094833/0000/*.root"]
#WJet_mad_1=run_obj("WJet_mad_1",0, 0, 0, 0, "", WJet_mad_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_mad_1)
#WJet_mad_2_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170117_094833/ext2/*.root"]
#WJet_mad_2=run_obj("WJet_mad_2",0, 0, 0, 0, "", WJet_mad_2_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WJet_mad_2)
#WW_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/WW_TuneCUETP8M1_13TeV-pythia8/crab_WW/170116_152440/0000/*.root"]
#WW=run_obj("WW",0, 0, 0, 0, "", WW_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WW)
#WZ_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/WZ_TuneCUETP8M1_13TeV-pythia8/crab_WZ/170116_152416/0000/*.root"]
#WZ=run_obj("WZ",0, 0, 0, 0, "", WZ_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(WZ)
#ZZ_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/ZZ_TuneCUETP8M1_13TeV-pythia8/crab_ZZ/170116_152158/0000/*.root"]
#ZZ=run_obj("ZZ",0, 0, 0, 0, "", ZZ_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(ZZ)
#ST_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/crab_ST_top/170116_152222/0000/*.root"]
#ST=run_obj("ST",0, 0, 0, 0, "", ST_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(ST)
#ST_anti_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/crab_ST_antitop/170116_152655/0000/*.root"]
#ST_anti=run_obj("ST_anti",0, 0, 0, 0, "", ST_anti_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(ST_anti)
#GJ_1_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_40To100_ext/170116_152502/0000/*.root"]
#GJ_1=run_obj("GJ_40To100",0, 0, 0, 0, "", GJ_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_1)
#GJ_12_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_40To100/170119_143957/0000/*.root"]
#GJ_12=run_obj("GJ_40To100_ext",0, 0, 0, 0, "", GJ_12_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_12)
#GJ_21_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_100To200/170116_152353/0000/*.root"]
#GJ_21=run_obj("GJ_100To200_1",0, 0, 0, 0, "", GJ_21_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_21)
#GJ_22_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_100To200_ext/170116_152245/0000/*.root"]
#GJ_22=run_obj("GJ_100To200_2",0, 0, 0, 0, "", GJ_22_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_22)
#GJ_3_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_200To400_ext/170116_152133/0000/*.root"]
#GJ_3=run_obj("GJ_200To400",0, 0, 0, 0, "", GJ_3_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_3)
#GJ_41_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_400To600/170116_152331/0000/*.root"]
#GJ_41=run_obj("GJ_400To600_1",0, 0, 0, 0, "", GJ_41_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_41)
#GJ_42_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_400To600_ext/170116_152633/0000/*.root"]
#GJ_42=run_obj("GJ_400To600_2",0, 0, 0, 0, "", GJ_42_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_42)
#GJ_51_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_600ToInf/170116_152743/0000/*.root"]
#GJ_51=run_obj("GJ_600ToInf_1",0, 0, 0, 0, "", GJ_51_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_51)
#GJ_52_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/MINIAOD/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_600ToInf_ext/170116_152104/0000/*.root"]
#GJ_52=run_obj("GJ_600ToInf_2",0, 0, 0, 0, "", GJ_52_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(GJ_52)
#TT_1_path=["/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_13TeV-powheg-MiniAOD/170117_094909/0000/*.root"]
#TT_1=run_obj("TTbar",0, 0, 0, 0, "", TT_1_path,Ele27WPtight_trigger,0 ,0 ,0 )               
#Run_data.append(TT_1)



for i_data in Run_data:
    i_data.get_version()
    i_data.creat_script()
    print "create script for %s"%(i_data.name)
    
 
