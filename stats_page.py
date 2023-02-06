from dash import dcc, html, dash_table
from dash import Input, Output, State, callback
import json
import plotly.express as px
from copy import deepcopy

import dash_bootstrap_components as dbc

import pandas as pd

with open('./data/kaf.json', encoding='utf8') as spec_codes:
    SPEC_CODES_DICT = json.load(spec_codes)

with open('./data/stat_years.json', encoding='utf8') as stats:
    STATS_DICT = json.load(stats)

with open('./data/to_rus.json', encoding='utf8') as localize_fp:
    LOCALIZE_DICT = json.load(localize_fp)

def get_df_by_base_names(base_names, df):
    comparation_list = {
         'count_human': 'Количество человек, подавших заявление',
         'count_apps': 'Количество заявлений',
         'count_apps_obsh': 'Количество заявлений, поданных на общих основаниях',
         'sred_obsh': 'Средний балл абитуриентов, подавших заявление на общих основаниях',
         'count_apps_cel': 'Количество заявлений, поданных на целевую квоту',
         'sred_cel': 'Средний балл абитуриентов, подавших заявление на целевую квоту',
         'count_apps_kvot': 'Количество заявлений, поданных на особую и специальную квоту',
         'sred_kvot': 'Средний балл абитуриентов, подавших заявление на особую и специальную квоту',
         'count_apps_plat': 'Количество заявлений, поданных на места по договорам об оказании платных услуг',
         'sred_plat': 'Средний балл абитуриентов, подавших заявление на места по договорам об оказании платных услуг',
         'count_apps_obsh_post': 'Количество заявлений, по которым абитуриенты были зачислены на общих основаниях',
         'sred_obsh_post': 'Средний балл зачисленных абитуриентов на общих основаниях',
         'min_obsh_post': 'Минимальный проходной балл зачисленного абитуриента на общих основаниях',
         'count_apps_cel_post': 'Количество заявлений, по которым абитуриенты были зачислены на целевую квоту',
         'sred_cel_post': 'Средний балл зачисленных абитуриентов на целевую квоту',
         'min_cel_post': 'Минимальный проходной балл зачисленного абитуриента на целевую квоту',
         'count_apps_kvot_post': 'Количество заявлений, по которым абитуриенты были зачислены на особую и специальную квоту',
         'sred_kvot_post': 'Средний балл зачисленных абитуриентов на особую и специальную квоту',
         'min_kvot_post': 'Минимальный проходной балл зачисленного абитуриента на особую и специальную квоту',
         'count_apps_plat_post': 'Количество заявлений, по которым абитуриенты были зачислены на места по договорам об оказании платных услуг',
         'sred_plat_post': 'Средний балл зачисленных абитуриентов на места по договорам об оказании платных услуг',
         'min_plat_post': 'Минимальный проходной балл зачисленного абитуриента на места по договорам об оказании платных услуг'}
    indexes = [list(comparation_list).index(x) for x in base_names]
    titles = [comparation_list[x] for x in base_names]
    d = [dict(df.iloc[index][1:]) for index in indexes]
    years = list(d[0])
    counts = [list(x.values()) for x in d]
    dict_to_df = {titles[x]: counts[x] for x in range(len(base_names))}
    dict_to_df['Год'] = years
    df = pd.DataFrame(dict_to_df)
    return df

def get_fig(data_frame, title):

    fig = px.bar(data_frame, x=data_frame['Год'], y=data_frame.columns, barmode='group',
                 height=400)
    fig.update_layout(
        xaxis_title="Год",
        yaxis_title='',
        legend_title="",
        legend=dict(
            x=0,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black"
            ),
            bgcolor="White",
            bordercolor="Black",
            borderwidth=2,
            yanchor="bottom"
        )
    )

    return fig

DEFAULT_DICT = {
    "code": "-",
    "name": "-",
    "count_human": 0,
    "count_apps": 0,
    "count_apps_obsh": 0,
    "sred_obsh": None,
    "count_apps_cel": 0,
    "sred_cel": None,
    "count_apps_kvot": 0,
    "sred_kvot": None,
    "count_apps_plat": 0,
    "sred_plat": None,
    "count_apps_obsh_post": 0,
    "sred_obsh_post": None,
    "min_obsh_post": 0,
    "count_apps_cel_post": 0,
    "sred_cel_post": None,
    "min_cel_post": 0,
    "count_apps_kvot_post": 0,
    "sred_kvot_post": None,
    "min_kvot_post": 0,
    "count_apps_plat_post": 0,
    "sred_plat_post": None,
    "min_plat_post": 0
}


def get_spec_codes(kaf_name):
    return SPEC_CODES_DICT[kaf_name]

def get_spec_code_stats(spec_code):
    all_year_dict = {key: val.get(spec_code, DEFAULT_DICT) for key, val in STATS_DICT.items()}
    return all_year_dict

def get_stats_df(stats_dict):
    stats_dict = deepcopy(stats_dict)
    for key in stats_dict:
        st_dict = stats_dict[key]
        if 'code' in st_dict.keys():
            del st_dict['code'], st_dict['name']

    df = {'Показатель': stats_dict['2022'].keys()}

    for key in stats_dict:
        df[key] = stats_dict[key].values()

    df = pd.DataFrame(df)

    return df


def generate_layout(kaf_name):
    spec_codes = get_spec_codes(kaf_name=kaf_name)
    options = {spec_code: f'{spec_code} - {STATS_DICT["2022"][spec_code]["name"]}' for spec_code in spec_codes}
    stats =  html.Div([
        html.H2(children=f'Статистика кафедры {kaf_name}', id='h1'),
        html.Button(children='Выйти', id='logout'),
        html.Br(),
        dcc.Dropdown(options=options, value=spec_codes[0], id='spec_codes', multi=False, clearable=False),
        html.Br(),
        dbc.Col(
            html.Div(children='', id='kaf_stats')
        ),
        dcc.Graph(id='fig1'),
        dcc.Graph(id='fig2'),
        dcc.Graph(id='fig3'),
        dcc.Graph(id='fig4'),
        dcc.Graph(id='fig5'),
    ])

    return stats

@callback(
    [Output('fig1', 'figure'), Output('fig2', 'figure'), Output('fig3', 'figure'), Output('fig4', 'figure'), Output('fig5', 'figure')],
    [Input('spec_codes', 'value')]
)
def get_plots(spec_code):
    df = get_stats_df(get_spec_code_stats(spec_code))

    df_1 = get_df_by_base_names(['sred_obsh', 'sred_cel', 'sred_kvot', 'sred_plat'], df)

    df_2 = get_df_by_base_names(['count_apps_obsh', 'count_apps_plat'], df)

    df_3 = get_df_by_base_names(['count_apps_cel', 'count_apps_kvot'], df)

    df_4 = get_df_by_base_names(['count_human'], df)

    df_5 = get_df_by_base_names(['count_apps'], df)

    fig_1 = get_fig(df_1, 'Средний балл абитуриентов')
    fig_2 = get_fig(df_2, 'Количество заявлений (общий конкурс и ДОУ)')
    fig_3 = get_fig(df_3, 'Количество заявлений (целевая и особая/специальная квота)')
    fig_4 = get_fig(df_4, 'Количество человек, подавших заявление')
    fig_5 = get_fig(df_5, 'Количество поданных заявлений')

    return fig_5, fig_4, fig_1, fig_2, fig_3

@callback(
    Output('kaf_stats', 'children'),
    [Input('spec_codes', 'value')]
)
def get_stats(spec_code):

    df = get_stats_df(get_spec_code_stats(spec_code))

    df['Показатель'] = df['Показатель'].apply(lambda var_name: LOCALIZE_DICT.get(var_name))

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'textAlign': 'left', 'minWidth': '100px'},
        export_format='xlsx'
        )

@callback(
    Output('url', 'pathname'),
    [Input('logout', 'n_clicks')]
)
def logout_button(n_clicks):
    return '/'
