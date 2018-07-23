

genre_order = [gen.to_dict() for gen in Genre.query.order_by(Genre.name).all()]
#shows a count of how many genres had movies
def genre_count_layout():
    genres = [gen.name for gen in Genre.query.order_by(Genre.name).all()]
    genre_count = [Genre.query.filter(Genre.id == MovieGenre.genre_id).filter(Genre.name== type).count() for type in genres]
    return {'data' : [{
                 'x' : genres,
                 'y' : genre_count,
                 'name' : "Movie Genres",
                 'type' : 'bar'
                 }],
                 'layout' : {'title': "Total Genres Released"}
                 }

def movies_to_genre(genre):
    pay_movies = [movie for movie in Movie.query.filter(Movie.revenue >  0).all()]
    total = 0
    for pay in pay_movies:
        if pay.title in genre['movies']:
            total += pay.revenue
    tot =round(total)
    return '${:,}'.format(tot)



#Genre total made
def genre_total_layout():
    total = [movies_to_genre(g) for g in genre_order]
    x_values = [genre['name'] for genre in genre_order]
    y_values = total
    return  {'data' : [{
                 'x' : x_values,
                 'y' : y_values,
                 'name' : "Movie Genres",
                 'type' : 'bar',
                 'color' : "green"
                 }],
                 'layout' :{'title': "Total Amount made for each Genre"}
                 }

        # avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))

def genre_avg(genre):
    pay_movies = [movie for movie in Movie.query.filter(Movie.revenue >  0).all()]
    total = 0
    amt = 0
    for pay in pay_movies:
        if pay.title in genre['movies']:
            total += pay.revenue
            amt+=1
    full_avg = round(total/amt)
    return '${:,}'.format(full_avg)
#Genre avg made
def genre_avg_layout():
    total = [genre_avg(g) for g in genre_order]
    x_values = [genre['name'] for genre in genre_order]
    y_values = total
    return {'data' : [{
                 'x' : x_values,
                 'y' : y_values,
                 'name' : "Movie Genres",
                 'type' : 'bar',
                 'color' : 'red'
                 }],
                 'layout' : {'title': "Average Amount Made for each Genre"}
                 }
app.layout = html.Div(children =[
    html.H1('Welcome to our Movie Database.'),
    html.H3('To fully enjoy your experience, play around with different routes to learn more about movie performance.'),
    html.H2('Our movies genres'),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[
            {'label': 'Count', 'value': 'CT'},
            {'label': 'Total', 'value': 'TOT'},
            {'label': 'Average', 'value': 'AVG'}
        ],
        value='CT'
    ),
    html.Div(id='genres-graph'),


])


@app.callback(
    Output('genres-graph', 'children'),
    [Input('genre-dropdown', 'value')])

def update_output(value):
    if value == 'CT':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_count_layout())
    elif value == 'TOT':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_total_layout())
    elif value == 'AVG':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_avg_layout())
    else:
        return "Error, no value"
