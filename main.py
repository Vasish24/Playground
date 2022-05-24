import pandas as pd

import matplotlib.pyplot as plt

import datetime

# import pvlib forecast models
from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
from pvlib import solarposition, irradiance, atmosphere, pvsystem, inverter, temperature

# specify location (Tucson, AZ)
latitude, longitude, tz = 32.2, -110.9, 'US/Arizona'

# specify time range.
start = pd.Timestamp(datetime.date.today(), tz=tz)

end = start + pd.Timedelta(days=7)

irrad_vars = ['ghi', 'dni', 'dhi']

# GFS model, defaults to 0.5 degree resolution
# 0.25 deg available
model = GFS()

# retrieve data. returns pandas.DataFrame object
raw_data = model.get_data(latitude, longitude, start, end)

print(raw_data.head())

data = raw_data

# rename the columns according the key/value pairs in model.variables.
data = model.rename(data)

# convert temperature
data['temp_air'] = model.kelvin_to_celsius(data['temp_air'])

# convert wind components to wind speed
data['wind_speed'] = model.uv_to_speed(data)

# calculate irradiance estimates from cloud cover.
# uses a cloud_cover to ghi to dni model or a
# uses a cloud cover to transmittance to irradiance model.
# this step is discussed in more detail in the next section
irrad_data = model.cloud_cover_to_irradiance(data['total_clouds'])

data = data.join(irrad_data, how='outer')

# keep only the final data
data = data[model.output_variables]

print(data.head())

data = model.process_data(raw_data)

print(data.head())

data = model.get_processed_data(latitude, longitude, start, end)

print(data.head())

# plot cloud cover percentages
cloud_vars = ['total_clouds', 'low_clouds',
              'mid_clouds', 'high_clouds']


data[cloud_vars].plot()

plt.ylabel('Cloud cover %')

plt.xlabel('Forecast Time ({})'.format(tz))

plt.title('GFS 0.5 deg forecast for lat={}, lon={}'
          .format(latitude, longitude))


plt.legend()

solpos = location.get_solarposition(cloud_cover.index)
cs = location.get_clearsky(cloud_cover.index, model='ineichen')
# offset and cloud cover in decimal units here
# larson et. al. use offset = 0.35
ghi = (offset + (1 - offset) * (1 - cloud_cover)) * ghi_clear
dni = disc(ghi, solpos['zenith'], cloud_cover.index)['dni']
dhi = ghi - dni * np.cos(np.radians(solpos['zenith']))

# plot irradiance data
data = model.rename(raw_data)

irrads = model.cloud_cover_to_irradiance(data['total_clouds'], how='clearsky_scaling')

irrads.plot()

plt.ylabel('Irradiance ($W/m^2$)')

plt.xlabel('Forecast Time ({})'.format(tz));

plt.title('GFS 0.5 deg forecast for lat={}, lon={} using "clearsky_scaling"'
          .format(latitude, longitude));


plt.legend();