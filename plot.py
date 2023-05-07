import pandas as pd
import numpy as np
import cufflinks as cf
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from plotly.offline import download_plotlyjs, init_notebook_mode
init_notebook_mode(connected=True)
cf.go_offline()

# Remove unnecessary control items in figures (for Plotly)
config = {
    'modeBarButtonsToRemove': ['zoomIn', 'zoomOut', 'resetScale2d', 'select2d', 'lasso2d'],
    'responsive': True,
    'displaylogo': False,
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'ifsc-analysis',
        'scale': 1
      }
}

def gen_bar_top20(df, title, sub, country=False, orientation='h'):
    """
    Displays an interactive plotly graph using the given column and dataframe.
    
    df: dataframe containing relevant data
    title, sub: title and subtitle for figure
    """
    # Plot specifics
    cols = ['Qualification', 'Semi-Final', 'Final', 
            'Podium', 'Bronze', 'Silver', 'Gold']
    color_discrete_map = {"M": "#10baee", "F": "#ff007e"}
    active = 3 # Default column to show - 3: Podium
    
    # Define plot
    fig = go.Figure()
    for k, col in enumerate(cols):
        dfp = df.sort_values(col, ascending=False)[:20]
        
        if country:
            colors = ["#10baee"] * 20
            y = dfp['Country']
        else:
            g = dfp['Gender']
            colors = [color_discrete_map[x] for x in g]
            y = dfp['Name']
            
        fig.add_traces(
            go.Bar(x=dfp[col], 
                   y=y,
                   customdata=[f'Total {col}s']*20,
                   name='', 
                   marker_color=colors,
                   orientation=orientation,
                   hovertemplate="<b>%{y}</b><br>%{customdata}: %{x}",
                   visible=True if k == active else False
                   ))
    
    # Define buttons for dropdown
    col_opts = list(cols)
    buttons_opts = []
    for i, opt in enumerate(col_opts):
        args = [False] * len(col_opts)
        args[i] = True
        buttons_opts.append(
            dict(
                method='restyle',
                label=opt,
                args=[{
                    'visible': args, #this is the key line!
                    'title': opt,
                    'showlegend': False
                }]
            )
        )
        
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig.update_layout(
        updatemenus = [go.layout.Updatemenu(
            active=active,
            buttons=buttons_opts,
            x=1.12,
            xanchor='right',
            y=1.1,
            yanchor='top'
            )],
        xaxis={
            'showgrid': True
        },
        yaxis={
            'autorange': "reversed",
            'showline': True,
            'linecolor': 'black',
            'title': None
        },
        title=dict(text=title, font=dict(size=30)),
        showlegend=False,
        width=1000,
        height=600,
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#f0f0f0',
        margin=dict(l=105, r=25, t=95, b=45)
    )
    
    return fig.show(config=config)


def gen_bar_top5(df, col, title):
    """
    Displays an interactive plotly graph using the given column and dataframe.
    
    df: dataframe containing relevant data
    col: data to be displayed along x-axis
    title: title (and subtitle) for given visualization
    """
    vals = list(df[col].unique().astype(str))
    
    # Creates graph object figure
    fig = go.Figure()

    # Creates dictionary of dataframes
    top5_dict = {}
    if df[col].dtype == 'object': #strings
        for val in vals:
            top5_dict[val] = df[df[col] == val]
    else: #ints
        for val in vals:
            top5_dict[val] = df[df[col] == int(val)]

    # Adds trace for each year to our graph object
    for val in vals:
        fig.add_trace(
            go.Bar(
                x=top5_dict[val]['Name'],
                y=top5_dict[val]['Podiums'],
                name=val,
                marker=dict(color='#10baee'),
                visible=True if val == vals[-1] else False
            )
        )

    # Creates list of buttons for each year
    buttons_opts = []
    for i, val in enumerate(vals):
        args = [False] * len(vals)
        args[i] = True

        buttons_opts.append(
            dict(
                method='update',
                label=val,
                args=[{
                    'visible': args, #this is the key line!
                    'title': val,
                    'showlegend': False
                }]
            )
        )

    # Styling
    fig.update_layout(
        updatemenus = [go.layout.Updatemenu(
            active=len(vals)-1,
            buttons=buttons_opts,
            x=1.12,
            xanchor='right',
            y=1.1,
            yanchor='top'
            )],
        yaxis={ 
            'tickvals': [*range(0, 64)]
        },
        title=dict(text=title, font=dict(size=30)),
        width=1000,
        height=600,
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#f0f0f0',
        yaxis_title=None,
        xaxis_title=None,
        margin=dict(l=85, r=125, t=95, b=45)
        # margin=dict(l=25, r=25, t=85, b=25)
    )

    fig.update_xaxes(
        showline=True,
        linecolor='black'
    )

    fig.update_yaxes(
        showticklabels=True,
        gridcolor='#cbcbcb'
    )
    
    return fig.show(config=config)

def gen_line(df, title, sub):
    fig = px.line(df,
                  width=1000,
                  height=600
                 )
    
    title = f"{title}<br><sup>{sub}"

    fig.update_layout(
        title=dict(text=title, font=dict(size=30)),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#f0f0f0',
        yaxis_title=None,
        xaxis_title=None,
        margin=dict(l=65, r=125, t=95, b=45)
    )
    fig.update_xaxes(
        showline=True,
        linecolor='black',
        gridcolor='#cbcbcb'
    )
    fig.update_yaxes(
        showticklabels=True,
        gridcolor='#cbcbcb'
    )
    return fig


def gen_choro(df, title, sub, slider):
    """
    Displays an interactive plotly choropleth map with year-slider to display the 
    distribution of athletes by country over time.
    
    df: dataframe containing relevant data
    title, sub: title & subtitle for the visualization
    """    
    data_bal = []
    for i in slider:
        data_upd = [dict(type='choropleth',
                         name=str(i),
                         locations=df.loc[i].index,
                         z=df.loc[i],
                         locationmode='ISO-3',
                         colorbar=dict(title='# of Athletes'),
                         visible=True if i == slider[-1] else False
                        )
                   ]    
        data_bal.extend(data_upd)
    
    # Slider creation
    steps = []
    for idx, j in enumerate(slider):
        step = dict(method="restyle",
                    args=["visible", [False] * len(data_bal)],
                    label=str(j))
        step['args'][1][idx] = True
        steps.append(step)

    # Sliders layout:
    sliders = [dict(active=len(slider) - 1,
                    currentvalue={"prefix": "Year: "},
                    pad={"t": 20},
                    steps=steps)]

    # Plot layout
    title = f"{title}<br><sup>{sub}"
    layout = dict(title=dict(text=title,
                             font=dict(size=30)),
                  geo=dict(scope='world',
                           projection=dict()),
                  sliders=sliders,
                  width=1000,
                  height=600,
                  plot_bgcolor='#f0f0f0',
                  paper_bgcolor='#f0f0f0')

    fig = go.Figure(data=data_bal, layout=layout)
    fig.update_layout(autotypenumbers='strict')
    return fig.show(config=config)


def plot_heatmap(df, num=3):
    """
    Generates interesting heatmap displaying climbers finals appearances
    over time. Sorted by the weighted average of final appearance per year.
    
    df: data frame containing all the results (all_results)
    num: threshold of finals the climber needs to have appeared in
    """
    finalists = df[df['Final'].notna()]
    num_finals = finalists.groupby('Name', as_index=False)['Final'].count()
    climbers = np.unique(num_finals.loc[num_finals['Final'] >= num, 'Name'])
    years = np.unique(finalists['Year'])
    
    # count number of finals per climber and year, and sorts
    dat = pd.DataFrame(np.nan, columns=years, index=climbers)
    grp = finalists[finalists["Name"].isin(climbers)].groupby(["Name", "Year"], as_index=False).count()
    for idx, row in grp.iterrows():
        dat.loc[row["Name"], row["Year"]] = row["Final"]
    srt = ((dat * dat.columns).mean(1)/dat.mean(1)).argsort() #weighted average

    heat = go.Heatmap(x=years,
                      y=dat.iloc[srt].index, 
                      z=dat.iloc[srt],
                      name='',
                      hoverongaps=False,
                      hovertemplate="<b>%{y}</b><br>Year: %{x}<br>Finals: %{z}",
                      coloraxis="coloraxis"
                     )    

    title = ("Finals Appearances Per Climber Per Year<br>"
            "<sup>As new climbers enter the scene, the older climbers get phased out - though some remain dominant")

    fig = go.Figure(heat)
    fig.update_layout(width=1200, height=1400,
                      title=dict(text=title,
                                 font=dict(size=30)),
                      coloraxis=dict(colorscale='Viridis',
                                     colorbar_thickness=20),
                      plot_bgcolor='#f0f0f0',
                      paper_bgcolor='#f0f0f0',
                      yaxis_autorange='reversed',
                      yaxis=dict(autorange='reversed',
                                 tickfont=dict(size=9)),
                      margin=dict(l=25, r=25, t=85, b=45))

    return fig.show(config=config)


def plot_event(df, title, sub):
    """
    Displays an interactive plotly graph using the given dataframe.
    
    df: dataframe containing relevant data
    title, sub: title and subtitle for figure
    """
    # Plot specifics
    cols = ['Event', 'Climbers', 'Q_Top', 'S_Top', 'F_Top', 'Q_Top%', 'S_Top%', 'F_Top%']
    # color_discrete_map = {"M": "#10baee", "F": "#ff007e"}
    active = 4
    
    # Define plot
    fig = go.Figure()
    for k, col in enumerate(cols):
        df[col]
        fig.add_traces(
            go.Bar(x=df.index, 
                   y=df[col],
                   # color=df[['Q_Top', 'S_Top', 'F_Top']],
                   name='', 
                   customdata=[f'Total {col}s']*len(df),
                   # marker_color=colors,
                   marker={'color': '#10baee'},
                   hovertemplate="<b>%{x}</b><br>%{customdata}: %{y:.2f}",
                   visible=True if k == active else False
                   ))
    
    # Define buttons for dropdown
    col_opts = list(cols)
    buttons_opts = []
    for i, opt in enumerate(col_opts):
        args = [False] * len(col_opts)
        args[i] = True
        buttons_opts.append(
            dict(
                method='restyle',
                label=opt,
                args=[{
                    'visible': args, #this is the key line!
                    'title': opt,
                    'showlegend': False
                }]
            )
        )
        
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig.update_layout(
        updatemenus = [go.layout.Updatemenu(
            active=active,
            buttons=buttons_opts,
            x=1.12,
            xanchor='right',
            y=1.1,
            yanchor='top'
            )],
        xaxis={
            'showgrid': True
        },
        yaxis={
            # 'autorange': "reversed",
            'showline': True,
            'linecolor': 'black',
            'title': None
        },
        title=dict(text=title, font=dict(size=30)),
        showlegend=False,
        width=1000,
        height=600,
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#f0f0f0',
        margin=dict(l=105, r=25, t=95, b=45)
    )
    
    return fig.show(config=config)