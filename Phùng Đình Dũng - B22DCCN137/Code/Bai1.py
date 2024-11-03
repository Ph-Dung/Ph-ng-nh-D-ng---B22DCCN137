import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

urls = [
    "https://fbref.com/en/squads/b8fd03ef/2023-2024/Manchester-City-Stats",
    "https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats",
    "https://fbref.com/en/squads/822bd0ba/2023-2024/Liverpool-Stats",
    "https://fbref.com/en/squads/8602292d/2023-2024/Aston-Villa-Stats",
    "https://fbref.com/en/squads/361ca564/2023-2024/Tottenham-Hotspur-Stats",
    "https://fbref.com/en/squads/cff3d9bb/2023-2024/Chelsea-Stats",
    "https://fbref.com/en/squads/b2b47a98/2023-2024/Newcastle-United-Stats",
    "https://fbref.com/en/squads/19538871/2023-2024/Manchester-United-Stats",
    "https://fbref.com/en/squads/7c21e445/2023-2024/West-Ham-United-Stats",
    "https://fbref.com/en/squads/47c64c55/2023-2024/Crystal-Palace-Stats",
    "https://fbref.com/en/squads/d07537b9/2023-2024/Brighton-and-Hove-Albion-Stats",
    "https://fbref.com/en/squads/4ba7cbea/2023-2024/Bournemouth-Stats",
    "https://fbref.com/en/squads/fd962109/2023-2024/Fulham-Stats",
    "https://fbref.com/en/squads/8cec06e1/2023-2024/Wolverhampton-Wanderers-Stats",
    "https://fbref.com/en/squads/d3fd31cc/2023-2024/Everton-Stats",
    "https://fbref.com/en/squads/cd051869/2023-2024/Brentford-Stats",
    "https://fbref.com/en/squads/e4a775cb/2023-2024/Nottingham-Forest-Stats",
    "https://fbref.com/en/squads/e297cd13/2023-2024/Luton-Town-Stats",
    "https://fbref.com/en/squads/943e8050/2023-2024/Burnley-Stats",
    "https://fbref.com/en/squads/1df6b87e/2023-2024/Sheffield-United-Stats"
]
dataframes = []
for url in urls:
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    team_name = url.split("/")[-1].replace("-Stats", "")

    standard_data = []
    goalkeeping_data = []
    shooting_data = []
    passing_data = []
    pass_types_data = []
    gsc_data = []
    defensive_data = []
    possession_data = []
    playing_time_data = []
    miscellaneous_data = []

    standard_table = soup.find("table", {"id": "stats_standard_9"})
    standard_rows = standard_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề
    for row in standard_rows[:len(standard_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        min_text = cols[5].text.strip().replace(",", "")

        if not min_text.isdigit() or int(min_text) <= 90:
            continue
        player_data = {
            'Player': player_th.text.strip(),
            'Nation': cols[0].text.strip() or 'N/A',
            'Team': team_name,
            'Position': cols[1].text.strip() or 'N/A',
            'Age': cols[2].text.strip() or '0',
            'MP': cols[3].text.strip() or 'N/A',
            'Starts': cols[4].text.strip() or 'N/A',
            'Min': cols[5].text.strip() or '0',
            '90s': cols[6].text.strip() or 'N/A',
            'Gls': cols[7].text.strip() or 'N/A',
            'Ast': cols[8].text.strip() or 'N/A',
            'G+A': cols[9].text.strip() or 'N/A',
            'G-PK': cols[10].text.strip() or 'N/A',
            'PK': cols[11].text.strip() or 'N/A',
            'PKatt': cols[12].text.strip() or 'N/A',
            'CrdY': cols[13].text.strip() or 'N/A',
            'CrdR': cols[14].text.strip() or 'N/A',
            'xG': cols[15].text.strip() or 'N/A',
            'npxG': cols[16].text.strip() or 'N/A',
            'xAG': cols[17].text.strip() or 'N/A',
            'npxG+xAG': cols[18].text.strip() or 'N/A',
            'PrgC': cols[19].text.strip() or 'N/A',
            'PrgP': cols[20].text.strip() or 'N/A',
            'PrgR': cols[21].text.strip() or 'N/A',
            'Gls/90': cols[22].text.strip() or 'N/A',
            'Ast/90': cols[23].text.strip() or 'N/A',
            'G+A/90': cols[24].text.strip() or 'N/A',
            'G-PK/90': cols[25].text.strip() or 'N/A',
            'G+A-PK/90': cols[26].text.strip() or 'N/A',
            'xG/90': cols[27].text.strip() or 'N/A',
            'xAG/90': cols[28].text.strip() or 'N/A',
            'xG+xAG/90': cols[29].text.strip() or 'N/A',
            'npxG/90': cols[30].text.strip() or 'N/A',
            'npxG+xAG/90': cols[31].text.strip() or 'N/A',
        }
        standard_data.append(player_data)

    goalkeeping_table = soup.find("table", {"id": "stats_keeper_9"})
    goalkeeping_rows = goalkeeping_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề

    for row in goalkeeping_rows[:len(goalkeeping_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        keeper_data = {
            'Player': player_th.text.strip(),
            'GA': cols[7].text.strip() or 'N/A',
            'GA90': cols[8].text.strip() or 'N/A',
            'SoTA': cols[9].text.strip() or 'N/A',
            'Saves': cols[10].text.strip() or 'N/A',
            'Save%': cols[11].text.strip() or 'N/A',
            'W': cols[12].text.strip() or 'N/A',
            'D': cols[13].text.strip() or 'N/A',
            'L': cols[14].text.strip() or 'N/A',
            'CS': cols[15].text.strip() or 'N/A',
            'CS%': cols[16].text.strip() or 'N/A',
            'PKatt': cols[17].text.strip() or 'N/A',
            'PKA': cols[18].text.strip() or 'N/A',
            'PKsv': cols[19].text.strip() or 'N/A',
            'PKm': cols[20].text.strip() or 'N/A',
            'PKSave%': cols[21].text.strip() or 'N/A',
        }
        goalkeeping_data.append(keeper_data)

    # Lấy dữ liệu từ bảng "Shooting"
    shooting_table = soup.find("table", {"id": "stats_shooting_9"})
    shooting_rows = shooting_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề

    for row in shooting_rows[:len(shooting_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        shooting_data.append({
            'Player': player_th.text.strip(),
            'SGls': cols[4].text.strip() or 'N/A',
            'SSh': cols[5].text.strip() or 'N/A',
            'SSoT': cols[6].text.strip() or 'N/A',
            'SSoT%': cols[7].text.strip() or 'N/A',
            'SSh/90': cols[8].text.strip() or 'N/A',
            'SSoT/90': cols[9].text.strip() or 'N/A',
            'SG/Sh': cols[10].text.strip() or 'N/A',
            'SG/SoT': cols[11].text.strip() or 'N/A',
            'SDist': cols[12].text.strip() or 'N/A',
            'SFK': cols[13].text.strip() or 'N/A',
            'SPK': cols[14].text.strip() or 'N/A',
            'SPKatt': cols[15].text.strip() or 'N/A',
            'SxG': cols[16].text.strip() or 'N/A',
            'SnpxG': cols[17].text.strip() or 'N/A',
            'SnpxG/Sh': cols[18].text.strip() or 'N/A',
            'SG-xG': cols[19].text.strip() or 'N/A',
            'Snp:G-xG': cols[20].text.strip() or 'N/A',
        })

    passing_table = soup.find("table", {"id": "stats_passing_9"})
    passing_rows = passing_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề

    for row in passing_rows[:len(passing_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        passing_data.append({
            'Player': player_th.text.strip(),
            'Cmp': cols[4].text.strip() or 'N/A',
            'Att': cols[5].text.strip() or 'N/A',
            'Cmp%': cols[6].text.strip() or 'N/A',
            'TotDist': cols[7].text.strip() or 'N/A',
            'PrgDist': cols[8].text.strip() or 'N/A',
            'Short_Cmp': cols[9].text.strip() or 'N/A',
            'Short_Att': cols[10].text.strip() or 'N/A',
            'Short_Cmp%': cols[11].text.strip() or 'N/A',
            'Medium_Cmp': cols[12].text.strip() or 'N/A',
            'Medium_Att': cols[13].text.strip() or 'N/A',
            'Medium_Cmp%': cols[14].text.strip() or 'N/A',
            'Long_Cmp': cols[15].text.strip() or 'N/A',
            'Long_Att': cols[16].text.strip() or 'N/A',
            'Long_Cmp%': cols[17].text.strip() or 'N/A',
            'Ast': cols[18].text.strip() or 'N/A',
            'xAG': cols[19].text.strip() or 'N/A',
            'xA': cols[20].text.strip() or 'N/A',
            'A-xAG': cols[21].text.strip() or 'N/A',
            'KP': cols[22].text.strip() or 'N/A',
            '1/3': cols[23].text.strip() or 'N/A',
            'PPA': cols[24].text.strip() or 'N/A',
            'CrsPA': cols[25].text.strip() or 'N/A',
            'PrgP': cols[26].text.strip() or 'N/A',
        })

    pass_types_table = soup.find("table", {"id": "stats_passing_types_9"})
    pass_types_rows = pass_types_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề

    for row in pass_types_rows[:len(pass_types_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        pass_types_data.append({
            'Player': player_th.text.strip(),
            'Live': cols[5].text.strip() or 'N/A',
            'Dead': cols[6].text.strip() or 'N/A',
            'FK': cols[7].text.strip() or 'N/A',
            'TB': cols[8].text.strip() or 'N/A',
            'Sw': cols[9].text.strip() or 'N/A',
            'Crs': cols[10].text.strip() or 'N/A',
            'TI': cols[11].text.strip() or 'N/A',
            'CK': cols[12].text.strip() or 'N/A',
            'Corner_Kicks_In': cols[13].text.strip() or 'N/A',
            'Corner_Kicks_Out': cols[14].text.strip() or 'N/A',
            'Corner_Kicks_Str': cols[15].text.strip() or 'N/A',
            'Outcomes_Cmp': cols[16].text.strip() or 'N/A',
            'Outcomes_Off': cols[17].text.strip() or 'N/A',
            'Outcomes_Blocks': cols[18].text.strip() or 'N/A',
        })

    gsc_table = soup.find("table", {"id": "stats_gca_9"})
    gsc_rows = gsc_table.find_all('tr')[2:]  # Bỏ qua hàng tiêu đề

    for row in gsc_rows[:len(gsc_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        gsc_data.append({
            'Player': player_th.text.strip(),
            'SCA': cols[4].text.strip() or 'N/A',
            'SCA90': cols[5].text.strip() or 'N/A',
            'PassLive': cols[6].text.strip() or 'N/A',
            'PassDead': cols[7].text.strip() or 'N/A',
            'TO': cols[8].text.strip() or 'N/A',
            'Sh': cols[9].text.strip() or 'N/A',
            'Fld': cols[10].text.strip() or 'N/A',
            'Def': cols[11].text.strip() or 'N/A',
            'GCA': cols[12].text.strip() or 'N/A',
            'GCA90': cols[13].text.strip() or 'N/A',
            'GCA_PassLive': cols[14].text.strip() or 'N/A',
            'GCA_PassDead': cols[15].text.strip() or 'N/A',
            'GCA_TO': cols[16].text.strip() or 'N/A',
            'GCA_Sh': cols[17].text.strip() or 'N/A',
            'GCA_Fld': cols[18].text.strip() or 'N/A',
            'GCA_Def': cols[19].text.strip() or 'N/A',
        })

    defensive_actions_table = soup.find("table", {"id": "stats_defense_9"})
    defensive_actions_rows = defensive_actions_table.find_all('tr')[2:]
    for row in defensive_actions_rows[:len(defensive_actions_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        defensive_data.append({
            'Player': player_th.text.strip(),
            'Tkl': cols[4].text.strip() or 'N/A',
            'TklW': cols[5].text.strip() or 'N/A',
            'Def 3rd': cols[6].text.strip() or 'N/A',
            'Mid 3rd': cols[7].text.strip() or 'N/A',
            'Att 3rd': cols[8].text.strip() or 'N/A',
            'Chall_Tkl': cols[9].text.strip() or 'N/A',
            'Chall_Att': cols[10].text.strip() or 'N/A',
            'Chall_Tkl%': cols[11].text.strip() or 'N/A',
            'Chall_Lost': cols[12].text.strip() or 'N/A',
            'Blocks': cols[13].text.strip() or 'N/A',
            'Blocks_Sh': cols[14].text.strip() or 'N/A',
            'Blocks_Pass': cols[15].text.strip() or 'N/A',
            'Blocks_Int': cols[16].text.strip() or 'N/A',
            'Blocks_Tkl+Int': cols[17].text.strip() or 'N/A',
            'Blocks_Clr': cols[18].text.strip() or 'N/A',
            'Blocks_Err': cols[19].text.strip() or 'N/A',
        })

    possession_table = soup.find("table", {"id": "stats_possession_9"})
    possession_rows = possession_table.find_all('tr')[2:]
    for row in possession_rows[:len(possession_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        possession_data.append({
            'Player': player_th.text.strip(),
            'Touches': cols[4].text.strip() or 'N/A',
            'Def Pen': cols[5].text.strip() or 'N/A',
            'Def 3rd': cols[6].text.strip() or 'N/A',
            'Mid 3rd': cols[7].text.strip() or 'N/A',
            'Att 3rd': cols[8].text.strip() or 'N/A',
            'Att Pen': cols[9].text.strip() or 'N/A',
            'Live': cols[10].text.strip() or 'N/A',
            'Take-Ons_Att': cols[11].text.strip() or 'N/A',
            'Take-Ons_Succ': cols[12].text.strip() or 'N/A',
            'Take-Ons_Succ%': cols[13].text.strip() or 'N/A',
            'Take-Ons_Tkld': cols[14].text.strip() or 'N/A',
            'Take-Ons_Tkld%': cols[15].text.strip() or 'N/A',
            'Carries': cols[16].text.strip() or 'N/A',
            'Carries_TotDist': cols[17].text.strip() or 'N/A',
            'Carries_ProDist': cols[18].text.strip() or 'N/A',
            'Carries_ProgC': cols[19].text.strip() or 'N/A',
            'Carries_1/3': cols[20].text.strip() or 'N/A',
            'Carries_CPA': cols[21].text.strip() or 'N/A',
            'Carries_Mis': cols[22].text.strip() or 'N/A',
            'Carries_Dis': cols[23].text.strip() or 'N/A',
            'Receiving_Rec': cols[24].text.strip() or 'N/A',
            'Receiving_PrgR': cols[25].text.strip() or 'N/A',
        })

    playing_time_table = soup.find("table", {"id": "stats_playing_time_9"})
    playing_time_rows = playing_time_table.find_all('tr')[2:]
    for row in playing_time_rows[:len(playing_time_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        playing_time_data.append({
            'Player': player_th.text.strip(),
            'Starts': cols[8].text.strip() or 'N/A',
            'Mn/Start': cols[9].text.strip() or 'N/A',
            'Compl': cols[10].text.strip() or 'N/A',
            'Subs': cols[11].text.strip() or 'N/A',
            'Mn/Sub': cols[12].text.strip() or 'N/A',
            'unSub': cols[13].text.strip() or 'N/A',
            'PPM': cols[14].text.strip() or 'N/A',
            'onG': cols[15].text.strip() or 'N/A',
            'onGA': cols[16].text.strip() or 'N/A',
            'onxG': cols[20].text.strip() or 'N/A',
            'onxGA': cols[21].text.strip() or 'N/A',
        })

    miscellaneous_table = soup.find("table", {"id": "stats_misc_9"})
    miscellaneous_rows = miscellaneous_table.find_all('tr')[2:]
    for row in miscellaneous_rows[:len(miscellaneous_rows) - 2]:
        player_th = row.find('th', {'data-stat': 'player'})
        cols = row.find_all('td')
        miscellaneous_data.append({
            'Player': player_th.text.strip(),
            'Fls': cols[7].text.strip() or 'N/A',
            'Fld': cols[8].text.strip() or 'N/A',
            'Off': cols[9].text.strip() or 'N/A',
            'Crs': cols[10].text.strip() or 'N/A',
            'OG': cols[15].text.strip() or 'N/A',
            'Recov': cols[16].text.strip() or 'N/A',
            'Aerial_Won': cols[17].text.strip() or 'N/A',
            'Aerial_Lost': cols[18].text.strip() or 'N/A',
            'Aerial_Won%': cols[19].text.strip() or 'N/A',
        })

    df_standard = pd.DataFrame(standard_data)
    df_goalkeeping = pd.DataFrame(goalkeeping_data)
    df_shooting = pd.DataFrame(shooting_data)
    df_passing = pd.DataFrame(passing_data)
    df_pass_types = pd.DataFrame(pass_types_data)
    df_gsc = pd.DataFrame(gsc_data)
    df_defensive = pd.DataFrame(defensive_data)
    df_possession = pd.DataFrame(possession_data)
    df_playing_time = pd.DataFrame(playing_time_data)
    df_miscellaneous = pd.DataFrame(miscellaneous_data)

    merged_df = pd.merge(df_standard, df_goalkeeping, on='Player', how='outer', suffixes=('', '_Keeper'))
    merged_df = pd.merge(merged_df, df_shooting, on='Player', how='outer', suffixes=('', '_Shooting'))
    merged_df = pd.merge(merged_df, df_passing, on='Player', how='outer', suffixes=('', '_Passing'))
    merged_df = pd.merge(merged_df, df_pass_types, on='Player', how='outer', suffixes=('', '_PassTypes'))
    merged_df = pd.merge(merged_df, df_gsc, on='Player', how='outer', suffixes=('', '_GSC'))
    merged_df = pd.merge(merged_df, df_defensive, on='Player', how='outer', suffixes=('', '_Defensive'))
    merged_df = pd.merge(merged_df, df_possession, on='Player', how='outer', suffixes=('', '_Possession'))
    merged_df = pd.merge(merged_df, df_playing_time, on='Player', how='outer', suffixes=('', '_PlayingTime'))
    merged_df = pd.merge(merged_df, df_miscellaneous, on='Player', how='outer', suffixes=('', '_Miscellaneous'))

    merged_df.replace('', 'N/A', inplace=True)
    merged_df.fillna('N/A', inplace=True)
    for index, row in merged_df.iterrows():
        if row['Min'] == 'N/A':
            merged_df.drop(index, inplace=True)
    dataframes.append(merged_df)
    time.sleep(5)

result_df = pd.DataFrame()
for df in dataframes:
    result_df = pd.concat([result_df, df], ignore_index=True)

result_df['Age'] = pd.to_numeric(result_df['Age'], errors='coerce')
result_df_sorted = result_df.sort_values(by=['Player', 'Age'], ascending=[True, False])
result_df_sorted.to_csv('result.csv', index=False)