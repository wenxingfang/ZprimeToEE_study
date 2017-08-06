import math

from mod_settings import *
from mod_variable import variables
from mod_sample   import samples, sample_object

def kinematic_plots(card):
    canvas_kinematics = ROOT.TCanvas('canvas_kinematics','',100,100,800,600)
    canvas_kinematics.cd()
    size = 0.25
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw()

    canvas_kinematics_sum = ROOT.TCanvas('canvas_kinematics_sum','',100,100,800,600)
    canvas_kinematics_sum.cd()
    pad1_sum = ROOT.TPad('pad1_sum', '', 0.0, size, 1.0, 1.0, 0)
    pad2_sum = ROOT.TPad('pad2_sum', '', 0.0, 0.0, 1.0, size, 0)
    pad1_sum.Draw()
    pad2_sum.Draw()
    ROOT.TH1.SetDefaultSumw2()
    for sname in samples:
        samples[sname].load_histograms_from_file()
    
    pad1.cd()
    pad1.SetLogy(True)
    pad1.SetBottomMargin(0)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.37)
    
    pad1_sum.SetLogy(True)
    pad1_sum.SetBottomMargin(0)
    pad2_sum.SetTopMargin(0)
    pad2_sum.SetBottomMargin(0.25)

    for rname in card.region_names:
        for HEEPname in card.HEEP_names:
            for PUWname in card.PUW_names:
                stack_MC_mee  = ROOT.THStack()
                stack_MC_Et   = ROOT.THStack()
                stack_MC_EtAve   = ROOT.THStack()
                stack_MC_eta  = ROOT.THStack()
                stack_MC_eta_BE  = ROOT.THStack()
                stack_MC_phi  = ROOT.THStack()
                stack_MC_nVtx = ROOT.THStack()
                stack_MC_Pt   = ROOT.THStack()
            
                h_mee  = {}
                h_Et   = {}
                h_EtAve   = {}
                h_eta  = {}
                h_eta_BE  = {}
                h_eta_barrel  = {}
                h_eta_endcap  = {}
                h_phi  = {}
                h_nVtx = {}
                h_Pt   = {}
                sample_names_all = ['QCD','GamJet1','GamJet2','GamJet3','GamJet4','GamJet5','ST','ST_anti','WW','WZ','ZZ','WJets','WJets_1','WJets_2','WJets_3','WJets_4','WJets_5','ZToTT','ttbar','ZToEE','ZToEE_1','ZToEE_2','ZToEE_3','ZToEE_4','ZToEE_5']
                sample_names_tmp =[]
                for Name in sample_names_all:
                    if Name in samples:
                        sample_names_tmp.append(Name)
                legend_titles = {'ZToEE':'Z#rightarrowee','ttbar':'t#bar{t}','WW':'Di-Boson','WZ':'WZ','ZZ':'ZZ','WJets':'W+jets','ZToTT':'Z#rightarrow#tau#tau','ST':'Single Top','ST_anti':'Single anti-Top','QCD':'mult-jets(data)','GamJet1':'#gamma+Jet','GamJet2':'#gamma+Jet HT100-200','GamJet3':'#gamma+Jet HT200-400','GamJet4':'#gamma+Jet HT400-600','GamJet5':'#gamma+Jet HT600-Inf'}
                if samples['ZToEE'] and "DYToLL" in samples['ZToEE'].name:
                    legend_titles['ZToEE']='DY#rightarrowLL'
                sample_names_tmp_reverse = sample_names_tmp + []
                sample_names_tmp_reverse.reverse()
            
                first = True
                OSSS_name=card.OSSS_names[0]
                #OSSS_name='AS'
                #OSSS_name='OS'
                #OSSS_name='SS'
                probe_charge='ea'
                tag_charge='ta'
                altCut_names=card.altCut_names[0]
                for sname in sample_names_tmp:
                    mee_args  = ('phi' , rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    Et_args   = ('Et'  , rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                #    EtAve_args= ('EtAve', rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    eta_args  = ('eta' , rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    eta_barrel_args  = ('eta' , 'Barrel', probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    eta_endcap_args  = ('eta' , 'Endcap', probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    phi_args  = ('phi' , rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    nVtx_args = ('nVtx', rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                    Pt_args  = ('Pt' , rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)


                    h_mee [sname] = samples[sname].get_cut_histogram( mee_args).ProjectionY('h_mee_%s' %sname)
                    h_Et  [sname] = samples[sname].get_cut_histogram(  Et_args).ProjectionX('h_Et_%s'  %sname)
                #    if (sname=='QCD' or sname=="WJets") and PUWname == 'PUW':
                #        print '%s, %s, %s, Et=%f'%(sname, HEEPname, rname, h_Et  [sname].GetSumOfWeights())
                #    h_EtAve[sname] = samples[sname].get_cut_histogram(EtAve_args).ProjectionX('h_EtAve_%s'  %sname)
                    h_eta [sname] = samples[sname].get_cut_histogram( eta_args).ProjectionX('h_eta_%s' %sname)
                    h_eta_barrel [sname] = samples[sname].get_cut_histogram( eta_barrel_args).ProjectionX('h_eta_Barrel_%s' %sname)
                    h_eta_endcap [sname] = samples[sname].get_cut_histogram( eta_endcap_args).ProjectionX('h_eta_Endcap_%s' %sname)
                    h_phi [sname] = samples[sname].get_cut_histogram( phi_args).ProjectionX('h_phi_%s' %sname)
                    h_nVtx[sname] = samples[sname].get_cut_histogram(nVtx_args).ProjectionX('h_nVtx_%s'%sname)
                    h_Pt [sname] = samples[sname].get_cut_histogram( Pt_args).ProjectionX('h_Pt_%s' %sname)
                #    h_list = [h_mee[sname], h_Et[sname], h_EtAve[sname], h_eta[sname], h_eta_barrel[sname], h_eta_endcap[sname], h_phi[sname], h_nVtx[sname], h_Pt[sname]]
                    h_list = [h_mee[sname], h_Et[sname], h_eta[sname], h_eta_barrel[sname], h_eta_endcap[sname], h_phi[sname], h_nVtx[sname], h_Pt[sname]]
                    if sname == 'QCD':
                        for h_tmp in h_list:
                            for bin in range(1, h_tmp.GetNbinsX()+1):
                                if float(h_tmp.GetBinContent(bin)) <= 0:
                                    h_tmp.SetBinContent(bin,0)
                                    h_tmp.SetBinError(bin,0)
                    w = card.lumi/samples[sname].effectiveLumi
                    w *= MCGlobalScale[rname]
                    w_w = card.lumi/samples[sname].effectiveLumi
                    w_barrel= w_w*MCGlobalScale['Barrel']
                    w_endcap= w_w*MCGlobalScale['Endcap']
                    h_eta_barrel[sname].Scale(w_barrel)
                    h_eta_endcap[sname].Scale(w_endcap)
                    h_eta_BE[sname]=h_eta_barrel[sname].Clone('h_eta_Barrel+Endcap_%s' %sname)
                    h_eta_BE[sname].Sumw2()
                    h_eta_BE[sname].Add(h_eta_barrel[sname],h_eta_endcap[sname],1,1)
                    
                    N_QCD=0
                    N_QCD_error=0
                    if sname=='QCD' and HEEPname =='fail' and PUWname == 'PUW':
                        for bin in range(1,h_eta_BE[sname].GetNbinsX()+1):
                            N_QCD_error=N_QCD_error+math.pow(h_eta_BE[sname].GetBinError(bin),2)
                            N_QCD      =N_QCD+h_eta_BE[sname].GetBinContent(bin)
                        N_QCD_error=math.sqrt(N_QCD_error)
                        print 'N_QCD_error= %f'%(N_QCD_error)
                        print 'N_QCD= %f'%(N_QCD)
                    styles[sname].style_histogram(h_eta_BE[sname])
                    
                    #hs = [h_mee[sname],h_Et[sname],h_EtAve[sname] ,h_eta[sname],h_phi[sname],h_nVtx[sname],h_Pt [sname]]
                    hs = [h_mee[sname],h_Et[sname],h_eta[sname],h_phi[sname],h_nVtx[sname],h_Pt [sname]]
                    for h in hs:
                        styles[sname].style_histogram(h)
                        h.Scale(w)
                    if (sname=='QCD' or sname=="WJets") and PUWname == 'PUW':
                        print '%s, %s, %s, Et=%f'%(sname, HEEPname, rname, hs[1].GetSumOfWeights())
                    
                    if first:
                        first = False
                        h_mee ['sum'] = h_mee [sname].Clone('h_mee_sum' )
                        h_Et  ['sum'] = h_Et  [sname].Clone('h_Et_sum'  )
                    #    h_EtAve  ['sum'] = h_EtAve  [sname].Clone('h_Et_sum'  )
                        h_eta_BE  ['sum'] = h_eta_BE  [sname].Clone('h_eta_BE_sum'  )
                        h_eta ['sum'] = h_eta [sname].Clone('h_eta_sum' )
                        h_phi ['sum'] = h_phi [sname].Clone('h_phi_sum' )
                        h_nVtx['sum'] = h_nVtx[sname].Clone('h_nVtx_sum')
                        h_Pt ['sum'] = h_Pt [sname].Clone('h_Pt_sum' )
                    else:
                        h_mee ['sum'].Add(h_mee [sname])
                        h_Et  ['sum'].Add(h_Et  [sname])
                     #   h_EtAve  ['sum'].Add(h_EtAve  [sname])
                        h_eta ['sum'].Add(h_eta [sname])
                        h_eta_BE ['sum'].Add(h_eta_BE [sname])
                        h_phi ['sum'].Add(h_phi [sname])
                        h_nVtx['sum'].Add(h_nVtx[sname])
                        h_Pt ['sum'].Add(h_Pt [sname])
                
                    #print "ET: add sample %s, %s, %s, %s, last bin value %f and error %f"%(sname, rname, HEEPname, PUWname, h_Et['sum'].GetBinContent(h_Et['sum'].GetNbinsX()),h_Et['sum'].GetBinError(h_Et['sum'].GetNbinsX()))
                    stack_MC_mee .Add(h_mee [sname])
                    stack_MC_Et  .Add(h_Et  [sname])
              #      stack_MC_EtAve  .Add(h_EtAve  [sname])
                    stack_MC_eta .Add(h_eta [sname])
                    stack_MC_eta_BE .Add(h_eta_BE [sname])
                    stack_MC_phi .Add(h_phi [sname])
                    stack_MC_nVtx.Add(h_nVtx[sname])
                    stack_MC_Pt .Add(h_Pt [sname])
                h_mee['sum'].SetMarkerSize(0)
                h_mee['sum'].SetFillColor(ROOT.kBlack)
                h_mee['sum'].SetFillStyle(3244)
                h_mee['sum'].SetLineWidth(0)
                h_mee['sum'].SetLineColor(0)
                h_Et['sum'].SetMarkerSize(0)
                h_Et['sum'].SetFillColor(ROOT.kBlack)
                h_Et['sum'].SetFillStyle(3244)
                h_Et['sum'].SetLineWidth(0)
            #    h_EtAve['sum'].SetMarkerSize(0)
            #    h_EtAve['sum'].SetFillColor(ROOT.kBlack)
            #    h_EtAve['sum'].SetFillStyle(3244)
            #    h_EtAve['sum'].SetLineWidth(0)
                h_eta['sum'].SetMarkerSize(0)
                h_eta['sum'].SetFillColor(ROOT.kBlack)
                h_eta['sum'].SetFillStyle(3244)
                h_eta['sum'].SetLineWidth(0)
                h_eta_BE['sum'].SetMarkerSize(0)
                h_eta_BE['sum'].SetFillColor(ROOT.kBlack)
                h_eta_BE['sum'].SetFillStyle(3244)
                h_eta_BE['sum'].SetLineWidth(0)
                h_phi['sum'].SetMarkerSize(0)
                h_phi['sum'].SetFillColor(ROOT.kBlack)
                h_phi['sum'].SetFillStyle(3244)
                h_phi['sum'].SetLineWidth(0)
                h_nVtx['sum'].SetMarkerSize(0)
                h_nVtx['sum'].SetFillColor(ROOT.kBlack)
                h_nVtx['sum'].SetFillStyle(3244)
                h_nVtx['sum'].SetLineWidth(0)
                h_Pt['sum'].SetMarkerSize(0)
                h_Pt['sum'].SetFillColor(ROOT.kBlack)
                h_Pt['sum'].SetFillStyle(3244)
                h_Pt['sum'].SetLineWidth(0)

                legend = ROOT.TLegend(0.65, 0.5, 0.88, 0.88)
                legend.SetBorderSize(0)
                legned_list=['ZToEE','ZToTT','ST','WW','ttbar','WJets','GamJet1','QCD','DYToLL']
                #for sname in sample_names_tmp_reverse:
                #    if sname in legned_list:
                #        legend.AddEntry(h_mee[sname], legend_titles[sname], 'f')
                #legend.AddEntry(h_mee['sum'],"Uncert." , 'f')
 
                h_dummy=h_mee["ZToEE"].Clone("%s_dummy"%h_mee["ZToEE"].GetName())
                h_dummy.SetLineColor(ROOT.kBlack)
                h_dummy.SetMarkerColor(ROOT.kBlack)
                h_dummy.SetMarkerStyle(8)
                legend.AddEntry(h_dummy,"Data(Ele35)" , 'pe')
                legend.AddEntry(h_mee["ZToEE"],"Data(Ele32)" , 'f')
                
                title_size_Y = 0.06
                label_size_Y = 0.04
                title_offset_Y = 0.85

                stack_MC_mee .Draw()
                stack_MC_mee .GetYaxis().SetTitle('Number / 1 GeV/c^{2}')
                stack_MC_mee .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_mee .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_mee .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_mee .GetXaxis().SetTitle('m(ee) (GeV/c^{2})')
            
                stack_MC_Et  .Draw()
                stack_MC_Et  .GetYaxis().SetTitle('Number')
                stack_MC_Et .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_Et .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_Et .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_Et  .GetXaxis().SetTitle('E_{T} (GeV)')
            
            #    stack_MC_EtAve  .Draw()
            #    stack_MC_EtAve  .GetYaxis().SetTitle('Number')
            #    stack_MC_EtAve .GetYaxis().SetTitleSize(title_size_Y)
            #    stack_MC_EtAve .GetYaxis().SetTitleOffset(title_offset_Y);
            #    stack_MC_EtAve .GetYaxis().SetLabelSize(label_size_Y)
            #    stack_MC_EtAve  .GetXaxis().SetTitle('E_{T} (GeV)')

                stack_MC_eta .Draw()
                stack_MC_eta .GetYaxis().SetTitle('Number')
                stack_MC_eta .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_eta .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_eta .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_eta .GetXaxis().SetTitle('#eta')

                stack_MC_eta_BE .Draw()
                stack_MC_eta_BE .GetYaxis().SetTitle('Number')
                stack_MC_eta_BE .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_eta_BE .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_eta_BE .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_eta_BE .GetXaxis().SetTitle('#eta')

                stack_MC_phi .Draw()
                stack_MC_phi .GetYaxis().SetTitle('Number')
                stack_MC_phi .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_phi .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_phi .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_phi .GetXaxis().SetTitle('#phi')
            
                stack_MC_nVtx .Draw()
                stack_MC_nVtx .GetYaxis().SetTitle('Number')
                stack_MC_nVtx .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_nVtx .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_nVtx .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_nVtx .GetXaxis().SetTitle('Nvxt')
            
                stack_MC_Pt .Draw()
                stack_MC_Pt .GetYaxis().SetTitle('Number')
                stack_MC_Pt .GetYaxis().SetTitleSize(title_size_Y)
                stack_MC_Pt .GetYaxis().SetTitleOffset(title_offset_Y);
                stack_MC_Pt .GetYaxis().SetLabelSize(label_size_Y)
                stack_MC_Pt .GetXaxis().SetTitle('P_{T} (GeV/c)')

                h_data = {}
                args = ('phi', rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                h_data['mee'] = samples[card.data_name].get_cut_histogram(args).ProjectionY('h_mee_%s'%card.data_name)
               # for vname in ['Et','eta','phi','nVtx','Pt','EtAve']:
                for vname in ['Et','eta','phi','nVtx','Pt']:
                    args = (vname, rname, probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)

                    h_data[vname] = samples[card.data_name].get_cut_histogram(args).ProjectionX('h_%s_%s'%(vname,card.data_name))
                  
                args_barrel = ('eta', 'Barrel', probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)
                args_endcap = ('eta', 'Endcap', probe_charge, tag_charge, HEEPname, OSSS_name, altCut_names, PUWname)


                h_data_barrel_eta = samples[card.data_name].get_cut_histogram(args_barrel).ProjectionX('h_eta_Barrel_%s'%(card.data_name))
                h_data_endcap_eta = samples[card.data_name].get_cut_histogram(args_endcap).ProjectionX('h_eta_Endcap_%s'%(card.data_name))
                h_data_eta_BE=h_data_barrel_eta.Clone('h_eta_Barrel+Endcap_%s'%(card.data_name))
                h_data_eta_BE.Sumw2()
                h_data_eta_BE.Add(h_data_barrel_eta,h_data_endcap_eta,1,1)
                h_data['eta_BE']=h_data_eta_BE
            #    stacks = {'mee':stack_MC_mee, 'Et':stack_MC_Et, 'EtAve':stack_MC_EtAve,'eta':stack_MC_eta, 'phi':stack_MC_phi, 'nVtx':stack_MC_nVtx, 'eta_BE':stack_MC_eta_BE,'Pt':stack_MC_Pt}
            #    h_sums = {'mee':h_mee['sum'], 'Et':h_Et['sum'], 'EtAve':h_EtAve['sum'],'eta':h_eta['sum'], 'phi':h_phi['sum'], 'nVtx':h_nVtx['sum'], 'eta_BE':h_eta_BE['sum'],'Pt':h_Pt['sum']}
                stacks = {'mee':stack_MC_mee, 'Et':stack_MC_Et, 'eta':stack_MC_eta, 'phi':stack_MC_phi, 'nVtx':stack_MC_nVtx, 'eta_BE':stack_MC_eta_BE,'Pt':stack_MC_Pt}
                h_sums = {'mee':h_mee['sum'], 'Et':h_Et['sum'], 'eta':h_eta['sum'], 'phi':h_phi['sum'], 'nVtx':h_nVtx['sum'], 'eta_BE':h_eta_BE['sum'],'Pt':h_Pt['sum']}
            
                labels = make_labels(args=[rname,HEEPname,'data',OSSS_name,probe_charge], lumi=card.lumi)
                labels['region'  ].SetTextAlign(12)
                labels['CMS'] .SetX(0.15)
            
                labels['lumibeam'].SetX(0.85)
                labels['lumibeam'].SetY(0.95)
            
                labels['HEEP'    ].SetX(0.15)
                labels['HEEP'    ].SetY(0.79)
            
                labels['region'  ].SetX(0.15)
                labels['region'  ].SetY(0.73)
            
                labels['OSSS'    ].SetX(0.15)
                labels['OSSS'    ].SetY(0.67)
            
                for stack_name in stacks:
                    s = stacks[stack_name]
                    h = h_data[stack_name]
                    if stack_name=='eta_BE':
                        labels = make_labels(args=['Barrel+Endcap',HEEPname,'data',OSSS_name,probe_charge], lumi=card.lumi)
                        labels['region'  ].SetTextAlign(12)
                        labels['CMS'] .SetX(0.15)
                        labels['CMS'].SetTextAlign(12)
                        labels['lumibeam'].SetX(0.75)
                        labels['lumibeam'].SetY(0.95)
                        labels['HEEP'    ].SetX(0.15)
                        labels['HEEP'    ].SetY(0.79)
                        labels['region'  ].SetX(0.15)
                        labels['region'  ].SetY(0.73)
                        labels['OSSS'    ].SetX(0.15)
                        labels['OSSS'    ].SetY(0.67)
                    else:
                        labels = make_labels(args=[rname,HEEPname,'data',OSSS_name,probe_charge], lumi=card.lumi)
                        labels['region'  ].SetTextAlign(12)
                        labels['CMS'] .SetX(0.15)
                        labels['CMS'].SetTextAlign(12)
                        labels['lumibeam'].SetX(0.75)
                        labels['lumibeam'].SetY(0.95)
                        labels['HEEP'    ].SetX(0.15)
                        labels['HEEP'    ].SetY(0.79)
                        labels['region'  ].SetX(0.15)
                        labels['region'  ].SetY(0.73)
                        labels['OSSS'    ].SetX(0.15)
                        labels['OSSS'    ].SetY(0.67)
                    canvas_kinematics.cd()      
                    pad1.cd()
                    if stack_name=='Et' or stack_name=='EtAve':
                        pad1.SetLogx(True)
                        pad2.SetLogx(True)
                    else:
                        pad1.SetLogx(False)
                        pad2.SetLogx(False)
                    
                    #if stack_name in ['nVtx','Et','Pt','EtAve']:
                    if stack_name in ['nVtx','Et']:
                    #if stack_name in ['nVtx','Pt']:
                        pad1.SetLogy(False)
                    else: 
                        pad1.SetLogy(True)

                    h.SetMarkerStyle(8)
                    h.SetMarkerSize(0.5)
                    h.SetMarkerColor(ROOT.kBlack)
                    h.SetLineColor(ROOT.kBlack)
                    s.SetMinimum(1)
                    if stack_name in ['nVtx','Et','EtAve']:
                        s.SetMaximum(1.7*s.GetMaximum())
                    else:
                        s.SetMaximum(50000*s.GetMaximum())
                    s.Draw('hist')

                    h_sums[stack_name].Draw('sames:e2')
                    legend.Draw()
                    labels['lumibeam'].SetTextAlign(12)
                    for lname in labels:
                        labels[lname].SetTextSize(0.04)
                        labels[lname].Draw()
                    suffix = 'stack_%s_%s_%s_%s'%(stack_name,rname,HEEPname,PUWname)
                    
                    if stack_name=='eta_BE':
                        suffix = 'stack_%s_Barrel+Endcap_%s_%s'%(stack_name,HEEPname,PUWname)
                    
                    h.Draw('pe:sames')
                
                    nMC   = h_sums[stack_name].GetSumOfWeights()
                    if nMC==0:
                        print 'nMC==0'+stack_name
                    nData = h.GetSumOfWeights()

                    if stack_name=='phi':
                        print '%s, %s, %s : N mc= %d, N data= %d'%(stack_name, rname, HEEPname,  nMC, nData)
                    if nData < 1e-3:
                        continue
                    ratio = nData/nMC
                    error = ratio*math.sqrt(1/nMC+1/nData)
                    #ratio_label = ROOT.TLatex(0.15,0.60,'Data/MC=%.3f#pm%.3f'%(ratio,error))##Change
                    ratio_label = ROOT.TLatex(0.15,0.60,'Data(Ele35)/Data(Ele32)=%.3f#pm%.3f'%(ratio,error))##Change
                    ratio_label.SetNDC()
                    ratio_label.Draw()
                
                    pad2.cd()
                    pad2.SetGridy()
                    h_ratio = h.Clone('h_ratio')
                    h_ratio.Divide(h_sums[stack_name])
                    h_ratio.SetMinimum(0.5)
                    h_ratio.SetMaximum(1.5)
                    h_ratio.GetXaxis().SetTitle(s.GetXaxis().GetTitle())
                    h_ratio.GetYaxis().SetTitle('data/MC')
                    h_ratio.GetYaxis().SetNdivisions(505)
                    h_ratio.GetXaxis().SetTitleSize(0.14)
                    h_ratio.GetYaxis().SetTitleSize(0.2)
                    h_ratio.GetXaxis().SetLabelSize(0.15)
                    h_ratio.GetYaxis().SetLabelSize(0.15)
                    h_ratio.GetYaxis().SetTitleOffset(0.22)
                    h_ratio.GetXaxis().SetTitleOffset(1.2)
                    h_ratio.GetXaxis().SetMoreLogLabels()
                    h_ratio.GetXaxis().SetNoExponent()
                    h_ratio.GetXaxis().SetLabelOffset(0.01)
                    h_ratio.Draw('pe')
                
                    if abs(1.0-card.ttbarScale) > 1e-3:
                        suffix = '%s_ttbarscale%d'%(suffix,int(100*card.ttbarScale))
                    if abs(1.0-card.   WWScale) > 1e-3:
                        suffix = '%s_WWcsale%d'   %(suffix,int(100*card.   WWScale))
                    if abs(1.0-card.   ZZScale) > 1e-3:
                        suffix = '%s_ZZcsale%d'   %(suffix,int(100*card.   ZZScale))
                    if abs(1.0-card.   WZScale) > 1e-3:
                        suffix = '%s_WZcsale%d'   %(suffix,int(100*card.   WZScale))
                    if abs(1.0-card.WJetsScale) > 1e-3:
                        suffix = '%s_WJetsscale%d'%(suffix,int(100*card.WJetsScale))
                    if abs(1.0-card.ZToTTScale) > 1e-3:
                        suffix = '%s_ZToTTscale%d'%(suffix,int(100*card.ZToTTScale))
                    if abs(1.0-card.STScale) > 1e-3:
                        suffix = '%s_STscale%d'%(suffix,int(100*card.STScale))
                    if abs(1.0-card.ST_antiScale) > 1e-3:
                        suffix = '%s_ST_antiscale%d'%(suffix,int(100*card.ST_antiScale))
                    if abs(lower_mee-card.mee_range[0]) > 1e-3 or abs(upper_mee-card.mee_range[1]) > 1e-3:
                        suffix = '%s_mee%dTo%d'%(suffix,int(card.mee_range[0]),int(card.mee_range[1]))

                    canvas_kinematics.Print('%s/%s.png'%(card.plot_prefix,suffix))
                   # canvas_kinematics.Print('%s/%s.eps'%(card.plot_prefix,suffix))
##########################################################################################################

def compare_plot(ScaleFactors, labels, vname, suffix, card, file_out):
#    labels['altcut'  ].SetX(0.15)
#    labels['altcut'  ].SetX(0.70)
#    labels['altcut'  ].SetY(0.85)
    labels['OSSS'    ].SetTextAlign(32)
#    labels['altcut'  ].SetTextAlign(12)

    legend_y = 0.8
    legend_h = 0.1*len(ScaleFactors)
    if Increase_SF_ratio is True:
        legend_h=0.2
    legend = ROOT.TLegend(0.15, legend_y, 0.50, legend_y-legend_h)
    legend.SetFillStyle(0)
    legend.SetShadowColor(0)
    legend.SetBorderSize(0)
    
    legend_ratio_h = 0.15*len(ScaleFactors)
    legend_ratio = ROOT.TLegend(0.2, 1.0, 0.9, 1.0-legend_ratio_h)
    legend_ratio.SetFillStyle(0)
    legend_ratio.SetShadowColor(0)
    legend_ratio.SetBorderSize(0)
     
    canvas = ROOT.TCanvas('canvas_split_%s'%suffix, '', 0, 0, 1000, 1000)
    size = 0.2
    
    if Increase_SF_ratio is True:
        size = 0.5
       # ratio_min=0.92
       # ratio_max=1.02
    pad1 = ROOT.TPad('pad1_%s'%suffix, '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2_%s'%suffix, '', 0.0, 0.0, 1.0, size, 0)
    
    pad1.Draw()
    pad2.Draw()
    
    pad1.SetBottomMargin(0)
    pad1.SetGridx()
    pad1.SetGridy()
    
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.4)
    
    pad1.SetLogx(vname=='Et')
    pad2.SetLogx(vname=='Et')
    
    min =  1e6
    max = -1e6
    for SF in ScaleFactors:
        if SF.min < min:
            min = SF.min
        if SF.max > max:
            max = SF.max
    
    first = True # Keep track of when to add :sames to the draw options.
    
    histos = []
    for SF in ScaleFactors:
        h_numer = SF.hw_numer.h.Clone('%s_final'%SF.hw_numer.h.GetName())
        h_denom = SF.hw_denom.h.Clone('%s_final'%SF.hw_denom.h.GetName())
        h_ratio = SF.hw_ratio.h.Clone('%s_final'%SF.hw_ratio.h.GetName())
        
        # Store these so they don't get garbage collected.
        histos.append(h_numer)
        histos.append(h_denom)
        histos.append(h_ratio)
        
        for h in [h_numer,h_denom]:
            h.GetYaxis().SetTitleSize  (0.06)
            h.GetYaxis().SetTitleOffset(0.75)
            h.SetMinimum(min*0.9)
            h.SetMaximum(1.10)
            #h.SetMinimum(0.75)
            #h.SetMinimum(0.92)#for special translation situation
            #h.SetMaximum(1.12)
            if card.name =="N_3_Trk":
                h.SetMinimum(0.85)#for special translation situation
                h.SetMaximum(1.15)
            
            if Increase_SF_ratio is True:
                h.GetYaxis().SetTitleSize  (0.09)
                h.GetYaxis().SetTitleOffset(0.55)
                #h.SetMinimum(min*0.98)
        
        legend.AddEntry(h_numer, SF.hw_numer.legend, 'pl')
        legend.AddEntry(h_denom, SF.hw_denom.legend, 'f' )
        
        ratio_diff = ratio_max-ratio_min
        h_ratio.SetMinimum(ratio_min)
        h_ratio.SetMaximum(ratio_max)
      #  h_ratio.GetYaxis().SetRangeUser(ratio_min,ratio_max)
        if len(ScaleFactors) > 1:
            h_ratio.SetMaximum(ratio_min + ratio_diff*(1+0.5*len(ScaleFactors)))
        h_ratio.SetMarkerStyle(h_numer.GetMarkerStyle()+4)
        
        # Now draw the plots.
        pad1.cd()
        if first:
            h_denom.Draw('e2')
        else:
            h_denom.Draw('e2:sames')
        h_numer.Draw('pe1:sames')
        h_denom.Draw('axis:sames')
        
        for lname in labels:
            labels[lname].Draw()

        # Now the lower pad.
        pad2.cd()
        
        # Make a line at 1.0.
        line_1 = ROOT.TLine(h_ratio.GetXaxis().GetXmin(), 1.0, h_ratio.GetXaxis().GetXmax(), 1.0)
        line_1.SetLineColor(ROOT.kBlack)
        line_1.SetLineStyle(ROOT.kDashed)
        
        v = variables[vname]
        xaxis = v.latex if v.unit=='' else '%s [%s]'%(v.latex,v.unit)
        h_ratio.GetXaxis().SetTitle(xaxis)
        if vname=='Et':
            h_ratio.GetXaxis().SetNdivisions(510,False)
        h_ratio.GetYaxis().SetNdivisions(102,False)
        h_ratio.GetXaxis().SetTickLength(0.1)
    
        if Increase_SF_ratio is True:
            h_ratio.GetYaxis().SetNdivisions(10,0,0,ROOT.kFALSE)
            pad2.SetGridy()
            h_ratio.GetYaxis().SetLabelSize(0.05)
            h_ratio.GetXaxis().SetLabelSize(0.05)
            h_ratio.GetXaxis().SetTitleSize(0.1)
        # Draw the ratio plot.
        if first:
            first = False
            h_ratio.Draw('pe1')
        else:
            h_ratio.Draw('pe1:sames')
        line_1.Draw()
        h_ratio.Draw('axis:sames')
        
#        legend_text = '%s #chi^{2}/ndof = %.2f/%d, SF = %.4f (#pm %.4f)'%(SF.title, SF.chi2, SF.ndof, SF.a_value, SF.a_error)
        legend_text = '%s SF = %.4f (#pm %.4f)'%(SF.title, SF.a_value, SF.a_error)
        legend_ratio.AddEntry(h_ratio, legend_text, 'pl')
    pad1.cd()
    legend.Draw()
    
    pad2.cd()
    if len(ScaleFactors)==1:
        SF = ScaleFactors[0]
#        SF.chi2_label  .Draw()
        SF.params_label.Draw()
    else:
        legend_ratio.Draw()
    
    if abs(1.0-card.ttbarScale) > 1e-3:
        suffix = '%s_ttbarscale%d'%(suffix,int(100*card.ttbarScale))
    if abs(1.0-card.   WWScale) > 1e-3:
        suffix = '%s_WWscale%d'   %(suffix,int(100*card.   WWScale))
    if abs(1.0-card.   WZScale) > 1e-3:
        suffix = '%s_WZscale%d'   %(suffix,int(100*card.   WZScale))
    if abs(1.0-card.   ZZScale) > 1e-3:
        suffix = '%s_ZZscale%d'   %(suffix,int(100*card.   ZZScale))
    if abs(1.0-card.WJetsScale) > 1e-3:
        suffix = '%s_WJetsscale%d'%(suffix,int(100*card.WJetsScale))
    if abs(1.0-card.ZToTTScale) > 1e-3:
        suffix = '%s_ZToTTscale%d'%(suffix,int(100*card.ZToTTScale))
    if abs(1.0-card.STScale) > 1e-3:
        suffix = '%s_STscale%d'%(suffix,int(100*card.STScale))
    if abs(1.0-card.ST_antiScale) > 1e-3:
        suffix = '%s_ST_antiscale%d'%(suffix,int(100*card.ST_antiScale))
    if abs(1.0-card.   GJ1Scale) > 1e-3:
        suffix = '%s_GJ1scale%d'   %(suffix,int(100*card.   GJ1Scale))
    if abs(1.0-card.   GJ2Scale) > 1e-3:
        suffix = '%s_GJ2scale%d'   %(suffix,int(100*card.   GJ2Scale))
    if abs(1.0-card.   GJ3Scale) > 1e-3:
        suffix = '%s_GJ3scale%d'   %(suffix,int(100*card.   GJ3Scale))
    if abs(1.0-card.   GJ4Scale) > 1e-3:
        suffix = '%s_GJ4scale%d'   %(suffix,int(100*card.   GJ4Scale))
    if abs(1.0-card.   GJ5Scale) > 1e-3:
        suffix = '%s_GJ5scale%d'   %(suffix,int(100*card.   GJ5Scale))
    if abs(1.0-card.   QCDScale) > 1e-3:
        suffix = '%s_QCDscale%d'   %(suffix,int(100*card.   QCDScale))
        
    if abs(lower_mee-card.mee_range[0]) > 1e-3 or abs(upper_mee-card.mee_range[1]) > 1e-3:
        suffix = '%s_mee%dTo%d'%(suffix,int(card.mee_range[0]),int(card.mee_range[1]))
    
    canvas.Print('%s/h_compare_%s.png'%(card.plot_prefix,suffix))
   # canvas.Print('%s/h_compare_%s.eps'%(card.plot_prefix,suffix))
    
    if file_out:
        file_out.cd()
        for h in histos:
            h.Write()
    
def gr_compare_plot(ScaleFactors, labels, vname, suffix, card, file_out):
#    labels['altcut'  ].SetX(0.15)
#    labels['altcut'  ].SetX(0.70)
#    labels['altcut'  ].SetY(0.85)
    labels['OSSS'    ].SetTextAlign(32)
#    labels['altcut'  ].SetTextAlign(12)

    legend_y = 0.8
    legend_h = 0.1*len(ScaleFactors)
    if Increase_SF_ratio is True:
        legend_h=0.2
    legend = ROOT.TLegend(0.15, legend_y, 0.50, legend_y-legend_h)
    legend.SetFillStyle(0)
    legend.SetShadowColor(0)
    legend.SetBorderSize(0)
    
    legend_ratio_h = 0.15*len(ScaleFactors)
    legend_ratio = ROOT.TLegend(0.2, 1.0, 0.9, 1.0-legend_ratio_h)
    legend_ratio.SetFillStyle(0)
    legend_ratio.SetShadowColor(0)
    legend_ratio.SetBorderSize(0)
     
    canvas = ROOT.TCanvas('canvas_split_%s'%suffix, '', 0, 0, 1000, 1000)
    size = 0.2
    
    if Increase_SF_ratio is True:
        size = 0.5
       # ratio_min=0.92
       # ratio_max=1.02
    pad1 = ROOT.TPad('pad1_%s'%suffix, '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2_%s'%suffix, '', 0.0, 0.0, 1.0, size, 0)
    
    pad1.Draw()
    pad2.Draw()
    
    pad1.SetBottomMargin(0)
    pad1.SetGridx()
    pad1.SetGridy()
    
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.25)
    
    pad1.SetLogx(vname=='Et')
    pad2.SetLogx(vname=='Et')
    
    min =  1e6
    max = -1e6
    for SF in ScaleFactors:
        if SF.min < min:
            min = SF.min
        if SF.max > max:
            max = SF.max
    
    first = True # Keep track of when to add :sames to the draw options.
    
    histos = []
    for SF in ScaleFactors:
        h_numer = SF.gw_numer.h.Clone('%s_final'%SF.gw_numer.h.GetName())
        h_denom = SF.gw_denom.h.Clone('%s_final'%SF.gw_denom.h.GetName())
        h_ratio = SF.gw_ratio.h.Clone('%s_final'%SF.gw_ratio.h.GetName())
        v = variables[vname] 
        # Store these so they don't get garbage collected.
        histos.append(h_numer)
        histos.append(h_denom)
        histos.append(h_ratio)
        # Now draw the plots.
        pad1.cd()
        X_min=-2.5
        X_max=2.5
        
        for range_name in card.region_names:
            if range_name in SF.gw_numer.h.GetName() and "Barrel+Endcap" not in SF.gw_numer.h.GetName():
                X_min=v.binBoundaries_cut[range_name][0]
                X_max=v.binBoundaries_cut[range_name][-1]
            if "Barrel+Endcap" in SF.gw_numer.h.GetName(): 
                X_min=-2.5
                X_max=2.5
        Y_max=1.10
        Y_min=0.70
        #Y_min=0.9
        if "Et" in vname:
            Y_max=1.10
            Y_min=0.70
        if card.name =="N_3_Trk":
            Y_min=0.85#for special translation situation
            Y_max=1.15
        if "N_1" in card.name or "N_2" in card.name:
            Y_min=0.9#for special translation situation
            Y_max=1.1
        hpx = ROOT.TH2F("hpx","Zoomed Graph Example",1,X_min,X_max,1,Y_min,Y_max) 
        hpx.GetYaxis().SetTitle("Efficiency")
        hpx.GetYaxis().SetTitleSize  (0.09)
        hpx.GetYaxis().SetTitleOffset(0.55)
        hpx.SetStats(ROOT.kFALSE)
        hpx.Draw()
        if first:
            h_denom.SetMarkerColor(ROOT.kRed)
            h_denom.SetLineColor(ROOT.kRed)
            h_denom.SetFillColor(ROOT.kRed-10)
           # h_denom.Draw('p|>')
            h_denom.Draw('2p')
            h_denom.Draw('p')
        else:
            h_denom.Draw('ap2:sames')
        h_numer.Draw('p:sames')
        for h in [h_numer,h_denom]:
            h.GetYaxis().SetTitleSize  (0.06)
            h.GetYaxis().SetTitleOffset(0.75)
            #h.SetMinimum(0.7)
            #h.SetMaximum(1.10)
            
            if Increase_SF_ratio is True:
                h.GetYaxis().SetTitleSize  (0.09)
                h.GetYaxis().SetTitleOffset(0.55)
                #h.SetMinimum(min*0.98)
#        h_numer.GetXaxis().SetRangeUser(X_min,X_max)
#        h_denom.GetXaxis().SetRangeUser(X_min,X_max)
#        if "Et"in SF.gw_numer.h.GetName():
#            h_numer.GetXaxis().SetLimits(X_min,X_max)
#            h_denom.GetXaxis().SetLimits(X_min,X_max)
#        # Now draw the plots again.
#        if first:
#            h_denom.SetMarkerColor(ROOT.kRed)
#            h_denom.SetLineColor(ROOT.kRed)
#            h_denom.Draw('ap|>')
#        else:
#            h_denom.Draw('ap2:sames')
#        h_numer.Draw('p:sames')


#            h_ratio.GetXaxis().SetLimits(35,700)
        
        for lname in labels:
            labels[lname].Draw()
        #legend.AddEntry(h_numer, SF.gw_numer.legend, 'ple')
        #legend.AddEntry(h_denom, SF.gw_denom.legend, 'fple' )
        legend.AddEntry(h_numer, "Data(Ele35)", 'ple')
        legend.AddEntry(h_denom, "Data(Ele32)", 'fple' )

        # Now the lower pad.
        pad2.cd()
        
        hpx_1 = ROOT.TH2F("hpx1","Zoomed Graph Example",1,X_min,X_max,1,ratio_min,ratio_max) 
        hpx_1.SetStats(ROOT.kFALSE)
        v = variables[vname]
        xaxis = v.latex if v.unit=='' else '%s [%s]'%(v.latex,v.unit)
        hpx_1.GetXaxis().SetTitle(xaxis)
        hpx_1.GetYaxis().SetNdivisions(102,False)
        hpx_1.GetYaxis().SetTitle("scale factor")
        hpx_1.GetYaxis().CenterTitle()
        hpx_1.GetXaxis().SetTickLength(0.1)
        if Increase_SF_ratio is True:
            hpx_1.GetYaxis().SetNdivisions(10,0,0,ROOT.kFALSE)
            pad2.SetGridy()
            hpx_1.GetYaxis().SetLabelSize(0.05)
            hpx_1.GetXaxis().SetLabelSize(0.05)
            hpx_1.GetXaxis().SetTitleSize(0.1)
            hpx_1.GetYaxis().SetTitleSize(0.08)
            hpx_1.GetYaxis().SetTitleOffset(0.6)
        hpx_1.GetXaxis().SetMoreLogLabels()
        hpx_1.GetXaxis().SetNoExponent()
        hpx_1.Draw()
        # Make a line at 1.0.
        #line_1 = ROOT.TLine(h_ratio.GetXaxis().GetXmin(), 1.0, h_ratio.GetXaxis().GetXmax(), 1.0)
        line_1 = ROOT.TLine(X_min, 1.0, X_max, 1.0)
        line_1.SetLineColor(ROOT.kBlack)
        line_1.SetLineStyle(ROOT.kDashed)
        line_1.Draw()
        # Draw the ratio plot.
        if first:
            first = False
           # h_ratio.Draw('ap')
            h_ratio.Draw('p0')
        else:
            h_ratio.Draw('p:sames')
        
        v = variables[vname]
        xaxis = v.latex if v.unit=='' else '%s [%s]'%(v.latex,v.unit)
        h_ratio.GetXaxis().SetTitle(xaxis)
        h_ratio.GetYaxis().SetNdivisions(102,False)
        h_ratio.GetXaxis().SetTickLength(0.1)
        if Increase_SF_ratio is True:
            h_ratio.GetYaxis().SetNdivisions(10,0,0,ROOT.kFALSE)
            pad2.SetGridy()
            h_ratio.GetYaxis().SetLabelSize(0.05)
            h_ratio.GetXaxis().SetLabelSize(0.05)
            h_ratio.GetXaxis().SetTitleSize(0.1)
        ratio_diff = ratio_max-ratio_min
        h_ratio.GetXaxis().SetMoreLogLabels()
        h_ratio.GetXaxis().SetNoExponent()
        if len(ScaleFactors) > 1:
            h_ratio.SetMaximum(ratio_min + ratio_diff*(1+0.5*len(ScaleFactors)))
        h_ratio.SetMarkerStyle(h_numer.GetMarkerStyle()+4)
        
        legend_text = '%s SF = %.4f (#pm %.4f)'%(SF.title, SF.a_value, SF.a_error)
        legend_ratio.AddEntry(h_ratio, legend_text, 'pl')
        # Draw the ratio plot.
#        if first:
#            first = False
#            h_ratio.Draw('ap')
#        else:
#            h_ratio.Draw('p:sames')
    
    pad1.cd()
    legend.Draw()
    
    pad2.cd()
    if len(ScaleFactors)==1:
        SF = ScaleFactors[0]
#        SF.chi2_label  .Draw()
        SF.params_label.Draw()
    else:
        legend_ratio.Draw()
    
    if abs(1.0-card.ttbarScale) > 1e-3:
        suffix = '%s_ttbarscale%d'%(suffix,int(100*card.ttbarScale))
    if abs(1.0-card.   WWScale) > 1e-3:
        suffix = '%s_WWscale%d'   %(suffix,int(100*card.   WWScale))
    if abs(1.0-card.   WZScale) > 1e-3:
        suffix = '%s_WZscale%d'   %(suffix,int(100*card.   WZScale))
    if abs(1.0-card.   ZZScale) > 1e-3:
        suffix = '%s_ZZscale%d'   %(suffix,int(100*card.   ZZScale))
    if abs(1.0-card.WJetsScale) > 1e-3:
        suffix = '%s_WJetsscale%d'%(suffix,int(100*card.WJetsScale))
    if abs(1.0-card.ZToTTScale) > 1e-3:
        suffix = '%s_ZToTTscale%d'%(suffix,int(100*card.ZToTTScale))
    if abs(1.0-card.STScale) > 1e-3:
        suffix = '%s_STscale%d'%(suffix,int(100*card.STScale))
    if abs(1.0-card.ST_antiScale) > 1e-3:
        suffix = '%s_ST_antiscale%d'%(suffix,int(100*card.ST_antiScale))
    if abs(1.0-card.   GJ1Scale) > 1e-3:
        suffix = '%s_GJ1scale%d'   %(suffix,int(100*card.   GJ1Scale))
    if abs(1.0-card.   GJ2Scale) > 1e-3:
        suffix = '%s_GJ2scale%d'   %(suffix,int(100*card.   GJ2Scale))
    if abs(1.0-card.   GJ3Scale) > 1e-3:
        suffix = '%s_GJ3scale%d'   %(suffix,int(100*card.   GJ3Scale))
    if abs(1.0-card.   GJ4Scale) > 1e-3:
        suffix = '%s_GJ4scale%d'   %(suffix,int(100*card.   GJ4Scale))
    if abs(1.0-card.   GJ5Scale) > 1e-3:
        suffix = '%s_GJ5scale%d'   %(suffix,int(100*card.   GJ5Scale))
    if abs(1.0-card.   QCDScale) > 1e-3:
        suffix = '%s_QCDscale%d'   %(suffix,int(100*card.   QCDScale))
        
    if abs(lower_mee-card.mee_range[0]) > 1e-3 or abs(upper_mee-card.mee_range[1]) > 1e-3:
        suffix = '%s_mee%dTo%d'%(suffix,int(card.mee_range[0]),int(card.mee_range[1]))
    
    canvas.Print('%s/g_compare_%s.png'%(card.plot_prefix,suffix))
    
    if file_out:
        file_out.cd()
        for h in histos:
            h.Write()
    
def compare_plot_xmas(ScaleFactors, labels, vname, suffix, card, file_out):
    labels['altcut'  ].SetX(0.15)
    labels['altcut'  ].SetY(0.85)
    labels['OSSS'    ].SetTextAlign(32)
    labels['altcut'  ].SetTextAlign(12)

    legend_y = 0.8
    legend_h = 0.1*len(ScaleFactors)
    legend = ROOT.TLegend(0.15, legend_y, 0.50, legend_y-legend_h)
    legend.SetFillStyle(0)
    legend.SetShadowColor(0)
    legend.SetBorderSize(0)
    
    legend_ratio_h = 0.15*len(ScaleFactors)
    legend_ratio = ROOT.TLegend(0.2, 1.0, 0.9, 1.0-legend_ratio_h)
    legend_ratio.SetFillStyle(0)
    legend_ratio.SetShadowColor(0)
    legend_ratio.SetBorderSize(0)
    
    canvas = ROOT.TCanvas('canvas_split_%s'%suffix, '', 0, 0, 1000, 1000)
    size = 0.2
    pad1 = ROOT.TPad('pad1_%s'%suffix, '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2_%s'%suffix, '', 0.0, 0.0, 1.0, size, 0)
    
    pad1.Draw()
    pad2.Draw()
    
    pad1.SetFillStyle(ROOT.kCyan)
    
    pad1.SetBottomMargin(0)
    pad1.SetGridx()
    pad1.SetGridy()
    
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.4)
    
    pad1.SetLogx(vname=='Et')
    pad2.SetLogx(vname=='Et')
    
    min =  1e6
    max = -1e6
    for SF in ScaleFactors:
        if SF.min < min:
            min = SF.min
        if SF.max > max:
            max = SF.max
    
    first = True # Keep track of when to add :sames to the draw options.
    
    histos = []
    snowflakes = []
    RNG = ROOT.TRandom3()
    
    colors = [ROOT.kRed,ROOT.kBlue,ROOT.kYellow,ROOT.kGreen,ROOT.kOrange,ROOT.kMagenta]
    iColor = 0
    for SF in ScaleFactors:
        h_numer = SF.hw_numer.h.Clone('%s_final'%SF.hw_numer.h.GetName())
        h_denom = SF.hw_denom.h.Clone('%s_final'%SF.hw_denom.h.GetName())
        h_ratio = SF.hw_ratio.h.Clone('%s_final'%SF.hw_ratio.h.GetName())
        
        # Store these so they don't get garbage collected.
        histos.append(h_numer)
        histos.append(h_denom)
        histos.append(h_ratio)
        
        for h in [h_numer,h_denom]:
            h.GetYaxis().SetTitleSize  (0.06)
            h.GetYaxis().SetTitleOffset(0.75)
            h.SetMinimum(min*0.9)
            h.SetMaximum(1.10)
        
        legend.AddEntry(h_numer, SF.hw_numer.legend, 'pl')
        legend.AddEntry(h_denom, SF.hw_denom.legend, 'f' )
        
        ratio_diff = ratio_max-ratio_min
        h_ratio.SetMinimum(ratio_min)
        h_ratio.SetMaximum(ratio_max)
        if len(ScaleFactors) > 1:
            h_ratio.SetMaximum(ratio_min + ratio_diff*(1+0.5*len(ScaleFactors)))
        h_ratio.SetMarkerStyle(h_numer.GetMarkerStyle()+4)
        
        h_numer.SetMarkerSize(2)
        h_numers = []
        h_ratios = []
        
        for i in range(0,len(colors)):
            h_numers.append(h_numer.Clone('h_numers_%d'%i))
            h_ratios.append(h_ratio.Clone('h_numers_%d'%i))
            color = colors[(i+iColor)%len(colors)]
            h_numers[i].SetMarkerColor(color)
            h_numers[i].SetLineColor  (color)
            h_ratios[i].SetMarkerColor(color)
            h_ratios[i].SetLineColor  (color)
            
        for bin in range(1,h_numer.GetNbinsX()+1):
            for i in range(0,len(colors)):
                if (bin-i)%len(colors)!=0:
                    h_numers[i].SetBinContent(bin,-100)
                    h_ratios[i].SetBinContent(bin,-100)
                
        
        # Now draw the plots.
        pad1.cd()
        if first:
            h_sky  = h_denom.Clone('h_snow')
            h_sky.SetFillColor(ROOT.kBlue)
            h_sky.SetLineColor(ROOT.kBlue)
            
            h_snow = ROOT.TH1F('h_snow', '', 10000, h_denom.GetXaxis().GetXmin(),h_denom.GetXaxis().GetXmax())
            h_snow.SetFillColor(ROOT.kWhite)
            h_snow.SetLineColor(ROOT.kWhite)
            
            histos.append(h_sky )
            histos.append(h_snow)
            
            x0 = h_denom.GetXaxis().GetXmin()
            y0 = h_denom.GetMinimum()
            for bin in range(1,h_snow.GetNbinsX()+1):
                x  = h_sky.GetBinCenter(bin)
                y  = 0.88 - 0.1*math.exp(-0.00001*(x-x0))
                h_snow.SetBinContent(bin,    0.5*(y+y0) )
                h_snow.  SetBinError(bin,abs(0.5*(y-y0)))
            for bin in range(1,h_sky.GetNbinsX()+1):
                h_sky.SetBinContent(bin, 10.0)
                
            h_sky.Draw('hist')
            h_snow.Draw('e3:sames')
            #h_denom.Draw('e2:sames')
            
            for i in range(0,20):
                x = RNG.Uniform(h_denom.GetXaxis().GetXmin(),h_denom.GetXaxis().GetXmax())
                y = RNG.Uniform(0.7,1.1)
                snowflake1 = ROOT.TMarker(x, y,  3)
                snowflake2 = ROOT.TMarker(x, y, 20)
                snowflake1.SetMarkerColor(ROOT.kWhite)
                snowflake2.SetMarkerColor(ROOT.kWhite)
                snowflake1.SetMarkerSize(4)
                snowflake2.SetMarkerSize(1)
                snowflakes.append(snowflake1)
                snowflakes.append(snowflake2)
                snowflake1.Draw()
                snowflake2.Draw()
            
            moon1 = snowflake = ROOT.TMarker(0.80, 0.80, 20)
            moon2 = snowflake = ROOT.TMarker(0.79, 0.80, 20)
            moon1.SetMarkerSize(10)
            moon2.SetMarkerSize( 8)
            moon1.SetNDC()
            moon2.SetNDC()
            moon1.SetMarkerColor(ROOT.kYellow)
            moon2.SetMarkerColor(ROOT.kBlue)
            
            moon1.Draw()
            moon2.Draw()
            
            snowflakes.append(moon1)
            snowflakes.append(moon2)
            
        else:
            pass
            #h_denom.Draw('e2:sames')
        for h in h_numers:
            h.Draw('pe1:sames')
        h_denom.Draw('axis:sames')
        
        #for lname in labels:
        #    labels[lname].Draw()

        # Now the lower pad.
        pad2.cd()
        
        # Make a line at 1.0.
        line_1 = ROOT.TLine(h_ratio.GetXaxis().GetXmin(), 1.0, h_ratio.GetXaxis().GetXmax(), 1.0)
        line_1.SetLineColor(ROOT.kBlack)
        line_1.SetLineStyle(ROOT.kDashed)
        
        v = variables[vname]
        xaxis = v.latex if v.unit=='' else '%s [%s]'%(v.latex,v.unit)
        h_ratio.GetXaxis().SetTitle(xaxis)
        if vname=='Et':
            h_ratio.GetXaxis().SetNdivisions(510,False)
        h_ratio.GetYaxis().SetNdivisions(102,False)
        h_ratio.GetXaxis().SetTickLength(0.1)
    
        # Draw the ratio plot.
        if first:
            first = False
            h_ratio.Draw('pe1')
            for h in h_ratios:
                h.Draw('pe1:sames')
        else:
            for h in h_ratios:
                h.Draw('pe1:sames')
        line_1.Draw()
        h_ratio.Draw('axis:sames')
        
        legend_text = '%s #chi^{2}/ndof = %.2f/%d, SF = %.4f (#pm %.4f)'%(SF.title, SF.chi2, SF.ndof, SF.a_value, SF.a_error)
        legend_ratio.AddEntry(h_ratio, legend_text, 'pl')
    
    pad1.cd()
    #legend.Draw()
    
    pad2.cd()
    if len(ScaleFactors)==1:
        SF = ScaleFactors[0]
        SF.chi2_label  .Draw()
        SF.params_label.Draw()
    else:
        pass
        #legend_ratio.Draw()
    
    if abs(1.0-card.ttbarScale) > 1e-3:
        suffix = '%s_ttbarscale%d'%(suffix,int(100*card.ttbarScale))
    if abs(1.0-card.   WWScale) > 1e-3:
        suffix = '%s_WWscale%d'   %(suffix,int(100*card.   WWScale))
    if abs(1.0-card.   WZScale) > 1e-3:
        suffix = '%s_WZscale%d'   %(suffix,int(100*card.   WZScale))
    if abs(1.0-card.   ZZScale) > 1e-3:
        suffix = '%s_ZZscale%d'   %(suffix,int(100*card.   ZZScale))
    if abs(1.0-card.WJetsScale) > 1e-3:
        suffix = '%s_WJetsscale%d'%(suffix,int(100*card.WJetsScale))
    if abs(1.0-card.ZToTTScale) > 1e-3:
        suffix = '%s_ZToTTscale%d'%(suffix,int(100*card.ZToTTScale))
    if abs(1.0-card.STScale) > 1e-3:
        suffix = '%s_STscale%d'%(suffix,int(100*card.STScale))
    if abs(1.0-card.ST_antiScale) > 1e-3:
        suffix = '%s_ST_antiscale%d'%(suffix,int(100*card.ST_antiScale))
        
    if abs(lower_mee-card.mee_range[0]) > 1e-3 or abs(upper_mee-card.mee_range[1]) > 1e-3:
        suffix = '%s_mee%dTo%d'%(suffix,int(card.mee_range[0]),int(card.mee_range[1]))
    
    canvas.Print('%s/h_compare_%s.png'%(card.plot_prefix,suffix))
   # canvas.Print('%s/h_compare_%s.eps'%(card.plot_prefix,suffix))
    
    if file_out:
        file_out.cd()
        for h in histos:
            h.Write()
    
