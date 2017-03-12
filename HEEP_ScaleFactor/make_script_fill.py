import math
import datetime
import ROOT
import os

isSimple=True

class_name = "fh = ROOT.fill_histograms()"
if isSimple : class_name = "fh = ROOT.fill_histograms_simple()"

str_import=["import os","import ROOT"]

#str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_MC_Morid17/fill_histograms_C.so'"')" 
#str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_MC_Morid17/fill_histograms_C_ACLiC_dict_rdict.pcm'"')"
str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_MC_Morid17/fill_histograms_simple_C.so'"')" 
str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_MC_Morid17/fill_histograms_simple_C_ACLiC_dict_rdict.pcm'"')"
#
#str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_data/fill_histograms_C.so'"')" 
#str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_data/fill_histograms_C_ACLiC_dict_rdict.pcm'"')"
#str_import_so=   "ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_data/fill_histograms_simple_C.so'"')" 
#str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_data/fill_histograms_simple_C_ACLiC_dict_rdict.pcm'"')"

#str_import_so="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_dir_data_FR/fill_histograms_C.so'"')"
#str_import_aclic="ROOT.gSystem.Load('"'/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/so_dir_data_FR/fill_histograms_C_ACLiC_dict_rdict.pcm'"')"
path_script="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/fill_hist_script/script/"



class fill_obj:
    def __init__(self, name, input_file, out_name):
        self.name=name
        self.input_file=input_file
        self.out_name=out_name
    def create_script(self):
        
        f1 = open(path_script+"script_"+self.name+".py",'w') 
        for im in range(0,len(str_import)):
            f1.write(str_import[im]) 
            f1.write("\n")
        f1.write(str_import_so)
        f1.write("\n")
        f1.write(str_import_aclic)
        f1.write("\n")
        f1.write("ch_"+self.name+"= ROOT.TChain('"'tap'"')")
        f1.write("\n")
        for pa in range(0,len(self.input_file)):
            f1.write("ch_"+self.name+".Add("'"'+self.input_file[pa]+'"'")")        
            f1.write("\n")
        f1.write(class_name)
        f1.write("\n")
        f1.write("fh.Init(ch_"+self.name+")")
        f1.write("\n")
        f1.write("fh.Loop("'"'+self.out_name+ '"'")")
  
        f2 = open(path_script+"script_"+self.name+".sh",'w') 
        f2.write("cd /user/wenxing/HEEP/CMSSW_7_4_10_patch2/src")
        f2.write("\n")
        f2.write("eval `scramv1 runtime -sh`")
        f2.write("\n")
        f2.write("python "+path_script+"script_"+self.name+".py")
        f2.close()

obj_list=[]

#################### DATA #####################

#input_data_BCDEFGH=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/reMiniAOD/RunBCDEFGH_reMiniAOD.root"]
#data_BCDEFGH=fill_obj("data_BCDEFGH_reMiniAOD",input_data_BCDEFGH,"data_BCDEFGH_reMiniAOD")
#obj_list.append(data_BCDEFGH)
#input_data_BCDEF=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/reMiniAOD/RunBCDEF_reMiniAOD.root"]
#data_BCDEF=fill_obj("data_BCDEF_reMiniAOD",input_data_BCDEF,"data_BCDEF_reMiniAOD")
#obj_list.append(data_BCDEF)
#input_data_GH=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/reMiniAOD/RunGH_reMiniAOD.root"]
#data_GH=fill_obj("data_GH_reMiniAOD",input_data_GH,"data_GH_reMiniAOD")
#obj_list.append(data_GH)

#input_data_B=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunB.root"]
#data_B=fill_obj("data_B_Ele27tight",input_data_B,"data_B_Ele27tight")
#obj_list.append(data_B)
#input_data_C=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunC.root"]
#data_C=fill_obj("data_C_Ele27tight",input_data_C,"data_C_Ele27tight")
#obj_list.append(data_C)
#input_data_D=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunD.root"]
#data_D=fill_obj("data_D_Ele27tight",input_data_D,"data_D_Ele27tight")
#obj_list.append(data_D)
#input_data_E=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunE.root"]
#data_E=fill_obj("data_E_Ele27tight",input_data_E,"data_E_Ele27tight")
#obj_list.append(data_E)
#input_data_F=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunF.root"]
#data_F=fill_obj("data_F_Ele27tight",input_data_F,"data_F_Ele27tight")
#obj_list.append(data_F)
#input_data_G=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunG.root"]
#data_G=fill_obj("data_G_Ele27tight",input_data_G,"data_G_Ele27tight")
#obj_list.append(data_G)
#input_data_H=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/MiniAOD/RunH.root"]
#data_H=fill_obj("data_H_Ele27tight",input_data_H,"data_H_Ele27tight")
#obj_list.append(data_H)

################## MC Morid17 #######################


#input_DYToEE_powheg=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE.root"]
#DYToEE_powheg=fill_obj("DYToEE_powheg",input_DYToEE_powheg,"DYToEE_powheg")
#obj_list.append(DYToEE_powheg)
##
#input_ST=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/ST.root"]
#ST=fill_obj("ST",input_ST,"ST")
#obj_list.append(ST)
#input_ST_anti=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/ST_anti.root"]
#ST_anti=fill_obj("ST_anti",input_ST_anti,"ST_anti")
#obj_list.append(ST_anti)
##
#input_WW=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WW.root"]
#WW=fill_obj("WW",input_WW,"WW")
#obj_list.append(WW)
#input_WZ=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WZ.root"]
#WZ=fill_obj("WZ",input_WZ,"WZ")
#obj_list.append(WZ)
#input_ZZ=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/ZZ.root"]
#ZZ=fill_obj("ZZ",input_ZZ,"ZZ")
#obj_list.append(ZZ)
##
#input_TTbar=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/TTbar.root"]
#TTbar=fill_obj("TTbar",input_TTbar,"TTbar")
#obj_list.append(TTbar)
#input_WJet_mad=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_mad_*.root"]
#WJet_mad=fill_obj("WJet_mad",input_WJet_mad,"WJet_mad")
#obj_list.append(WJet_mad)

#input_WJet_amc_pt_100=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_amc_pt_100_new.root"]
#WJet_amc_pt_100=fill_obj("WJet_amc_pt_100_new",input_WJet_amc_pt_100,"WJet_amc_pt_100_new")
#obj_list.append(WJet_amc_pt_100)
#input_WJet_amc_pt_100_250=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_amc_pt_100_250.root"]
#WJet_amc_pt_100_250=fill_obj("WJet_amc_pt_100_250",input_WJet_amc_pt_100_250,"WJet_amc_pt_100_250")
#obj_list.append(WJet_amc_pt_100_250)
#input_WJet_amc_pt_250_400=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_amc_pt_250_400.root"]
#WJet_amc_pt_250_400=fill_obj("WJet_amc_pt_250_400",input_WJet_amc_pt_250_400,"WJet_amc_pt_250_400")
#obj_list.append(WJet_amc_pt_250_400)
#input_WJet_amc_pt_400_600=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_amc_pt_400_600.root"]
#WJet_amc_pt_400_600=fill_obj("WJet_amc_pt_400_600",input_WJet_amc_pt_400_600,"WJet_amc_pt_400_600")
#obj_list.append(WJet_amc_pt_400_600)
#input_WJet_amc_pt_600_Inf=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/WJet_amc_pt_600_Inf.root"]
#WJet_amc_pt_600_Inf=fill_obj("WJet_amc_pt_600_Inf",input_WJet_amc_pt_600_Inf,"WJet_amc_pt_600_Inf")
#obj_list.append(WJet_amc_pt_600_Inf)

#input_DYToLL_amc_pt50=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt50_new.root"]
#DYToLL_amc_pt50=fill_obj("DYToEE_amc_pt50_new",input_DYToLL_amc_pt50,"DYToEE_amc_pt50_new")
#obj_list.append(DYToLL_amc_pt50)
input_DYToLL_amc_pt100=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt100_new_*.root"]
DYToLL_amc_pt100=fill_obj("DYToEE_amc_pt100_new",input_DYToLL_amc_pt100,"DYToEE_amc_pt100_new")
obj_list.append(DYToLL_amc_pt100)
#input_DYToLL_amc_pt50_100=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt50_100.root"]
#DYToLL_amc_pt50_100=fill_obj("DYToEE_amc_pt50_100",input_DYToLL_amc_pt50_100,"DYToEE_amc_pt50_100")
#obj_list.append(DYToLL_amc_pt50_100)
#input_DYToLL_amc_pt100_250=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt100_250_*.root"]
#DYToLL_amc_pt100_250=fill_obj("DYToEE_amc_pt100_250",input_DYToLL_amc_pt100_250,"DYToEE_amc_pt100_250")
#obj_list.append(DYToLL_amc_pt100_250)
#input_DYToLL_amc_pt250_400=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt250_400.root"]
#DYToLL_amc_pt250_400=fill_obj("DYToEE_amc_pt250_400",input_DYToLL_amc_pt250_400,"DYToEE_amc_pt250_400")
#obj_list.append(DYToLL_amc_pt250_400)
#input_DYToLL_amc_pt400_650=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt400_650.root"]
#DYToLL_amc_pt400_650=fill_obj("DYToEE_amc_pt400_650",input_DYToLL_amc_pt400_650,"DYToEE_amc_pt400_650")
#obj_list.append(DYToLL_amc_pt400_650)
#input_DYToLL_amc_pt650_Inf=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_amc_pt650_Inf.root"]
#DYToLL_amc_pt650_Inf=fill_obj("DYToEE_amc_pt650_Inf",input_DYToLL_amc_pt650_Inf,"DYToEE_amc_pt650_Inf")
#obj_list.append(DYToLL_amc_pt650_Inf)
#
#input_ZToTT_mad=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToLL.root"]
#ZToTT_mad=fill_obj("ZToTT_mad",input_ZToTT_mad,"ZToTT_mad")
#obj_list.append(ZToTT_mad)
#input_DYToLL_Zpt100=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_mad_Zpt100_new.root"]
#DYToLL_Zpt100=fill_obj("DYToEE_mad_Zpt100_new",input_DYToLL_Zpt100,"DYToEE_mad_Zpt100_new")
#obj_list.append(DYToLL_Zpt100)
#input_DYToLL_Zpt100_200=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_mad_Zpt100_200.root"]
#DYToLL_Zpt100_200=fill_obj("DYToEE_mad_Zpt100_200",input_DYToLL_Zpt100_200,"DYToEE_mad_Zpt100_200")
#obj_list.append(DYToLL_Zpt100_200)
#input_DYToLL_Zpt200_Inf=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToEE_mad_Zpt200_Inf.root"]
#DYToLL_Zpt200_Inf=fill_obj("DYToEE_mad_Zpt200_Inf",input_DYToLL_Zpt200_Inf,"DYToEE_mad_Zpt200_Inf")
#obj_list.append(DYToLL_Zpt200_Inf)
##
#input_GJet_40_100 =["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_40To100*.root"]
#GJet_40_100=fill_obj("GJet_40_100",input_GJet_40_100,"GJet_40_100")
#obj_list.append(GJet_40_100)
#input_GJet_100_200=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_100To200*.root"]
#GJet_100_200=fill_obj("GJet_100_200",input_GJet_100_200,"GJet_100_200")
#obj_list.append(GJet_100_200)
#input_GJet_200_400=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_200To400.root"]
#GJet_200_400=fill_obj("GJet_200_400",input_GJet_200_400,"GJet_200_400")
#obj_list.append(GJet_200_400)
#input_GJet_400_600=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_400To600*.root"]
#GJet_400_600=fill_obj("GJet_400_600",input_GJet_400_600,"GJet_400_600")
#obj_list.append(GJet_400_600)
#input_GJet_600_Inf=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_600ToInf*.root"]
#GJet_600_Inf=fill_obj("GJet_600_Inf",input_GJet_600_Inf,"GJet_600_Inf")
#obj_list.append(GJet_600_Inf)


#input_DYToLL_mad=["/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/DYToLL_ele.root"]
#DYToLL_mad=fill_obj("DYToLL_mad",input_DYToLL_mad,"DYToLL_mad")
#obj_list.append(DYToLL_mad)

###################################
for obj in obj_list:
    obj.create_script()
    print " create script for %s"%(obj.name)
