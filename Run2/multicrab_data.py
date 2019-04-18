import os
#os.system('voms-proxy-init --voms cms:/cms/becms') ## init the voms-proxy
##########################
#                                                    #
# Check ../python/IIHETree_cfi.py  before submit crab
#                                                    #
##########################
dataset = {
#'Muon_Run2016C':'/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD',
'Muon_Run2017C':'/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD',
################################### 2018 ##########################
#'EGamma_Run2018A-ReReco-v2':'/EGamma/Run2018A-17Sep2018-v2/MINIAOD',
#'EGamma_Run2018B-ReReco-v1':'/EGamma/Run2018B-17Sep2018-v1/MINIAOD',
#'EGamma_Run2018C-ReReco-v1':'/EGamma/Run2018C-17Sep2018-v1/MINIAOD',
#'EGamma_Run2018D-PromptReco-v2':'/EGamma/Run2018D-22Jan2019-v2/MINIAOD'
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
    config.General.workArea = 'crab_projects_test'
    config.General.transferLogs = False
    config.General.transferOutputs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'IIHE.py'
    config.JobType.pyCfgParams = ['DataProcessing=data2017']
#    config.JobType.pyCfgParams = ['DataProcessing=data2016']
#    config.JobType.pyCfgParams = ['DataProcessing=data2018']
    config.JobType.inputFiles   = ['data']
#    config.JobType.inputFiles   = [os.environ['CMSSW_BASE'] +'/src/UserCode/IIHETree/test/data']
    config.Data.inputDBS = 'global'
#    config.Data.splitting = 'Automatic'
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = 14
    config.Data.publication = False
#    config.Data.ignoreLocality = True
#    config.Data.allowNonValidInputDataset = True
#    config.Data.lumiMask = '/user/wenxing/2018_data/CMSSW_10_4_0/src/UserCode/IIHETree/test/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
    config.Data.outLFNDirBase = '/store/user/wenxing/crab_test/'
    config.Site.storageSite = 'T2_BE_IIHE'
    config.User.voGroup     = 'becms'

    for sample in dataset:
        config.General.requestName = sample
        config.Data.inputDataset = dataset[sample]
#        config.Data.outputDatasetTag = sample
        submit(config)

