from paraview.simple import *
import numpy as np
from matplotlib import pyplot as plt

folder_path = "/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_100_advective"

def Get_Char_Amount(folder_path, n):
 
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

    degree_of_char = point_data.GetArray('Degree of Char-internal')

    points = resampled_data.GetPoints()
    x_coords = np.array([points.GetPoint(i)[0] for i in range(points.GetNumberOfPoints())])
    char_values = np.array([degree_of_char.GetValue(i) for i in range(degree_of_char.GetNumberOfValues())])

    np.savetxt(f'{folder_path}/char_values_step_{n}.txt', np.column_stack((x_coords, char_values)))

def Get_Char_For_FT_ADV(final_time, adv):
    if adv == True:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_advective"
    else:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_no_adv"
    for step in range(2, int(final_time/10) + 1):
        Get_Char_Amount(folder_path, step)

Get_Char_For_FT_ADV(300, adv=False)
Get_Char_For_FT_ADV(300, adv=True)
