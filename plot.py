import pandas as pd
import numpy as np
import cufflinks as cf
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

def gen_layout(fig, title, title_size=40, legendy_anchor='bottom', legendx_anchor='center', 
               width=1000, height =600, plot_bg='#f0f0f0', paper_bg='#f0f0f0', 
               y_title=None, x_title=None, l_mar=45, r_mar=45, t_mar=115, b_mar=45, 
               x_showline=False, y_showline=False, linecolor='black', y_labels=True, 
               gridcolor='#cbcbcb', barmode='group', x_showgrid=False, y_showgrid=False,
               fontcolor="#001c40", fontsize=14):
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_size, family="Oswald, Bold", color=fontcolor)),
        width=width,
        height=height,
        barmode=barmode,
        plot_bgcolor=plot_bg,
        paper_bgcolor=paper_bg,
        yaxis_title=y_title,
        xaxis_title=x_title,
        margin=dict(l=l_mar, r=r_mar, t=t_mar, b=b_mar),        
        xaxis=dict(
            showgrid=x_showgrid,
            showline=x_showline,
            linecolor=linecolor,
            gridcolor=gridcolor
        ),
        yaxis=dict(
            showgrid=y_showgrid,
            showline=y_showline,
            showticklabels=y_labels,
            linecolor=linecolor,
            gridcolor=gridcolor
        ),
        font=dict(
            family="Oswald, Light",
            color=fontcolor,
            size=fontsize
        )
    )
    return fig

def gen_menu(active, buttons):
    """
    Generates menu configurations for dropdown.
    
    active: default button to have upon generation
    buttons: list of different menu options
    """
    updatemenus = [
        go.layout.Updatemenu(
            active=active,
            buttons=buttons,
            x=1.0,
            xanchor='right',
            y=1.1,
            yanchor='top'
        )
    ]
    return updatemenus

def gen_buttons(vals, multi=0):
    """
    Generates dropdown menu buttons.
    
    vals: list of values to turn into buttons
    """
    buttons_opts = []    
    i = 0
    for val in vals:
        if multi:
            multivals = [v for v in vals for i in range(3)]
            args = [False] * len(multivals)
            args[i:i+3] = [True] * 3
            i += 3
        else:
            args = [False] * len(vals)
            args[i] = True
            i += 1

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
    return buttons_opts

def gen_bar_top20(df, title, sub, country=False, orientation='h'):
    """
    Displays an interactive plotly graph using the given column and dataframe.
    
    df: dataframe containing relevant data
    title, sub: title and subtitle for figure
    """
    # Plot specifics
    cols = ['Qualification', 'Semi-Final', 'Final', 
            'Podium', 'Bronze', 'Silver', 'Gold']
    color_discrete_map = {"M": "#00cfe6", "F": "#ff007e", "N": "#ac8639"}
    active = 3 # Default column to show - 3: Podium
    
    # Define plot
    fig = go.Figure()
    for k, col in enumerate(cols):
        dfp = df.sort_values(col, ascending=False)[:20]
        
        if country:
            colors = ["#ac8639"] * 20
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
    buttons_opts = gen_buttons(cols)
        
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig = gen_layout(fig, title, l_mar=105, r_mar=25, t_mar=95, b_mar=45)
    fig.update_layout(
        updatemenus = gen_menu(active, buttons_opts),
        xaxis={
            'showgrid': True,
        },
        yaxis={
            'autorange': "reversed",
            'showline': True,
            'linecolor': 'black',
            'title': None
        }
    )
    
    return fig.show(config=config)

def gen_bar_top10(df, col, title, sub):
    """
    Displays an interactive plotly graph using the given column and dataframe.
    
    df: dataframe containing relevant data
    col: data to be displayed along x-axis
    title: title (and subtitle) for given visualization
    """
    vals = list(df[col].unique().astype(str))
    color_discrete_map = {"M": "#00cfe6", "F": "#ff007e"}
    active = len(vals)-1
    
    # Creates graph object figure
    fig = go.Figure()

    # Adds trace for each year to our graph object
    for val in vals:
        if df[col].dtype == 'object': #strings
            dfp = df[df[col] == val]
        else: #int
            dfp = df[df[col] == int(val)]
        
        # Get color for gender
        g = dfp['Gender']
        colors = [color_discrete_map[x] for x in g]
        
        fig.add_trace(
            go.Bar(
                x=dfp['Name'],
                y=dfp['Podiums'],
                name='',
                marker_color=colors,
                hovertemplate="<b>%{x}</b><br>Podiums: %{y}",
                visible=True if val == vals[-1] else False
            )
        )

    # Creates list of buttons for each year
    buttons_opts = gen_buttons(vals)

    # Styling
    title = f"{title}<br><sup>{sub}"
    fig = gen_layout(fig, title, l_mar=85, r_mar=85, t_mar=95, b_mar=45, y_showgrid=True, x_showline=True)
    fig.update_layout(
        updatemenus = gen_menu(active, buttons_opts),
        yaxis={ 
            'tickvals': [*range(0, 64)]
        }
    )
    
    return fig.show(config=config)

def gen_line(df, title, sub):
    fig = go.Figure()
    for col in df.columns[1:]:
        fig.add_trace(
            go.Scatter(x=df['Year'],
                       y=df.loc[:,col],
                       customdata=[f'{col}'] * len(df.columns[1:]),
                       name=f'{col}',
                       hovertemplate="<b>%{customdata}</b><br>%{x} Finalists: %{y}<extra></extra>"
                      )
        )
    
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig = gen_layout(fig, title, x_showgrid=True, y_showgrid=True, x_showline=True, 
                     l_mar=65, r_mar=125, t_mar=95, b_mar=45)
    
    return fig.show(config=config)

def gen_choro(df, title, sub, slider):
    """
    Displays an interactive plotly choropleth map with year-slider to display the 
    distribution of athletes by country over time.
    
    df: dataframe containing relevant data
    title, sub: title & subtitle for the visualization
    slider: list for slider values
    """    
    data_bal = []
    for i in slider:
        data_upd = [dict(type='choropleth',
                         name=str(i),
                         locations=df.loc[i].index,
                         z=df.loc[i],
                         locationmode='ISO-3',
                         coloraxis="coloraxis",
                         # colorbar={"x": 0.8},
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

    fig = go.Figure(data=data_bal)#, layout=layout)
    
    # Plot layout
    title = f"{title}<br><sup>{sub}"    
    fig = gen_layout(fig, title, t_mar=115)
    fig.update_layout(
        autotypenumbers='strict',
        geo=dict(scope='world', projection=dict()),
        sliders=sliders,
        coloraxis=dict(colorscale='Viridis',
                       colorbar_thickness=20,
                       colorbar_title='# of Athletes', 
                       colorbar=dict(x=0.92)))
    return fig.show(config=config)

def plot_heatmap(df, title, sub, num=4):
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

    title = f"{title}<br><sup>{sub}"
    fig = go.Figure(heat)
    fig = gen_layout(fig, title, width=1200, height=1400, x_showgrid=True, y_showgrid=True,
                    l_mar=25, r_mar=25, t_mar=115, b_mar=45)
    fig.update_layout(coloraxis=dict(colorscale='Viridis',
                                     colorbar_thickness=20),
                      yaxis=dict(tickfont=dict(size=12),
                                 autorange='reversed'))

    return fig.show(config=config)


def plot_event(df, title, sub, orientation='v'):
    """
    Displays an interactive plotly graph using the given dataframe.
    
    df: dataframe containing relevant data
    title, sub: title and subtitle for figure
    """
    # Plot specifics
    cols = ['Climbers', 'Q_Top', 'S_Top', 'F_Top', 'Q_Top%', 'S_Top%', 'F_Top%']
    hovtext = {
        'Climbers': '# of Climbers',
        'Q_Top': '# of Tops in Qualifier',
        'S_Top': '# of Tops in Semi-Finals',
        'F_Top': '# of Tops in Finals',
        'Q_Top%': '% of Tops in Qualifier',
        'S_Top%': '% of Tops in Semi-Finals',
        'F_Top%': '% of Tops in Finals'        
    }
    color_discrete_map = {"M": "#00cfe6", "F": "#ff00ff"}
    active = 4
    
    # Define plot
    fig = go.Figure()
    for k, col in enumerate(cols):
        if orientation == 'v':
            fig.add_traces(            
                go.Bar(x=df.index, 
                       y=df[col],
                       name='', 
                       customdata=[hovtext[col]] * len(df),
                       orientation=orientation,
                       marker={'color': color_discrete_map["M"]},
                       hovertemplate="<b>%{x}</b><br>%{customdata}: %{y:.2f}",
                       visible=True if k == active else False
                       ))
        else:
            fig.add_traces(
                go.Bar(x=df[col], 
                       y=df.index,
                       name='', 
                       customdata=[hovtext[col]] * len(df),
                       orientation=orientation,
                       marker={'color': color_discrete_map["M"]},
                       hovertemplate="<b>%{x}</b><br>%{customdata}: %{y:.2f}",
                       visible=True if k == active else False
                       ))
    
    # Define buttons for dropdown
    buttons_opts = gen_buttons(cols)
        
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig = gen_layout(fig, title, l_mar=105, r_mar=25, t_mar=95, b_mar=45, x_showline=True)
    fig.update_layout(
        updatemenus = gen_menu(active, buttons_opts),
        yaxis={
            'showgrid': True if orientation=='v' else False
        }
    )
    
    return fig.show(config=config)

def plot_event_multi(title, sub, df1, df2, df3):
    # Plot specifics
    col_labels = ['Climbers', 'Q_Top', 'S_Top', 'F_Top', 'Q_Top%', 'S_Top%', 'F_Top%']
    hovtext = {
        'Climbers': '# of Climbers',
        'Q_Top': '# of Tops in Qualifier',
        'S_Top': '# of Tops in Semi-Finals',
        'F_Top': '# of Tops in Finals',
        'Q_Top%': '% of Tops in Qualifier',
        'S_Top%': '% of Tops in Semi-Finals',
        'F_Top%': '% of Tops in Finals'        
    }
    color_discrete_map = {"M": "#00cfe6", "F": "#ff007e", "N": "#ac8639"}
    active = 0
    
    fig = go.Figure()
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"rowspan": 2, "colspan":1}, {}],
               [None, {}]],
        column_widths=[0.6, 0.4],
        vertical_spacing=0.1,
        horizontal_spacing=0.06,
        subplot_titles=("Event","Competition Location", "Year"))
    
    # Define plot    
    for k, colm in enumerate(col_labels):
        # Individual events plot
        fig.add_trace(
            go.Bar(x=df1[colm], 
                   y=df1.index,
                   name='', 
                   customdata=[hovtext[colm]] * len(df1),
                   orientation='h',
                   marker={'color': color_discrete_map["N"]},
                   hovertemplate="<b>%{y}</b><br>%{customdata}: %{x:.2f}",
                   showlegend=False,
                   visible=True if k == active else False
                   ),
            row=1, col=1)
        
        # Country plot
        fig.add_trace(
            go.Bar(x=df2.index, 
                   y=df2[colm],
                   name='', 
                   customdata=[hovtext[colm]] * len(df2),
                   orientation='v',
                   marker={'color': color_discrete_map["N"]},
                   hovertemplate="<b>%{x}</b><br>%{customdata}: %{y:.2f}",
                   showlegend=False,
                   visible=True if k == active else False
                   ),
            row=1, col=2)
    
        # Year plot
        fig.add_trace(
            go.Bar(x=df3.index, 
                   y=df3[colm],
                   name='', 
                   customdata=[hovtext[colm]] * len(df3),
                   orientation='v',
                   marker={'color': color_discrete_map["N"]},
                   hovertemplate="<b>%{x}</b><br>%{customdata}: %{y:.2f}",
                   showlegend=False,
                   visible=True if k == active else False
                   ),
            row=2, col=2)
        
    # Define buttons for dropdown
    buttons_opts = gen_buttons(col_labels, 1)
        
    # Styling
    title = f"{title}<br><sup>{sub}"
    fig = gen_layout(fig, title, x_showline=True, width=1100, height=1000, t_mar=115, fontsize=12)
    fig.update_layout(
        updatemenus = gen_menu(active, buttons_opts),
        xaxis=dict(showgrid=True, showline=False),
        yaxis=dict(showline=True),
        
        xaxis2=dict(showline=True, linecolor='black'),
        yaxis2=dict(showgrid=True, gridcolor='#cbcbcb', linecolor='black', showline=False),
        
        xaxis3=dict(showline=True, linecolor='black'),
        yaxis3=dict(showgrid=True, gridcolor='#cbcbcb', linecolor='black', showline=False)
    )
    
    return fig.show(config=config)