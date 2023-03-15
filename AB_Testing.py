import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

#view options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Step 1 : Data Preparation and Analysis
df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")
df_control.head()
df_test.head()


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

df_control["group"] = "control"
df_test["group"] = "test"

#Merge two dataframes with concat method
df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()
df.shape

# number of purchase for control group and test group
df.groupby("group").agg({"Purchase": "mean"})

############################################
# Step 2 : Defining the A/B Test Hypothesis
############################################

# H0 : M1 = M2 (There is no difference between the purchasing averages of control group and test group.)
# H1 : M1 = !M2 (There is a difference between the purchasing averages of the control group and the test group.)

############################################
# Step 3 : Assumption Check
############################################

# Normal Distribution

# H0 : Fits normal distribution
# H1 : Doesn't fit normal distribution

test_stat, pvalue = shapiro(df.loc[df["group"]=="control", "Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
#Test Stat = 0.9773, p-value = 0.5891
# p-value > 0.05 H0 can not be rejected.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541
# p-value > 0.05 H0 can not be rejected.

# Variance Homogeneity

# H0 : Variances are homogeneous
# H1 : Variances are not homogeneous

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 2.6393, p-value = 0.1083
# p-value > 0.05 H0 can not be rejected.

############################################
# Step 4 : Hypothesis Testing
############################################

# Normal distribution and varians homogeneity asumptions are provided
# parametric t testing

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493
# p-value > 0.05 H0 can not be rejected.
# There is no statistically significant difference between the two groups.

