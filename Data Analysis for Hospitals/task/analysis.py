# write your code here
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


matplotlib.use('TkAgg')  # Replace 'TkAgg' with the appropriate backend for your system



pd.set_option('display.max_columns', 8)

general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')

df_general = pd.DataFrame(general)
df_prenatal = pd.DataFrame(prenatal)
df_sports = pd.DataFrame(sports)

df_prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
df_sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

df_merge = pd.concat([df_general, df_prenatal, df_sports], ignore_index=True)

df_merge.drop(columns=['Unnamed: 0'], inplace=True)

df_cleaned = df_merge.dropna(how='all')
gender_mapping = {'female': 'f', 'male': 'm', 'man': 'm', 'woman': 'f'}
df_cleaned['gender'] = df_cleaned['gender'].map(gender_mapping)

df_cleaned.loc[df_cleaned['hospital'] == 'prenatal', 'gender'] = 'f'

columns_to_fill_with_zero = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
df_cleaned[columns_to_fill_with_zero] = df_cleaned[columns_to_fill_with_zero].fillna(0)

#print(df_cleaned.shape)
#print(df_cleaned.sample(n=20, random_state=30))

num_patients = df_cleaned['hospital'].value_counts().idxmax()
#print(f"The answer to the 1st question is {num_patients}")

stomach_related_condition = (df_cleaned['hospital'] == 'general') & (df_cleaned['diagnosis'].str.contains('stomach', case=False, na=False))
share_stomach_issues = (stomach_related_condition.sum() / df_cleaned[df_cleaned['hospital'] == 'general'].shape[0])
share_stomach_issues_rounded = round(share_stomach_issues, 3)
#print(f"The answer to the 2nd question is {share_stomach_issues_rounded}")

dislocation_issue = (df_cleaned['hospital'] == 'sports') & (df_cleaned['diagnosis'].str.contains('dislocation', case=False, na=False))
share_dislocation_issues = (dislocation_issue.sum() /df_cleaned[df_cleaned['hospital'] == 'sports'].shape[0])
share_dislocation_rounded = round(share_dislocation_issues, 3)
#print(f"The answer to the 3rd question is {share_dislocation_rounded}")

general_age = df_cleaned[df_cleaned['hospital'] == 'general']['age']
sports_age = df_cleaned[df_cleaned['hospital'] == 'sports']['age']
median_age_general = general_age.median()
median_age_sports = sports_age.median()
median_age_difference = median_age_general - median_age_sports
#print(f"The answer to the 4th question is {int(median_age_difference)}")

blood_test_taken = df_cleaned[df_cleaned['blood_test'] == 't']
blood_test_counts = blood_test_taken.groupby('hospital')['blood_test'].count()
hospital_max_tests = blood_test_counts.idxmax()
max_tests_count = blood_test_counts.max()
#print(f"The answer to the 5th question is {hospital_max_tests}, {max_tests_count} blood tests")


plt.hist(df_cleaned['age'], bins=[0, 15, 35, 55, 70, 80], color='skyblue', edgecolor='black')
plt.title('Age Distribution of Patients')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.show()


# Count the occurrences of each diagnosis
diagnosis_counts = df_cleaned['diagnosis'].value_counts()

# Create a pie chart
plt.pie(diagnosis_counts, labels=diagnosis_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Distribution of Diagnoses Among Patients')
plt.show()


sns.violinplot(x='hospital', y='height', data=df_cleaned)
plt.title('Height Distribution by Hospitals')
plt.xlabel('Hospital')
plt.ylabel('Height')
plt.show()

print(f"The answer to the 1st question: 15-35 ")
print(f"The answer to the 2nd question: pregnancy")
print(f"The answer to the 3rd question: Without specific information on the unit of measurement for height and characteristics of hospitals, it's challenging to determine the main reason for the gap and peaks.Potential reasons for the observed features could include differences in hospital specializations, measurement units, or the presence of distinct patient populations.")