import array
import math
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

nBins_mee = 40
lower_mee = 70
upper_mee = 110

MCGlobalScale = {}
MCGlobalScale['Barrel'    ] = 1#0.829
MCGlobalScale['Transition'] = MCGlobalScale['Barrel']
MCGlobalScale['Endcap'    ] = 1#0.775

date = '20170227'
do_poisson=False#don't use it
do_asymmetric_error=True
##########################################################################################
#                                  Configuration flags                                   #
##########################################################################################
campaign_names = ['silver','silverNotGolden','golden2015D','golden2015C25ns','golden2015BC50ns']

lumi_by_campaign = {}
lumi_by_campaign['golden2015D'     ] = 35867 
lumi_by_campaign['silver'          ] = 35867 
lumi_by_campaign['silverUp'        ] = 35867 
lumi_by_campaign['silverDown'      ] = 35867 
lumi_by_campaign['silverNotGolden' ] = 35867 
#36814  B2H
#20236  BCEDF
#16578  GH
chargeNames    = ['ep','em','ea']
tagChargeNames = ['tp','tm','ta']
strategyNames  = ['data_inc','data_exc','MC_inc','MC_exc']
#variableNames  = ['Et','eta','phi','nVtx','Pt','EtAve','nVtxL']
variableNames  = ['Et','eta','phi','nVtx','Pt']
regionNames    = ['Barrel','Transition','Endcap']
data_names     = ['SE_50ns','SE_50ns_0T','SE_25ns_golden','SE_25ns_silver','SE_25ns_silver_not_golden','SE_25ns_0T','SE_25ns_3p8T','SE_All']
OSSSNames      = ['OS','SS','AS']
HEEPNames      = ['probes','pass','fail']
#PUWNames       = ["PUW","NoPUW"]
PUWNames       = ["PUW","NoPUW","PUWrunB2F","PUWrunGH"]

altCut_names = []
altCut_names.append('nominal'        )
altCut_names.append('N_1_EcalDriven'   )
altCut_names.append('N_1_DEtaIn'       )
altCut_names.append('N_1_DPhiIn'       ) 
altCut_names.append('N_1_Shower'       )      
altCut_names.append('N_1_TrkIso'       )      
altCut_names.append('N_1_EMHD1Iso'     )     
altCut_names.append('N_1_MissHit'      )  
altCut_names.append('N_1_Dxy'          )   
altCut_names.append('N_1_HoE'          )   
altCut_names.append('N_2_Isolation'    )
altCut_names.append('N_3_Trk'          )

altCut_names.append('N_2_DetaIn_Dxy')
altCut_names.append('ProbeEt_35_50'   )
altCut_names.append('ProbeEt_50_100'   )
altCut_names.append('ProbeEt_100_inf' )
altCut_names.append('ProbeEt_300_inf' )
altCut_names.append('ProbeEt_500_inf' )




base_options = {}
base_options['do_analysis'    ] = True
base_options['do_fits'        ] = False
base_options['do_cuts'        ] = True
base_options['print_effs'     ] = True
base_options['print_effs_eta' ] = True
base_options['do_compare'     ] = True
base_options['base_histograms'] = False
base_options['kinematics'     ] = False
base_options['do_PUStudy'     ] = False

class card_object:
    def choose_fields(self, choices, default, input):
        result = []
        for choice in choices:
            if choice in input:
                result.append(choice)
        if result == []:
            result = default
        return result
        
    def __init__(self,
            name='',
            options={},
            selections={},
            ttbarScale=1.0,
            WWScale=1.0,
            WJetsScale=1.0,
            ZToTTScale=1.0,
            WZScale=1.0,
            ZZScale=1.0,
            STScale=1.0,
            ST_antiScale=1.0,
            GJ1Scale=1.0,
            GJ2Scale=1.0,
            GJ3Scale=1.0,
            GJ4Scale=1.0,
            GJ5Scale=1.0,
            QCDScale=1.0,
            mee_range=[lower_mee,upper_mee],
            campaign='silver'):
        self.name = name
        self.options = {}
        self.mee_range = mee_range
        self.charge_names    = self.choose_fields(chargeNames   , ['ea']                   , selections)
        self.tagCharge_names = self.choose_fields(tagChargeNames, ['ta']                   , selections)
        self.region_names    = self.choose_fields(regionNames   , ['Barrel','Endcap']      , selections)
        self.OSSS_names      = self.choose_fields(OSSSNames     , ['AS']                   , selections)
        self.HEEP_names      = self.choose_fields(HEEPNames     , ['probes','pass','fail']        , selections)
        self.altCut_names    = self.choose_fields(altCut_names  , ['nominal']              , selections)
        #self.variable_names  = self.choose_fields(variableNames , ['Et','eta','phi','nVtx','Pt','EtAve','nVtxL'], selections)
        self.variable_names  = self.choose_fields(variableNames , ['Et','eta','phi','nVtx','Pt'], selections)
        self.PUW_names       = self.choose_fields(PUWNames      , ['PUW']            , selections)
        self.ttbarScale = ttbarScale
        self.WWScale    = WWScale
        self.WJetsScale = WJetsScale
        self.ZToTTScale = ZToTTScale
        self.STScale = STScale
        self.ST_antiScale = ST_antiScale
        self.WZScale    = WZScale
        self.ZZScale    = ZZScale
        self.GJ1Scale    = GJ1Scale
        self.GJ2Scale    = GJ2Scale
        self.GJ3Scale    = GJ3Scale
        self.GJ4Scale    = GJ4Scale
        self.GJ5Scale    = GJ5Scale
        self.QCDScale    = QCDScale
        
        self.campaign = campaign
        self.plot_prefix = 'plots/%s/%s'%(date,self.campaign)
        self.ntuple_prefix = 'ntuples/'
        #self.out_ntuple_prefix = '%sout/'%(self.ntuple_prefix)
        self.out_ntuple_prefix = '%sout/simple/'%(self.ntuple_prefix)
        self.filename_histos = '%sTagAndProbe_histos_%s.root'%(self.out_ntuple_prefix,self.name)
        self.compare_histos  = '%sSFPlots_%s.root'%(self.out_ntuple_prefix,self.name)
        self.json = 'golden'
#        if 'silver' in self.campaign:
#            self.json = 'silver'
        if self.campaign is 'silverNotGolden':
            self.json = 'silver'
        if self.campaign is 'silver':
            self.json = 'combined'
        if self.campaign is 'silverUp':
            self.json = 'silverUp'
        if self.campaign is 'silverDown':
            self.json = 'silverDown'
        self.data_name = 'data_%s'%self.campaign
        self.lumi = 2612.9
        if self.campaign in lumi_by_campaign:
            self.lumi = lumi_by_campaign[self.campaign]
        
        for oname in base_options:
            if oname in options:
                self.options[oname] = options[oname]
            else:
                self.options[oname] = base_options[oname]

base_histo_card  = card_object(options={'base_histograms':True, 'do_cuts':False, 'print_effs':False, 'do_compare':False, 'test_fits':False}, selections=['Barrel','Transition','Endcap'])

# Nominal card for getting real results.
nominal_card     = card_object(name='nominal'    , options={'kinematics':True})
kinematic_card   = card_object(name='kinematics' , options={'kinematics':True, 'do_analysis':True, 'print_effs':False, 'do_compare':False})

# Additional results as requested.
transition_card  = card_object(name='transition' , selections=['Transition' ])

N_3_Trk_card        = card_object(name='N_3_Trk'       , selections=['N_3_Trk']       ,options={'kinematics':False})
N_2_Isolation_card  = card_object(name='N_2_Isolation' , selections=['N_2_Isolation'] ,options={'kinematics':False})
N_2_DetaIn_Dxy_card = card_object(name='N_2_DetaIn_Dxy', selections=['N_2_DetaIn_Dxy'],options={'kinematics':False})
N_1_DEtaIn_card     = card_object(name='N_1_DEtaIn'    , selections=['N_1_DEtaIn']    ,options={'kinematics':False})
N_1_DPhiIn_card     = card_object(name='N_1_DPhiIn'    , selections=['N_1_DPhiIn'  ]  ,options={'kinematics':False})
N_1_Dxy_card        = card_object(name='N_1_Dxy'       , selections=['N_1_Dxy'     ]  ,options={'kinematics':False})
N_1_EcalDriven_card = card_object(name='N_1_EcalDriven', selections=['N_1_EcalDriven'],options={'kinematics':False})
N_1_Shower_card     = card_object(name='N_1_Shower'    , selections=['N_1_Shower'  ]  ,options={'kinematics':False})
N_1_MissHit_card    = card_object(name='N_1_MissHit'   , selections=['N_1_MissHit' ]  ,options={'kinematics':False})
N_1_HoE_card        = card_object(name='N_1_HoE'       , selections=['N_1_HoE'     ]  ,options={'kinematics':False})
N_1_TrkIso_card     = card_object(name='N_1_TrkIso'    , selections=['N_1_TrkIso'  ]  ,options={'kinematics':False})
N_1_EMHD1Iso_card   = card_object(name='N_1_EMHD1Iso'  , selections=['N_1_EMHD1Iso']  ,options={'kinematics':False})

ProbeEt_35_50_card =    card_object(name='ProbeEt_35_50'   , selections=['ProbeEt_35_50'   ],options={'kinematics':True})
ProbeEt_50_100_card =    card_object(name='ProbeEt_50_100'   , selections=['ProbeEt_50_100'   ],options={'kinematics':True})
ProbeEt_75_100_card =   card_object(name='ProbeEt_75_100'  , selections=['ProbeEt_75_100'  ],options={'kinematics':True})
ProbeEt_100_inf_card =  card_object(name='ProbeEt_100_inf' , selections=['ProbeEt_100_inf' ],options={'kinematics':True})
ProbeEt_200_inf_card =  card_object(name='ProbeEt_200_inf' , selections=['ProbeEt_200_inf' ],options={'kinematics':True})
ProbeEt_300_inf_card =  card_object(name='ProbeEt_300_inf' , selections=['ProbeEt_300_inf' ],options={'kinematics':True})
ProbeEt_500_inf_card =  card_object(name='ProbeEt_500_inf' , selections=['ProbeEt_500_inf' ],options={'kinematics':True})



# Variable cards, for seeing if we are binning too coarsely or finely.
Et_card               = card_object(name='varEt'  , selections=['Et'  , 'Barrel', 'Transition', 'Endcap'], options={'print_effs':False,'do_compare':False})
eta_card              = card_object(name='varEta' , selections=['eta' , 'Barrel', 'Transition', 'Endcap'], options={'print_effs':False,'do_compare':False})
phi_card              = card_object(name='varPhi' , selections=['phi' , 'Barrel', 'Transition', 'Endcap'], options={'print_effs':False,'do_compare':False})
nVtx_card             = card_object(name='varNVtx', selections=['nVtx', 'Barrel', 'Transition', 'Endcap'], options={'print_effs':False,'do_compare':False})

# Cross checks, show results by charge, sign etc.
tagCharge_card        = card_object(name='tagCharge'   , selections=['tm','tp'])
charge_card           = card_object(name='charge'      , selections=['em','ep'])
OSSS_card             = card_object(name='OSSS'        , selections=['OS','SS'], options={'print_effs':False})
mee85To95_card        = card_object(name='tigheMeeWindow', mee_range=[85,95])

# Kinematic plots of probes which fail the ID.
#fail_card             = card_object(name='failedProbes', selections=['fail'], options={'do_analysis':False, 'print_effs':False, 'do_compare':False, 'kinematics':True})
fail_card             = card_object(name='failedProbes', selections=['probes','pass','fail'], options={'kinematics':True})

# Do the fits instead of cut and count.
fits_card             = card_object(name='fits', options={'do_cuts':False,'do_fits':True,'do_analysis':True})

# Scale stuff up and down as a cross check, and limited range.
ttbarScaleUp_card     = card_object(name='ttbarScaleUp'  , ttbarScale=1.1)#1.1
ttbarScaleDown_card   = card_object(name='ttbarScaleDown', ttbarScale=0.9)#0.9
WWScaleUp_card        = card_object(name='WWScaleUp'     ,    WWScale=1.025)
WWScaleDown_card      = card_object(name='WWScaleDown'   ,    WWScale=0.975)
WJetsScaleUp_card     = card_object(name='WJetsScaleUp'  , WJetsScale=1.5)
WJetsScaleDown_card   = card_object(name='WJetsScaleDown', WJetsScale=0.5)
ZToTTScaleUp_card     = card_object(name='ZToTTScaleUp'  , ZToTTScale=1.05)
ZToTTScaleDown_card   = card_object(name='ZToTTScaleDown', ZToTTScale=0.95)
GJ1ScaleUp_card     = card_object(name='GJ1ScaleUp'  , GJ1Scale=1.05)
GJ1ScaleDown_card   = card_object(name='GJ1ScaleDown', GJ1Scale=0.95)
GJ2ScaleUp_card     = card_object(name='GJ2ScaleUp'  , GJ2Scale=1.05)
GJ2ScaleDown_card   = card_object(name='GJ2ScaleDown', GJ2Scale=0.95)
GJ3ScaleUp_card     = card_object(name='GJ3ScaleUp'  , GJ3Scale=1.05)
GJ3ScaleDown_card   = card_object(name='GJ3ScaleDown', GJ3Scale=0.95)
GJ4ScaleUp_card     = card_object(name='GJ4ScaleUp'  , GJ4Scale=1.05)
GJ4ScaleDown_card   = card_object(name='GJ4ScaleDown', GJ4Scale=0.95)
GJ5ScaleUp_card     = card_object(name='GJ5ScaleUp'  , GJ5Scale=1.05)
GJ5ScaleDown_card   = card_object(name='GJ5ScaleDown', GJ5Scale=0.95)
QCDScaleUp_card     = card_object(name='QCDScaleUp'  , QCDScale=1.5)
QCDScaleDown_card   = card_object(name='QCDScaleDown', QCDScale=0.5)

NoIso_ttbarScaleUp_card     = card_object(name='NoIso_ttbarScaleUp'  ,selections=['N_2_Isolation'], ttbarScale=1.1)#1.1
NoIso_ttbarScaleDown_card   = card_object(name='NoIso_ttbarScaledown',selections=['N_2_Isolation'], ttbarScale=0.9)#0.9
NoIso_WWScaleUp_card        = card_object(name='NoIso_WWScaleUp'     ,selections=['N_2_Isolation'],    WWScale=1.025)
NoIso_WWScaleDown_card      = card_object(name='NoIso_WWScaleDown'   ,selections=['N_2_Isolation'],    WWScale=0.975)
NoIso_WJetsScaleUp_card     = card_object(name='NoIso_WJetsScaleUp'  ,selections=['N_2_Isolation'], WJetsScale=1.5)
NoIso_WJetsScaleDown_card   = card_object(name='NoIso_WJetsScaleDown',selections=['N_2_Isolation'], WJetsScale=0.5)
NoIso_ZToTTScaleUp_card     = card_object(name='NoIso_ZToTTScaleUp'  ,selections=['N_2_Isolation'], ZToTTScale=1.05)
NoIso_ZToTTScaleDown_card   = card_object(name='NoIso_ZToTTScaleDown',selections=['N_2_Isolation'], ZToTTScale=0.95)

NoDY_ScaleUp_card     = card_object(name='NoDYScaleUp'  , ttbarScale=1.5, WWScale=1.5, WJetsScale=1.5, ZToTTScale=1.5)
NoDY_ScaleDown_card     = card_object(name='NoDYScaleDown'  , ttbarScale=0.5, WWScale=0.5, WJetsScale=0.5, ZToTTScale=0.5)

# Different data periods.
silver_card           = card_object(name='silver'          , campaign='silver'          , options={'kinematics':True})
silverUp_card         = card_object(name='silverUp'        , campaign='silverUp'        , options={'kinematics':True})
silverDown_card       = card_object(name='silverDown'      , campaign='silverDown'      , options={'kinematics':True})
silverNotGolden_card  = card_object(name='silverNotGolden' , campaign='silverNotGolden' , options={'kinematics':True})
golden2015D_card      = card_object(name='golden2015D'     , campaign='golden2015D'     , options={'kinematics':True})
golden2015C25ns_card  = card_object(name='golden2015C25ns' , campaign='golden2015C25ns' , options={'kinematics':True})
golden2015BC50ns_card = card_object(name='golden2015BC50ns', campaign='golden2015BC50ns', options={'kinematics':True})

PUW_card              = card_object(name='PUW', campaign='silver', selections=PUWNames, options={'do_PUStudy':True, 'kinematics':True, 'do_compare':True})

deck_of_cards = []

if False:
    deck_of_cards.append(      base_histo_card)

deck_of_cards.append(         nominal_card)

#deck_of_cards.append(             PUW_card)
#deck_of_cards.append(         N_3_Trk_card)
#deck_of_cards.append(         N_2_Isolation_card)
#deck_of_cards.append(         N_2_DetaIn_Dxy_card)
#deck_of_cards.append(         N_1_EcalDriven_card)
#deck_of_cards.append(         N_1_DEtaIn_card)
#deck_of_cards.append(         N_1_DPhiIn_card)
#deck_of_cards.append(         N_1_Dxy_card)
#deck_of_cards.append(         N_1_Shower_card)
#deck_of_cards.append(         N_1_MissHit_card)
#deck_of_cards.append(         N_1_HoE_card)
#deck_of_cards.append(         N_1_TrkIso_card)
#deck_of_cards.append(         N_1_EMHD1Iso_card)
#deck_of_cards.append(         ProbeEt_35_50_card)
#deck_of_cards.append(         ProbeEt_50_100_card)
#deck_of_cards.append(         ProbeEt_100_inf_card)
#deck_of_cards.append(         ProbeEt_300_inf_card)
#deck_of_cards.append(         ProbeEt_500_inf_card)

#deck_of_cards.append(            fits_card)
#deck_of_cards.append(       kinematic_card)

#deck_of_cards.append(      transition_card)
#deck_of_cards.append(          charge_card)
#deck_of_cards.append(       tagCharge_card)
#deck_of_cards.append(            OSSS_card)

#deck_of_cards.append(   NoDY_ScaleDown_card)
#deck_of_cards.append(   NoDY_ScaleUp_card)
#deck_of_cards.append(  ttbarScaleUp_card)
#deck_of_cards.append(  ttbarScaleDown_card)
#deck_of_cards.append(  WJetsScaleUp_card)
#deck_of_cards.append(  WJetsScaleDown_card)
#deck_of_cards.append(  QCDScaleUp_card)
#deck_of_cards.append(  QCDScaleDown_card)
#deck_of_cards.append(     WWScaleUp_card)
#deck_of_cards.append(     WWScaleDown_card)
#deck_of_cards.append(    ZToTTScaleUp_card)
#deck_of_cards.append(  ZToTTScaleDown_card)

#deck_of_cards.append(    NoIso_ttbarScaleUp_card)
#deck_of_cards.append(  NoIso_ttbarScaleDown_card)
#deck_of_cards.append(       NoIso_WWScaleUp_card)
#deck_of_cards.append(     NoIso_WWScaleDown_card)
#deck_of_cards.append(    NoIso_WJetsScaleUp_card)
#deck_of_cards.append(  NoIso_WJetsScaleDown_card)
#deck_of_cards.append(    NoIso_ZToTTScaleUp_card)
#deck_of_cards.append(  NoIso_ZToTTScaleDown_card)
#deck_of_cards.append(       mee85To95_card)
#deck_of_cards.append(            fail_card)

#deck_of_cards.append(              Et_card)
#deck_of_cards.append(             eta_card)
#deck_of_cards.append(             phi_card)
#deck_of_cards.append(            nVtx_card)

#deck_of_cards.append(          silver_card)
#deck_of_cards.append( silverNotGolden_card)
#deck_of_cards.append(     golden2015D_card)

# Ignore these to save memory and CPU time
#deck_of_cards.append(        silverUp_card)
#deck_of_cards.append(      silverDown_card)
#deck_of_cards.append( golden2015C25ns_card)
#deck_of_cards.append(golden2015BC50ns_card)

##########################################################################################
#                                        Styles                                          #
##########################################################################################
class style_object:
    def __init__(self, color, marker):
        self.color  = color
        self.marker = marker
    def style_histogram(self, h):
        if "SetFillColor" in dir(h): h.SetFillColor  (self.color )
        if "SetLineColor" in dir(h): h.SetLineColor  (self.color )
        h.SetMarkerColor(self.color )
        h.SetMarkerStyle(self.marker)
        h.SetLineWidth(2)

styles = {}
if False:
    styles['data_inc'] = style_object(ROOT.kBlack  , 24)
    styles['data_exc'] = style_object(ROOT.kMagenta, 20)
    styles[  'MC_inc'] = style_object(ROOT.kRed    , 25)
    styles[  'MC_exc'] = style_object(ROOT.kBlue   , 21)
    styles[   'ratio'] = style_object(ROOT.kBlack  , 20)

styles['data_inc'] = style_object(ROOT.kGreen-2, 20)
styles['data_exc'] = style_object(ROOT.kBlue   , 20)
styles[  'MC_inc'] = style_object(ROOT.kGreen  , 21)
styles[  'MC_exc'] = style_object(ROOT.kCyan   , 21)
styles[   'ratio'] = style_object(ROOT.kBlack  , 20)

styles[      'Et'] = style_object(ROOT.kRed    , 20)
styles[      'Pt'] = style_object(ROOT.kYellow , 24)
styles[     'eta'] = style_object(ROOT.kBlue   , 21)
styles[     'phi'] = style_object(ROOT.kGreen-2, 22)
styles[    'nVtx'] = style_object(ROOT.kMagenta, 23)

##########################################################################################
#                                   General settings                                     #
##########################################################################################
debug = True
minNEventsPerFit = 100

randomNumberGenerator = ROOT.TRandom3()
randomNumberGenerator.SetSeed(1)

# Minimum and maximum of the SF plots (lower part of the compare canvas.)
ratio_min = 0.9
ratio_max = 1.1
Increase_SF_ratio=True
if Increase_SF_ratio is True:
    #ratio_min = 0.95
    #ratio_max = 1.05
    ratio_min = 0.94
    ratio_max = 1.04
SF_consider_MC_eff_error=True

hBase_mee = ROOT.TH1F('hBase_mee', '', nBins_mee, lower_mee, upper_mee)
hBase_mee.Sumw2()
hBase_mee.GetXaxis().SetTitle('m(ee) [GeV]')
hBase_mee.GetYaxis().SetTitle('efficiency (HEEP)')
hBase_mee.SetMarkerStyle(20)
hBase_mee.SetMarkerColor(ROOT.kBlack)
hBase_mee.SetLineColor(ROOT.kBlack)

hBase_chi2 = ROOT.TH1F('hBase_chi2', '', 100, 0, 10)
hBase_chi2.GetXaxis().SetTitle('#chi^{2}/n')
hBase_chi2.GetYaxis().SetTitle('fits')

canvas = ROOT.TCanvas('canvas', '', 100, 100, 1200, 800)
canvas.SetGridx()
canvas.SetGridy()

##########################################################################################
#                                Get weighted histograms                                 #
##########################################################################################
def poisson(N):
    alpha = float(1 - 0.6827)
    L =  0 if N==0  else (ROOT.Math.gamma_quantile(alpha/2,N,1.))
    U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
    return [N-L,U-N]
#    return [math.sqrt(N),math.sqrt(N)]
def get_histos_from_args(args, strname, samples, card):
    ROOT.TH1.SetDefaultSumw2()
    histos_2D_fit = {}
    histos_2D_cut = {}
    weights_to_data = {}
    weights_to_DY   = {}
    DY_lumi = samples['ZToEE'].effectiveLumi
    Name_list=[card.data_name]
    for sname in samples:
        if "data" not in sname:
            Name_list.append(sname)
#    for sname in [card.data_name,'ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
    for sname in Name_list:
        s = samples[sname]
        
        histos_2D_fit[sname] = s.get_fit_histogram(args)
        histos_2D_cut[sname] = s.get_cut_histogram(args)
        
        MCScale = 1.0
        for rname in regionNames:
            if rname in args:
                MCScale = MCGlobalScale[rname]
        weights_to_data[sname] = MCScale
        weights_to_DY  [sname] = MCScale
#        if sname in ['ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
#        if sname in ['ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
        weights_to_data[sname] *= card.lumi/s.effectiveLumi
        weights_to_DY  [sname] *=   DY_lumi/s.effectiveLumi
    for sname in samples:
        if "WJets" in sname:
            weights_to_data[sname] *=card.WJetsScale
            weights_to_DY[sname] *=card.WJetsScale
        elif "ttbar" in sname: 
            weights_to_data[sname] *=card.ttbarScale
            weights_to_DY[sname] *=card.ttbarScale
        elif "QCD" in sname: 
            weights_to_data[sname] *=card.QCDScale
            weights_to_DY[sname] *=card.QCDScale
#    weights_to_data['ttbar'] *= card.ttbarScale
#    weights_to_data['WJets'] *= card.WJetsScale
#    weights_to_data['QCD'  ] *= card.QCDScale
#    weights_to_data['WW'   ] *= card.   WWScale
#    weights_to_data['ZToTT'] *= card.ZToTTScale
#    weights_to_data['ST'] *= card.STScale
#    weights_to_data['ST_anti'] *= card.ST_antiScale
#    weights_to_data['WZ'   ] *= card.   WZScale
#    weights_to_data['ZZ'   ] *= card.   ZZScale
#    weights_to_data['GamJet1'   ] *= card.   GJ1Scale
#    weights_to_data['GamJet2'   ] *= card.   GJ2Scale
#    weights_to_data['GamJet3'   ] *= card.   GJ3Scale
#    weights_to_data['GamJet4'   ] *= card.   GJ4Scale
#    weights_to_data['GamJet5'   ] *= card.   GJ5Scale
    ###Add weight to DY
#    weights_to_DY['ttbar'] *= card.ttbarScale
#    weights_to_DY['WJets'] *= card.WJetsScale
#    weights_to_DY['QCD'       ] *= card.   QCDScale
#    weights_to_DY['ZToTT'] *= card.ZToTTScale
#    weights_to_DY['WW'   ] *= card.   WWScale
#    weights_to_DY['ST'] *= card.STScale
#    weights_to_DY['ST_anti'] *= card.ST_antiScale
#    weights_to_DY['WZ'   ] *= card.   WZScale
#    weights_to_DY['ZZ'   ] *= card.   ZZScale
#    weights_to_DY['GamJet1'   ] *= card.   GJ1Scale
#    weights_to_DY['GamJet2'   ] *= card.   GJ2Scale
#    weights_to_DY['GamJet3'   ] *= card.   GJ3Scale
#    weights_to_DY['GamJet4'   ] *= card.   GJ4Scale
#    weights_to_DY['GamJet5'   ] *= card.   GJ5Scale

    h_2D_fit = histos_2D_fit[card.data_name].Clone('h_2D_fit')
    h_2D_cut = histos_2D_cut[card.data_name].Clone('h_2D_cut')
    h_2D_fit.Scale(0.0)
    h_2D_cut.Scale(0.0)
    h_2D_fit.Sumw2()
    h_2D_cut.Sumw2()
    
    if strname=='data_inc':
        h_2D_fit.Add(histos_2D_fit[card.data_name])
        h_2D_cut.Add(histos_2D_cut[card.data_name])
    elif strname=='data_exc':
        h_2D_fit.Add(histos_2D_fit[card.data_name])
        h_2D_cut.Add(histos_2D_cut[card.data_name])
#        for sname in ['ttbar','WW','WJets','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
        for sname in Name_list:
            if "data" not in sname and "ZToEE" not in sname:
                h_2D_fit.Add(histos_2D_fit[sname], -1*weights_to_data[sname])
                h_2D_cut.Add(histos_2D_cut[sname], -1*weights_to_data[sname])
    elif strname=='MC_inc':
#        for sname in ['ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
        for sname in Name_list:
            if "data" not in sname:
                h_2D_fit.Add(histos_2D_fit[sname], 1*weights_to_DY[sname])
                h_2D_cut.Add(histos_2D_cut[sname], 1*weights_to_DY[sname])
           
    elif strname=='MC_exc':
        for sname in Name_list:
            if "ZToEE" in sname:
                h_2D_fit.Add(histos_2D_fit[sname],  1*weights_to_DY[sname])
                h_2D_cut.Add(histos_2D_cut[sname],  1*weights_to_DY[sname])
################## For ID cut  ###############################################
    histos_1D_cut = {}
    histos_1D_cut_poisson_L = {}
    histos_1D_cut_poisson_U = {}
    h_1D_cut          =histos_2D_cut[card.data_name].ProjectionX("h_cut_1D")
    h_1D_cut_poisson_L=histos_2D_cut[card.data_name].ProjectionX("h_cut_1D_poisson_L")
    h_1D_cut_poisson_U=histos_2D_cut[card.data_name].ProjectionX("h_cut_1D_poisson_U")
    h_1D_cut.Scale(0)
    h_1D_cut_poisson_L.Scale(0)
    h_1D_cut_poisson_U.Scale(0)
    if do_poisson:
#        for sname in [card.data_name,'ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
        for sname in Name_list:
            histos_1D_cut[sname]=histos_2D_cut[sname].ProjectionX(sname+"_1D")
            histos_1D_cut_poisson_L[sname]=histos_2D_cut[sname].ProjectionX(sname+"_1D_poisson_L")
            histos_1D_cut_poisson_U[sname]=histos_2D_cut[sname].ProjectionX(sname+"_1D_poisson_U")
            histos_1D_cut_poisson_L[sname].Scale(0)
            histos_1D_cut_poisson_U[sname].Scale(0)       
 
            for i in range(1, histos_1D_cut[sname].GetNbinsX()+1):
                err=[]
                err=poisson(histos_1D_cut[sname].GetBinContent(i))
                histos_1D_cut_poisson_L[sname].SetBinContent(i,float(err[0]))
                histos_1D_cut_poisson_U[sname].SetBinContent(i,float(err[1]))
                
        if strname=='data_inc':
            h_1D_cut.Add(histos_1D_cut[card.data_name])
            h_1D_cut_poisson_L.Add(histos_1D_cut_poisson_L[card.data_name])
            h_1D_cut_poisson_U.Add(histos_1D_cut_poisson_U[card.data_name])
        elif strname=='data_exc':
            h_1D_cut.Add(histos_1D_cut[card.data_name])
            h_1D_cut_poisson_L.Add(histos_1D_cut_poisson_L[card.data_name])
            h_1D_cut_poisson_U.Add(histos_1D_cut_poisson_U[card.data_name])
           # for sname in ['ttbar','WW','WJets','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
            for sname in Name_list:
                if "data" not in sname and "ZToEE" not in sname:
                    h_1D_cut.Add(histos_1D_cut[sname], -1*weights_to_data[sname])
                    for i in range(1, histos_1D_cut[sname].GetNbinsX()+1):
                        err_L=math.sqrt(math.pow(h_1D_cut_poisson_L.GetBinContent(i),2)+math.pow(weights_to_data[sname]*histos_1D_cut_poisson_L[sname].GetBinContent(i),2))
                        err_U=math.sqrt(math.pow(h_1D_cut_poisson_U.GetBinContent(i),2)+math.pow(weights_to_data[sname]*histos_1D_cut_poisson_U[sname].GetBinContent(i),2))
                        h_1D_cut_poisson_L.SetBinContent(i,float(err_L))
                        h_1D_cut_poisson_U.SetBinContent(i,float(err_U))
        elif strname=='MC_inc':
            #for sname in ['ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
            for sname in Name_list:
                if "data" not in sname:
                    h_1D_cut.Add(histos_1D_cut[sname], 1*weights_to_DY[sname])
                    for i in range(1, histos_1D_cut[sname].GetNbinsX()+1):
                        err_L=math.sqrt(math.pow(h_1D_cut_poisson_L.GetBinContent(i),2)+math.pow(weights_to_DY[sname]*histos_1D_cut_poisson_L[sname].GetBinContent(i),2))
                        err_U=math.sqrt(math.pow(h_1D_cut_poisson_U.GetBinContent(i),2)+math.pow(weights_to_DY[sname]*histos_1D_cut_poisson_U[sname].GetBinContent(i),2))
                        h_1D_cut_poisson_L.SetBinContent(i,float(err_L))
                        h_1D_cut_poisson_U.SetBinContent(i,float(err_U))
        elif strname=='MC_exc':
            for sname in Name_list:
                if "ZToEE" in sname:
                    h_1D_cut.Add(histos_1D_cut[sname], 1*weights_to_DY[sname])
                    for i in range(1, histos_1D_cut[sname].GetNbinsX()+1):
                        err_L=math.sqrt(math.pow(h_1D_cut_poisson_L.GetBinContent(i),2)+math.pow(weights_to_DY[sname]*histos_1D_cut_poisson_L[sname].GetBinContent(i),2))
                        err_U=math.sqrt(math.pow(h_1D_cut_poisson_U.GetBinContent(i),2)+math.pow(weights_to_DY[sname]*histos_1D_cut_poisson_U[sname].GetBinContent(i),2))
                        h_1D_cut_poisson_L.SetBinContent(i,float(err_L))
                        h_1D_cut_poisson_U.SetBinContent(i,float(err_U))
#######################
    if do_asymmetric_error:
        h_1D_cut.Sumw2()
#        for sname in [card.data_name,'ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
        for sname in Name_list:
            histos_1D_cut[sname]=histos_2D_cut[sname].ProjectionX(sname+"_1D",1,histos_2D_cut[sname].GetNbinsY(),"e")
        if strname=='data_inc':
            h_1D_cut.Add(histos_1D_cut[card.data_name])
        elif strname=='data_exc':
            h_1D_cut.Add(histos_1D_cut[card.data_name])
           # for sname in ['ttbar','WW','WJets','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
            for sname in Name_list:
                if "data" not in sname and "ZToEE" not in sname:
                    h_1D_cut.Add(histos_1D_cut[sname], -1*weights_to_data[sname])
        elif strname=='MC_inc':
            #for sname in ['ttbar','WW','WJets','ZToEE','ZToTT','ST','ST_anti','WZ','ZZ','QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5']:
            for sname in Name_list:
                if "data" not in sname:
                    h_1D_cut.Add(histos_1D_cut[sname], 1*weights_to_DY[sname])
        elif strname=='MC_exc':
            for sname in Name_list:
                if "ZToEE" in sname:
                    h_1D_cut.Add(histos_1D_cut[sname],  1*weights_to_DY[sname])
       


#############################################################################    
    return {'fit':h_2D_fit,'cut':h_2D_cut,'cut_1D':h_1D_cut,'cut_1D_poisson_L':h_1D_cut_poisson_L,'cut_1D_poisson_U':h_1D_cut_poisson_U}



##########################################################################################
#                                         Labels                                         #
##########################################################################################
def make_labels(args=[], chi2=0, NDof=0, chi2OverNDof=0, vartext='', lumi=0):
    labels = {}
    x1 = 0.65
    x2 = 0.85
    x3 = 0.98
    y1 = 0.85
    dy = 0.085
    
    add_CMS      = True
    add_lumibeam = True
    add_HEEP     = False
    add_region   = False
    add_sample   = False
    add_var      = False
    add_altcut   = False
    add_strategy = False
    add_OSSS     = False
    
    if 'probes' in args:
        HEEP_text = 'All probes'
        add_HEEP = True
    elif 'pass' in args:
        HEEP_text = 'Passing probes'
        add_HEEP = True
    elif 'fail' in args:
        HEEP_text = 'Failing probes'
        add_HEEP = True
    if add_HEEP:
        labels['HEEP'] = ROOT.TLatex(x1, 0.20 , HEEP_text)
        labels['HEEP'].SetTextAlign(12)
    
    sample_text = ''
    if 'data' in args:
        sample_text = 'SingleElectron Run 2016'
        add_sample = True
    if 'MCDY' in args or 'MCOther' in args or 'MC' in args:
        sample_text = 'RunIISpringDR74 MC'
        add_sample = True
    if add_sample:
        labels['sample'] = ROOT.TLatex(0.025, 0.95, sample_text)
        labels['sample'].SetTextAlign(12)
    
    strategy_text = ''
    if 'inc' in args:
        strategy_text = 'Non-DY included'
        add_strategy = True
    if 'exc' in args:
        strategy_text = 'Non-DY subtracted'
        add_strategy = True
    if add_strategy:
        labels['strategy'] = ROOT.TLatex(x2, y1-dy*0, strategy_text)
        labels['strategy'].SetTextAlign(32)
    
    OSSS_text = ''
    if 'OS' in args:
        OSSS_text = 'OS'
        add_OSSS = True
    elif 'SS' in args:
        OSSS_text = 'SS'
        add_OSSS = True
    elif 'AS' in args:
        OSSS_text = 'OS+SS'
        add_OSSS = True
    if add_OSSS:
#        labels['OSSS'] = ROOT.TLatex(x1, y1-dy*2, OSSS_text)
        labels['OSSS'] = ROOT.TLatex(0.85, y1-dy*1.5, OSSS_text)
        labels['OSSS'].SetTextAlign(12)
    
    e_text = ''
    if 'ep' in args:
        e_text = 'e^{+}'
    elif 'em' in args:
        e_text = 'e^{-}'
    elif 'ea' in args:
        e_text = 'e^{#pm}'
    
    region_text = ''
    if 'Barrel' in args:
#        region_text = 'Barrel'
        region_text = '|#eta_{%s}| < 1.4442' %(e_text)
    if 'Endcap' in args:
#        region_text = 'Endcap'
        region_text = '1.566 < |#eta_{%s}| < 2.5'%(e_text)
    if 'Transition' in args:
        region_text = '1.4442 < |#eta_{%s}| < 1.566'%(e_text)
    if 'Barrel+Endcap' in args:
        region_text = '|#eta_{%s}| < 1.4442 or 1.566 < |#eta_{%s}| < 2.5'%(e_text,e_text)
    if e_text != '' and region_text != '':
        add_region = True
    if add_region:
#        labels['region'] = ROOT.TLatex(x2, y1-dy*2, '%s %s'%(region_text,e_text))
        labels['region'] = ROOT.TLatex(x2, y1-dy*3, '%s'%(region_text))
        labels['region'].SetTextAlign(32)
    
    altcut_texts = {
      'nominal'        : '',
      'N_1_EcalDriven'   : 'EcalDriven',
      'N_3_Trk'          : '#Delta#eta_{in}^{seed}, #Delta#phi_{in},|d_{xy}|',
      'N_1_DEtaIn'       : '#Delta#eta_{in}^{seed}',
      'N_2_Isolation'    : 'trkIso, EM+HD1',
      'N_1_DPhiIn'       : '#Delta#phi_{in}',  
      'N_1_Shower'       : 'ShowerShape', 
      'N_1_TrkIso'       : 'trkIso', 
      'N_1_EMHD1Iso'     : 'EM+HD1',   
      'N_1_MissHit'      : 'MissingHit',  
      'N_1_Dxy'          : '|d_{xy}|',  
      'N_1_HoE'          : 'H/E',  
      'N_2_DetaIn_Dxy'   : '#Delta#eta_{in}^{seed},|d_{xy}|', 
      'ProbeEt_35_50'    : 'Et:35-50', 
      'ProbeEt_50_100'   : 'Et:50-100', 
      'ProbeEt_75_100'   : 'Et:75-100', 
      'ProbeEt_100_inf'  : 'Et:100-inf', 
      'ProbeEt_200_inf'  : 'Et:200-inf',
      'ProbeEt_300_inf'  : 'Et:300-inf', 
      'ProbeEt_500_inf'  : 'Et:500-inf', 
      'nominal_allPUW'   : 'Nominal'
    }
    altcut_text = ''
    for aname in altcut_texts:
        if aname in args:
            altcut_text = altcut_texts[aname]
            add_altcut = True
    if add_altcut:
#        labels['altcut'] = ROOT.TLatex(x2, 0.5, "")
        labels['altcut'] = ROOT.TLatex(x2, y1-dy*4.5, altcut_text)
        labels['altcut'].SetTextAlign(32)
    
    if add_CMS:
#        labels['CMS'] = ROOT.TLatex(x3 , 0.95, 'CMS internal')
        labels['CMS'] = ROOT.TLatex(0.35 , y1-dy*0, 'CMS internal')
        labels['CMS'].SetTextAlign(32)
        
    if add_lumibeam:
#        labels['lumibeam'] = ROOT.TLatex(x2 , y1-dy*0, '%.1f fb^{-1} 13 TeV 25 ns'%(lumi*1e-3))
        labels['lumibeam'] = ROOT.TLatex(0.85 , 0.95, '%.1f fb^{-1} 13 TeV 25 ns'%(lumi*1e-3))
        labels['lumibeam'].SetTextAlign(32)
    
    if vartext != '':
        labels['var'] = ROOT.TLatex(x1, 0.26 , vartext)
        labels['var'].SetTextAlign(12)
#    if chi2 > 1e-3:
#        labels['chi2'] = ROOT.TLatex(x1, 0.32, '#chi^{2}/ndof = %.2f/%d = %.2f'%(chi2, NDof, chi2OverNDof))
#        labels['chi2'].SetTextAlign(12)
    
    for lname in labels:
        labels[lname].SetTextSize(0.04)
        if Increase_SF_ratio is True:
            labels[lname].SetTextSize(0.08)
        labels[lname].SetNDC()
    
    return labels
