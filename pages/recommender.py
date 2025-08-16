import ast
import dash
from dash import dcc, html, callback, Output, Input, State #Clientside_callback, ClientFunction
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from shared_data import  df_sunburst, df_books, df_users # Import your data


dash.register_page(__name__, name='Your Profile')

layout = dbc.Container([
    # "Login" Section
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("User Profile"),
                dbc.CardBody([
                    html.P("Enter your User ID to see your personalized dashboard."),
                    dbc.Input(id='user-id-input', placeholder="Enter User ID...", type='text', className="mb-2"),
                    dbc.Button("Load Profile", id='load-profile-button', color="primary"),
                ])
            ]),
            width=12,
            lg=6,
            className="mx-auto mb-4"  # Center the login box on large screens
        )
    ),

    # This Div will be updated by the callback after "login"
    dcc.Loading(html.Div(id='profile-content-area'))

], fluid=True)

# --- Callback to Update Page Content ---
@callback(
    Output('profile-content-area', 'children'),
    Input('load-profile-button', 'n_clicks'),
    State('user-id-input', 'value'), # Use State to get the value only when the button is clicked
    prevent_initial_call=True
)
def update_profile_page(n_clicks, user_id):
    if not user_id:
        return dbc.Alert("Please enter a User ID.", color="warning")

    # --- Filter data for the selected user ---
    real_id =df_users[df_users['dummy_id'] == user_id]['user_id'].values[0]
    user_name = df_users[df_users['dummy_id'] == user_id]['name'].values[0]
    user=df_users[df_users['dummy_id'] == user_id]

    if user.empty:
        return dbc.Alert(f"No data found for User ID: {user_id}", color="danger")

    # --- 1. Calculate KPI Metrics ---
    books_read = df_users[df_users['dummy_id']==user_id]['books_read'].values[0]
    avg_user_rating = df_users[df_users['dummy_id']==user_id]['avg_rating'].values[0]
    avg_reading_time = pd.to_timedelta(df_users[df_users['dummy_id']==user_id]['avg_reading_time'].iloc[0])

    try:
        fav_genre=df_users[df_users['dummy_id']==user_id]['favorite_genre']
    except (KeyError, IndexError):
        fav_genre = "N/A"

    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H4(books_read), html.P("Books Read")])), className="text-center"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4(f"{avg_user_rating:.2f} ★"), html.P("Your Avg. Rating")])),
                className="text-center"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4(f"{avg_reading_time.days} days, {int(avg_reading_time.seconds/3600)} hrs"), html.P("Avg. Reading Time")])),
                className="text-center"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4(fav_genre), html.P("Favorite Genre")])), className="text-center"),
    ])

    # --- 2. Create Virtual Bookshelf (Recently Read) ---
    recent_books_list = df_users[df_users['dummy_id']==user_id]['recent_reads'].iloc[0]
    recent_books = df_books[df_books['work_id'].isin(recent_books_list)][['image_url', 'original_title', 'work_id']]
    bookshelf_cards = [
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src=row['image_url'],
                            top=True,
                            style={'height': '250px', 'objectFit': 'contain'}),
                dbc.CardBody([
                    dcc.Link(html.H6(row['original_title'], className="card-title"),
                            href = f"/book_dive/{row['work_id']}", className = 'text-black fw-bold me-2'
                             ),
                    #html.P(f"You rated: {row['rating']} ★", className="small")
                ], className='border-0')
            ], className = 'border-0'),
            width=6, lg=1
        ) for i, row in recent_books.iterrows()
    ]
    bookshelf = dbc.Row(bookshelf_cards, className='flex-nowrap', style={'overflowX': 'auto', 'padding': '15px'})
    book_id_string = df_users[df_users ['dummy_id'] == user_id]['book_recs_id'].iloc[0]
    recshelf_list=ast.literal_eval(book_id_string)
    recshelf_cards = [
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src=df_books[df_books['work_id']==id]['image_url'],
                            top=True,
                            style={'height': '250px', 'objectFit': 'contain'}),
                dbc.CardBody([
                    dcc.Link(html.H6(df_books[df_books['work_id']==id]['original_title'], className="card-title"),
                             href=f"/book_dive/{df_books[df_books['work_id']==id]['work_id']}", className='text-black fw-bold me-2'),
                ], className='border-0')
            ], className='border-0'),
            width=6, lg=1
        ) for id in recshelf_list
    ]
    recshelf = dbc.Row(recshelf_cards, className='flex-nowrap', style={'overflowX': 'auto', 'padding': '15px'})


    # --- 3. Create Personalized Visualizations ---
    # Rating Habits Bar Chart
    rating_cols = ['5_star_rating', '4_star_rating', '3_star_rating', '2_star_rating', '1_star_rating']
    rating_values = list(df_users[df_users['dummy_id']==user_id][rating_cols].iloc[0])
    rating_labels = ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star']
    ratings_fig = px.bar(
        y=rating_values, x=rating_labels, orientation='v',
        labels={'y': 'Number of Books', 'x': ''},
        color = rating_values, color_continuous_scale=['#B0B8C0', '#4A6D8C']#, '#4A6D8C']
    )

    ratings_fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor='white',
        margin=dict(t=40, l=0, r=0, b=0),
    )


    # Reading Tastes Sunburst
    tastes_fig = px.sunburst(
        df_sunburst[df_sunburst['user_id'] == real_id].dropna(subset=['main_genre', 'author']),
        path=['main_genre', 'author'],
        title="Your Reading Tastes: Genres & Authors"
    )
    tastes_fig.update_layout(margin=dict(t=40, l=0,r=0, b=0))

    visualizations = dbc.Row([
        dbc.Col(dcc.Graph(figure=ratings_fig), width=12, md=4),
        dbc.Col(dcc.Graph(figure=tastes_fig), width=12, md=4),
    ], className="mt-4")

    # --- Assemble the Final Layout for the user ---
    return html.Div([
        html.H2(f"Welcome, {user_name}"),
        html.Hr(),
        kpi_cards,
        html.H3("Your Recent Reads", className="mt-4"),
        bookshelf,
        html.Hr(),
        visualizations,
        html.H3("Top Picks For You", className="mt-4"),
        recshelf,

    ])