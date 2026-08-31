### HiForest Configuration
# Input: miniAOD
# Type: mc
import sys

import FWCore.ParameterSet.Config as cms
### FLAG
from Configuration.Eras.Era_Run2_2018_pp_on_AA_cff import Run2_2018_pp_on_AA
from Configuration.ProcessModifiers.run2_miniAOD_pp_on_AA_103X_cff import run2_miniAOD_pp_on_AA_103X
process = cms.Process('HiForest', Run2_2018_pp_on_AA,run2_miniAOD_pp_on_AA_103X)
#process = cms.Process('HiForest')
#process.options = cms.untracked.PSet()


###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, mc")

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    skipBadFiles = cms.untracked.bool(True),
    fileNames = cms.untracked.vstring(
        #'/store/himc/RunIISummer20UL17pp5TeVMiniAODv2/QCD_pThat-15_Dijet_TuneCP5_5p02TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_forppRef5TeV_v3-v3/40000/0B3412D3-9FD9-C344-9ECA-80B728D1CEA6.root'
        '/store/himc/HINPbPbSpring21MiniAOD/DiJet_pThat-15_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/MINIAODSIM/FixL1CaloGT_New_Release_112X_upgrade2018_realistic_HI_v9-v1/2520000/00147e49-765a-424c-a7e0-29860f11847d.root'
        #'/store/data/Run2017G/DoubleMuon/MINIAOD/UL2017_MiniAODv2-v1/110000/002B68F9-703B-0F47-AC73-CD040D50A932.root'
	),
    )


# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

# Uncomment the line below to skip the first 509 events (including the problematic one)
#process.source.skipEvents = cms.untracked.uint32(609)

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic_hi', '') ### FLAG
#process.GlobalTag = GlobalTag(process.GlobalTag, 'Autumn18_HI_V8_MC_AK3PF', '') ### FLAG
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")

'''
process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
             tag = cms.string("JPcalib_Data94X_2017pp_v2"), # data JP calib tag
            #  tag = cms.string("JPcalib_MC94X_2017pp_v2"), # mc JP calib tag
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")

         )
      ])
'''

process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("GEMRecoGeometryRcd"),
              tag = cms.string("GEMRECO_Geometry_131DD4hepV1_mc_v2"),
              connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
          )
])


###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestMiniAOD.root"))

###############################################################################
# Gen Analyzer
process.load('HeavyIonsAnalysis.EventAnalysis.HiGenAnalyzer_cfi')


# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlineSlimmedPrimaryVertices")
#process.hiEvtAnalyzer.doCentrality = cms.bool(False)
#process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_mc ### HEADS
process.hltobject.triggerNames = trigger_list_mc


'''
################################
# electrons, photons, muons
SS2018PbPbMC = "HeavyIonsAnalysis/EGMAnalysis/data/SS2018PbPbMC.dat"
process.load('HeavyIonsAnalysis.EGMAnalysis.correctedElectronProducer_cfi')
process.correctedElectrons.correctionFile = SS2018PbPbMC
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = cms.bool(True)
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.ggHiNtuplizer.electronSrc = "correctedElectrons"
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
'''
################################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_mc_cff')
process.tagInfoSequence = cms.Sequence()
process.recoJetSequence = cms.Sequence()
################################

# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
# Fix lostTracks issue for ppTracks - use empty collection since it doesn't exist in miniAOD
#process.ppTracks.lostTracksSrc = cms.InputTag("packedPFCandidates")

#muons
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
process.unpackedMuons.muonSelectors = cms.vstring()
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
process.muonAnalyzer.doGen = cms.bool(True)
process.muonAnalyzer.doSim = cms.bool(True)


# ZDC analyzer ### FLAG
#process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
#process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')
#process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')

#process.zdcanalyzer.doZDCRecHit = False
#process.zdcanalyzer.doZDCDigi = True
#process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
#process.zdcanalyzer.zdcDigiSrc = cms.InputTag("hcalDigis", "ZDC")
#process.zdcanalyzer.calZDCDigi = False
#process.zdcanalyzer.verbose = False


#################################
# rho
process.load("RecoJets.JetProducers.fixedGridRhoProducerFastjet_cfi")
process.fixedGridRhoFastjetAll.pfCandidatesTag = cms.InputTag("packedPFCandidates")
process.rhoSequence = cms.Sequence(
    process.fixedGridRhoFastjetAll
)

###############################################################################

###############################################################################
# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hltanalysis +
    process.hiEvtAnalyzer +
    process.trackSequencePbPb +
    process.unpackedMuons +
    process.muonAnalyzer +
    process.HiGenParticleAna +
    #process.tagInfoSequence +
    process.recoJetSequence +
    process.rhoSequence
)

'''
#################### D finder #################
runOnMC = False # or True, up to if it's data or MC
VtxLabel = "offlineSlimmedPrimaryVertices"
TrkLabel = "packedPFCandidates"
TrkChi2Label = "packedPFCandidateTrackChi2"
GenLabel = "prunedGenParticles"
from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X,setCutForAllChannelsDfinder
finderMaker_75X(process, runOnMC, VtxLabel, TrkLabel, TrkChi2Label, GenLabel)
# Fix muonMatch to use miniAOD collections
process.muonMatch.src = cms.InputTag("slimmedMuons")
process.muonMatch.matched = cms.InputTag("prunedGenParticles")
process.Dfinder.tkPtCut = cms.double(1.) # before fit
process.Dfinder.tkEtaCut = cms.double(2.4) # before fit
process.Dfinder.Dchannel = cms.vint32(1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0)
setCutForAllChannelsDfinder(process, dPtCut = 3, VtxChiProbCut = 0.05, svpvDistanceCut = 2.5, alphaCut = 999.)
# process.Dfinder.printInfo = cms.bool(False)
#process.dfinder = cms.Path(process.DfinderSequence)

#################### B finder #################
process.Bfinder.tkPtCut = cms.double(1.) # before fit
process.Bfinder.tkEtaCut = cms.double(2.4) # before fit
process.Bfinder.jpsiPtCut = cms.double(0.0) # before fit
process.Bfinder.Bchannel = cms.vint32(1, 1, 1, 0, 0, 0, 0)
process.Bfinder.bPtCut = cms.vdouble(3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0) # before fit
process.Bfinder.VtxChiProbCut = cms.vdouble(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
process.Bfinder.svpvDistanceCut = cms.vdouble(3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0)
process.Bfinder.MuonTriggerMatchingPath = cms.vstring("")
process.Bfinder.MuonTriggerMatchingFilter = cms.vstring("")
process.BfinderSequence.insert(0, process.unpackedMuons)
process.BfinderSequence.insert(0, process.unpackedTracksAndVertices)
#process.bfinder = cms.Path(process.BfinderSequence)
'''

## Customization
doAggregation = False
doChargedOnly = True
doLatekt_ = False

tmva_variables = ["trkIp3dSig", "trkIp2dSig", "trkDistToAxis",
                  "svtxdls", "svtxdls2d", "svtxm", "svtxmcorr",
                  "svtxnormchi2", "svtxNtrk", "svtxTrkPtOverSv",
                  "jtpt"]


jetPtMin = 45
jetAbsEtaMax = 2.5
doBtagging = True
isMC = True
# The analyzer uses this reco-to-reco match to access the embedded IP/SV tag
# information in both data and MC.
matchJets = True

doSvtx = True
doTracks = True
doAggregation = True
doHiJetID = False


jetLabel = "3"

# Generator particle processing removed - not needed for this analysis

# add candidate tagging, copy/paste to add other jet radii
from HeavyIonsAnalysis.JetAnalysis.deepNtupleSettingsFullAggregation_cff import candidateBtaggingMiniAOD
candidateBtaggingMiniAOD(
    process,
    isMC=isMC,
    jetPtMin=jetPtMin,
    jetCorrLevels=['L2Relative', 'L3Absolute'],
    doBtagging=doBtagging,
    labelR=jetLabel,
    runAggregation=doAggregation,
)
process.TrackToGenParticleMapProducer.genParticleSrc = cms.InputTag("packedGenParticles")

# setup jet analyzer
setattr(process,"ak"+jetLabel+"CsPFJetAnalyzer",process.akCs4PFJetAnalyzer.clone())
#getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetTag = "patJetsAK"+jetLabel+"PFCHSAggr"
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetTag = "selectedUpdatedPatJetsDeepFlavour"
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetName = 'ak'+jetLabel+'CsPF'
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").isMC = cms.untracked.bool(isMC)
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").matchJets = matchJets
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").doHiJetID = doHiJetID
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").matchTag = 'patJetsAK'+jetLabel+'PFUnsubJets'
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").originalCSTag = cms.InputTag("selectedUpdatedPatJetsDeepFlavour")
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetPtMin = jetPtMin
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetAbsEtaMax = cms.untracked.double(jetAbsEtaMax)
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").doPFjetID = cms.untracked.bool(True)
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").rParam = 0.4 if jetLabel=="0" else float(jetLabel)*0.1
if isMC:
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").genParticles = cms.untracked.InputTag("prunedGenParticles")
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").jetFlavourInfos = cms.InputTag("ak"+jetLabel+"PFUnsubJetFlavourInfos")
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").fillGenJets = cms.untracked.bool(True)
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").genPtMin = cms.untracked.double(10.0)
    if jetLabel != "0":
        genJetLabel = "ak"+jetLabel+("aggregatedGenJetsNoNu" if doAggregation else "GenJetsRecluster")
        getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").genjetTag = cms.InputTag(genJetLabel)

# cone size dependent but not dependent on declustering
getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").rhoSrc = cms.InputTag("fixedGridRhoFastjetAll")
#process.forest += getattr(process,"recoJetSequence")
if doBtagging:
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").useNewBtaggers = True
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").pfJetProbabilityBJetTag = cms.untracked.string("pfJetProbabilityBJetTagsDeepFlavour")
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").pfUnifiedParticleTransformerAK4JetTags = cms.untracked.string("pfUnifiedParticleTransformerAK4JetTagsDeepFlavour")
if doTracks:
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").doTracks = cms.untracked.bool(True)
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").ipTagInfoLabel = cms.untracked.string("pfImpactParameter")
if doSvtx:
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").doSvtx = cms.untracked.bool(True)
    getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer").svTagInfoLabel = cms.untracked.string("pfInclusiveSecondaryVertexFinder")
process.forest += getattr(process,"ak"+jetLabel+"CsPFJetAnalyzer")




#########################
# Jet Selection
#########################

# for b tagging SF
# process.mujetSelector = cms.EDFilter("PatJetXSelector",
#                              src = cms.InputTag("slimmedJets"),
#                              offPV = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                              cut = cms.string("pt > 5.0 && abs(rapidity()) < 3."),
#                              dummy = cms.bool(False)
#                          )
# process.recoJetSequence += process.mujetSelector
# process.ak2PFJetAnalyzer.mujetTag = cms.InputTag("mujetSelector")

#########################
# Event Selection -> add the needed filters here
#########################

process.patJetsAK3PFUnsubJets.addBTagInfo = True
process.patJetsAK3PFUnsubJets.addTagInfos = True
process.patJetsAK3PFUnsubJets.tagInfoSources = cms.VInputTag(
    "pfInclusiveSecondaryVertexFinderTagInfos",
    "pfImpactParameterTagInfos",
)
process.patJetsAK3PFUnsubJets.addDiscriminators = False

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
#process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)

#process.NoScraping = cms.EDFilter("FilterOutScraping",
# applyfilter = cms.untracked.bool(True),
# debugOn = cms.untracked.bool(False),
# numtrack = cms.untracked.uint32(10),
# thresh = cms.untracked.double(0.25),
# src = cms.untracked.InputTag("unpackedTracksAndVertices")
#)

#process.pBeamScrapingFilter=cms.Path(process.unpackedTracksAndVertices + process.NoScraping)
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pAna = cms.EndPath(process.skimanalysis)

selectedHLTPaths = cms.vstring(
    'HLT_ZeroBias_Beamspot_v*',
    'HLT_HIL1DoubleMu0_v*',
    'HLT_HIL1DoubleMuOpen_v*',
    'HLT_HIL2_L1DoubleMu10_v*',
    'HLT_HIL1MuOpen_Centrality_80_100_v*',
    'HLT_HIL1DoubleMu10_v*',
    'HLT_HIL3_L1DoubleMu10_v*',
    'HLT_HIL3DoubleMuOpen_v*',
    'HLT_HIL1DoubleMuOpen_Centrality_50_100_v*',
    'HLT_HIAK4PFJet30_v*', 'HLT_HIAK4PFJet40_v*', 'HLT_HIAK4PFJet60_v*',
    'HLT_HIAK4PFJet80_v*', 'HLT_HIAK4PFJet100_v*',
    'HLT_ZeroBias_v*',
    'HLT_HIZeroBias_part0_v*', 'HLT_HIZeroBias_part1_v*', 'HLT_HIZeroBias_part2_v*',
    'HLT_HIZeroBias_part3_v*', 'HLT_HIZeroBias_part4_v*', 'HLT_HIZeroBias_part5_v*',
    'HLT_HIZeroBias_part6_v*', 'HLT_HIZeroBias_part7_v*', 'HLT_HIZeroBias_part8_v*',
    'HLT_HIZeroBias_part9_v*', 'HLT_HIZeroBias_part10_v*', 'HLT_HIZeroBias_part11_v*'
)
process.hltanalysis.hltPaths = selectedHLTPaths
# Record the requested trigger decisions, but do not reject MC events using
# DATA HLT paths that may not exist or fire in the simulated sample.
process.skimanalysis.superFilters = cms.vstring()
