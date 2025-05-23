import pandas as pd

df = pd.read_csv('employees.csv')
df.columns = df.columns.str.strip()
print("Доступные колонки:", df.columns.tolist())

df_fulltime = df[df['EmployeeClassificationType'] == 'Full-Time']
employees = df_fulltime[['EmpID', 'FirstName', 'LastName', 'Title', 'DepartmentType',
                         'BusinessUnit', 'GenderCode', 'Performance Score']].copy()
employees['Label'] = employees['FirstName'] + ' ' + employees['LastName']
employees = employees.drop(columns=['FirstName', 'LastName'])


supervisors = df_fulltime[['Supervisor']].dropna().drop_duplicates()
supervisors = supervisors.rename(columns={'Supervisor': 'Label'})

all_people = pd.concat([employees[['EmpID', 'Label']], supervisors], ignore_index=True)
all_people = all_people.drop_duplicates(subset=['Label']).reset_index(drop=True)
all_people['Id'] = all_people.index + 1  #уникальные Id

nodes = pd.merge(all_people, employees, on='Label', how='left')
nodes = nodes.rename(columns={'EmpID': 'OriginalEmpID'})
nodes = nodes[['Id', 'Label', 'Title', 'DepartmentType', 'BusinessUnit', 'GenderCode', 'Performance Score']]
nodes.to_csv('nodes.csv', index=False)

edges = df_fulltime[['EmpID', 'Supervisor']].dropna()
emp_to_id = dict(zip(employees['Label'], employees['EmpID']))
emp_node_id = dict(zip(employees['EmpID'], employees['Label']))
sup_to_id = {name: all_people[all_people['Label'] == name]['Id'].iloc[0] if name in all_people.values else None for name in edges['Supervisor'].unique()}

edges['Source'] = edges['EmpID'].map(lambda x: all_people[all_people['Label'] == emp_node_id.get(x, '')]['Id'].iloc[0] if x in emp_node_id else None)
edges['Target'] = edges['Supervisor'].map(sup_to_id)
edges['Type'] = 'directed'
edges = edges[['Source', 'Target', 'Type']].dropna()
edges.to_csv('edges.csv', index=False)

print("Файлы nodes.csv и edges.csv успешно созданы")