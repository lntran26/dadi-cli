import dadi
import dadi.Godambe
import dadi.DFE as DFE
import glob, pickle
import numpy as np
from Models import get_dadi_model_func
from Distribs import get_dadi_pdf

def godambe_stat(fs, model, cache1d, cache2d, sele_dist, sele_dist2,
                 bootstrap_dir, ll_complex, ll_simple, pi, popt, theta, misid, lrt, logscale):

    fs = dadi.Spectrum.from_file(fs)
    fs_files = glob.glob(bootstrap_dir + '/*.fs')
    all_boot = []
    for f in fs_files:
        boot_fs = dadi.Spectrum.from_file(f)
        all_boot.append(boot_fs)

    if cache1d != None:
        s1 = pickle.load(open(cache1d, 'rb'))
    if cache2d != None:
        s2 = pickle.load(open(cache2d, 'rb'))

    if model != None:
        func = get_dadi_model_func(model)
    if sele_dist != None:
        sele_dist = get_dadi_pdf(sele_dist)
    if sele_dist2 != None:
        sele_dist2 = get_dadi_pdf(sele_dist2)

    if (cache1d != None) and (cache2d != None):
        func = dadi.DFE.mixture
        if misid:
            func = dadi.Numerics.make_anc_state_misid_func(func)
        def model_func(pin, ns, pts):
            #for mixture model, pin = [mu, sigma, p0, misid]
            # Add in gammapos parameter
            params = np.concatenate([pin[0:2], [0], pin[2:]])
            return func(params, None, s1, s2, sele_dist, 
                        sele_dist2, theta, None, exterior_int=True)

    boot_theta_adjusts = [b.sum()/fs.sum() for b in all_boot]
    if lrt:
        adj = dadi.Godambe.LRT_adjust(model_func, [], all_boot, popt, fs,
                                      nested_indices=[pi-1], multinom=False, boot_theta_adjusts=boot_theta_adjusts)
        D_adj = adj*2*(ll_complex - ll_simple)
        pval = dadi.Godambe.sum_chi2_ppf(D_adj, weights=(0.5,0.5))
        print('Adjusted D statistic: {0}'.format(D_adj))
        print('p-value for rejecting the simple model: {0}'.format(pval))
    else:
        uncerts_adj = dadi.Godambe.GIM_uncert(model_func, [], all_boot, popt,
                                              fs, multinom=False, eps=1e-4, log=logscale,
                                              boot_theta_adjusts=boot_theta_adjusts)
        print('Estimated 95% uncerts (theta adj): {0}'.format(1.96*uncerts_adj))
        if logscale:
            print('Lower bounds of 95% confidence interval : {0}'.format(np.exp(np.log(popt)-1.96*uncerts_adj)))
            print('Upper bounds of 95% confidence interval : {0}'.format(np.exp(np.log(popt)+1.96*uncerts_adj)))
        else:
            print('Lower bounds of 95% confidence interval : {0}'.format(popt-1.96*uncerts_adj))
            print('Upper bounds of 95% confidence interval : {0}'.format(popt+1.96*uncerts_adj))