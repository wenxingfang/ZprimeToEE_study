##########################
#                        #
#  2017-01-16 MC         #
#                        #
##########################
dataset = {
"DYToEE_NNPDF30_13TeV-powheg-pythia8":"/DYToEE_NNPDF30_13TeV-powheg-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM",
"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1":"/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM",
"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2":"/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v2/MINIAODSIM",
"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_ext1":"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM",
"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_ext2":"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v2/MINIAODSIM",
"WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":"/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v1/MINIAODSIM",
"GJet_DoubleEMEnriched_13TeV_pythia8":"/GJet_DoubleEMEnriched_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM"
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
    config.General.workArea = 'crab_projects_MC_1019'
    config.General.transferLogs = False
    config.General.transferOutputs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'IIHE.py'
#    config.JobType.psetName = 'IIHE_PL.py'
    config.JobType.pyCfgParams = ['DataProcessing=mc2017']
#    config.JobType.inputFiles   = ['data','rcdata.2016.v3']
    config.Data.inputDBS = 'global'
    #config.Data.splitting = 'FileBased'
    #config.Data.unitsPerJob = 1
    config.Data.splitting = 'EventAwareLumiBased'
    config.Data.unitsPerJob = 20000
    config.Data.publication = False
    config.Data.ignoreLocality = True
    config.Site.storageSite = 'T2_BE_IIHE'

    for sample in dataset:
        config.General.requestName = sample
        config.Data.inputDataset = dataset[sample]
#        config.Data.outputDatasetTag = sample
        submit(config)

