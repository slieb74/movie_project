## Gathering Insights from Movie Box Office Performance and Reviews

### Goal

To understand which types of movies tended to perform well in the box office, and whether seasonality had a large impact 

### ETL

We gathered our data from two sources. First, we got the director names, genres, and IMDb rating from datasets provided by IMDb. Second, we called TheMovieDB's API to get budget, revenue, release date, and runtime data. Both sources identified movies using the same ID code, so we merged the two data streams into one dataframe using Pandas. We limited the scope of our data to only films released since 2000.

### SQL Database

The schema of our SQL Database consisted of 3 primary classes: Movie, Genre, and Director. There was a many-to-many relationship between the Movie and Genre classes, and a one-to-one relationship between the Movie and Director classes as we only focused on the primary director for each movie.

### Dashboard

To show our visualizations, we built a dashboard using Flask as the backend and Dash as the front end.  Our dashboard consisted of three main tabs, one for each of the Movie, Genre, and Director classes. Under each tab, a user can select from a dropdown of options or select radio buttons to see different charts and visualizations highlighting some of the features we used. 

#### Movies Released by Month 

#### Detailed Movie Info by Month
![img] (https://github.com/slieb74/movie_project/blob/master/images/Screen%20Shot%202018-10-08%20at%202.39.18%20PM.png)

#### Average Revenue by Season

#### Budget vs. Revenue

#### Revenue vs. IMDb Rating

#### IMDb Rating vs. Profit

#### Average Revenue per Genre

#### Genre Profit Comparison by Month

#### Revenue per Director
