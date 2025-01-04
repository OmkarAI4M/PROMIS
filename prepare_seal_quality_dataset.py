
import pandas as pd
import numpy as np
import os

def create_dataset(num_samples, Machine_name, folder_path, file_path):
    # Read Excel file
    df = pd.read_excel(file_path)
    df = df.dropna()
    # Ensure column names have no leading/trailing spaces
    df.columns = df.columns.str.strip()

    ################################# Roll & env parameters ######################################
    Heat_cond_coeff_min = 0.000334    # K-sq.m/W
    Heat_cond_coeff_max = 0.000390
    delta_thickenss_min = 0.0663      # In mm
    delta_thickenss_max = 0.0774
    Sachet_temp_min = 53
    Sachet_temp_max = 58

    ########################### Settings & variations ##############################
    for i in range(df.shape[0]):
        # Access values using df.loc or df.iloc
        Set_temp = df.loc[i, "Temp"]
        Set_stroke_1 = df.loc[i, "Stroke_1"]
        Set_stroke_2 = df.loc[i, "Stroke_2"]

        Sealer_temp_min = df.loc[i, "T_min"]
        Sealer_temp_max = df.loc[i, "T_max"]

        Seal_mot_current_min = df.loc[i, "I_min"]
        Seal_mot_current_max = df.loc[i, "I_max"]

        Seal_pressure_min = df.loc[i, "P_min"]
        Seal_pressure_max = df.loc[i, "P_max"]

        Seal_quality_min = df.loc[i, "Q_min"]
        Seal_quality_max = df.loc[i, "Q_max"]

        ########################################################

        feature_dict = {
            'T': [Sealer_temp_min, Sealer_temp_max],
            'Ts': [Sachet_temp_min, Sachet_temp_max],
            'K': [Heat_cond_coeff_min, Heat_cond_coeff_max],
            'Is': [Seal_mot_current_min, Seal_mot_current_max],
            'P': [Seal_pressure_min, Seal_pressure_max],
            'd': [delta_thickenss_min, delta_thickenss_max],
            'Quality': [Seal_quality_min, Seal_quality_max],
        }

        # Validate feature ranges
        for key, values in feature_dict.items():
            if values[0] >= values[1]:
                raise ValueError(f"Invalid range for {key}: {values}")

        # Generate synthetic data
        data = {
            key: np.random.uniform(low=values[0], high=values[1], size=num_samples)
            for key, values in feature_dict.items()
        }


        df_event = pd.DataFrame(data)

        ################################################################################################

        df_event['E_heat'] = ((df_event['T'] - df_event['Ts']) * 0.0008784) / df_event['K']
        df_event['E_press'] = (df_event['P'] * df_event['d']) * 0.47072
        df_event.drop(columns=['d'], inplace=True)
        quality_column = df_event.pop('Quality')  
        df_event['Quality'] = quality_column      

        ###################################################################################################

        # Save eventwise data
        os.makedirs(folder_path, exist_ok=True)
        filename = f"{Machine_name}_{Set_temp}_{Set_stroke_1}_{Set_stroke_2}.csv"
        file_path_event = os.path.join(folder_path, filename)
        df_event.to_csv(file_path_event, index=False)

    # Combine all eventwise files
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith('.csv')]
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save combined data
    combined_file_name = f"{Machine_name}_Train_data.csv"
    file_path_combined = os.path.join(folder_path, combined_file_name)
    combined_df.to_csv(file_path_combined, index=False)
    print(f"DataFrame saved to: {file_path_combined}")


if __name__ == "__main__":


    ################################################################################################################################

    num_samples = 500         # Define the number of observations per event
    Machine_name = 'mc22'     #Enter machine name
    folder_path = '/home/omkar/Desktop/HUL_Haridwar/Seal_quality/Model_training_files/Datasets/Eventwise_synthetic_data'  # Mention folder to store eventwise csv files
    file_path = '/home/omkar/Downloads/eventwise_ranges.xlsx'    # Mention eventwise_ranges excel file path

    ####################################################################################################################################

    create_dataset(num_samples, Machine_name, folder_path, file_path)

