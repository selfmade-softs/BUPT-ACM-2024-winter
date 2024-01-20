import os
from glob import glob
import pandas as pd

def read_rank(rank):
    df = pd.read_excel(rank, header=[0,1], index_col=0)
    df.columns = df.columns.get_level_values(0)
    teams = df['Team']
    teams = teams.apply(lambda x: x.split('(')[-1].split(')')[0])
    df['Team'] = teams
    return df

ranks=glob('ranks/*')
ranks=list(map(read_rank,ranks))

record=pd.DataFrame()

cols=['1月19日','1月22日','1月24日','1月26日','1月29日',
    '1月31日','2月2日','2月19日','2月21日','2月23日']

for col, rank in zip(cols[:len(ranks)],ranks):
    rank=rank.sort_values(by=['Team'])[['Team','Score']]
    rank.columns=['姓名', col]

    record = rank if record.empty else \
        pd.merge(cols, rank, how='outer', on='姓名') 
    
record.to_excel('record.xlsx', index=False, sheet_name='赛时签到表(含补签)')

print('rank to records complete')