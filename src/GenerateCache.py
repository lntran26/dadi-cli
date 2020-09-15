import dadi
import dadi.DFE as DFE
import pickle
from Models import get_dadi_model_func

def generate_cache(model, grids, demo_params,
                   gamma_bounds, gamma_pts, additional_gammas,
                   output, sample_sizes, mp):

    func, is_cache1d = get_dadi_model_func(model, True)
    if grids == None:
        grids = [sample_sizes[0]+10, sample_sizes[0]+20, sample_sizes[0]+30]

    if is_cache1d:
       spectra = DFE.Cache1D(demo_params, sample_sizes, func, pts_l=grids, additional_gammas=additional_gammas, gamma_bounds=gamma_bounds, gamma_pts=gamma_pts, mp=mp) 
    else:
       spectra = DFE.Cache2D(demo_params, sample_sizes, func, pts=grids, additional_gammas=additional_gammas, gamma_bounds=gamma_bounds, gamma_pts=gamma_pts, mp=mp)

    fid = open(output, 'wb')
    pickle.dump(spectra, fid, protocol=2)
    fid.close()
