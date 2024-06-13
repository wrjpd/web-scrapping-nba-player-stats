import pandas as pd
import requests
import time
import numpy as np
import re

start_year = int(input("Choose the first year (between 1951 and 2023): "))
while start_year>2023 or start_year <1951:
    print("\n")
    print("Must be between 1951 and 2023")
    start_year = int(input("Choose the first year (between 1951 and 2023): "))

final_year = int(input("Choose the final year (between 1951 and 2023): "))
while final_year>2023 or final_year <1951:
    print("\n")
    print("Must be between 1951 and 2023")
    final_year = int(input("Choose the final year (between 1951 and 2023): "))
    
years=list(range(start_year,final_year))

print("\n")
playoffs = str(input("Must include Playoffs? (y/n)")).strip().lower()
season_type=['Regular%20Season']
if playoffs=='y': season_type.append("Playoffs")
print(season_type)



url="https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS"
r=requests.get(url=url).json()
headers=r['resultSet']['headers']

def main():  
    
    
    df_columns=['Year','Season_type']+headers
    df=pd.DataFrame(columns=df_columns)    
    
    for year in years:   
        season_year=str(year)+'-'+str(year+1)[-2:]
        for season in season_type:                 
            url=f"https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={season_year}&SeasonType={season}&StatCategory=PTS"       
            r=requests.get(url=url,
                           headers={
                                'Accept': '*/*',
                                'Accept-Encoding': 'gzip, deflate, br, zstd',
                                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                                'Connection': 'keep-alive',
                                'Host': 'stats.nba.com',
                                'Origin': 'https://www.nba.co',
                                'Referer': 'https://www.nba.com/',
                                'Sec-Fetch-Dest': 'empty',
                                'Sec-Fetch-Mode': 'cors',
                                'Sec-Fetch-Site': 'same-site',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                           }).json()
            
            temp=pd.DataFrame(r['resultSet']['rowSet'],columns=headers)
            temp['Year']=year
            temp['Season_type']=season.split('%')[0]   
            
            df=pd.concat([df,temp],axis=0)
               
    df.to_csv('nba-player-stats.csv',index=False)
    
    print('Done')
      
main()