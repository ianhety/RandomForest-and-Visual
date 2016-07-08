import numpy as np
import pandas as pd
import seaborn as sns

%pylab inline
sns.set_style('darkgrid')

data = pd.read_csv("C:\\Users\\310249682\\Downloads\\WorldPhones.csv")
data.head()

sns.set(font_scale=2.5) 
fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6))= plt.subplots(3, 2, sharex='col', sharey=False)
fig.set_size_inches(23, 20.5)
sns.pointplot(data=data, x="Year", y="N.Amer",ax=ax1)
sns.pointplot(data=data, x="Year", y="Europe",ax=ax2)
sns.pointplot(data=data, x="Year", y="Asia",ax=ax3)
sns.pointplot(data=data, x="Year", y="S.Amer",ax=ax4)
sns.pointplot(data=data, x="Year", y="Oceania",ax=ax5)
sns.pointplot(data=data, x="Year", y="Africa",ax=ax6)
