# -*- coding: utf-8 -*-
"""
@author: Manchun LEI

This file is an extension of sixs.py.

I want add some extension fontion to the class SixS,
so I create a class SixSPlus here as a Child class of SixS.

"""
import os
import numpy as np
import datetime
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
py6s_path = os.path.join(current_dir, 'Py6S')
if py6s_path not in sys.path:
    sys.path.append(py6s_path)

from Py6S import *

class SixSPlus(SixS):
    def __init__(self,path=None,outfile=None):
        super().__init__(path)
        if outfile is not None:
            f = open(outfile,"rb")
            lines = f.read()
            f.close()
            self.outputs = Outputs(lines,'')
        
    def outs(self):
        outputs = {}
        # angles (deg)
        outputs['sza'] = self.outputs.values['solar_z']
        outputs['saa'] = self.outputs.values['solar_a']
        outputs['vza'] = self.outputs.values['view_z']
        outputs['vaa'] = self.outputs.values['view_a']
        outputs['raa'] = self.outputs.values['azimuthal_angle_difference']
        outputs['scattering_angle'] = self.outputs.values['scattering_angle']
        # atmos profil param
        if 'visibility' in self.outputs.values:
            outputs['vis'] = self.outputs.values['visibility']
            outputs['aot550'] = self.outputs.values['aot550']
        # ground param
        outputs['ground_pressure'] = self.outputs.values['ground_pressure']
        outputs['ground_alt'] = self.outputs.values['ground_altitude']
        # toa intrinsic solar irradiance (w/m2/um)
        if 'int_solar_spectrum' in self.outputs.values:
            outputs['F0'] = self.outputs.values['int_solar_spectrum']/self.outputs.values['int_funct_filt']
        else:
            outputs['F0'] = self.outputs.values['solar_spectrum']
        # toa radiance - total (w/m2/um/sr)
        outputs['toa_rad'] = self.outputs.values['apparent_radiance']
        # toa reflectance - total, atm, obj, env
        outputs['toa_refl'] = self.outputs.values['apparent_reflectance']
        outputs['toa_atm_refl'] = self.outputs.values['atmospheric_intrinsic_reflectance']
        outputs['toa_obj_refl'] = self.outputs.values['pixel_reflectance']
        outputs['toa_env_refl'] = self.outputs.values['background_reflectance']       
        # boa irradiance - total, dir, dif, env
        outputs['boa_dir_irr'] = self.outputs.values['direct_solar_irradiance']
        outputs['boa_dif_irr'] = self.outputs.values['diffuse_solar_irradiance']
        outputs['boa_env_irr'] = self.outputs.values['environmental_irradiance']
        outputs['boa_irr'] = outputs['boa_dir_irr']+outputs['boa_dif_irr']+outputs['boa_env_irr']
        # ground reflectance
        outputs['ground_refl'] = self.outputs.values['ground_reflectance']
        
        # atm spherical albedo
        outputs['total_sph_alb'] = self.outputs.rat['spherical_albedo'].total
        
        # optical depth - total, rayleigh, aerosol
        outputs['total_opt_dep'] = self.outputs.rat['optical_depth_total'].total
        outputs['ray_opt_dep'] = self.outputs.rat['optical_depth_total'].rayleigh
        outputs['aer_opt_dep'] = self.outputs.rat['optical_depth_total'].aerosol
               
        # transmittance - total, downward, upward
        # gas
        outputs['total_gas_trans'] = self.outputs.trans['global_gas'].total
        outputs['down_gas_trans'] = self.outputs.trans['global_gas'].downward
        outputs['up_gas_trans'] = self.outputs.trans['global_gas'].upward        
        # ozone
        outputs['total_ozone_trans'] = self.outputs.trans['ozone'].total
        outputs['down_ozone_trans'] = self.outputs.trans['ozone'].downward
        outputs['up_ozone_trans'] = self.outputs.trans['ozone'].upward
        
        # rayleigh scattering transmittance - total, downard, upward
        outputs['total_ray_trans'] = self.outputs.trans['rayleigh_scattering'].total
        outputs['down_ray_trans'] = self.outputs.trans['rayleigh_scattering'].downward
        outputs['up_ray_trans'] = self.outputs.trans['rayleigh_scattering'].upward      
        # aerosol scattering transmittance - total, downard, upward
        outputs['total_aer_trans'] = self.outputs.trans['aerosol_scattering'].total
        outputs['down_aer_trans'] = self.outputs.trans['aerosol_scattering'].downward
        outputs['up_aer_trans'] = self.outputs.trans['aerosol_scattering'].upward
        
        # total scattering transmittance - total, downard, upward
        outputs['total_scat_trans'] = self.outputs.trans['total_scattering'].total
        outputs['down_scat_trans'] = self.outputs.trans['total_scattering'].downward
        outputs['up_scat_trans'] = self.outputs.trans['total_scattering'].upward
        
        
        # level 2 parameters calculation
        # this parameters are derivated from level1 (direct outputs) parameters
        outputs['mus'] = np.cos(np.radians(outputs['sza']))
        outputs['muv'] = np.cos(np.radians(outputs['vza']))
        # direct scat trans - downward, upward
        outputs['down_dir_scat_trans'] = np.exp(-outputs['total_opt_dep']/outputs['mus'])
        outputs['up_dir_scat_trans'] = np.exp(-outputs['total_opt_dep']/outputs['muv'])
        # diffuse scat trans - downward, upward
        outputs['down_dif_scat_trans'] = outputs['down_scat_trans'] - outputs['down_dir_scat_trans']
        outputs['up_dif_scat_trans'] = outputs['up_scat_trans'] - outputs['up_dir_scat_trans']
        
        
        return outputs