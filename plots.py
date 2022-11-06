import pandas as pd
import plotly.express as px



def rates_area(df, currency, base):
    cur = df["ccy"][:1].squeeze()
    fig = px.area(df, x = 'date', y = base,
            template = 'simple_white'
                    )
    fig = fig.update_traces(
                            texttemplate='%{text:.2s}',
                            textposition = 'top center',
                            textfont_size = 10,
                            fillcolor = '#F7F7F7',
                            opacity = 0.1
                            )
    fig = fig.update_xaxes(title = None,
                          )

    fig = fig.update_yaxes(title = f'{cur}/{base}',
                            showgrid=True,
                            tickfont=dict(size=8))
    fig = fig.update_layout(
                            yaxis_range= [df.iloc[:,2:3].min().squeeze()*0.98, 
                            df.iloc[:,2:3].max().squeeze()*1.02],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "Foreign Exchange Rates over time",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            )
    return fig