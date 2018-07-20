import pandas as pd
from pandas import DataFrame

#title basics
tb = pd.read_csv('imdb_datasets/title_basics.tsv', sep='\t', names=['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres'])

tb_data = tb.to_dict('records')[1:]
tb_df = pd.DataFrame(tb_data)

tb_df_clean = tb_df.drop(columns=['endYear','originalTitle', 'isAdult'])

tb_mask = (tb_df_clean['startYear'] > '1999') & (tb_df_clean['titleType'] =='movie')

cleaned_data_tb = tb_df_clean[tb_mask]

##title crew (directors)
tc = pd.read_csv('imdb_datasets/title_crew.tsv', sep='\t', names=['tconst', 'directors', 'writers'])

tc_data = tc.to_dict('records')[1:]
tc_df = pd.DataFrame(tc_data)

tc_df_clean = tc_df.drop(columns='writers')


##title ratings

tr = pd.read_csv('imdb_datasets/title_ratings.tsv', sep='\t', names=['tconst','averageRating','numVotes'])

tr_data = tr.to_dict('records')[1:]
tr_df = pd.DataFrame(tr_data)


combined_tables = pd.merge(pd.merge(cleaned_data_tb,tc_df_clean, on='tconst'), tr_df, on="tconst")

combined_tables.to_csv('combined_imdb_tables.csv')
