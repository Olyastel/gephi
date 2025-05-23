import pandas as pd


df = pd.read_csv('employees.csv')
full_time = df[df['EmployeeClassificationType'] == 'Full-Time']
contract = df[df['EmployeeClassificationType'] == 'Contract']
part_time = df[df['EmployeeClassificationType'] == 'Part-Time']

df['Group'] = df['EmployeeClassificationType']
df['Performance Score'] = df['Performance Score'].fillna('Unknown')
performance_distribution = pd.crosstab(
    index=df['Group'],
    columns=df['Performance Score'],
    margins=True,
    margins_name='Total'
)

score_order = {
    'PIP': 0,
    'Needs Improvement': 1,
    'Fully Meets': 2,
    'Exceeds': 3
}

df['ScoreValue'] = df['Performance Score'].map(score_order)
average_efficiency = df.groupby('Group')['ScoreValue'].mean().round(2)

print("\nРаспределение оценок эффективности по типу занятости:")
print(performance_distribution)
print("\nСредний уровень эффективности по типу занятости:")
print(average_efficiency)

performance_distribution.to_csv('performance_by_type.csv')
average_efficiency.to_csv('average_efficiency_by_type.csv')