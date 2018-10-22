# Case Study from DataCamp course ...

from sqlalchemy import MetaData,Table,create_engine,cast,case,Float,select,func,desc
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Connecting with database
engine = create_engine('sqlite:///census.sqlite')
metadata = MetaData()
connection = engine.connect()
census = Table('census',metadata,autoload = True, autoload_with = engine)
state_fact = Table('state_fact',metadata,autoload=True, autoload_with = engine)


print('--------------------------------------------------')
print('Average age in US in 2008 by Gender')
stmt1 = select([census.columns.sex,(func.sum(census.columns.pop2008*census.columns.age)/
                                    func.sum(census.columns.pop2008)).label('average_age')])
stmt1 = stmt1.group_by(census.columns.sex)
results1 = connection.execute(stmt1).fetchall()
for result in results1:
    print('{:21}{}'.format(result[0],result[1]))
    

print('--------------------------------------------------')
print('Average female age in US in 2008 by State')
stmt2 = select([census.columns.state,
    (func.sum(
        case([
            (census.columns.sex == 'F', census.columns.pop2000)
        ], else_=0)) /
     cast(func.sum(census.columns.pop2000), Float) * 100).label('percent_female')
])
stmt2 = stmt2.group_by(census.columns.state)
results2 = connection.execute(stmt2).fetchall()
for result in results2:
    print('{:21}{}'.format(result.state,result.percent_female))
    

print('--------------------------------------------------')
print('Differecne between population by State from the 2000 and 2008')
stmt3 = select([census.columns.state, (census.columns.pop2008-census.columns.pop2000).label('pop_change')])
stmt3 = stmt3.group_by(census.columns.state)
stmt3 = stmt3.order_by(desc('pop_change'))
results3 = connection.execute(stmt3).fetchall()
for result in results3:
    print('{:21}{}'.format(result.state, result.pop_change))


df = pd.DataFrame(results3)
df.columns = results3[0].keys()
df.plot.bar()

plt.title('Differecne between population by State from the 2000 and 2008')
plt.xticks(range(len(df)),df.state.values, fontsize = 8)
plt.legend().set_visible(False)
plt.show()
