# File path will be:
# outLFNDirBase/inputDataset/requestName/time_tag/...
from CRABClient.UserUtilities import config

config = config()

config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'HIDoubleMuon_PbPb18_recipe6_080826_auto240'
config.General.workArea = '/afs/cern.ch/user/a/aholterm/crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'recipe6_DATA.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['HiForestMiniAOD.root']
config.JobType.maxMemoryMB = 3000
config.JobType.numCores = 1

config.Data.inputDataset = '/HIDoubleMuon/HIRun2018A-PbPb18_MiniAODv1-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.lumiMask = 'pbpbgolden.json'
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True

# Automatic splitting runs probe jobs and targets unitsPerJob minutes.
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 480
config.Data.totalUnits = -1

config.Data.outLFNDirBase = '/store/group/phys_heavyions/aholterm/forestIII/HIDoubleMuon_PbPb18'

config.section_('Site')
config.Site.whitelist = ['T2_FR_*', 'T2_US_*', 'T2_CH_CERN', 'T2_IN_TIFR']
config.Site.blacklist = ['T2_US_Nebraska']
config.Site.storageSite = 'T2_CH_CERN'
