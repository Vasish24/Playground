import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.axes as ax
import numpy as np

I020 = [ line.strip('\n').split(",") for line in
open(r'D:\Downloads\book.xlsx')][1:]
Time = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I020 ]
Time1 = [ mdates.date2num(line) for line in Time ]
Power = [ float(line[1]) for line in I020 ]
order = np.argsort(Time1)
xs = np.array(Time1)[order]
ys = np.array(Power)[order]
plt.title('Solar data')
plt.xlabel('Time')
plt.ylabel('Power')
ax.plot_date(xs, ys, 'k-')
hfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(hfmt)
plt.show()