import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'D:\Downloads\Book (7).xlsx', sheet_name='Sheet4')
print(df)


x = df['Time']
y = df['Power']

plt.figure(figsize=(12,4))
plt.style.use('seaborn')
plt.step(x,y)
plt.ylabel('AC Power (W)')
plt.title("Actual data for 23rd may")
plt.gcf().autofmt_xdate()
plt.show()