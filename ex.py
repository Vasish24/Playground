import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pvlib
from pvlib import pvsystem
from pvlib.forecast import GFS, NAM, NDFD, HRRR
import numpy as np
from pvlib.pvsystem import PVSystem, retrieve_sam
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.tracking import SingleAxisTracker
from pvlib.modelchain import ModelChain
from datetime import date,datetime, timedelta

if __name__ == '__main__':
    # latitude, longitude, name, altitude, timezone
    timeZone = "Europe/Amsterdam"
    location = pvlib.location.Location(latitude=51.993842263869766, longitude=4.463203943422604, tz=timeZone, altitude=43+6, name='Alken')

    # import the database
    module_database = pvlib.pvsystem.retrieve_sam(name='CECMod') #https://github.com/NREL/SAM/blob/develop/deploy/libraries/CEC%20Modules.csv
    module = module_database["Seraphim_Solar_USA_Manufacturing_Inc__SRP_365_6QA_WS_50"]
    inverter_database = pvlib.pvsystem.retrieve_sam(name="cecinverter")
    inverter = inverter_database["Huawei_Technologies_Co___Ltd___SUN2000_7_6KTL_USL0__240V_"]
    temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass'] # check
   # mount_east = pvsystem.Array(pvsystem.FixedMount(surface_tilt=45, surface_azimuth=-135), module_parameters=module, modules_per_string=13, strings=1, temperature_model_parameters=temperature_model_parameters)
    mount_south = pvsystem.Array(pvsystem.FixedMount(surface_tilt=45, surface_azimuth=135), module_parameters=module, modules_per_string=13, strings=1, temperature_model_parameters=temperature_model_parameters)
    system_multi_array = pvsystem.PVSystem(arrays=[ mount_south], inverter_parameters=inverter)

    weatherForecastModel = GFS(resolution="quarter", set_type="best") # Global Forecast System (GFS) (27-28km)
    start = pd.Timestamp(datetime.today()- timedelta(days=2), tz=timeZone)
    end = start + pd.Timedelta(days=2)
    raw_data = weatherForecastModel.get_data(location.latitude, location.longitude, start, end)
    data =raw_data
    irrad_vars = ['ghi', 'dni', 'dhi']
    data = weatherForecastModel.rename(data)
    data['temp_air'] = weatherForecastModel.kelvin_to_celsius(data['temp_air'])
    data['wind_speed'] = weatherForecastModel.uv_to_speed(data)

    irrad_data = weatherForecastModel.cloud_cover_to_irradiance(data['total_clouds'])
    data = data.join(irrad_data, how='outer')
    data = data[weatherForecastModel.output_variables]
    data = weatherForecastModel.process_data(raw_data)
    data['precipitable_water'] = 0.1
    print(data.columns)

    PVSystemModel = ModelChain(system_multi_array, weatherForecastModel.location, aoi_model="no_loss")
    print(system_multi_array)
    print(PVSystemModel)

    PVSystemModel.run_model(data)
    PVSystemModel.results.ac.fillna(0).plot()
    plt.ylim(0, None)
    plt.ylabel('AC Power (W)')

    plt.show()