# built-in python modules
import inspect
import os
from datetime import date,datetime, timedelta

# scientific python add-ons
import numpy as np
import pandas as pd

# plotting stuff
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# finally, we import the pvlib library
from pvlib import solarposition, irradiance, atmosphere, pvsystem, inverter, temperature
from pvlib.forecast import GFS, NAM, NDFD, RAP, HRRR
from netCDF4 import num2date

# Choose a location.
latitude = 51.993842263869766
longitude = 4.463203943422604
tz = 'Europe/Amsterdam'
panel = 13
surface_tilt = 45
surface_azimuth = 135 # pvlib uses 0=North, 90=East, 180=South, 270=West convention
albedo = 0.2

start = pd.Timestamp(datetime.today() - timedelta(days=4), tz=tz) # date
end = start + pd.Timedelta(days=7) # 7 days from mentioned date

# Define forecast model
fm = GFS(resolution='Quarter')
#fm = NAM()
#fm = NDFD()
#fm = RAP()
#fm = HRRR()

# Retrieve data
forecast_data = fm.get_processed_data(latitude , longitude ,  start, end)
print(forecast_data.head())
# forecast_data['temp_air'].plot()
# plot.show()

ghi = forecast_data['ghi']
# ghi.plot()
# plt.ylabel('Irradiance ($W/m^{-2}$)')
# plt.title('GHI')
# plt.show()

# retrieve time and location parameters
time = forecast_data.index
a_point = fm.location

solpos = a_point.get_solarposition(time)
#solpos.plot()
#plt.show()

dni_extra = irradiance.get_extra_radiation(fm.time)
#dni_extra.plot()
#plt.ylabel('Extra terrestrial radiation ($W/m^{-2}$)')
#plt.show()

airmass = atmosphere.get_relative_airmass(solpos['apparent_zenith'])
#airmass.plot()
#plt.ylabel('Airmass')
#plt.show()

poa_sky_diffuse = irradiance.haydavies(surface_tilt, surface_azimuth,
                                       forecast_data['dhi'], forecast_data['dni'], dni_extra,
                                       solpos['apparent_zenith'], solpos['azimuth'])
#poa_sky_diffuse.plot()
#plt.ylabel('Irradiance ($W/m^{-2}$)')
#plt.show()

poa_ground_diffuse = irradiance.get_ground_diffuse(surface_tilt, ghi, albedo=albedo)
#poa_ground_diffuse.plot()
#plt.ylabel('Irradiance ($W/m^{-2}$)')
#plt.show()

aoi = irradiance.aoi(surface_tilt, surface_azimuth, solpos['apparent_zenith'], solpos['azimuth'])
#aoi.plot()
#plt.ylabel('Angle of incidence (deg)')
#plt.show()

poa_irrad = irradiance.poa_components(aoi, forecast_data['dni'], poa_sky_diffuse, poa_ground_diffuse)
# poa_irrad.plot()
# plt.ylabel('Irradiance ($W/m^{-2}$)')
# plt.title('POA Irradiance')
# plt.show()

ambient_temperature = forecast_data['temp_air']
wnd_spd = forecast_data['wind_speed']
thermal_params = temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_polymer']
pvtemp = temperature.sapm_cell(poa_irrad['poa_global'], ambient_temperature, wnd_spd, **thermal_params)
# pvtemp.plot()
# plt.ylabel('Temperature (C)')
# plt.title('PV Temp')
# plt.show()

sandia_modules = pvsystem.retrieve_sam('SandiaMod')
sandia_module = sandia_modules.Advent_Solar_Ventura_210___2008_                 #Canadian_Solar_CS5P_220M___2009_Trina_TSM_240PA05__2013_
#print(sandia_module())

effective_irradiance = pvsystem.sapm_effective_irradiance(poa_irrad.poa_direct, poa_irrad.poa_diffuse,
                                                          airmass, aoi, sandia_module)

sapm_out = pvsystem.sapm(effective_irradiance, pvtemp, sandia_module)*panel
#print(sapm_out.head())

# sapm_out[['p_mp']].plot()
# plt.ylabel('DC Power (W)')
# plt.title('DC Power Forecast')
# plt.show()
sapm_inverters = pvsystem.retrieve_sam('sandiainverter')
sapm_inverter = sapm_inverters['SolarEdge_Technologies_Ltd___SE3000__208V_'] #ABB__MICRO_0_3HV_I_OUTD_US_208__208V_ABB__PVI_3_0_OUTD_S_US_Z_A__208V_
#print(sapm_inverter())

p_ac = inverter.sandia(sapm_out.v_mp, sapm_out.p_mp, sapm_inverter)*panel
#list = p_ac.tolist()
#print("AC power for next 7days with 3 hours resolution",list)
# p_ac.plot()
# plt.ylabel('AC Power (W)')
# plt.ylim(0, None)
# plt.title('Power Forecast')
# plt.show()
p_ac[start:start+pd.Timedelta(days=2,hours=1)].plot(drawstyle="steps-post",figsize=(12,4))
list = p_ac[start:start+pd.Timedelta(days=2,hours=1)].tolist()
print("AC power for next 2days with 3 hours resolution",list)
plt.ylabel('AC Power (W)')
plt.title('Forecast data for 23rd may')
plt.show()

#p_ac.to.csv('export_p_ac.csv')
print(p_ac.describe())
p_ac.index.freq
# integrate power to find energy yield over the forecast period
#print(p_ac.sum() * 3)

