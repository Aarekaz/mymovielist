path = 'src/data/web_imdb_clean/movies.csv'
path_rates = 'src/data/OECD/DP_LIVE_16072021155836489.csv'

intro = '''
# Audiences, critics and box office on IMDb
### Exploratory data analysis | Movies 2014 to 2019
The objective of this study is to look for relationships between user ratings and film critics, and the economic characteristics of films such as budget and box office receipts.
With the intention of analyzing representative data of all types of films, the IMDb portal has been used, the most complete at the international level, and the data has been extracted in two ways: downloading free relational tables from IMDb and through *web scrapping* of the movies on the IMDb portal. The scope of this study is limited by the information freely accessible on the IMDb portal, and at a temporal level, it focuses on the years between 2014 and 2019.
The initial objective was to study the 10 years prior to 2020 (from 2010 to 2019), but due to lack of resources it has only been possible to collect data for 6 years (2014 to 2019).
### Processes
#### 1. Relational tables downloaded from IMDb
IMDb offers, free of charge, a series of `.csv` files that correspond to some of the information in its database. From these tables I have obtained information such as IMDb identifier, title in Spanish and in its original version, duration, genres, IMDb rating, year.
#### 2. *Web scrapping* IMDb portal
As the files provided by IMDb do not contain economic information of the films, I have collected this information from the IMDb portal itself through *web scrapping*. The critical assessment data was also important, the Metascore, which without being IMDb's own data, can be viewed on the portal. I have also collected information that could be relevant later as directors, screenwriters, actors and countries. Due to the huge amount of information, I had to use the *parallel* library to collect information from several pages simultaneously, one page per core of my laptop's processor. The main tool for this phase was Selenium.
> **117,482 scrapped pages** (all movies from 2014 to 2020)
#### 3. Study variables
Once we have all the data available, we select our main variables for the study.
We find two types of variables: On the one hand we have the variables that make an assessment of the films - IMDb User Rating, Metascore- and on the other hand we have economic type variables (Budget, Revenue, Profit and ROI).
#### 4. *Data mining* and *merge* of tables
The next step was to clean the tables as there were many *fake* records, both in the tables downloaded from IMDb and on the portal.
In this phase it was necessary to convert the information scraped from the portal since everything was text. In the case of the budget and the collection, it was also necessary to separate the information of the currency and the amount. The currency had to be transferred to its ISO code to be able to assign the exchange rate corresponding to the currency and the year. I finally normalized the dollar values ​​for all the movies.
And, having the budget and collection information, I generated two new economic data: profit and return on investment or ROI.
#### 5. Scan
At this stage I did a univariate, bivariate and multivariate analysis of the valuation and collection data.
'''


intro_source_tools = '''
---
## Used tools
| Web scraping | datamining | Visualization |
|--- |--- |--- |
| -Visual StudioCode | - Jupyter Lab | - Stream lit |
| -Python | -Python | -Python |
| - Panda | -Regex | -Regex |
| -Selenium | - Panda | - Panda |
| -Joblib/Parallel | -Numpy | -Numpy |
| - Logging | | - Matplotlib |
| - Pickles | | - Plotly |
| | | -Google Slides |
<p><br></p>
---
## Sources
IMDd Datasets
https://datasets.imdbws.com/
IMDb. Documentation for the datasets:
https://www.imdb.com/interfaces/
OECD. Exchange rates main currencies per year:
https://data.oecd.org/conversion/exchange-rates.htm
Exchange Rates. Exchange rates for other currencies per year:
https://www.exchangerates.org.uk/
Google Developers. List of country coordinates:
https://developers.google.com/public-data/docs/canonical/countries_csv
'''


variables_intro_rating = '''
Visualizing the distribution of the IMDb Rating we can see that users tend to approve the movies. Thus, the mean and median are `6.37` and `6.4` points, respectively. The minimum value is `1.40` and the maximum is `8.6`, so we see that users continue to be demanding and the average of the maximum score is not close to the maximum possible score: `10 `.
'''

variables_intro_metascore = '''
We can see that the critic scores are more dispersed than the User Rating, and even reach the minimum and maximum scores of `1` and `100` points. Surely this is due to how the Metacritic algorithm that awards these scores in an automated way is developed. Within our dataset, the movie with the highest Metascore is 'Boyhood' from 2014, which, surprisingly, gets the perfect score: `100`.
'''

budget_intro_variables = '''
Although in this period of time we have some of the most expensive films in the history of cinema, we see that the majority are below 13.5 million dollars. 'Avengers: Endgame' is the movie with the highest budget with 378 million dollars.
'''


variables_intro_collection = '''
'''

variables_intro_benefit = '''
Again, the film with the highest value or highest profit is 'Avengers: Endgame' with more than 2.4 billion dollars. However, we see that a large percentage of movies are losing with negative values ​​for profit. 25% of movies have a loss of at least $3 million, and the median is $4.3 million.
'''

variables_intro_roi = '''
The ROI, as it is an independent variable of the budget of the film, already shows us a totally different list of films at the top of the table. In this case we have had to limit the list to films with a maximum value of 30 since we detected that there was invalid data in some cases. Surprising the number of horror or thriller movies in the top positions.
'''
