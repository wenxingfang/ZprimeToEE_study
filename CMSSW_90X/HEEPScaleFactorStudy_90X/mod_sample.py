import math
import datetime

import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from mod_settings import *
from mod_variable import variables

##########################################################################################
#                                     Create samples                                     #
##########################################################################################
class sample_object:
    def __init__(self, name, crossSection, nEvents, type, color):
        self.name = name
        self.crossSection = crossSection
        self.nEvents = nEvents
        self.effectiveLumi = float(self.nEvents/self.crossSection)
        self.type = type # 'data', 'MCDY', 'MCOther'
        self.color = color
        
        self.h_2D_fit  = {}
        self.h_2D_fit_tmp  = {}
        self.h_2D_cut_tmp  = {}
        self.h_2D_cut  = {}
        self.tfile = None
        
        self.card = nominal_card
    
    def set_card(self, card):
        self.card = card
        self.tfilename = '%s%s_slices.root'%(self.card.out_ntuple_prefix,self.name)
        self.tfile = ROOT.TFile(self.tfilename,'READ')
    
    def load_histograms_from_file(self):
        for vname in self.card.variable_names:
            for rname in self.card.region_names:
                for cname in self.card.charge_names:
                    for HEEPname in self.card.HEEP_names:
                        for OSSSname in self.card.OSSS_names:
                            for aname in self.card.altCut_names:
                                for PUWname in self.card.PUW_names:
                                    for tname in self.card.tagCharge_names:
                                        suffix = '%s_%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.name, vname, rname, cname, tname, OSSSname, aname, self.card.json, HEEPname, PUWname)
                                        args = (vname,rname,cname,tname,HEEPname,OSSSname,aname,PUWname)
                                    
                                        hName_fit  = 'h_fit_%s' %suffix
                                        hName_cut  = 'h_cut_%s' %suffix
                                    
                                        self.h_2D_fit_tmp[args] = self.tfile.Get(hName_fit)
                                        if not self.h_2D_fit_tmp[args]:
                                            print 'error: not found'
                                            print hName_fit
                                            print self.tfilename 
                                        nbX_fit = self.h_2D_fit_tmp[args].GetNbinsX()
                                        nbY_fit = self.h_2D_fit_tmp[args].GetNbinsY()
                                        for binX in range(1,nbX_fit+1):
                                            self.h_2D_fit_tmp[args].SetBinContent(binX,    0,0)
                                            self.h_2D_fit_tmp[args].SetBinContent(binX,nbY_fit+1,0)
                                        for binY in range(1,nbY_fit+1):
                                            self.h_2D_fit_tmp[args].SetBinContent(    0,binY,0)
                                            self.h_2D_fit_tmp[args].SetBinContent(nbX_fit+1,binY,0)
                                     #   self.h_2D_fit[args] = self.tfile.Get(hName_fit)
                                        self.h_2D_fit[args] = self.h_2D_fit_tmp[args]
                                        
                                        self.h_2D_cut_tmp[args] = self.tfile.Get(hName_cut)
                                        nbX_cut = self.h_2D_cut_tmp[args].GetNbinsX()
                                        nbY_cut = self.h_2D_cut_tmp[args].GetNbinsY()
                                        for binX in range(1,nbX_cut+1):
                                            self.h_2D_cut_tmp[args].SetBinContent(binX,    0,0)
                                            self.h_2D_cut_tmp[args].SetBinContent(binX,nbY_cut+1,0)
                                        for binY in range(1,nbY_cut+1):
                                            self.h_2D_cut_tmp[args].SetBinContent(    0,binY,0)
                                            self.h_2D_cut_tmp[args].SetBinContent(nbX_cut+1,binY,0)
                                      ################## set the bin in Et or eta ... to 0 ###########
                                        if self.type == 'QCD':
                                            #print "%s:"%(self.name)
                                            for binX in range(1,nbX_cut+1):
                                                value=0
                                                for binY in range(1,nbY_cut+1):
                                                    value=value+ self.h_2D_cut_tmp[args].GetBinContent(binX,binY)
                                                if float(value) <= 0:
                                                    for binY in range(1,nbY_cut+1):
                                                        self.h_2D_cut_tmp[args].SetBinContent(binX,binY,0)
                                                        self.h_2D_cut_tmp[args].SetBinError(binX,binY,0)
                                      #################################################################          
                                     #   self.h_2D_cut[args] = self.tfile.Get(hName_cut)
                                        self.h_2D_cut[args] = self.h_2D_cut_tmp[args] 
                                            
    def get_fit_histogram(self, args):
        h = self.h_2D_fit[args]
        return h

    def get_cut_histogram(self, args):
        h = self.h_2D_cut[args]
        return h
samples = {}
#samples['data_golden2015D'     ] = sample_object('data_BCDEFGH_Ele27tight_newScale' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverUp'        ] = sample_object('data_BCDEFGH_Ele27tight_newScale' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverDown'      ] = sample_object('data_BCDEFGH_Ele27tight_newScale' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silver'          ] = sample_object('data_BCDEFGH_Ele27tight_newScale' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverNotGolden' ] = sample_object('data_BCDEFGH_Ele27tight_newScale' , -1,-1, 'data', ROOT.kBlack)

#samples['data_golden2015D'     ] = sample_object('data_BCDEFGH_GSFix' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverUp'        ] = sample_object('data_BCDEFGH_GSFix' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverDown'      ] = sample_object('data_BCDEFGH_GSFix' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silver'          ] = sample_object('data_BCDEFGH_GSFix' , -1,-1, 'data', ROOT.kBlack)
#samples['data_silverNotGolden' ] = sample_object('data_BCDEFGH_GSFix' , -1,-1, 'data', ROOT.kBlack)

samples['data_golden2015D'     ] = sample_object('data_BC_Ele35_noEcalDriven' , -1,-1, 'data', ROOT.kBlack)
samples['data_silverUp'        ] = sample_object('data_BC_Ele35_noEcalDriven' , -1,-1, 'data', ROOT.kBlack)
samples['data_silverDown'      ] = sample_object('data_BC_Ele35_noEcalDriven' , -1,-1, 'data', ROOT.kBlack)
samples['data_silver'          ] = sample_object('data_BC_Ele35_noEcalDriven' , -1,-1, 'data', ROOT.kBlack)
samples['data_silverNotGolden' ] = sample_object('data_BC_Ele35_noEcalDriven' , -1,-1, 'data', ROOT.kBlack)



#samples['ZToEE']   = sample_object('data_BC_Ele32_noEcalDriven',    1,  4889, 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE']   = sample_object('data_BC_Ele32_noEcalDriven_v1',    1,  4889, 'MCDY'   , ROOT.kGreen  )
samples['ZToEE']   = sample_object('data_BC_Ele32_noEcalDriven_v2',    1,  4889, 'MCDY'   , ROOT.kGreen  )

#samples['ZToEE']   = sample_object('DYToEE_amc_pt50_new',    5765.4,  77879147.0, 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE_1'] = sample_object('DYToEE_amc_pt50_100',    354.3,   38600513.0, 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE_2'] = sample_object('DYToEE_amc_pt100_250',   83.12,   29137898.0, 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE_3'] = sample_object('DYToEE_amc_pt250_400',   3.047,   7202718.0 , 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE_4'] = sample_object('DYToEE_amc_pt400_650',   0.3921,  596698.0  , 'MCDY'   , ROOT.kGreen  )
#samples['ZToEE_5'] = sample_object('DYToEE_amc_pt650_Inf',   0.03636, 666919.0  , 'MCDY'   , ROOT.kGreen  )
#
#samples['ZToTT']   = sample_object(       'ZToTT_mad',   5765.4,  46380395.0, 'MCOther', ROOT.kCyan   )
#samples['ttbar']   = sample_object(           'TTbar',   831.76,  77044310.0, 'MCOther', ROOT.kYellow )
#samples['ST']      = sample_object(              'ST',   35.6,    6952830.0,  'MCOther', ROOT.kRed )
#samples['ST_anti'] = sample_object(         'ST_anti',   35.6,    5975196.0,  'MCOther', ROOT.kRed )
#samples['WJets']   = sample_object(       'WJet_mad',    61526.7, 86006937.0, 'MCOther', ROOT.kBlue   )
#samples['WW'   ]   = sample_object(              'WW',   118.7,   580368.0,   'MCOther', ROOT.kMagenta)
#samples['WZ'   ]   = sample_object(              'WZ',   47.13,   1000000.0,  'MCOther', ROOT.kMagenta)
#samples['ZZ'   ]   = sample_object(              'ZZ',   16.523,  642912.0,   'MCOther', ROOT.kMagenta)
#samples['GamJet1'] = sample_object(     'GJet_40_100',   20790,   9183102,    'MCOther', ROOT.kCyan-10)
#samples['GamJet2'] = sample_object(    'GJet_100_200',   9238,    9313377,    'MCOther', ROOT.kCyan-10)
#samples['GamJet3'] = sample_object(    'GJet_200_400',   2305,    9971105,    'MCOther', ROOT.kCyan-10)
#samples['GamJet4'] = sample_object(    'GJet_400_600',   274.4,   4619848,    'MCOther', ROOT.kCyan-10)
#samples['GamJet5'] = sample_object(    'GJet_600_Inf',   93.46,   5022940,    'MCOther', ROOT.kCyan-10)
#samples['QCD'  ]  = sample_object(   'QCD_DYToEE_amc_new_WJet_mad_RunBCDEFGH_reMiniAOD' , 1.0, 35867,    'QCD', ROOT.kYellow-5)

for sname in samples:
    styles[sname] = style_object(samples[sname].color, 20)
 
