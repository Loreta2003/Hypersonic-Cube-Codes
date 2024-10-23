from paraview.simple import *
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

folder_path = "/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_300_advective"

temperature_data = [200, 250, 298, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200, 3500]
molar_mass_data = [21.996, 21.996, 21.996, 21.994, 21.984, 21.949, 21.849, 21.204, 19.069, 15.132, 13.808, 13.742, 12.558, 11.69, 11.063, 11.005, 10.979, 10.865, 10.48, 9.5573, 8.0901, 6.8549]
viscosity_data = [1.78, 1.52, 1.31, 1.15, 1.02, 0.91, 0.83, 0.69, 0.58, 0.50, 0.44, 0.39, 0.30, 0.24, 0.19, 0.16, 0.14, 0.12, 0.10, 0.09, 0.08, 0.07] 
virgin_thermal_conductivity = [3.975E-01, 4.025E-01, 4.162E-01, 4.530E-01, 4.698E-01, 4.860E-01, 5.234E-01, 5.601E-01, 6.978E-01, 8.723E-01, 1.109E+00, 1.751E+00, 2.779E+00]
char_thermal_conductivity = [3.975E-01, 4.025E-01, 4.162E-01, 4.530E-01, 4.698E-01, 4.860E-01, 5.234E-01, 5.601E-01, 6.050E-01, 7.290E-01, 9.221E-01, 1.458E+00, 2.318E+00]


def Get_Molar_Mass(T):
    molar_mass_interpolation = interp1d(temperature_data, molar_mass_data, kind='linear', fill_value='extrapolate')
    return molar_mass_interpolation(T)

def Get_Viscosity(T):
    viscosity_interpolation = interp1d(temperature_data, viscosity_data, kind='linear', fill_value='extrapolate')
    return viscosity_interpolation(T)

def Get_Gas_Density(p, T):
    rho = []
    R = 8.314 #ideal gas constant
    for i in range(len(p)):
        M = Get_Molar_Mass(T[i])
        rho.append(p[i]*M/(R*T[i]))
    return np.array(rho)

def Get_Thermal_Conductivity(T, x):
    interp_virgin = interp1d(temperature_data[:len(virgin_thermal_conductivity)], virgin_thermal_conductivity, kind='linear', fill_value="extrapolate")
    interp_char = interp1d(temperature_data[:len(char_thermal_conductivity)], char_thermal_conductivity, kind='linear', fill_value="extrapolate")
    kappa_virgin = interp_virgin(T)
    kappa_char = interp_char(T)
    kappa_total = x*kappa_char + (1-x)*kappa_virgin
    return kappa_total

def Get_Permeability(T, x):
    temp_data = [255, 298, 444, 555, 644, 833, 1111, 1389, 1667, 1944, 2222, 2778, 3333]
    virgin_permeability = [3.975E-01, 4.025E-01, 4.162E-01, 4.530E-1, 4.698E-01, 4.860E-01, 5.234E-01, 5.601E-01, 6.978E-01, 8.723E-01, 1.109, 1.751, 2.779]
    char_permeability = [3.975E-01, 4.025E-01, 4.162E-01, 4.530E-1, 4.698E-01, 4.860E-01, 5.234E-01, 5.601E-01, 6.050E-01, 7.290E-01, 9.221E-01, 1.458, 2.318]
    interp_k_virgin = interp1d(temp_data[:len(virgin_permeability)], virgin_permeability, kind='linear', fill_value="extrapolate")
    interp_k_char = interp1d(temp_data[:len(char_permeability)], char_permeability, kind='linear', fill_value="extrapolate")
    k_virgin = interp_k_virgin(T)
    k_char = interp_k_char(T)
    k_total = x*k_char + (1-x)*k_virgin
    return k_total

x = 1 #-----------------------------------------------Change x---------------------------------------------------#
def Get_Peclet(folder_path, n):
    data_reader = OpenDataFile(f"{folder_path}/Thermal/output-0000-{str(n).zfill(8)}.vtu")

    UpdatePipeline()
    data = servermanager.Fetch(data_reader)
    points = data.GetPoints()
    num_points = points.GetNumberOfPoints()
    coords = np.array([points.GetPoint(i) for i in range(num_points)])
    point_data = data.GetPointData()

    theta = point_data.GetArray("Temperature-internal") #temperature
    theta = np.array([theta.GetValue(i) for i in range(num_points)])
    myu = Get_Viscosity(theta) #viscosity
    Kappa = Get_Thermal_Conductivity(theta, x) #thermal conductivity
    k = Get_Permeability(theta, x) #permeability
    p = point_data.GetArray("pressure") #pressure
    p = np.array([p.GetValue(i) for i in range(num_points)])
    h_g = point_data.GetArray("Gas Enthalpy-internal") #gas enthalpy
    h_g = np.array([h_g.GetValue(i) for i in range(num_points)])
    rho_g = Get_Gas_Density(p, theta) #gas density

    peclet = np.array([(theta[i]*myu[i]*Kappa[i])/(k[i]*p[i]*h_g[i]*rho_g[i]) for i in range(num_points)])

peclet = Get_Peclet(folder_path, 25)
print(peclet)
