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

#dataset="DoubleEG"
#dataset="DoubleMuon"
#dataset="MuonEG"
#dataset="SingleElectron"
#dataset="SingleMuon"
#dataset="MET"
dataset="MC"

str_import=["import os","import ROOT"]
str_import_so=["ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc/reskim_C.so'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_1F/reskim_FR_1F_C.so'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_2F/reskim_FR_2F_C.so'"')"]
str_import_aclic=["ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc/reskim_C_ACLiC_dict_rdict.pcm'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_1F/reskim_FR_1F_C_ACLiC_dict_rdict.pcm'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_2F/reskim_FR_2F_C_ACLiC_dict_rdict.pcm'"')"]
dir_out_put="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/reskim_out/normal_perone/reMiniAOD/"+dataset+"/"
path_script="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/script_perone/reMiniAOD/"+dataset+"/"

Ele27_trigger={}
Ele27_trigger["v2"]=["273158","273730"]
Ele27_trigger["v3"]=["274094","275066"]
Ele27_trigger["v4"]=["275067","275311"]
Ele27_trigger["v5"]=["275319","276834"]
Ele27_trigger["v6"]=["276870","278240"]
Ele27_trigger["v7"]=["278273","280385"]
Ele27_trigger["v8"]=["281613","284044"]

Ele33_trigger={}
Ele33_trigger["DoubleEle33_CaloIdL_MW_v1234"]=["273158","276437"]
Ele33_trigger["DoubleEle33_CaloIdL_GsfTrkIdVL_v678"]=["276454","278822"]
Ele33_trigger["DoubleEle33_CaloIdL_MW_v78"]=["278873","284044"]

Ele23_Ele12_trigger={}
Ele23_Ele12_trigger["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]=["273158","284044"]


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
    def __init__(self, name, isData, isTTbar, isZToTT, isWW,run, file_path, trigger, use_trigger, is_file_path_txt, do_FR_1F, do_FR_2F):
        self.name=name
        self.isData=isData
        self.isZToTT=isZToTT
        self.isTTbar=isTTbar
        self.isWW=isWW
        self.run=run
        self.file_path=file_path
        self.trigger=trigger
        self.trigger_used={}
        self.use_trigger=use_trigger
        self.is_file_path_txt=is_file_path_txt
        self.do_FR_1F=do_FR_1F
        self.do_FR_2F=do_FR_2F
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
            self.trigger_used["wo_trig"]=[0,9999999] 
        for tr in self.trigger_used:
            if self.is_file_path_txt ==1:
                f_in = open(self.file_path,'r') 
                f_list=f_in.readlines()
                tmp_num=0
                for fi in f_list:
                    fi=fi[:-1]
                    str_tmp=fi.split(".root")
                    str_num=""
                    if "outfile" in str_tmp[0]:
                        str_num=str_tmp[0].split("outfile")
                    elif "out_file" in str_tmp[0]:
                        str_num=str_tmp[0].split("out_file")
                    else:print "wrong name"
                    #fi_num=str_num[-1]
                    tmp_num=tmp_num+1
                    fi_num=str(tmp_num)
                    f1 = open(path_script+self.run+"/"+"script_"+self.name+"_"+fi_num+"_"+tr+".py",'w') 
                    for im in range(0,len(str_import)):
                        f1.write(str_import[im]) 
                        f1.write("\n")
                    if  self.do_FR_1F ==0 and  self.do_FR_2F==0:
                        f1.write(str_import_so[0])
                        f1.write("\n")
                        f1.write(str_import_aclic[0])
                        f1.write("\n")
                    elif  self.do_FR_1F ==1 and  self.do_FR_2F==0:
                        f1.write(str_import_so[1])
                        f1.write("\n")
                        f1.write(str_import_aclic[1])
                        f1.write("\n")
                    else:
                        f1.write(str_import_so[2])
                        f1.write("\n")
                        f1.write(str_import_aclic[2])
                        f1.write("\n")
                    f1.write("ch_"+self.name+"= ROOT.TChain('"'IIHEAnalysis'"')")
                    f1.write("\n")
                    f1.write("ch_"+self.name+".Add("'"'+fi+'"'")")        
                    f1.write("\n")
                    f1.write("print '"'add file done'"'")
                    f1.write("\n")
                    reskim_list=["reskim_",self.name,"=ROOT.reskim(ch_",self.name,", False",", False",", False",", False,",'"'+tr+'"'+",", str(self.trigger_used[tr][0])+",",str(self.trigger_used[tr][1])+")"]
                    if self.do_FR_1F==1:
                        reskim_list[0]="reskim_FR_1F_"
                        reskim_list[2]="=ROOT.reskim_FR_1F(ch_"
                    if self.do_FR_2F==1:
                        reskim_list[0]="reskim_FR_2F_"
                        reskim_list[2]="=ROOT.reskim_FR_2F(ch_"
                    if self.isData==1:
                        reskim_list[4]=", True"
                    if self.isTTbar==1:
                        reskim_list[5]=", True"
                    if self.isZToTT==1:
                        reskim_list[6]=", True"
                    if self.isWW==1:
                        reskim_list[7]=", True,"
                    
                    f1.write(reskim_list[0]+reskim_list[1]+reskim_list[2]+reskim_list[3]+reskim_list[4]+reskim_list[5]+reskim_list[6]+reskim_list[7]+reskim_list[8]+reskim_list[9]+reskim_list[10])
                    f1.write("\n")
                    f1.write(reskim_list[0]+self.name+".Loop("'"'+dir_out_put+self.run+"/"+self.name+"_"+fi_num+"_"+tr+".root"'"'")") 
                    f1.write("\n")
                    f1.close()
                    
                    f2 = open(path_script+self.run+"/"+"script_"+self.name+"_"+fi_num+"_"+tr+".sh",'w') 
                    f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_8_0_25/src")
                    f2.write("\n")
                    f2.write("eval `scramv1 runtime -sh`")
                    f2.write("\n")
                    f2.write("python "+path_script+self.run+"/"+"script_"+self.name+"_"+fi_num+"_"+tr+".py")
                    f2.close()



    def run(self):
        self.get_version()
        self.creat_script()
  
#run_data={}
Run_data=[]
########################### Data ########################################
#runB_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunB.txt"
#runB=run_obj("runB",1, 0, 0, 0, "RunB", runB_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runB)
#runC_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunC.txt"
#runC=run_obj("runC",1, 0, 0, 0, "RunC", runC_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runC)
#runD_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunD.txt"
#runD=run_obj("runD",1, 0, 0, 0, "RunD", runD_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runD)
#runE_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunE.txt"
#runE=run_obj("runE",1, 0, 0, 0, "RunE", runE_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runE)
#runF_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunF.txt"
#runF=run_obj("runF",1, 0, 0, 0, "RunF", runF_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runF)
#runG_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunG.txt"
#runG=run_obj("runG",1, 0, 0, 0, "RunG", runG_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runG)
#runHv2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunHv2.txt"
#runHv2=run_obj("runHv2",1, 0, 0, 0, "RunHv2", runHv2_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runHv2)
#runHv3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/RunHv3.txt"
#runHv3=run_obj("runHv3",1, 0, 0, 0, "RunHv3", runHv3_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(runHv3)

###################### MC ##########################################

#################### For tw ###########################
TTTo2L2Nu_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TTTo2L2Nu.txt"
TTTo2L2Nu=run_obj("TTTo2L2Nu",0, 0, 0, 0, "mc_all", TTTo2L2Nu_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TTTo2L2Nu)
#------------- TT inclusive ------------------
#TT_inclusive_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_inclusive.txt"
#TT_inclusive=run_obj("TT_inclusive",0, 0, 0, 0, "mc_all", TT_inclusive_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TT_inclusive)

#DYJetsToLL_M10to50_amc_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M10to50_amc.txt"
#DYJetsToLL_M10to50_amc=run_obj("DYJetsToLL_M10to50_amc",0, 0, 0, 0, "mc_all", DYJetsToLL_M10to50_amc_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M10to50_amc)
#DYJetsToLL_M50_amc_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc.txt"
#DYJetsToLL_M50_amc=run_obj("DYJetsToLL_M50_amc",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc)
#
#WJet_mad_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/WJet_mad.txt"
#WJet_mad=run_obj("WJet_mad",0, 0, 0, 0, "mc_all", WJet_mad_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(WJet_mad)
#
#TTJets_Dilept_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TTJets_Dilept.txt"
#TTJets_Dilept=run_obj("TTJets_Dilept",0, 0, 0, 0, "mc_all", TTJets_Dilept_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TTJets_Dilept)
#TTJets_Dilept_ext1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TTJets_Dilept_ext1.txt"
#TTJets_Dilept_ext1=run_obj("TTJets_Dilept_ext1",0, 0, 0, 0, "mc_all", TTJets_Dilept_ext1_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TTJets_Dilept_ext1)
#
#TTJets_madgraph_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TTJets_madgraph.txt"
#TTJets_madgraph=run_obj("TTJets_madgraph",0, 0, 0, 0, "mc_all", TTJets_madgraph_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TTJets_madgraph)

#
#DYJetsToLL_M10to50_mad_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M10to50_mad.txt"
#DYJetsToLL_M10to50_mad=run_obj("DYJetsToLL_M10to50_mad",0, 0, 0, 0, "mc_all", DYJetsToLL_M10to50_mad_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M10to50_mad)
#DYJetsToLL_M50_mad_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_mad.txt"
#DYJetsToLL_M50_mad=run_obj("DYJetsToLL_M50_mad",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_mad_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_mad)
#
#DYToEE_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYToEE.txt"
#DYToEE=run_obj("DYToEE",0, 0, 0, 0, "mc_all", DYToEE_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYToEE)
#++++++++++++++++ DY PDF Qscale uncertainty ++++++++++++++++++++++++++++++++++++
#DYJetsToLL_M10to50_amc_LHE1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M10to50_amc_LHE1.txt"
#DYJetsToLL_M10to50_amc_LHE1=run_obj("DYJetsToLL_M10to50_amc_LHE1",0, 0, 0, 0, "mc_all", DYJetsToLL_M10to50_amc_LHE1_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M10to50_amc_LHE1)
#DYJetsToLL_M10to50_amc_LHE2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M10to50_amc_LHE2.txt"
#DYJetsToLL_M10to50_amc_LHE2=run_obj("DYJetsToLL_M10to50_amc_LHE2",0, 0, 0, 0, "mc_all", DYJetsToLL_M10to50_amc_LHE2_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M10to50_amc_LHE2)
#DYJetsToLL_M10to50_amc_LHE3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M10to50_amc_LHE3.txt"
#DYJetsToLL_M10to50_amc_LHE3=run_obj("DYJetsToLL_M10to50_amc_LHE3",0, 0, 0, 0, "mc_all", DYJetsToLL_M10to50_amc_LHE3_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M10to50_amc_LHE3)
#DYJetsToLL_M50_amc_LHE1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE1.txt"
#DYJetsToLL_M50_amc_LHE1=run_obj("DYJetsToLL_M50_amc_LHE1",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE1_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE1)
#DYJetsToLL_M50_amc_LHE2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE2.txt"
#DYJetsToLL_M50_amc_LHE2=run_obj("DYJetsToLL_M50_amc_LHE2",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE2_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE2)
#DYJetsToLL_M50_amc_LHE3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE3.txt"
#DYJetsToLL_M50_amc_LHE3=run_obj("DYJetsToLL_M50_amc_LHE3",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE3_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE3)
#DYJetsToLL_M50_amc_LHE4_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE4.txt"
#DYJetsToLL_M50_amc_LHE4=run_obj("DYJetsToLL_M50_amc_LHE4",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE4_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE4)
#DYJetsToLL_M50_amc_LHE5_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE5.txt"
#DYJetsToLL_M50_amc_LHE5=run_obj("DYJetsToLL_M50_amc_LHE5",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE5_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE5)
#DYJetsToLL_M50_amc_LHE6_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE6.txt"
#DYJetsToLL_M50_amc_LHE6=run_obj("DYJetsToLL_M50_amc_LHE6",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE6_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE6)
#DYJetsToLL_M50_amc_LHE7_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/DYJetsToLL_M50_amc_LHE7.txt"
#DYJetsToLL_M50_amc_LHE7=run_obj("DYJetsToLL_M50_amc_LHE7",0, 0, 0, 0, "mc_all", DYJetsToLL_M50_amc_LHE7_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(DYJetsToLL_M50_amc_LHE7)
##################### For tw: TT system samples ###########################
###++++++++++++++++ PDF uncertainty ++++++++++++++++++++++++++++++++++++
TT_PDF_To2L2Nu_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_PDF_To2L2Nu.txt"
TT_PDF_To2L2Nu=run_obj("TT_PDF_To2L2Nu",0, 0, 0, 0, "mc_all", TT_PDF_To2L2Nu_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_PDF_To2L2Nu)
###++++++++++++++++ other uncertainty ++++++++++++++++++++++++++++++++++++
#TT_TuneEE5C_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_TuneEE5C.txt"
#TT_TuneEE5C=run_obj("TT_TuneEE5C",0, 0, 0, 0, "mc_all", TT_TuneEE5C_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TT_TuneEE5C)
TT_TuneCUETP8M2T4down_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_TuneCUETP8M2T4down.txt"
TT_TuneCUETP8M2T4down=run_obj("TT_TuneCUETP8M2T4down",0, 0, 0, 0, "mc_all", TT_TuneCUETP8M2T4down_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_TuneCUETP8M2T4down)
TT_TuneCUETP8M2T4up_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_TuneCUETP8M2T4up.txt"
TT_TuneCUETP8M2T4up=run_obj("TT_TuneCUETP8M2T4up",0, 0, 0, 0, "mc_all", TT_TuneCUETP8M2T4up_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_TuneCUETP8M2T4up)
#TT_colourFlip_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_colourFlip.txt"
#TT_colourFlip=run_obj("TT_colourFlip",0, 0, 0, 0, "mc_all", TT_colourFlip_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TT_colourFlip)
TT_fsrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_fsrdown.txt"
TT_fsrdown=run_obj("TT_fsrdown",0, 0, 0, 0, "mc_all", TT_fsrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_fsrdown)
TT_fsrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_fsrup.txt"
TT_fsrup=run_obj("TT_fsrup",0, 0, 0, 0, "mc_all", TT_fsrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_fsrup)
TT_hdampDOWN_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_hdampDOWN.txt"
TT_hdampDOWN=run_obj("TT_hdampDOWN",0, 0, 0, 0, "mc_all", TT_hdampDOWN_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_hdampDOWN)
TT_hdampUP_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_hdampUP.txt"
TT_hdampUP=run_obj("TT_hdampUP",0, 0, 0, 0, "mc_all", TT_hdampUP_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_hdampUP)
TT_isrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_isrdown.txt"
TT_isrdown=run_obj("TT_isrdown",0, 0, 0, 0, "mc_all", TT_isrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_isrdown)
TT_isrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_isrup.txt"
TT_isrup=run_obj("TT_isrup",0, 0, 0, 0, "mc_all", TT_isrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_isrup)
#TT_mtop1665_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_mtop1665.txt"
#TT_mtop1665=run_obj("TT_mtop1665",0, 0, 0, 0, "mc_all", TT_mtop1665_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TT_mtop1665)
TT_mtop1695_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_mtop1695.txt"
TT_mtop1695=run_obj("TT_mtop1695",0, 0, 0, 0, "mc_all", TT_mtop1695_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_mtop1695)
TT_mtop1755_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_mtop1755.txt"
TT_mtop1755=run_obj("TT_mtop1755",0, 0, 0, 0, "mc_all", TT_mtop1755_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_mtop1755)
#TT_mtop1785_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_mtop1785.txt"
#TT_mtop1785=run_obj("TT_mtop1785",0, 0, 0, 0, "mc_all", TT_mtop1785_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TT_mtop1785)
TT_QCDbasedCRTune_erdON_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_QCDbasedCRTune_erdON.txt"
TT_QCDbasedCRTune_erdON=run_obj("TT_QCDbasedCRTune_erdON",0, 0, 0, 0, "mc_all", TT_QCDbasedCRTune_erdON_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_QCDbasedCRTune_erdON)
TT_GluonMoveCRTune_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_GluonMoveCRTune.txt"
TT_GluonMoveCRTune=run_obj("TT_GluonMoveCRTune",0, 0, 0, 0, "mc_all", TT_GluonMoveCRTune_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_GluonMoveCRTune)
TT_erdON_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TT_erdON.txt"
TT_erdON=run_obj("TT_erdON",0, 0, 0, 0, "mc_all", TT_erdON_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
Run_data.append(TT_erdON)
###################### For tw: TW system samples ###########################
#ST_tW_antitop_DS_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_DS.txt"
#ST_tW_antitop_DS=run_obj("ST_tW_antitop_DS",0, 0, 0, 0, "mc_all", ST_tW_antitop_DS_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_DS)
#ST_tW_antitop_MEscaledown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_MEscaledown.txt"
#ST_tW_antitop_MEscaledown=run_obj("ST_tW_antitop_MEscaledown",0, 0, 0, 0, "mc_all", ST_tW_antitop_MEscaledown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_MEscaledown)
#ST_tW_antitop_MEscaleup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_MEscaleup.txt"
#ST_tW_antitop_MEscaleup=run_obj("ST_tW_antitop_MEscaleup",0, 0, 0, 0, "mc_all", ST_tW_antitop_MEscaleup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_MEscaleup)
#ST_tW_antitop_PSscaledown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_PSscaledown.txt"
#ST_tW_antitop_PSscaledown=run_obj("ST_tW_antitop_PSscaledown",0, 0, 0, 0, "mc_all", ST_tW_antitop_PSscaledown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_PSscaledown)
#ST_tW_antitop_PSscaleup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_PSscaleup.txt"
#ST_tW_antitop_PSscaleup=run_obj("ST_tW_antitop_PSscaleup",0, 0, 0, 0, "mc_all", ST_tW_antitop_PSscaleup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_PSscaleup)
#ST_tW_antitop_fsrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_fsrdown.txt"
#ST_tW_antitop_fsrdown=run_obj("ST_tW_antitop_fsrdown",0, 0, 0, 0, "mc_all", ST_tW_antitop_fsrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_fsrdown)
#ST_tW_antitop_fsrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_fsrup.txt"
#ST_tW_antitop_fsrup=run_obj("ST_tW_antitop_fsrup",0, 0, 0, 0, "mc_all", ST_tW_antitop_fsrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_fsrup)
#ST_tW_antitop_herwigpp_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_herwigpp.txt"
#ST_tW_antitop_herwigpp=run_obj("ST_tW_antitop_herwigpp",0, 0, 0, 0, "mc_all", ST_tW_antitop_herwigpp_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_herwigpp)
#ST_tW_antitop_isrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_isrdown.txt"
#ST_tW_antitop_isrdown=run_obj("ST_tW_antitop_isrdown",0, 0, 0, 0, "mc_all", ST_tW_antitop_isrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_isrdown)
#ST_tW_antitop_isrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_isrup.txt"
#ST_tW_antitop_isrup=run_obj("ST_tW_antitop_isrup",0, 0, 0, 0, "mc_all", ST_tW_antitop_isrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_isrup)
#ST_tW_antitop_mtop1695_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_mtop1695.txt"
#ST_tW_antitop_mtop1695=run_obj("ST_tW_antitop_mtop1695",0, 0, 0, 0, "mc_all", ST_tW_antitop_mtop1695_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_mtop1695)
#ST_tW_antitop_mtop1755_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_antitop_mtop1755.txt"
#ST_tW_antitop_mtop1755=run_obj("ST_tW_antitop_mtop1755",0, 0, 0, 0, "mc_all", ST_tW_antitop_mtop1755_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_antitop_mtop1755)
#
#ST_tW_top_DS_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_DS.txt"
#ST_tW_top_DS=run_obj("ST_tW_top_DS",0, 0, 0, 0, "mc_all", ST_tW_top_DS_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_DS)
#ST_tW_top_MEscaledown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_MEscaledown.txt"
#ST_tW_top_MEscaledown=run_obj("ST_tW_top_MEscaledown",0, 0, 0, 0, "mc_all", ST_tW_top_MEscaledown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_MEscaledown)
#ST_tW_top_MEscaleup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_MEscaleup.txt"
#ST_tW_top_MEscaleup=run_obj("ST_tW_top_MEscaleup",0, 0, 0, 0, "mc_all", ST_tW_top_MEscaleup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_MEscaleup)
#ST_tW_top_PSscaledown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_PSscaledown.txt"
#ST_tW_top_PSscaledown=run_obj("ST_tW_top_PSscaledown",0, 0, 0, 0, "mc_all", ST_tW_top_PSscaledown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_PSscaledown)
#ST_tW_top_PSscaleup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_PSscaleup.txt"
#ST_tW_top_PSscaleup=run_obj("ST_tW_top_PSscaleup",0, 0, 0, 0, "mc_all", ST_tW_top_PSscaleup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_PSscaleup)
#ST_tW_top_fsrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_fsrdown.txt"
#ST_tW_top_fsrdown=run_obj("ST_tW_top_fsrdown",0, 0, 0, 0, "mc_all", ST_tW_top_fsrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_fsrdown)
#ST_tW_top_fsrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_fsrup.txt"
#ST_tW_top_fsrup=run_obj("ST_tW_top_fsrup",0, 0, 0, 0, "mc_all", ST_tW_top_fsrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_fsrup)
#ST_tW_top_herwigpp_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_herwigpp.txt"
#ST_tW_top_herwigpp=run_obj("ST_tW_top_herwigpp",0, 0, 0, 0, "mc_all", ST_tW_top_herwigpp_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_herwigpp)
#ST_tW_top_isrdown_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_isrdown.txt"
#ST_tW_top_isrdown=run_obj("ST_tW_top_isrdown",0, 0, 0, 0, "mc_all", ST_tW_top_isrdown_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_isrdown)
#ST_tW_top_isrup_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_isrup.txt"
#ST_tW_top_isrup=run_obj("ST_tW_top_isrup",0, 0, 0, 0, "mc_all", ST_tW_top_isrup_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_isrup)
#ST_tW_top_mtop1695_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_mtop1695.txt"
#ST_tW_top_mtop1695=run_obj("ST_tW_top_mtop1695",0, 0, 0, 0, "mc_all", ST_tW_top_mtop1695_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_mtop1695)
#ST_tW_top_mtop1755_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/ST_tW_top_mtop1755.txt"
#ST_tW_top_mtop1755=run_obj("ST_tW_top_mtop1755",0, 0, 0, 0, "mc_all", ST_tW_top_mtop1755_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(ST_tW_top_mtop1755)

###################### For Zprime ###########################
#TTTo2L2Nu_M500_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/reMiniAOD/"+dataset+"/TTTo2L2Nu.txt"
#TTTo2L2Nu_M500=run_obj("TTTo2L2Nu_M500",0, 1, 0, 0, "mc_all", TTTo2L2Nu_M500_path,Ele23_Ele12_trigger,0 ,1, 0, 0)              
#Run_data.append(TTTo2L2Nu_M500)
#
###############################################################

for i_data in Run_data:
    i_data.get_version()
    i_data.creat_script()
    print "create script for %s"%(i_data.name)
    
 
