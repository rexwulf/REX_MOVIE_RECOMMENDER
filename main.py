import os
import sys
import re
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine    

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def erase_last(n=1):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

if __name__ == '__main__':
    item_cosine = np.load('./data/item_item_cosine_values.txt.npz')['a']  #load cosine table
    df_movies = pd.read_table('./data/ml-1M/movies.dat',sep='::',engine='python', usecols=['movieId','title']) #load movies data
    
    df_movies.style.set_properties(**{'text-align': 'right'})
    
    while(1):
        cls()
        print("Search movie:")
        query = input()

        pattern = '^'+query
        print("\nMovies found:\n")
        search_res = df_movies[df_movies['title'].str.contains(pattern,flags=re.IGNORECASE)]
        print(search_res.to_string(index=False))

        print("\nSelect Movies by entering Id: ")
        movie = int(input())

        movie_cand = item_cosine[movie]  #take out the column that contains cosine similarity of movie with all other movies
        result = np.argsort(movie_cand)[-20:] #pick top 20 elements with highest similarity

        print("\nTop recommendations liked by similar users:\n")
        cnt=1
        for r in result[-5:]:
            print(cnt,'.',df_movies.loc[df_movies['movieId'] == r]['title'].to_string(index=False))
            cnt+=1
        
        print("\nPress 1 for more recommendations,0 for new search:")
        resp = input()
        
        if resp:
            erase_last(3)
            for r in result[5:20]:
                print(cnt,'. ',df_movies.loc[df_movies['movieId'] == r]['title'].to_string(index=False))
                cnt+=1

        input("\nPress enter for new search.")
        cls()

