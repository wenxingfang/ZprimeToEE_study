import math
import gc
import sys
import ROOT
from array import array
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet, RooGenericPdf, RooAbsReal
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)




System_list=["nominal"]
System_list.append("normalization_scale_up_")
System_list.append("normalization_scale_down_")
#System_list.append("bgk_ttbar_scale_up_")
#System_list.append("bgk_ttbar_scale_down_")
#System_list.append("bgk_ZToTT_scale_up_")
#System_list.append("bgk_ZToTT_scale_down_")
#System_list.append("bgk_ww_scale_up_")
#System_list.append("bgk_ww_scale_down_")
#System_list.append("bgk_wz_scale_up_")
#System_list.append("bgk_wz_scale_down_")
#System_list.append("bgk_zz_scale_up_")
#System_list.append("bgk_zz_scale_down_")
#System_list.append("bgk_st_scale_up_")
#System_list.append("bgk_st_scale_down_")

########## Shape dependent#########################
System_list.append("PU_scale_up_"           )
System_list.append("PU_scale_down_"         )

System_list.append("BB_mass_scale_up_2016_"  )
System_list.append("BB_mass_scale_down_2016_")
System_list.append("BE_mass_scale_up_2016_"  )
System_list.append("BE_mass_scale_down_2016_")
System_list.append("BB_mass_scale_up_2017_"  )
System_list.append("BB_mass_scale_down_2017_")
System_list.append("BE_mass_scale_up_2017_"  )
System_list.append("BE_mass_scale_down_2017_")
System_list.append("BB_mass_scale_up_2018_"  )
System_list.append("BB_mass_scale_down_2018_")
System_list.append("BE_mass_scale_up_2018_"  )
System_list.append("BE_mass_scale_down_2018_")

System_list.append("Barrel_SF_scale_up_"  )
System_list.append("Barrel_SF_scale_down_")
System_list.append("Endcap_SF_scale_up_"  )
System_list.append("Endcap_SF_scale_down_")
System_list.append("pf_scale_up_"  )
System_list.append("pf_scale_down_")
System_list.append("pdf_scale_up_"  )
System_list.append("pdf_scale_down_")

F_tmp=ROOT.TFile("ntuples/sys_saved_hist/2016/20190621_GenM/all/hist_data_MiniAOD.root","read")

Hist_list=[]
for ih in range(0,F_tmp.GetListOfKeys().GetSize()):
    hname=F_tmp.GetListOfKeys()[ih].GetName()
    hist=F_tmp.Get(hname)
    if "TH2D" in str(type(hist)) or "TH2F" in str(type(hist)):
        continue
    Hist_list.append(hname)
print Hist_list

lumi={}
lumi['2016']=35922.0
lumi['2017']=41500.0
lumi['2018']=59401.0

Dir={}
Dir['2016']='ntuples/sys_saved_hist/2016/20190704_newBin/all/'
Dir['2017']='ntuples/sys_saved_hist/2017/20190704_newBin/all/'
Dir['2018']='ntuples/sys_saved_hist/2018/20190809_UpdateRunD/all/'
#Dir['2018']='ntuples/sys_saved_hist/2018/20190704_newBin/all/'
#Dir_out='ntuples/sys_saved_hist/Run2_final/'
Dir_out='ntuples/sys_saved_hist/Run2_final_0810/'

Normalize_factor={}
Normalize_factor['2016']={'BB_BE':0.951472,'BB':0.950691,'BE':0.953648,'EE':1.000935}
Normalize_factor['2017']={'BB_BE':0.895176,'BB':0.902374,'BE':0.874569,'EE':0.880076}
#Normalize_factor['2018']={'BB_BE':0.946177,'BB':0.949421,'BE':0.938068,'EE':0.980317}
Normalize_factor['2018']={'BB_BE':0.946127,'BB':0.949371,'BE':0.938017,'EE':0.980259}

class Sample:
    def __init__(self, name, event, xs):
        self.name =name
        self.event=event
        self.xs   =xs

Xs={}
Xs['ZToEE_50_120']   =  1975.0  
Xs['ZToEE_120_200']  =  19.32    
Xs['ZToEE_200_400']  =  2.73     
Xs['ZToEE_400_800']  =  0.241    
Xs['ZToEE_800_1400'] =  1.68E-2   
Xs['ZToEE_1400_2300']=  1.39E-3    
Xs['ZToEE_2300_3500']=  8.948E-5     
Xs['ZToEE_3500_4500']=  4.135E-6  
Xs['ZToEE_4500_6000']=  4.56E-7   
Xs['ZToEE_6000_Inf'] =  2.06E-8   

Xs['NNPDF31_ZToEE_50_120']   = 2112.90 
Xs['NNPDF31_ZToEE_120_200']  = 20.56   
Xs['NNPDF31_ZToEE_200_400']  = 2.89    
Xs['NNPDF31_ZToEE_400_800']  = 0.252   
Xs['NNPDF31_ZToEE_800_1400'] = 1.71E-2 
Xs['NNPDF31_ZToEE_1400_2300']= 1.37E-3 
Xs['NNPDF31_ZToEE_2300_3500']= 8.178E-5
Xs['NNPDF31_ZToEE_3500_4500']= 3.191E-6
Xs['NNPDF31_ZToEE_4500_6000']= 2.787E-7
Xs['NNPDF31_ZToEE_6000_Inf'] = 9.56E-9 

Xs['ZToTT']          =  5765.4   
Xs['TTbar']          =  87.31       
Xs['TTbar_500_800']  =  0.326    
Xs['TTbar_800_1200'] =  0.0326   
Xs['TTbar_1200_1800']=  3.05E-3     
Xs['TTbar_1800_Inf'] =  1.74E-4    
Xs['ST']             =  19.47    
Xs['ST_anti']        =  19.47   
Xs['WW']             =  12.178   
Xs['WW_200_600']     =  1.386    
Xs['WW_600_1200']    =  0.05665 
Xs['WW_1200_2500']   =  0.003557
Xs['WW_2500_Inf']    =  0.00005395
Xs['WZ_2L2Q']        =  6.331#5.595   
Xs['WZ_3LNu']        =  4.42965   
Xs['ZZ_2L2Nu']       =  0.564   
Xs['ZZ_2L2Q']        =  1.999   
Xs['ZZ_4L']          =  1.212   





files={}
files['ZToEE_50_120']   ={'2016':Sample('hist_ZToEE_50_120_fewz'   , 2998400.0 ,Xs['ZToEE_50_120']   ),'2017':Sample('hist_ZToEE_50_120_fewz'   ,2888223.0  ,Xs['NNPDF31_ZToEE_50_120']   )}
files['ZToEE_120_200']  ={'2016':Sample('hist_ZToEE_120_200_fewz'  , 100000.0  ,Xs['ZToEE_120_200']  ),'2017':Sample('hist_ZToEE_120_200_fewz'  ,98968.0    ,Xs['NNPDF31_ZToEE_120_200']  )}
files['ZToEE_200_400']  ={'2016':Sample('hist_ZToEE_200_400_fewz'  , 99200.0   ,Xs['ZToEE_200_400']  ),'2017':Sample('hist_ZToEE_200_400_fewz'  ,99572.0    ,Xs['NNPDF31_ZToEE_200_400']  )}
files['ZToEE_400_800']  ={'2016':Sample('hist_ZToEE_400_800_fewz'  , 100000.0  ,Xs['ZToEE_400_800']  ),'2017':Sample('hist_ZToEE_400_800_fewz'  ,99888.0    ,Xs['NNPDF31_ZToEE_400_800']  )}
files['ZToEE_800_1400'] ={'2016':Sample('hist_ZToEE_800_1400_fewz' , 100000.0  ,Xs['ZToEE_800_1400'] ),'2017':Sample('hist_ZToEE_800_1400_fewz' ,99974.0    ,Xs['NNPDF31_ZToEE_800_1400'] )}
files['ZToEE_1400_2300']={'2016':Sample('hist_ZToEE_1400_2300_fewz', 100000.0  ,Xs['ZToEE_1400_2300']),'2017':Sample('hist_ZToEE_1400_2300_fewz',99986.0    ,Xs['NNPDF31_ZToEE_1400_2300'])}
files['ZToEE_2300_3500']={'2016':Sample('hist_ZToEE_2300_3500_fewz', 100000.0  ,Xs['ZToEE_2300_3500']),'2017':Sample('hist_ZToEE_2300_3500_fewz',81440.0    ,Xs['NNPDF31_ZToEE_2300_3500'])}
files['ZToEE_3500_4500']={'2016':Sample('hist_ZToEE_3500_4500_fewz', 100000.0  ,Xs['ZToEE_3500_4500']),'2017':Sample('hist_ZToEE_3500_4500_fewz',99820.0    ,Xs['NNPDF31_ZToEE_3500_4500'])}
files['ZToEE_4500_6000']={'2016':Sample('hist_ZToEE_4500_6000_fewz', 99000.0   ,Xs['ZToEE_4500_6000']),'2017':Sample('hist_ZToEE_4500_6000_fewz',99326.0    ,Xs['NNPDF31_ZToEE_4500_6000'])}
files['ZToEE_6000_Inf'] ={'2016':Sample('hist_ZToEE_6000_Inf_fewz' , 99800.0   ,Xs['ZToEE_6000_Inf'] ),'2017':Sample('hist_ZToEE_6000_Inf_fewz' ,97935.0    ,Xs['NNPDF31_ZToEE_6000_Inf'] )}
files['ZToTT']          ={'2016':Sample('hist_ZToTT'               , 29137162.0,Xs['ZToTT']          ),'2017':Sample('hist_ZToTT'               ,123015566.0,Xs['ZToTT']                  )}
files['TTbar']          ={'2016':Sample('hist_TTbar2L_500'         , 79140880  ,Xs['TTbar']          ),'2017':Sample('hist_TTbar2L_500'         ,9511116    ,Xs['TTbar']                  )}
files['TTbar_500_800']  ={'2016':Sample('hist_TTbar2L_500_800'     , 200000    ,Xs['TTbar_500_800']  ),'2017':Sample('hist_TTbar2L_500_800'     ,755907     ,Xs['TTbar_500_800']          )}
files['TTbar_800_1200'] ={'2016':Sample('hist_TTbar2L_800_1200'    , 199800    ,Xs['TTbar_800_1200'] ),'2017':Sample('hist_TTbar2L_800_1200'    ,199636     ,Xs['TTbar_800_1200']         )}
files['TTbar_1200_1800']={'2016':Sample('hist_TTbar2L_1200_1800'   , 200000    ,Xs['TTbar_1200_1800']),'2017':Sample('hist_TTbar2L_1200_1800'   ,17507      ,Xs['TTbar_1200_1800']        )}
files['TTbar_1800_Inf'] ={'2016':Sample('hist_TTbar2L_1800_Inf'    , 40829     ,Xs['TTbar_1800_Inf'] ),'2017':Sample('hist_TTbar2L_1800_Inf'    ,953        ,Xs['TTbar_1800_Inf']         )}
files['ST']             ={'2016':Sample('hist_ST'                  , 8681495.0 ,Xs['ST']             ),'2017':Sample('hist_ST'                  ,4936387.0  ,Xs['ST']                     )}
files['ST_anti']        ={'2016':Sample('hist_ST_anti'             , 8681541.0 ,Xs['ST_anti']        ),'2017':Sample('hist_ST_anti'             ,5592819.0  ,Xs['ST_anti']                )}
files['WW']             ={'2016':Sample('hist_WW2L_200'            , 1999000.0 ,Xs['WW']             ),'2017':Sample('hist_WW2L_200'            ,1973294.0  ,Xs['WW']                     )}
files['WW_200_600']     ={'2016':Sample('hist_WW2L_200_600'        , 200000.0  ,Xs['WW_200_600']     ),'2017':Sample('hist_WW2L_200_600'        ,7922808.0  ,Xs['WW_200_600']             )}
files['WW_600_1200']    ={'2016':Sample('hist_WW2L_600_1200'       , 200000.0  ,Xs['WW_600_1200']    ),'2017':Sample('hist_WW2L_600_1200'       ,2623154.0  ,Xs['WW_600_1200']            )}
files['WW_1200_2500']   ={'2016':Sample('hist_WW2L_1200_2500'      , 200000.0  ,Xs['WW_1200_2500']   ),'2017':Sample('hist_WW2L_1200_2500'      ,161573.0   ,Xs['WW_1200_2500']           )}
files['WW_2500_Inf']    ={'2016':Sample('hist_WW2L_2500_Inf'       , 38969.0   ,Xs['WW_2500_Inf']    ),'2017':Sample('hist_WW2L_2500_Inf'       ,2349.0     ,Xs['WW_2500_Inf']            )}
files['WZ_2L2Q']        ={'2016':Sample('hist_WZ_2L2Q'             , 624225.0  ,Xs['WZ_2L2Q']        ),'2017':Sample('hist_WZ_2L2Q'             ,16534558.0 ,Xs['WZ_2L2Q']                )}
files['WZ_3LNu']        ={'2016':Sample('hist_WZ_3LNu'             , 19993200.0,Xs['WZ_3LNu']        ),'2017':Sample('hist_WZ_3LNu'             ,965938.0   ,Xs['WZ_3LNu']                )}
files['ZZ_2L2Nu']       ={'2016':Sample('hist_ZZ_2L2Nu'            , 8912125.0 ,Xs['ZZ_2L2Nu']       ),'2017':Sample('hist_ZZ_2L2Nu'            ,8733658.0  ,Xs['ZZ_2L2Nu']               )}
files['ZZ_2L2Q']        ={'2016':Sample('hist_ZZ_2L2Q'             , 496436.0  ,Xs['ZZ_2L2Q']        ),'2017':Sample('hist_ZZ_2L2Q'             ,17667929.0 ,Xs['ZZ_2L2Q']                )}
files['ZZ_4L']          ={'2016':Sample('hist_ZZ_4L'               , 6669988.0 ,Xs['ZZ_4L']          ),'2017':Sample('hist_ZZ_4L'               ,15912322.0 ,Xs['ZZ_4L']                  )}
files['ZToEE_50_120']   ['2018']=Sample('hist_ZToEE_50_120_fewz'   , 2780072.0  ,Xs['NNPDF31_ZToEE_50_120']   )
files['ZToEE_120_200']  ['2018']=Sample('hist_ZToEE_120_200_fewz'  , 99004.0    ,Xs['NNPDF31_ZToEE_120_200']  )
files['ZToEE_200_400']  ['2018']=Sample('hist_ZToEE_200_400_fewz'  , 99546.0    ,Xs['NNPDF31_ZToEE_200_400']  )
files['ZToEE_400_800']  ['2018']=Sample('hist_ZToEE_400_800_fewz'  , 99898.0    ,Xs['NNPDF31_ZToEE_400_800']  )
files['ZToEE_800_1400'] ['2018']=Sample('hist_ZToEE_800_1400_fewz' , 99972.0    ,Xs['NNPDF31_ZToEE_800_1400'] )
files['ZToEE_1400_2300']['2018']=Sample('hist_ZToEE_1400_2300_fewz', 99988.0    ,Xs['NNPDF31_ZToEE_1400_2300'])
files['ZToEE_2300_3500']['2018']=Sample('hist_ZToEE_2300_3500_fewz', 97958.0    ,Xs['NNPDF31_ZToEE_2300_3500'])
files['ZToEE_3500_4500']['2018']=Sample('hist_ZToEE_3500_4500_fewz', 99830.0    ,Xs['NNPDF31_ZToEE_3500_4500'])
files['ZToEE_4500_6000']['2018']=Sample('hist_ZToEE_4500_6000_fewz', 99368.0    ,Xs['NNPDF31_ZToEE_4500_6000'])
files['ZToEE_6000_Inf'] ['2018']=Sample('hist_ZToEE_6000_Inf_fewz' , 98162.0    ,Xs['NNPDF31_ZToEE_6000_Inf'] )
files['ZToTT']          ['2018']=Sample('hist_ZToTT_amc'           , 120782699.0,Xs['ZToTT']                  )
files['TTbar']          ['2018']=Sample('hist_TTbar2L_500'         , 60458546.0 ,Xs['TTbar']                  )
files['TTbar_500_800']  ['2018']=Sample('hist_TTbar2L_500_800'     , 755907     ,Xs['TTbar_500_800']          )
files['TTbar_800_1200'] ['2018']=Sample('hist_TTbar2L_800_1200'    , 199636     ,Xs['TTbar_800_1200']         )
files['TTbar_1200_1800']['2018']=Sample('hist_TTbar2L_1200_1800'   , 17507      ,Xs['TTbar_1200_1800']        )
files['TTbar_1800_Inf'] ['2018']=Sample('hist_TTbar2L_1800_Inf'    , 953        ,Xs['TTbar_1800_Inf']         )
files['ST']             ['2018']=Sample('hist_ST'                  , 8604210.0  ,Xs['ST']                     )
files['ST_anti']        ['2018']=Sample('hist_ST_anti'             , 6878049.0  ,Xs['ST_anti']                )
files['WW']             ['2018']=Sample('hist_WW2L_200'            , 7450398.0  ,Xs['WW']                     )
files['WW_200_600']     ['2018']=Sample('hist_WW2L_200_600'        , 7922808.0  ,Xs['WW_200_600']             )
files['WW_600_1200']    ['2018']=Sample('hist_WW2L_600_1200'       , 2623154.0  ,Xs['WW_600_1200']            )
files['WW_1200_2500']   ['2018']=Sample('hist_WW2L_1200_2500'      , 161573.0   ,Xs['WW_1200_2500']           )
files['WW_2500_Inf']    ['2018']=Sample('hist_WW2L_2500_Inf'       , 2349.0     ,Xs['WW_2500_Inf']            )
files['WZ_2L2Q']        ['2018']=Sample('hist_WZ_2L2Q'             , 23719470.0 ,Xs['WZ_2L2Q']                )
files['WZ_3LNu']        ['2018']=Sample('hist_WZ_3LNu'             , 1955248.0  ,Xs['WZ_3LNu']                )
files['ZZ_2L2Nu']       ['2018']=Sample('hist_ZZ_2L2Nu'            , 54199652.0 ,Xs['ZZ_2L2Nu']               )
files['ZZ_2L2Q']        ['2018']=Sample('hist_ZZ_2L2Q'             , 17405267.0 ,Xs['ZZ_2L2Q']                )
files['ZZ_4L']          ['2018']=Sample('hist_ZZ_4L'               , 98495102.0 ,Xs['ZZ_4L']                  )

###################### This code has memory leak, be careful########################
################# for MC ###########################################################
for sys in System_list:
    sys1=sys if sys!="nominal" else ""
    for fake in ["","_1F"]:
        str_fr=""
        if fake=="_1F":
            str_fr="_1F"
        for sample in files:
            if "pdf_scale" in sys:
                if "ZToEE" not in sample:continue
            f_out_name=Dir_out+sys1+"hist_"+sample+str_fr+".root"
            f_out=ROOT.TFile(f_out_name,"RECREATE")
            F_2016=0
            F_2017=0
            F_2018=0
            if sys in ['nominal','PU_scale_up_','PU_scale_down_',"Barrel_SF_scale_up_","Barrel_SF_scale_down_","Endcap_SF_scale_up_","Endcap_SF_scale_down_","pdf_scale_up_","pdf_scale_down_"]:
                F_2016=ROOT.TFile(Dir['2016']+sys1+files[sample]['2016'].name+str_fr+".root","read") 
                F_2017=ROOT.TFile(Dir['2017']+sys1+files[sample]['2017'].name+str_fr+".root","read") 
                F_2018=ROOT.TFile(Dir['2018']+sys1+files[sample]['2018'].name+str_fr+".root","read") 
            elif sys in ["pf_scale_up_","pf_scale_down_"]:
                F_2016=ROOT.TFile(Dir['2016']+sys1+files[sample]['2016'].name+str_fr+".root","read") 
                F_2017=ROOT.TFile(Dir['2017']+sys1+files[sample]['2017'].name+str_fr+".root","read") 
                F_2018=ROOT.TFile(Dir['2018']+""  +files[sample]['2018'].name+str_fr+".root","read") 
            elif sys in ["BB_mass_scale_up_2016_","BB_mass_scale_down_2016_","BE_mass_scale_up_2016_","BE_mass_scale_down_2016_","BB_mass_scale_up_2017_","BB_mass_scale_down_2017_","BE_mass_scale_up_2017_","BE_mass_scale_down_2017_","BB_mass_scale_up_2018_","BB_mass_scale_down_2018_","BE_mass_scale_up_2018_","BE_mass_scale_down_2018_"]:
                if "2016" in sys:
                    sys2=sys.split("2016")[0]
                    F_2016=ROOT.TFile(Dir['2016']+sys2+files[sample]['2016'].name+str_fr+".root","read") 
                    F_2017=ROOT.TFile(Dir['2017']+""  +files[sample]['2017'].name+str_fr+".root","read") 
                    F_2018=ROOT.TFile(Dir['2018']+""  +files[sample]['2018'].name+str_fr+".root","read") 
                elif "2017" in sys:
                    sys2=sys.split("2017")[0]
                    F_2016=ROOT.TFile(Dir['2016']+""  +files[sample]['2016'].name+str_fr+".root","read") 
                    F_2017=ROOT.TFile(Dir['2017']+sys2+files[sample]['2017'].name+str_fr+".root","read") 
                    F_2018=ROOT.TFile(Dir['2018']+""  +files[sample]['2018'].name+str_fr+".root","read") 
                elif "2018" in sys:
                    sys2=sys.split("2018")[0]
                    F_2016=ROOT.TFile(Dir['2016']+""  +files[sample]['2016'].name+str_fr+".root","read") 
                    F_2017=ROOT.TFile(Dir['2017']+""  +files[sample]['2017'].name+str_fr+".root","read") 
                    F_2018=ROOT.TFile(Dir['2018']+sys2+files[sample]['2018'].name+str_fr+".root","read") 
            elif sys in ['normalization_scale_up_','normalization_scale_down_']:
                F_2016=ROOT.TFile(Dir['2016']+""  +files[sample]['2016'].name+str_fr+".root","read") 
                F_2017=ROOT.TFile(Dir['2017']+""  +files[sample]['2017'].name+str_fr+".root","read") 
                F_2018=ROOT.TFile(Dir['2018']+""  +files[sample]['2018'].name+str_fr+".root","read") 
            else:print "wrong sys"
            for hist in Hist_list:
                H_2016=F_2016.Get(hist) 
                H_2017=F_2017.Get(hist) 
                H_2018=F_2018.Get(hist) 
                H_2016.Scale(lumi['2016']/(files[sample]['2016'].event/files[sample]['2016'].xs))
                H_2017.Scale(lumi['2017']/(files[sample]['2017'].event/files[sample]['2017'].xs))
                H_2018.Scale(lumi['2018']/(files[sample]['2018'].event/files[sample]['2018'].xs))
                if "BB" in hist:
                    if sys=="normalization_scale_up_":
                        H_2016.Scale(1.01*Normalize_factor['2016']['BB'])
                        H_2017.Scale(1.02*Normalize_factor['2017']['BB'])
                        H_2018.Scale(1.02*Normalize_factor['2018']['BB'])
                    elif sys=="normalization_scale_down_":
                        H_2016.Scale(0.99*Normalize_factor['2016']['BB'])
                        H_2017.Scale(0.98*Normalize_factor['2017']['BB'])
                        H_2018.Scale(0.98*Normalize_factor['2018']['BB'])
                    else:
                        H_2016.Scale(Normalize_factor['2016']['BB'])
                        H_2017.Scale(Normalize_factor['2017']['BB'])
                        H_2018.Scale(Normalize_factor['2018']['BB'])
                elif "BE" in hist:
                    if sys=="normalization_scale_up_":
                        H_2016.Scale(1.01*Normalize_factor['2016']['BE'])
                        H_2017.Scale(1.04*Normalize_factor['2017']['BE'])
                        H_2018.Scale(1.04*Normalize_factor['2018']['BE'])
                    elif sys=="normalization_scale_down_":
                        H_2016.Scale(0.99*Normalize_factor['2016']['BE'])
                        H_2017.Scale(0.96*Normalize_factor['2017']['BE'])
                        H_2018.Scale(0.96*Normalize_factor['2018']['BE'])
                    else:
                        H_2016.Scale(Normalize_factor['2016']['BE'])
                        H_2017.Scale(Normalize_factor['2017']['BE'])
                        H_2018.Scale(Normalize_factor['2018']['BE'])
                elif "EE" in hist:
                    if sys=="normalization_scale_up_":
                        H_2016.Scale(1.01*Normalize_factor['2016']['EE'])
                        H_2017.Scale(1.04*Normalize_factor['2017']['EE'])
                        H_2018.Scale(1.04*Normalize_factor['2018']['EE'])
                    elif sys=="normalization_scale_down_":
                        H_2016.Scale(0.99*Normalize_factor['2016']['EE'])
                        H_2017.Scale(0.96*Normalize_factor['2017']['EE'])
                        H_2018.Scale(0.96*Normalize_factor['2018']['EE'])
                    else:
                        H_2016.Scale(Normalize_factor['2016']['EE'])
                        H_2017.Scale(Normalize_factor['2017']['EE'])
                        H_2018.Scale(Normalize_factor['2018']['EE'])
                else:
                    if sys=="normalization_scale_up_":
                        H_2016.Scale(1.01*Normalize_factor['2016']['BB_BE'])
                        H_2017.Scale(1.02*Normalize_factor['2017']['BB_BE'])
                        H_2018.Scale(1.02*Normalize_factor['2018']['BB_BE'])
                    elif sys=="normalization_scale_down_":
                        H_2016.Scale(0.99*Normalize_factor['2016']['BB_BE'])
                        H_2017.Scale(0.98*Normalize_factor['2017']['BB_BE'])
                        H_2018.Scale(0.98*Normalize_factor['2018']['BB_BE'])
                    else:
                        H_2016.Scale(Normalize_factor['2016']['BB_BE'])
                        H_2017.Scale(Normalize_factor['2017']['BB_BE'])
                        H_2018.Scale(Normalize_factor['2018']['BB_BE'])
                H_Run2=H_2016.Clone("Run2_%s"%hist)
                H_Run2.Add(H_2017)
                H_Run2.Add(H_2018)
                f_out.cd()
                H_Run2.Write("%s"%hist)
                del H_2016
                del H_2017
                del H_2018
                del H_Run2
            f_out.Close()
            F_2016.Close()
            F_2017.Close()
            F_2018.Close()
            del f_out
            del F_2016
            del F_2017
            del F_2018
            gc.collect()
            print "%s_%s_%s"%(sys,fake,sample)
################# for data ###########################################################
for data_name in ["hist_data_MiniAOD","hist_data_FR1F_MiniAOD","hist_data_FR2F_MiniAOD"]:
    F_2016=ROOT.TFile(Dir['2016']+""  +data_name+".root","read") 
    F_2017=ROOT.TFile(Dir['2017']+""  +data_name+".root","read") 
    F_2018=ROOT.TFile(Dir['2018']+""  +data_name+".root","read") 
    f_out_name=Dir_out+data_name+".root"
    f_out=ROOT.TFile(f_out_name,"RECREATE")
    for hist in Hist_list:
        H_2016=F_2016.Get(hist) 
        H_2017=F_2017.Get(hist) 
        H_2018=F_2018.Get(hist) 
        H_Run2=H_2016.Clone("Run2_%s"%hist)
        H_Run2.Add(H_2017)
        H_Run2.Add(H_2018)
        f_out.cd()
        H_Run2.Write("%s"%hist)
    f_out.Close()
    F_2016.Close()
    F_2017.Close()
    F_2018.Close()
    del f_out
    del F_2016
    del F_2017
    del F_2018
    gc.collect()
    print "%s"%(data_name)


