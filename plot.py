import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import interp1d

def Char_DataList_FT_ADV(final_time, adv):
    if adv == True:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_advective"
    else:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_no_adv"
    
    char_data_list = []
    for step in range(2, int(final_time/10) + 1):
        char_data_list.append(np.loadtxt(f'{folder_path}/char_values_step_{step}.txt', delimiter=' ', skiprows=0))
    
    return char_data_list


def Print_Char_Over_Time(final_time, adv):
    label = ""
    c = ""
    if adv == True:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_advective"
        label = "Adv"
        c = "Blues"
    else:
        folder_path = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_no_adv"
        label = "No Adv"
        c = "Reds"
    
    char_data_list = Char_DataList_FT_ADV(final_time, adv)
    cmap = cm.get_cmap(c, len(char_data_list))
    
    for step in range(len(char_data_list)):
        char_data_current = np.loadtxt(f'{folder_path}/char_values_step_{step+2}.txt', delimiter=' ', skiprows=0)

        interp_func = interp1d(char_data_current[:, 0], char_data_current[:, 1], kind='cubic', fill_value="extrapolate")
        x_new = np.linspace(char_data_current[:, 0].min(), char_data_current[:, 0].max(), num=1000)  
        y_new = interp_func(x_new)

        color = cmap(step)

        plt.plot(x_new, y_new, c=color, label=f'Step {step + 2}, {label}')
    
    plt.xlabel('X Coordinates')
    plt.ylabel('Degree of Char')
    plt.legend()
    plt.show()

def Compare_Adv_No_Adv(final_time):
    folder_path_adv = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_advective"
    folder_path_no_adv = f"/home/foxy/dv/sumMITApps/hypersonics/development/Cube_For_CFD_Coupling/OUTPUT_FinalTime_{final_time}_no_adv"
    char_data_list_adv = Char_DataList_FT_ADV(final_time, True)
    char_data_list_no_adv = Char_DataList_FT_ADV(final_time, False)

    cmap_adv = cm.get_cmap('Blues', len(char_data_list_adv))
    cmap_no_adv = cm.get_cmap('Reds', len(char_data_list_no_adv))

    for step in range(len(char_data_list_adv)):
        char_data_current_adv = np.loadtxt(f'{folder_path_adv}/char_values_step_{step+2}.txt', delimiter=' ', skiprows=0)
        char_data_current_no_adv = np.loadtxt(f'{folder_path_no_adv}/char_values_step_{step+2}.txt', delimiter=' ', skiprows=0)

        interp_func_adv = interp1d(char_data_current_adv[:, 0], char_data_current_adv[:, 1], kind='cubic', fill_value="extrapolate")
        x_new_adv = np.linspace(char_data_current_adv[:, 0].min(), char_data_current_adv[:, 0].max(), num=1000)  
        y_new_adv = interp_func_adv(x_new_adv)

        interp_func_no_adv = interp1d(char_data_current_no_adv[:, 0], char_data_current_no_adv[:, 1], kind='cubic', fill_value="extrapolate")
        x_new_no_adv = np.linspace(char_data_current_no_adv[:, 0].min(), char_data_current_no_adv[:, 0].max(), num=1000)  
        y_new_no_adv = interp_func_no_adv(x_new_no_adv)

        plt.plot(x_new_adv, y_new_adv, c=cmap_adv(step + 2), label=f'Step {step + 2}, Adv')
        plt.plot(x_new_no_adv, y_new_no_adv, c=cmap_no_adv(step + 2), label=f'Step {step + 2}, No Adv')

    plt.xlabel('X Coordinates')
    plt.ylabel('Degree of Char')
    plt.legend()
    plt.show()

Print_Char_Over_Time(300, True)
Print_Char_Over_Time(300, False)
Compare_Adv_No_Adv(300)
