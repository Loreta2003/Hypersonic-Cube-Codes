from paraview.simple import *
import numpy as np
from matplotlib import pyplot as plt

folder_path = "/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_150_advective"

def Get_Adv_Heat_Flux_Amount(folder_path, n):
 
    data_reader = OpenDataFile(f"{folder_path}/Thermal/output-0000-{str(n).zfill(8)}.vtu")

    UpdatePipeline()

    line_source = Line()
    line_source.Point1 = [-0.0025, 0.0025, 0.0025]  
    line_source.Point2 = [0.0025, 0.0025, 0.0025]   
    line_source.Resolution = 1000 

    resample = ResampleWithDataset(SourceDataArrays=data_reader, DestinationMesh=line_source)
    UpdatePipeline()

    resampled_data = servermanager.Fetch(resample)

    point_data = resampled_data.GetPointData()

    adv_heat_flux_vector = point_data.GetArray('Advective Thermal Flux-internal')

    points = resampled_data.GetPoints()
    x_coords = np.array([points.GetPoint(i)[0] for i in range(points.GetNumberOfPoints())])
    adv_heat_flux_magnitude = np.array([np.sqrt(adv_heat_flux_vector.GetTuple3(i)[0]**2 + 
                                                adv_heat_flux_vector.GetTuple3(i)[1]**2 + 
                                                adv_heat_flux_vector.GetTuple3(i)[2]**2)
                                        for i in range(adv_heat_flux_vector.GetNumberOfTuples())])

    np.savetxt(f'{folder_path}/adv_heat_flux_values_step_{n}.txt', np.column_stack((x_coords, adv_heat_flux_magnitude)))

def Get_Adv_Heat_Flux_For_FT(final_time):
    folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_advective"
    for step in range(2, int(final_time/10) + 1):
        Get_Adv_Heat_Flux_Amount(folder_path, step)

final_time = 300
Get_Adv_Heat_Flux_For_FT(final_time)
