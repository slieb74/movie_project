## Gathering Insights from Movie Box Office Performance and Reviews

### Goal

To understand which types of movies tended to perform well in the box office, and whether seasonality had a large impact.

###### Dashboard Landing Page
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-12%20at%202.10.32%20PM.png">

### ETL

We gathered our data from two sources. First, we got the movie names, directors, genres, IMDb rating, and number of user reviews from three datasets provided by IMDb that we merged together and loaded with Pandas. Second, we called TheMovieDB's API to get budget, revenue, release date, and runtime data. The API only allowed us to submit 40 requests at once, so we integrated a sleep timer into our function that stopped for 10 seconds after every 40 calls. Due to time and computational constraints, we only called 25,000 movies using the API. Due to data leakage, and a lot of unused id codes on TheMovieDB's API, 25,000 calls resulted in way fewer actual movies. Once we had all of the data from the API in JSON format, we converted it into a Pandas dataframe. 

Both sources identified movies using the same ID code, so we merged the two data streams into one dataframe using Pandas. We limited the scope of our data to only films released since 2000, which resulted in a dataset of roughtly 1,500 movies.

### SQL Database

The schema of our SQL Database consisted of 3 primary classes: Movie, Genre, and Director. There was a many-to-many relationship between the Movie and Genre classes, and a one-to-many relationship between the Movie and Director classes as we only focused on the primary director for each movie.

The Movie class consisted of the following features: a unique ID code, the movie title, budget ($), international gross revenue ($), release date, runtime (minutes), user IMDb rating (0-10), genres, director, and a unique director ID code. The Director class consisted of a unique director ID, director name, and movies they directed. The Genre class consisted of the genre name, and all associated movies from that genre.

The Movie and Director classes backpopulated each other due to the one-to-many relationship. To deal with the many-to-many relationship between movies and genres, we added another class called MovieGenre which stored each movie id and genre id pairing. If a movie was part of three genres, it would appear three times in this table.

### Dashboard

To show our visualizations, we built a dashboard using Flask as the backend and Dash as the front end. We used numerous callback methods to allow for interactivity and user-responsiveness in our Dashboard. To make it visually pleasing, we used HTML templates to customize each landing page. Our dashboard consisted of three main tabs, one for each of the Movie, Genre, and Director classes. Under each tab, a user can select from a dropdown of options or select radio buttons to see different charts and visualizations highlighting some of the features we used. Whenever a dropdown or button was selected, the callbacks would find the associated routes we created and update the page accordingly. 

Beleow is a selection of different graphs displayed on our dashboard.

#### Movies Released by Month 
* Distribution of when movies in our dataset were released.
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.39.46%20PM.png" width='950' height='250'>

#### Detailed Movie Info by Month
* Can select any month and see which movies were released, and its associated features.
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.39.18%20PM.png" width='950' height='250'>

#### Average Revenue by Season
* Interesting to see that Summer movies had the highest average revenue despite containing the least common months for movie releases in our dataset. 
* However, the Summer is a popular time for high budget action movies (Spider-Man, Star Wars) which likely influenced the data.
<p align="center">
  <img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.40.09%20PM.png" width='350' height='250'>
</p>

#### Budget vs. Revenue
* Scatter plot that compares money spent vs. earned for each movie.
* Can also select plots between budget & IMDb rating, revenue & IMDb rating, runtime & profit, and IMDB rating & profit
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.41.20%20PM.png" width='850' height='300'>

#### Average Revenue per Genre
* Note: movies with multiple genres were counted for each genre they were considered part of
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.43.12%20PM.png" width='950' height='250'>

#### Genre Profit Comparison by Month
* Can compare how profit, revenue, and number of movies released per month differed for each of the genres.
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.43.49%20PM.png" width='950' height='250'>

#### Revenue per Director
* Allows the user to get a sense of which directors tended to make blockbuster films.
<img src="https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.45.05%20PM.png" width='950' height='300'>

### Next Steps
- Implement a regression model to predict revenue and/or IMDb rating based off other features
- Add more visualizations and interactive features to the dashboard
- Increase the scope to cover more than just movies from the 2000s
- Time series analysis to account for seasonal impacts
