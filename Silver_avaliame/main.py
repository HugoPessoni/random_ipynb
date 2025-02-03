from maps_scraper import Maps_Scraper
import pandas as pd
from pandas_gbq import read_gbq
import os

def read_from_bigquery(table_name: str) -> pd.DataFrame:
    project_id = os.getenv('PROJECT_ID')

    # Query para ler todos os dados da tabela
    query = f"SELECT * FROM `{project_id}.{table_name}`"

    df = read_gbq(query, project_id=project_id)

    return df

def only_non_scraped() -> pd.DataFrame:
    names_table = os.getenv('RESTAURANTS_NAMES_TABLE')
    reviews_table = os.getenv('DATASET_TABLE')

    df_names = read_from_bigquery(names_table)
    df_names = df_names.drop_duplicates()

    df_reviews = read_from_bigquery(reviews_table)

    df_names = df_names[~df_names['restaurant_name'].isin(df_reviews['restaurant'])]

    return df_names

def main():
    restaurants_list = only_non_scraped()

    for _, row in restaurants_list.iterrows():
        url = row['url']
        name = row['restaurant_name']
        n_reviews = row['reviews_number']
        print(f'Scraping {name}')
        scraper = Maps_Scraper(url=url, restaurant_name=name, n_reviews=n_reviews)
        scraper.start_scrap()


if __name__ == "__main__":
    main()
    