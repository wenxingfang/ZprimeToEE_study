import os
##########################
#                                                    #
# Check ../python/IIHETree_cfi.py  before submit crab
#                                                    #
##########################
dataset = {
"mc2016_ZToEE_NNPDF30_13TeV-powheg_M_120_200"  :"/ZToEE_NNPDF30_13TeV-powheg_M_120_200/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
#"mc2017_ZToEE_NNPDF30_13TeV-powheg_M_120_200"  :"/ZToEE_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM",
#"mc2018_ZToEE_NNPDF30_13TeV-powheg_M_120_200"  :"/ZToEE_NNPDF30_13TeV-powheg_M_120_200/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
################################## Autumn18 ########################################################################################
#"ZToEE_NNPDF30_13TeV-powheg_M_50_120"   :"/ZToEE_NNPDF30_13TeV-powheg_M_50_120/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_120_200"  :"/ZToEE_NNPDF30_13TeV-powheg_M_120_200/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_200_400"  :"/ZToEE_NNPDF30_13TeV-powheg_M_200_400/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_400_800"  :"/ZToEE_NNPDF30_13TeV-powheg_M_400_800/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_800_1400" :"/ZToEE_NNPDF30_13TeV-powheg_M_800_1400/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_1400_2300":"/ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_2300_3500":"/ZToEE_NNPDF30_13TeV-powheg_M_2300_3500/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_3500_4500":"/ZToEE_NNPDF30_13TeV-powheg_M_3500_4500/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_4500_6000":"/ZToEE_NNPDF30_13TeV-powheg_M_4500_6000/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf" :"/ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf/RunIIAutumn18MiniAOD-NZSPU0to70_102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#"DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8":"/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM",
#'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8' :'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':'/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext5-v1/MINIAODSIM',
#'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'WZ_TuneCP5_13TeV-pythia8':'/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM',
#'WW_TuneCP5_13TeV-pythia8':'/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
#'ZZ_TuneCP5_13TeV-pythia8':'/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
#'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8':'/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8':'/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-4cores5k_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8':'/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8':'/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
#'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8':'/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
#'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8':'/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',
#'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8':'/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',
#'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8':'/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
}

nfiles = {
}

filesPerJob = {
}

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand

    def submit(config):
        res = crabCommand('submit', config = config)

    from CRABClient.UserUtilities import config
    config = config()

    name = '_mc'
    config.General.workArea = 'crab_projects_test'
    config.General.transferLogs = False
    config.General.transferOutputs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'IIHE.py'
#    config.JobType.pyCfgParams = ['DataProcessing=mc2018']
#    config.JobType.pyCfgParams = ['DataProcessing=mc2017']
    config.JobType.pyCfgParams = ['DataProcessing=mc2016']
    config.JobType.inputFiles   = ['data']
    config.Data.inputDBS = 'global'
    #config.Data.unitsPerJob = 1
#    config.Data.splitting = 'FileBased'
#    config.Data.unitsPerJob = 1 
    config.Data.splitting = 'EventAwareLumiBased'
    config.Data.unitsPerJob = 20000
    config.Data.publication = False
    config.Data.allowNonValidInputDataset = True
    config.Data.ignoreLocality = True## default is False
    config.Site.whitelist =['T2_US_*','T2_CH_*','T2_ES_*'] #if config.Data.ignoreLocality is True, default it is False
    config.Data.outLFNDirBase = '/store/user/wenxing/crab_test/'
    config.Site.storageSite = 'T2_BE_IIHE'
    config.User.voGroup     = 'becms'

    for sample in dataset:
        config.General.requestName = sample
        config.Data.inputDataset = dataset[sample]
#        config.Data.outputDatasetTag = sample
        submit(config)

