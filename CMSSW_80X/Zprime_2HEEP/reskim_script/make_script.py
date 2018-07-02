import math
import datetime

import ROOT
import os


str_import=["import os","import ROOT"]
str_import_so=["ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc/reskim_C.so'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_1F/reskim_FR_1F_C.so'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_2F/reskim_FR_2F_C.so'"')"]
str_import_aclic=["ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc/reskim_C_ACLiC_dict_rdict.pcm'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_1F/reskim_FR_1F_C_ACLiC_dict_rdict.pcm'"')","ROOT.gSystem.Load('"'/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/so_data_mc_FR_2F/reskim_FR_2F_C_ACLiC_dict_rdict.pcm'"')"]
dir_out_put="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/reskim_out/normal/"
path_script="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/script/"

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
data_run_range[""]    =["0","9999999"]
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
            f1 = open(path_script+"script_"+self.name+".py",'w') 
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
            reskim_list=["reskim_",self.name,"=ROOT.reskim(ch_",self.name,", False",", False",", False",", False)"]
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
                reskim_list[7]=",True)"
            
            f1.write(reskim_list[0]+reskim_list[1]+reskim_list[2]+reskim_list[3]+reskim_list[4]+reskim_list[5]+reskim_list[6]+reskim_list[7])
            f1.write("\n")
            f1.write(reskim_list[0]+self.name+".Loop("'"'+dir_out_put+self.name+".root"'"'")") 
            f1.write("\n")
            f1.close()
             
            f2 = open(path_script+"script_"+self.name+".sh",'w') 
            f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_8_0_25/src")
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
                f1.write(reskim_list[0]+self.name+".Loop("'"'+dir_out_put+self.name+"_"+tr+".root"'"'")") 
                f1.write("\n")
                f1.close()
                
                f2 = open(path_script+"script_"+self.name+tr+".sh",'w') 
                f2.write("cd /user/wenxing/ST_TW_channel/CMSSW_8_0_25/src")
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
#runB1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_aa"
#runB1=run_obj("runB1",1, 0, 0, 0, "RunB", runB1_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB1)
#runB2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ab"
#runB2=run_obj("runB2",1, 0, 0, 0, "RunB", runB2_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB2)
#runB3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ac"
#runB3=run_obj("runB3",1, 0, 0, 0, "RunB", runB3_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB3)
#runB4_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ad"
#runB4=run_obj("runB4",1, 0, 0, 0, "RunB", runB4_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB4)
#runB5_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ae"
#runB5=run_obj("runB5",1, 0, 0, 0, "RunB", runB5_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB5)
#runB6_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_af"
#runB6=run_obj("runB6",1, 0, 0, 0, "RunB", runB6_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB6)
#runB7_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ag"
#runB7=run_obj("runB7",1, 0, 0, 0, "RunB", runB7_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB7)
#runB8_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ah"
#runB8=run_obj("runB8",1, 0, 0, 0, "RunB", runB8_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB8)
#runB9_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ai"
#runB9=run_obj("runB9",1, 0, 0, 0, "RunB", runB9_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB9)
#runB10_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_aj"
#runB10=run_obj("runB10",1, 0, 0, 0, "RunB", runB10_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB10)
#runB11_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/RunB_ak"
#runB11=run_obj("runB11",1, 0, 0, 0, "RunB", runB11_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runB11)

#runC1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunC_1.txt"
#runC1=run_obj("runC1",1, 0, 0, 0, "RunC", runC1_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runC1)
#runD1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunD_1.txt"
#runD1=run_obj("runD1",1, 0, 0, 0, "RunD", runD1_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runD1)
#runD2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunD_2.txt"
#runD2=run_obj("runD2",1, 0, 0, 0, "RunD", runD2_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runD2)
#runE1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunE_1.txt"
#runE1=run_obj("runE1",1, 0, 0, 0, "RunE", runE1_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runE1)
#runE2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunE_2.txt"
#runE2=run_obj("runE2",1, 0, 0, 0, "RunE", runE2_path,Ele33_trigger,1 ,1, 0, 0)              
#Run_data.append(runE2)
#runF1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunF_1.txt"
#runF1=run_obj("runF1",1, 0, 0, 0, "RunF", runF1_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runF1)
#runG1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunG_1.txt"
#runG1=run_obj("runG1",1, 0, 0, 0, "RunG", runG1_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runG1)
#runG2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunG_2.txt"
#runG2=run_obj("runG2",1, 0, 0, 0, "RunG", runG2_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runG2)
#runG3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunG_3.txt"
#runG3=run_obj("runG3",1, 0, 0, 0, "RunG", runG3_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runG3)
#runHv2_1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunHv2_1.txt"
#runHv2_1=run_obj("runHv2_1",1, 0, 0, 0, "RunHv2", runHv2_1_path,Ele33_trigger,1 ,1, 0, 0)            
#Run_data.append(runHv2_1)
#runHv2_2_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunHv2_2.txt"
#runHv2_2=run_obj("runHv2_2",1, 0, 0, 0, "RunHv2", runHv2_2_path,Ele33_trigger,1 ,1, 0, 0)            
#Run_data.append(runHv2_2)
#runHv2_3_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunHv2_3.txt"
#runHv2_3=run_obj("runHv2_3",1, 0, 0, 0, "RunHv2", runHv2_3_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runHv2_3)
#runHv3_1_path="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/data_list/Double_RunHv3_1.txt"
#runHv3_1=run_obj("runHv3_1",1, 0, 0, 0, "RunHv3", runHv3_1_path,Ele33_trigger,1 ,1, 0, 0)               
#Run_data.append(runHv3_1)


########################## Data FR_1F ########################################
#runB1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0000/*.root"]
#runB1_1F=run_obj("runB1_1F",1, 0, 0, 0, "RunB", runB1_path_1F,Ele33_trigger,1 ,0, 1, 0)     
#Run_data.append(runB1_1F)
#runB2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0001/*.root"]
#runB2_1F=run_obj("runB2_1F",1, 0, 0, 0, "RunB", runB2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runB2_1F)
#runB3_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0002/*.root"]
#runB3_1F=run_obj("runB3_1F",1, 0, 0, 0, "RunB", runB3_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runB3_1F)
#runB4_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0003/*.root"]
#runB4_1F=run_obj("runB4_1F",1, 0, 0, 0, "RunB", runB4_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runB4_1F)
#runB5_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0004/*.root"]
#runB5_1F=run_obj("runB5_1F",1, 0, 0, 0, "RunB", runB5_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runB5_1F)
#runB6_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0005/*.root"]
#runB6_1F=run_obj("runB6_1F",1, 0, 0, 0, "RunB", runB6_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runB6_1F)
#runC1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016C-23Sep2016-v1_AOD/161209_171822/0000/*.root"]
#runC1_1F=run_obj("runC1_1F",1, 0, 0, 0, "RunC", runC1_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runC1_1F)
#runC2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016C-23Sep2016-v1_AOD/161209_171822/0001/*.root"]
#runC2_1F=run_obj("runC2_1F",1, 0, 0, 0, "RunC", runC2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runC2_1F)
#runD1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0000/*.root"]
#runD1_1F=run_obj("runD1_1F",1, 0, 0, 0, "RunD", runD1_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runD1_1F)
#runD2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0001/*.root"]
#runD2_1F=run_obj("runD2_1F",1, 0, 0, 0, "RunD", runD2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runD2_1F)
#runD3_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0002/*.root"]
#runD3_1F=run_obj("runD3_1F",1, 0, 0, 0, "RunD", runD3_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runD3_1F)
#runE1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0000/*.root"]
#runE1_1F=run_obj("runE1_1F",1, 0, 0, 0, "RunE", runE1_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runE1_1F)
#runE2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0001/*.root"]
#runE2_1F=run_obj("runE2_1F",1, 0, 0, 0, "RunE", runE2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runE2_1F)
#runE3_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0002/*.root"]
#runE3_1F=run_obj("runE3_1F",1, 0, 0, 0, "RunE", runE3_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runE3_1F)
#runF1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016F-23Sep2016-v1_AOD/161209_172143/0000/*.root"]
#runF1_1F=run_obj("runF1_1F",1, 0, 0, 0, "RunF", runF1_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runF1_1F)
#runF2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016F-23Sep2016-v1_AOD/161209_172143/0001/*.root"]
#runF2_1F=run_obj("runF2_1F",1, 0, 0, 0, "RunF", runF2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runF2_1F)
#runG1_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0000/*.root"]
#runG1_1F=run_obj("runG1_1F",1, 0, 0, 0, "RunG", runG1_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runG1_1F)
#runG2_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0001/*.root"]
#runG2_1F=run_obj("runG2_1F",1, 0, 0, 0, "RunG", runG2_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runG2_1F)
#runG3_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0002/*.root"]
#runG3_1F=run_obj("runG3_1F",1, 0, 0, 0, "RunG", runG3_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runG3_1F)
#runG4_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0003/*.root"]
#runG4_1F=run_obj("runG4_1F",1, 0, 0, 0, "RunG", runG4_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runG4_1F)
#runG5_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0004/*.root"]
#runG5_1F=run_obj("runG5_1F",1, 0, 0, 0, "RunG", runG5_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runG5_1F)
#runHv21_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0000/*.root"]
#runHv21_1F=run_obj("runHv21_1F",1, 0, 0, 0, "RunHv2", runHv21_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv21_1F)
#runHv22_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0001/*.root"]
#runHv22_1F=run_obj("runHv22_1F",1, 0, 0, 0, "RunHv2", runHv22_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv22_1F)
#runHv23_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0002/*.root"]
#runHv23_1F=run_obj("runHv23_1F",1, 0, 0, 0, "RunHv2", runHv23_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv23_1F)
#runHv24_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0003/*.root"]
#runHv24_1F=run_obj("runHv24_1F",1, 0, 0, 0, "RunHv2", runHv24_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv24_1F)
#runHv25_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0004/*.root"]
#runHv25_1F=run_obj("runHv25_1F",1, 0, 0, 0, "RunHv2", runHv25_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv25_1F)
#runHv31_path_1F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v3_AOD/161209_172447/0000/*.root"]
#runHv31_1F=run_obj("runHv31_1F",1, 0, 0, 0, "RunHv3", runHv31_path_1F,Ele33_trigger,1 ,0, 1, 0)              
#Run_data.append(runHv31_1F)
############################ Data FR_2F ########################################

#runB1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0000/*.root"]
#runB1_2F=run_obj("runB1_2F",1, 0, 0, 0, "RunB", runB1_path_2F,Ele33_trigger,1 ,0, 0, 1)     
#Run_data.append(runB1_2F)
#runB2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0001/*.root"]
#runB2_2F=run_obj("runB2_2F",1, 0, 0, 0, "RunB", runB2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runB2_2F)
#runB3_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0002/*.root"]
#runB3_2F=run_obj("runB3_2F",1, 0, 0, 0, "RunB", runB3_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runB3_2F)
#runB4_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0003/*.root"]
#runB4_2F=run_obj("runB4_2F",1, 0, 0, 0, "RunB", runB4_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runB4_2F)
#runB5_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0004/*.root"]
#runB5_2F=run_obj("runB5_2F",1, 0, 0, 0, "RunB", runB5_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runB5_2F)
#runB6_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016B-23Sep2016-v3_AOD/161209_171706/0005/*.root"]
#runB6_2F=run_obj("runB6_2F",1, 0, 0, 0, "RunB", runB6_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runB6_2F)
#runC1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016C-23Sep2016-v1_AOD/161209_171822/0000/*.root"]
#runC1_2F=run_obj("runC1_2F",1, 0, 0, 0, "RunC", runC1_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runC1_2F)
#runC2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016C-23Sep2016-v1_AOD/161209_171822/0001/*.root"]
#runC2_2F=run_obj("runC2_2F",1, 0, 0, 0, "RunC", runC2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runC2_2F)
#runD1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0000/*.root"]
#runD1_2F=run_obj("runD1_2F",1, 0, 0, 0, "RunD", runD1_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runD1_2F)
#runD2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0001/*.root"]
#runD2_2F=run_obj("runD2_2F",1, 0, 0, 0, "RunD", runD2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runD2_2F)
#runD3_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016D-23Sep2016-v1_AOD/161209_171914/0002/*.root"]
#runD3_2F=run_obj("runD3_2F",1, 0, 0, 0, "RunD", runD3_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runD3_2F)
#runE1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0000/*.root"]
#runE1_2F=run_obj("runE1_2F",1, 0, 0, 0, "RunE", runE1_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runE1_2F)
#runE2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0001/*.root"]
#runE2_2F=run_obj("runE2_2F",1, 0, 0, 0, "RunE", runE2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runE2_2F)
#runE3_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016E-23Sep2016-v1_AOD/161209_172055/0002/*.root"]
#runE3_2F=run_obj("runE3_2F",1, 0, 0, 0, "RunE", runE3_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runE3_2F)
#runF1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016F-23Sep2016-v1_AOD/161209_172143/0000/*.root"]
#runF1_2F=run_obj("runF1_2F",1, 0, 0, 0, "RunF", runF1_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runF1_2F)
#runF2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016F-23Sep2016-v1_AOD/161209_172143/0001/*.root"]
#runF2_2F=run_obj("runF2_2F",1, 0, 0, 0, "RunF", runF2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runF2_2F)
#runG1_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0000/*.root"]
#runG1_2F=run_obj("runG1_2F",1, 0, 0, 0, "RunG", runG1_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runG1_2F)
#runG2_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0001/*.root"]
#runG2_2F=run_obj("runG2_2F",1, 0, 0, 0, "RunG", runG2_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runG2_2F)
#runG3_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0002/*.root"]
#runG3_2F=run_obj("runG3_2F",1, 0, 0, 0, "RunG", runG3_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runG3_2F)
#runG4_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0003/*.root"]
#runG4_2F=run_obj("runG4_2F",1, 0, 0, 0, "RunG", runG4_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runG4_2F)
#runG5_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016G-23Sep2016-v1_AOD/161209_172238/0004/*.root"]
#runG5_2F=run_obj("runG5_2F",1, 0, 0, 0, "RunG", runG5_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runG5_2F)
#runHv21_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0000/*.root"]
#runHv21_2F=run_obj("runHv21_2F",1, 0, 0, 0, "RunHv2", runHv21_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv21_2F)
#runHv22_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0001/*.root"]
#runHv22_2F=run_obj("runHv22_2F",1, 0, 0, 0, "RunHv2", runHv22_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv22_2F)
#runHv23_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0002/*.root"]
#runHv23_2F=run_obj("runHv23_2F",1, 0, 0, 0, "RunHv2", runHv23_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv23_2F)
#runHv24_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0003/*.root"]
#runHv24_2F=run_obj("runHv24_2F",1, 0, 0, 0, "RunHv2", runHv24_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv24_2F)
#runHv25_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v2_AOD/161209_172342/0004/*.root"]
#runHv25_2F=run_obj("runHv25_2F",1, 0, 0, 0, "RunHv2", runHv25_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv25_2F)
#runHv31_path_2F=["/pnfs/iihe/cms/store/user/rgoldouz/DoubleEG/crab_DoubleEG_Run2016H-PromptReco-v3_AOD/161209_172447/0000/*.root"]
#runHv31_2F=run_obj("runHv31_2F",1, 0, 0, 0, "RunHv3", runHv31_path_2F,Ele33_trigger,1 ,0, 0, 1)              
#Run_data.append(runHv31_2F)



################################## MC ########################################

####################For Zprime To EE only ##############################
#ZToEE_1_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_50_120/crab_ZToEE_M_50_120/170408_131656/0000/*.root"]
#ZToEE_1=run_obj("ZToEE_M_50_120",0, 0, 0, 0, "", ZToEE_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_1)
#ZToEE_2_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_120_200/crab_ZToEE_M_120_200/170408_131521/0000/*.root"]
#ZToEE_2=run_obj("ZToEE_M_120_200",0, 0, 0, 0, "", ZToEE_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_2)
#ZToEE_3_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_200_400/crab_ZToEE_M_200_400/170408_131751/0000/*.root"]
#ZToEE_3=run_obj("ZToEE_M_200_400",0, 0, 0, 0, "", ZToEE_3_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_3)
#ZToEE_4_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_400_800/crab_ZToEE_M_400_800/170408_131433/0000/*.root"]
#ZToEE_4=run_obj("ZToEE_M_400_800",0, 0, 0, 0, "", ZToEE_4_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_4)
#ZToEE_5_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_800_1400/crab_ZToEE_M_800_1400/170408_131303/0000/*.root"]
#ZToEE_5=run_obj("ZToEE_M_800_1400",0, 0, 0, 0, "", ZToEE_5_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_5)
#ZToEE_6_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/crab_ZToEE_M_1400_2300/170408_131609/0000/*.root"]
#ZToEE_6=run_obj("ZToEE_M_1400_2300",0, 0, 0, 0, "", ZToEE_6_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_6)
#ZToEE_7_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_2300_3500/crab_ZToEE_M_2300_3500/170408_131857/0000/*.root"]
#ZToEE_7=run_obj("ZToEE_M_2300_3500",0, 0, 0, 0, "", ZToEE_7_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_7)
#ZToEE_8_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_3500_4500/crab_ZToEE_M_3500_4500/170408_131358/0000/*.root"]
#ZToEE_8=run_obj("ZToEE_M_3500_4500",0, 0, 0, 0, "", ZToEE_8_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_8)
#ZToEE_9_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_4500_6000/crab_ZToEE_M_4500_6000/170408_131235/0000/*.root"]
#ZToEE_9=run_obj("ZToEE_M_4500_6000",0, 0, 0, 0, "", ZToEE_9_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_9)
#ZToEE_10_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf/crab_ZToEE_M_6000_Inf/170408_131331/0000/*.root"]
#ZToEE_10=run_obj("ZToEE_M_6000_Inf",0, 0, 0, 0, "", ZToEE_10_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToEE_10)
#ZToTT_amc_M50_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170408_132740/0000/*.root","/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170408_132740/0001/*.root"]
#ZToTT_amc_M50=run_obj("ZToTT_amc_M50",0, 0, 1, 0, "", ZToTT_amc_M50_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZToTT_amc_M50)
#
#WWTo2L2Nu_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/WWTo2L2Nu_13TeV-powheg/crab_WWTo2L2Nu/170408_130233/0000/*.root"]
#WWTo2L2Nu=run_obj("WWTo2L2Nu_Mll_200",0, 0, 0, 1, "", WWTo2L2Nu_path,Ele23_Ele12_trigger,0 ,0, 0, 0)              
#Run_data.append(WWTo2L2Nu)
WW_1_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/WWTo2L2Nu_Mll_200To600_13TeV-powheg/crab_WWTo2L2Nu_Mll_200To600/170408_125454/0000/*.root"]
WW_1=run_obj("WWTo2L2Nu_Mll_200To600",0, 0, 0, 0, "", WW_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(WW_1)
WW_2_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/WWTo2L2Nu_Mll_600To1200_13TeV-powheg/crab_WWTo2L2Nu_Mll_600To1200/170408_125358/0000/*.root"]
WW_2=run_obj("WWTo2L2Nu_Mll_600To1200",0, 0, 0, 0, "", WW_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(WW_2)
WW_3_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/WWTo2L2Nu_Mll_1200To2500_13TeV-powheg/crab_WWTo2L2Nu_Mll_1200To2500/170408_125713/0000/*.root"]
WW_3=run_obj("WWTo2L2Nu_Mll_1200To2500",0, 0, 0, 0, "", WW_3_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(WW_3)
WW_4_path=["/pnfs/iihe/cms/store/user/xgao/2017MC_Moriond/2017-04/WWTo2L2Nu_Mll_2500ToInf_13TeV-powheg/crab_WWTo2L2Nu_Mll_2500ToInf/170408_125426/0000/*.root"]
WW_4=run_obj("WWTo2L2Nu_Mll_2500ToInf",0, 0, 0, 0, "", WW_4_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(WW_4)
#
TTToLL_1_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-MiniAOD/170408_133703/0000/*.root"]
TTToLL_1=run_obj("TTToLL_M_500To800",0, 0, 0, 0, "", TTToLL_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(TTToLL_1)
TTToLL_2_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-MiniAOD/170408_133613/0000/*.root"]
TTToLL_2=run_obj("TTToLL_M_800To1200",0, 0, 0, 0, "", TTToLL_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(TTToLL_2)
TTToLL_3_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-MiniAOD/170408_133520/0000/*.root"]
TTToLL_3=run_obj("TTToLL_M_1200To1800",0, 0, 0, 0, "", TTToLL_3_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(TTToLL_3)
TTToLL_4_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC/TTToLL_MLL_1800ToInf_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TTToLL_MLL_1800ToInf_TuneCUETP8M1_13TeV-powheg-MiniAOD/170408_132301/0000/*.root"]
TTToLL_4=run_obj("TTToLL_M_1800ToInf",0, 0, 0, 0, "", TTToLL_4_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
Run_data.append(TTToLL_4)
######################## For Zprime Signal ###########################
#RSG_2000_path=["/pnfs/iihe/cms/store/user/xgao/RSGravToEEMuMu_kMpl-001_M-2000_TuneCUEP8M1_13TeV-pythia8/crab_GravToEEMuMu_M_2000/171006_173619/0000/*.root"]
#RSG_2000=run_obj("RSG_2000",0, 0, 0, 0, "", RSG_2000_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(RSG_2000)
#RSG_3000_path=["/pnfs/iihe/cms/store/user/xgao/RSGravToEEMuMu_kMpl-001_M-3000_TuneCUEP8M1_13TeV-pythia8/crab_GravToEEMuMu_M_3000/171006_173354/0000/*.root"]
#RSG_3000=run_obj("RSG_3000",0, 0, 0, 0, "", RSG_3000_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(RSG_3000)
##
####################### For Zprime and tw ###########################
#WZ_1_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/crab_WZTo3LNu_TuneCUETP8M1_13TeV-powheg-/170509_185048/0000/*.root"]
#WZ_1=run_obj("WZ_3LNu",0, 0, 0, 0, "", WZ_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(WZ_1)
#WZ_2_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/crab_WZTo2L2Q_13TeV_amcatnloFXFX_madspin/170509_193525/0000/*.root"]
#WZ_2=run_obj("WZ_2L2Q",0, 0, 0, 0, "", WZ_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(WZ_2)
#ZZ_1_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ZZTo2L2Nu_13TeV_powheg_pythia8/crab_ZZTo2L2Nu_13TeV_powheg/170509_190040/0000/*.root"]
#ZZ_1=run_obj("ZZ_2L2Nu",0, 0, 0, 0, "", ZZ_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZZ_1)
#ZZ_2_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ZZTo4L_13TeV_powheg_pythia8/crab_ZZTo4L_13TeV_powheg/170509_185651/0000/*.root"]
#ZZ_2=run_obj("ZZ_4L",0, 0, 0, 0, "", ZZ_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZZ_2)
#ZZ_3_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ZZTo2L2Q_13TeV_powheg_pythia8/crab_ZZTo2L2Q/170509_193919/0000/*.root"]
#ZZ_3=run_obj("ZZ_2L2Q",0, 0, 0, 0, "", ZZ_3_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ZZ_3)
#ST_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_top_5f_NoFullyHadronicDecays/170511_081359/0000/*.root","/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_top_5f_NoFullyHadronicDecays_ext1/170511_081746/0000/*.root"]
#ST=run_obj("ST_tW_top_5f_NoFullyHadronicDecays",0, 0, 0, 0, "", ST_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ST)
#ST_anti_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_antitop_5f_NoFullyHadronicDecays/170511_081323/0000/*.root","/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_antitop_5f_NoFullyHadronicDecays_ext1/170511_081437/0000/*.root"]
#ST_anti=run_obj("ST_tW_antitop_5f_NoFullyHadronicDecays",0, 0, 0, 0, "", ST_anti_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(ST_anti)

###################### Only for tw ###########################
#WG_1_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX/170509_200032/0000/*.root"]
#WG_1=run_obj("WG_LNuG",0, 0, 0, 0, "", WG_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(WG_1)
#
#WW_2L2Nu_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/WWTo2L2Nu_13TeV-powheg/crab_WWTo2L2Nu/170509_192532/0000/*.root"]
#WW_2L2Nu=run_obj("WWTo2L2Nu",0, 0, 0, 0, "", WW_2L2Nu_path,Ele23_Ele12_trigger,0 ,0, 0, 0)              
#Run_data.append(WW_2L2Nu)
#
#TT_1_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin/170509_194938/0000/*.root"]
#TT_1=run_obj("TTWJetsToQQ",0, 0, 0, 0, "", TT_1_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(TT_1)
#TT_2_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin/170510_225909/0000/*.root"]
#TT_2=run_obj("TTWJetsToLNu",0, 0, 0, 0, "", TT_2_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(TT_2)
#TT_3_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo/170509_201212/0000/*.root"]
#TT_3=run_obj("TTZToLLNuNu",0, 0, 0, 0, "", TT_3_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(TT_3)
#TT_4_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo/170509_194140/0000/*.root"]
#TT_4=run_obj("TTZToQQ",0, 0, 0, 0, "", TT_4_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(TT_4)
#TT_5_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin/170509_190936/0000/*.root"]
#TT_5=run_obj("TTGJets",0, 0, 0, 0, "", TT_5_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(TT_5)

#GGHWW_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/GluGluHToWWTo2L2Nu_M125_13TeV_powheg_pythia8/crab_GGHWW/170725_090814/0000/*.root"]
#GGHWW=run_obj("GGHWWTo2L2Nu",0, 0, 0, 0, "", GGHWW_path,Ele23_Ele12_trigger,0 ,0, 0, 0)              
#Run_data.append(GGHWW)
#VBFHWW_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/VBFHToWWTo2L2Nu_M125_13TeV_powheg_pythia8/crab_VBFHWW/170725_090730/0000/*.root"]
#VBFHWW=run_obj("VBFHWWTo2L2Nu",0, 0, 0, 0, "", VBFHWW_path,Ele23_Ele12_trigger,0 ,0, 0, 0)              
#Run_data.append(VBFHWW)

###################### Only for tw  BSM  and FCNC fast sim###########################
#BSM_TT_path=["/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/MVA/FastSim_emu/TT_emu.root"]
#BSM_TT=run_obj("BSM_TTTo2L2Nu",0, 0, 0, 0, "", BSM_TT_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(BSM_TT)
#BSM_TW_path=["/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/MVA/FastSim_emu/ST_emu.root"]
#BSM_TW=run_obj("BSM_TWTo2L2Nu",0, 0, 0, 0, "", BSM_TW_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(BSM_TW)
#FCNC_ST_tug_path=["/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/MVA/ST_FCNC_tug.root"]
#FCNC_ST_tug=run_obj("FCNC_ST_tug_fastsim",0, 0, 0, 0, "", FCNC_ST_tug_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tug)
#FCNC_ST_tcg_path=["/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/MVA/ST_FCNC_tcg.root"]
#FCNC_ST_tcg=run_obj("FCNC_ST_tcg_fastsim",0, 0, 0, 0, "", FCNC_ST_tcg_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tcg)
#
####################### Only for tw  FCNC full sim ###########################
#FCNC_ST_tug_fullsim_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC_0511_bjetsf/ST_tW_tugFCNC_leptonDecays_Madgraph/crab_ST_tW_tugFCNC_leptonDecays_Madgraph/170827_144241/0000/*.root"]
#FCNC_ST_tug_fullsim=run_obj("FCNC_ST_tug_fullsim",0, 0, 0, 0, "", FCNC_ST_tug_fullsim_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tug_fullsim)
#FCNC_ST_tcg_fullsim_path=["/pnfs/iihe/cms/store/user/wenxing/FINAL_sample/MC_0511_bjetsf/ST_tW_tcgFCNC_leptonDecays_Madgraph/crab_ST_tW_tcgFCNC_leptonDecays_Madgraph/170827_144108/0000/*.root"]
#FCNC_ST_tcg_fullsim=run_obj("FCNC_ST_tcg_fullsim",0, 0, 0, 0, "", FCNC_ST_tcg_fullsim_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tcg_fullsim)
####################### Only for tw  FCNC sys sample ###########################
#FCNC_ST_tug_PS_Down_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_tugFCNC_scaledown_leptonDecays_Madgraph/crab_FCNC_tug_sd/170812_222834/0000/*.root"]
#FCNC_ST_tug_PS_Down=run_obj("FCNC_ST_tug_PS_Down",0, 0, 0, 0, "", FCNC_ST_tug_PS_Down_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tug_PS_Down)
#FCNC_ST_tug_PS_Up_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_tugFCNC_scaleup_leptonDecays_Madgraph/crab_FCNC_tug_su/170812_222915/0000/*.root"]
#FCNC_ST_tug_PS_Up=run_obj("FCNC_ST_tug_PS_Up",0, 0, 0, 0, "", FCNC_ST_tug_PS_Up_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tug_PS_Up)
#FCNC_ST_tcg_PS_Down_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_tcgFCNC_scaledown_leptonDecays_Madgraph/crab_FCNC_tcg_sd/170812_222955/0000/*.root"]
#FCNC_ST_tcg_PS_Down=run_obj("FCNC_ST_tcg_PS_Down",0, 0, 0, 0, "", FCNC_ST_tcg_PS_Down_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tcg_PS_Down)
#FCNC_ST_tcg_PS_Up_path=["/pnfs/iihe/cms/store/user/xgao/2017-05-11_MC/ST_tW_tcgFCNC_scaleup_leptonDecays_Madgraph/crab_FCNC_tcg_su/170812_223034/0000/*.root"]
#FCNC_ST_tcg_PS_Up=run_obj("FCNC_ST_tcg_PS_Up",0, 0, 0, 0, "", FCNC_ST_tcg_PS_Up_path,Ele23_Ele12_trigger,0 ,0 ,0 ,0)               
#Run_data.append(FCNC_ST_tcg_PS_Up)
for i_data in Run_data:
    i_data.get_version()
    i_data.creat_script()
    print "create script for %s"%(i_data.name)
    
 
