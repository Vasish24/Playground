from pvlib.pvsystem import PVSystem, retrieve_sam
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.iotools import pvgis
import matplotlib.pyplot as plt
# Not required, but recommended.
# It avoids downloading same data over and over again from PVGIS.
# https://pypi.org/project/requests-cache/
# pip install requests-cache
import requests_cache
requests_cache.install_cache('pvgis_requests_cache', backend='sqlite')
#               latitude, longitude,  name                      , altitude, timezone
coordinates = [( 51.993842263869766   ,    4.463203943422604, 'Europe/Amsterdam'          ,      700, 'Etc/GMT+1')]

# Get the module and inverter specifications from SAM (https://github.com/NREL/SAM)
module = retrieve_sam('SandiaMod')['Canadian_Solar_CS5P_220M___2009_']
inverter = retrieve_sam('cecinverter')['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

temp_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

for latitude, longitude, name, altitude, timezone in coordinates:
    location = Location(latitude, longitude, name=name,
                        altitude=altitude, tz=timezone)

    # Download weather data from PVGIS server
    weather, _, info, _ = pvgis.get_pvgis_tmy(location.latitude,
                                              location.longitude)

    # Rename columns from PVGIS TMY in order to define the required data.
    weather = weather.rename(columns={'G(h)': 'ghi',
                                      'Gb(n)': 'dni',
                                      'Gd(h)': 'dhi',
                                      'T2m': 'temp_air'
                                      })
    print(weather.head())
    # Same logic as orientation_strategy='south_at_latitude_tilt', but might be
    # a bit clearer for locations in southern hemishpere.
    system = PVSystem(module_parameters=module,
                      inverter_parameters=inverter,
                      temperature_model_parameters=temp_parameters,
                      surface_tilt=abs(latitude),
                      surface_azimuth=180 if latitude > 0 else 0)
    mc = ModelChain(system, location)
    mc.run_model(weather)

    ghi = weather['ghi']


    # Reporting
    nominal_power = module.Impo * module.Vmpo
    annual_energy = mc.ac.sum()
    specific_yield = annual_energy / nominal_power
    global_poa = mc.total_irrad.poa_global.sum() / 1000
    average_ambient_temperature = weather.temp_air.mean()
    performance_ratio = specific_yield / global_poa
    weather_source = '%s (%d - %d)' % (info['meteo_data']['radiation_db'],
                                       info['meteo_data']['year_min'],
                                       info['meteo_data']['year_max'])
    latitude_NS = '%.1f°%s' % (abs(latitude), 'N' if latitude > 0 else 'S')
    longitude_EW = '%.1f°%s' % (abs(longitude), 'E' if longitude > 0 else 'W')

    print('## %s (%s %s, %s)' % (name, latitude_NS, longitude_EW, timezone))
    print('Nominal power         : %.2f kWp' % (nominal_power / 1000))
    print('Surface azimuth       : %.0f °' % system.surface_azimuth)
    print('Surface tilt          : %.0f °' % system.surface_tilt)
    print('Weather data source   : %s' % weather_source)
    print('Global POA irradiance : %.0f kWh / (m² · y)' % global_poa)
    print('Average temperature   : %.1f °C' % average_ambient_temperature)
    print('Total yield           : %.0f kWh / y' % (annual_energy / 1000))
    print('Specific yield        : %.0f kWh / (kWp · y)' % specific_yield)
    print('Performance ratio     : %.1f %%' % (performance_ratio * 100))
    print()
    mc.plt()
    plt.show()