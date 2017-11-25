##########################
#                        #
#  2017-01-16 MC         #
#                        #
##########################
dataset = {
'DoubleEG_Run2017B-PromptReco-v1'        : '/DoubleEG/Run2017B-PromptReco-v1/MINIAOD',
'DoubleEG_Run2017B-PromptReco-v2'        : '/DoubleEG/Run2017B-PromptReco-v2/MINIAOD',
'DoubleEG_Run2017C-PromptReco-v1'        : '/DoubleEG/Run2017C-PromptReco-v1/MINIAOD',
'DoubleEG_Run2017C-PromptReco-v2'        : '/DoubleEG/Run2017C-PromptReco-v2/MINIAOD',
'DoubleEG_Run2017C-PromptReco-v3'        : '/DoubleEG/Run2017C-PromptReco-v3/MINIAOD',
'DoubleEG_Run2017D-PromptReco-v1'        : '/DoubleEG/Run2017D-PromptReco-v1/MINIAOD',
'DoubleEG_Run2017E-PromptReco-v1'        : '/DoubleEG/Run2017E-PromptReco-v1/MINIAOD',
'DoubleEG_Run2017F-PromptReco-v1'        : '/DoubleEG/Run2017F-PromptReco-v1/MINIAOD',
'SingleElectron_Run2017B-PromptReco-v1'  : '/SingleElectron/Run2017B-PromptReco-v1/MINIAOD',
'SingleElectron_Run2017B-PromptReco-v2'  : '/SingleElectron/Run2017B-PromptReco-v2/MINIAOD',
'SingleElectron_Run2017C-PromptReco-v1'  : '/SingleElectron/Run2017C-PromptReco-v1/MINIAOD',
'SingleElectron_Run2017C-PromptReco-v2'  : '/SingleElectron/Run2017C-PromptReco-v2/MINIAOD',
'SingleElectron_Run2017C-PromptReco-v3'  : '/SingleElectron/Run2017C-PromptReco-v3/MINIAOD',
'SingleElectron_Run2017D-PromptReco-v1'  : '/SingleElectron/Run2017D-PromptReco-v1/MINIAOD',
'SingleElectron_Run2017E-PromptReco-v1'  : '/SingleElectron/Run2017E-PromptReco-v1/MINIAOD',
'SingleElectron_Run2017F-PromptReco-v1'  : '/SingleElectron/Run2017F-PromptReco-v1/MINIAOD'
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

    name = '_data'
    config.General.workArea = 'crab_projects_1116_data'
    config.General.transferLogs = False
    config.General.transferOutputs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'IIHE.py'
#    config.JobType.inputFiles   = ['data','rcdata.2016.v3']
    config.JobType.pyCfgParams = ['DataProcessing=data2017']
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = 10
    config.Data.ignoreLocality = True
    config.Data.lumiMask = '/user/wenxing/CMSSW_90X/CMSSW_9_2_6/src/UserCode/IIHETree/test/Cert_294927-306126_13TeV_PromptReco_Collisions17_JSON.txt'
    config.Site.storageSite = 'T2_BE_IIHE'

    for sample in dataset:
        config.General.requestName = sample
        config.Data.inputDataset = dataset[sample]
#        config.Data.outputDatasetTag = sample
        submit(config)

