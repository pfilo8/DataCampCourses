import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from usefull_functions import ecdf,draw_bs_reps,draw_bs_pairs_linreg

sns.set()

#### DATA ####
df1975 = pd.read_csv('finch_beaks_1975.csv')
df1975['Year'] = 1975
df2012 = pd.read_csv('finch_beaks_2012.csv')
df2012['Year'] = 2012
df2012.columns = df1975.columns

df = pd.concat([df1975,df2012])

#### EDA ####
_ = sns.swarmplot(x='Year',y='Beak depth, mm',data = df)
_ = plt.xlabel('Year')
_ = plt.ylabel('Beak depth, mm')
plt.show()

#### ECDFs ####
x1975,y1975 = ecdf(df1975['Beak depth, mm'])
x2012,y2012 = ecdf(df2012['Beak depth, mm'])

_ = plt.plot(x1975,y1975,marker='.',linestyle='none')
_ = plt.plot(x2012,y2012,marker='.',linestyle='none')
plt.margins(0.02)
_ = plt.xlabel('beak depth (mm)')
_ = plt.ylabel('ECDF')
_ = plt.legend(('1975', '2012'), loc='lower right')
plt.show()

#### PARAMETER ESTIMATES ####
mean_diff = df1975['Beak depth, mm'].mean() - df2012['Beak depth, mm'].mean()
bs_replicates_1975 = draw_bs_reps(df1975['Beak depth, mm'],np.mean,size=10000)
bs_replicates_2012 = draw_bs_reps(df2012['Beak depth, mm'],np.mean,size=10000)

bs_diff_replicates = bs_replicates_1975-bs_replicates_2012
conf_int = np.percentile(bs_diff_replicates,[2.5,97.5])
print('difference of means =', mean_diff, 'mm')
print('95% confidence interval =', conf_int, 'mm')

#### HYPOTHESIS TEST ####
combined_mean = np.mean(np.append(df1975['Beak depth, mm'],df2012['Beak depth, mm']))

bd1975_shifted = df1975['Beak depth, mm'] - df1975['Beak depth, mm'].mean() + combined_mean
bd2012_shifted = df2012['Beak depth, mm'] - df2012['Beak depth, mm'].mean() + combined_mean

bs_replicates_1975 = draw_bs_reps(bd1975_shifted,np.mean,size=10000)
bs_replicates_2012 = draw_bs_reps(bd2012_shifted,np.mean,size=10000)

bs_diff_replicates = bs_replicates_1975 - bs_replicates_2012

p = np.sum(bs_diff_replicates >= mean_diff)/len(bs_diff_replicates)
print('p =',p)
if p <= 0.05:
    print('Reject null hypothesis')
else:
    print('Cannot reject null hypothesis')

#### EDA BEAK LENGTH AND DEPTH ####
bl_1975 = df[df['Year'] == 1975]['Beak length, mm']
bl_2012 = df[df['Year'] == 2012]['Beak length, mm']
bd_1975 = df[df['Year'] == 1975]['Beak depth, mm']
bd_2012 = df[df['Year'] == 2012]['Beak depth, mm']

_ = plt.plot(bl_1975,bd_1975,marker='.',linestyle='none', alpha=0.5, color='blue')
_ = plt.plot(bl_2012,bd_2012,marker='.',linestyle='none', alpha=0.5, color='red')

_ = plt.xlabel('beak length (mm)')
_ = plt.ylabel('beak depth (mm)')
_ = plt.legend(('1975', '2012'), loc='upper left')

plt.show()

#### LINEAR REGRESSIONS ####

# Compute the linear regressions
slope_1975, intercept_1975 = np.polyfit(bl_1975,bd_1975,1)
slope_2012, intercept_2012 = np.polyfit(bl_2012,bd_2012,1)

# Perform pairs bootstrap for the linear regressions
bs_slope_reps_1975, bs_intercept_reps_1975 = draw_bs_pairs_linreg(bl_1975,bd_1975,1000)
bs_slope_reps_2012, bs_intercept_reps_2012 = draw_bs_pairs_linreg(bl_2012,bd_2012,1000)

# Compute confidence intervals of slopes
slope_conf_int_1975 = np.percentile(bs_slope_reps_1975,[2.5,97.5])
slope_conf_int_2012 = np.percentile(bs_slope_reps_2012,[2.5,97.5])
intercept_conf_int_1975 = np.percentile(bs_intercept_reps_1975,[2.5,97.5])
intercept_conf_int_2012 = np.percentile(bs_intercept_reps_2012,[2.5,97.5])

# Print the results
print('1975: slope =', slope_1975,
      'conf int =', slope_conf_int_1975)
print('1975: intercept =', intercept_1975,
      'conf int =', intercept_conf_int_1975)
print('2012: slope =', slope_2012,
      'conf int =', slope_conf_int_2012)
print('2012: intercept =', intercept_2012,
      'conf int =', intercept_conf_int_2012)

# Make scatter plot of 1975 data
_ = plt.plot(bl_1975, bd_1975, marker='.',
             linestyle='none', color='blue', alpha=0.5)

# Make scatter plot of 2012 data
_ = plt.plot(bl_2012, bd_2012, marker='.',
             linestyle='none', color='red', alpha=0.5)

# Label axes and make legend
_ = plt.xlabel('beak length (mm)')
_ = plt.ylabel('beak depth (mm)')
_ = plt.legend(('1975', '2012'), loc='upper left')

# Generate x-values for bootstrap lines: x
x = np.array([9, 17])

# Plot the bootstrap lines
for i in range(100):
    plt.plot(x, bs_slope_reps_1975[i]*x+bs_intercept_reps_1975[i],
             linewidth=0.5, alpha=0.2, color='blue')
    plt.plot(x, bs_slope_reps_2012[i]*x+bs_intercept_reps_2012[i],
             linewidth=0.5, alpha=0.2, color='red')

# Draw the plot again
plt.show()

#### DEPTH RATIO ####
ratio_1975 = bl_1975/bd_1975
ratio_2012 = bl_2012/bd_2012

mean_ratio_1975 = ratio_1975.mean()
mean_ratio_2012 = ratio_2012.mean()

# Generate bootstrap replicates of the means
bs_replicates_1975 = draw_bs_reps(ratio_1975,np.mean,size=10000)
bs_replicates_2012 = draw_bs_reps(ratio_2012,np.mean,size=10000)

# Compute the 99% confidence intervals
conf_int_1975 = np.percentile(bs_replicates_1975,[0.5,99.5])
conf_int_2012 = np.percentile(bs_replicates_2012,[0.5,99.5])

# Print the results
print('1975: mean ratio =', mean_ratio_1975,
      'conf int =', conf_int_1975)
print('2012: mean ratio =', mean_ratio_2012,
      'conf int =', conf_int_2012)
