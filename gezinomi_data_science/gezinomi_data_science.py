#######################
# Potential Customer Yield Calculation with Rule-Based Classification
#######################

#######################
# Business Problem
#######################
# Gezinomi creates new level-based sales definitions by using some features of the sales it makes.
# To create and create segments according to these new sales definitions and to attract new customers to the company according to these segments.
# wants to estimate how much money it can earn on average.
# For example: It is desired to determine how much a customer who wants to go to an All Inclusive hotel from Antalya during a busy period can earn on average.
#############################################
# PROJECT TASKS
#######################

#######################
# TASK 1: Answer the following questions.
#######################
# Question 1: Read the gezinomi.xlsx file and show general information about the data set.
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
df = pd.read_excel('dataset/gezinomi.xlsx')
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(df.head())
print(df.shape)
print(df.info())


# Question 2: How many unique cities are there? What are their frequencies?
print(df["SaleCityName"].nunique())
print(df["SaleCityName"].value_counts())

# Question 3: How many unique Concepts are there?
df["ConceptName"].nunique()

# Question 4: How many sales were made from which Concept?
df["ConceptName"].value_counts()

# Question 5: How much was earned from sales in total by city?
df.groupby("SaleCityName").agg({"Price": "sum"})

# Question 6: How much was earned according to concept types?
df.groupby("ConceptName").agg({"Price": "sum"})

# Question 7: What are the PRICE averages by city?
df.groupby(by=['SaleCityName']).agg({"Price": "mean"})

# Question 8: What are the PRICE averages according to concepts?
df.groupby(by=['ConceptName']).agg({"Price": "mean"})

# Question 9: What are the PRICE averages in the City-Concept breakdown?
df.groupby(by=["SaleCityName", 'ConceptName']).agg({"Price": "mean"})


#############################################
# TASK 2: Convert the sales_checkin_day_diff variable into a new categorical variable called EB_Score.
#############################################
bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)
#############################################
# TASK 3: Look at wage averages and frequencies in City, Concept, [EB_Score, Season, CInday] breakdown
#############################################
# Wage averages in City-Concept-EB Score breakdown
df.groupby(by=["SaleCityName", 'ConceptName', "EB_Score" ]).agg({"Price": ["mean", "count"]})

# Wage averages by City-Concept-Season
df.groupby(by=["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})

# Wage averages in City-Concept-Cinday breakdown
df.groupby(by=["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})


#######################
# TASK 4: Sort the output of the City-Concept-Season breakdown according to PRICE.
#######################
# To better see the output in the previous question, apply the sort_values ​​method to PRICE in decreasing order.
# Save the output as agg_df.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
agg_df.head(20)

#############################################
# TASK 5: Convert the names in the index into variable names.
#######################
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.
agg_df.reset_index(inplace=True)

agg_df.head()
#############################################
# TASK 6: Define new level based sales and add them to the data set as a variable.
#############################################
# Define a variable called sales_level_based and add this variable to the data set.
agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis=1)


#############################################
# TASK 7: Divide the personas into segments.
#############################################
# Segment by PRICE,
# add the segments to agg_df with the name "SEGMENT"
# describe the segments
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

#############################################
# TASK 8: Sort the final df according to the price variable.
# In which segment is "ANTALYA_HERŞEY DAHIL_HIGH" and how much does it cost?
#############################################
agg_df.sort_values(by="Price")


new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

