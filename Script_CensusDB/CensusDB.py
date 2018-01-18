# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 18:26:45 2018

An exercise to access and write to a local database

@author: shan
"""

import csv
from sqlalchemy import (create_engine, MetaData,
                        select, func, desc, insert,
                        Table, Column, String, Integer,
                        case, cast, Float)

# Define and initialize engine and metadata
url = 'sqlite:///datasets/census.sqlite'
engine = create_engine(url)
connection = engine.connect()
metadata = MetaData()

"""
# Section to clear test DB, use in console
metadata.drop_all(engine)
results = connection.execute('VACUUM')
"""

# Create table in the database
census = Table('census', metadata,
               Column('state', String(30)),
               Column('sex', String(1)),
               Column('age', Integer()),
               Column('pop2000', Integer()),
               Column('pop2008', Integer()))

metadata.create_all(engine)

# Build a values list from a CSV
values_list = []

with open('datasets/census.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    for row in csv_reader:
        data = {'state': row[0],
                'sex': row[1],
                'age': row[2],
                'pop2000': row[3],
                'pop2008': row[4]}
        values_list.append(data)

# Load data into the table defined previously
results0 = connection.execute(insert(census), values_list)
print('Rowcount check:', results0.rowcount)

# Build a query to calculate weighted average age and group result by sex
stmt1 = select([census.columns.sex,
               (func.sum(census.columns.pop2008 * census.columns.age) /
                func.sum(census.columns.pop2008)).label('average_age')
                ])

stmt1 = stmt1.group_by(census.columns.sex)
results1 = connection.execute(stmt1).fetchall()

print('Average age by sex: ')
for _ in results1:
    print(_.sex, _.average_age)
print('\n')

# Build a query to calculate the percentage of females in 2000 by state
stmt2 = select([census.columns.state,
               (func.sum(
                case([(census.columns.sex == 'F', census.columns.pop2000)],
                     else_=0)) / cast(func.sum(census.columns.pop2000),
                                      Float) * 100).label('percent_female')])

stmt2 = stmt2.group_by(census.columns.state)
results2 = connection.execute(stmt2).fetchall()

print('Percent female by state in 2000: ')
for _ in results2:
    print(_.state, _.percent_female)
print('\n')

# Build query to return state name and top 10 pop. difference from 2008 to 2000
stmt3 = select([census.columns.state,
               (census.columns.pop2008 - census.columns.pop2000).
               label('pop_change')])

stmt3 = stmt3.group_by(census.columns.state)
stmt3 = stmt3.order_by(desc(stmt3.columns.pop_change))
stmt3 = stmt3.limit(10)
results3 = connection.execute(stmt3).fetchall()

print('State and top 10 population change for each record: ')
for _ in results3:
    print('{}:{}'.format(_.state, _.pop_change))
