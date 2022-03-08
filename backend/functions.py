import streamlit as st
from item_recommender import df_f

posters=[]
def movie_bar(n):
    
    md_parasite = "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UY720_.jpg"
    md_boyhood = "https://m.media-amazon.com/images/M/MV5BMTYzNDc2MDc0N15BMl5BanBnXkFtZTgwOTcwMDQ5MTE@._V1_FMjpg_UX1000_.jpg"
    md_endgame = "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UY720_.jpg"
    md_interstellar = "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UY720_.jpg"
    md_showman = "https://m.media-amazon.com/images/M/MV5BYjQ0ZWJkYjMtYjJmYS00MjJiLTg3NTYtMmIzN2E2Y2YwZmUyXkEyXkFqcGdeQXVyNjk5NDA3OTk@._V1_FMjpg_UY720_.jpg"
    md_split = "https://m.media-amazon.com/images/M/MV5BZTJiNGM2NjItNDRiYy00ZjY0LTgwNTItZDBmZGRlODQ4YThkL2ltYWdlXkEyXkFqcGdeQXVyMjY5ODI4NDk@._V1_FMjpg_UY720_.jpg"
    md_sw_despertar = "https://m.media-amazon.com/images/M/MV5BOTAzODEzNDAzMl5BMl5BanBnXkFtZTgwMDU1MTgzNzE@._V1_FMjpg_UY720_.jpg"
    md_lalaland = "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_FMjpg_UY720_.jpg"

    # col1, col2, col3, col4, col5, col6, col7, col8,col9 = st.columns(9)

    # with col1:
    #     st.image(md_parasite, use_column_width='always')
    # with col2:
    #     st.image(md_endgame, use_column_width='always')
    # with col3:
    #     st.image(md_showman, use_column_width='always')
    # with col4:
    #     st.image(md_interstellar, use_column_width='always')
    # with col5:
    #     st.image(md_boyhood, use_column_width='always')
    # with col6:
    #     st.image(md_split, use_column_width='always')
    # with col7:
    #     st.image(md_sw_despertar, use_column_width='always')
    # with col8:
    #     st.image(md_lalaland, use_column_width='always')
    # with col9:
    #     st.image(md_lalaland, use_column_width='always')

    ncol = n
    wcol = 4

    cols = st.columns(ncol)

    for i in range(ncol):
        col = cols[i % wcol]
        col.image(posters[i], use_column_width="always")
