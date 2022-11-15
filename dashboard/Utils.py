import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html


def generate_table(dataframe, id, page_size=10, ):
    # return html.Table([
    #     html.Thead(
    #         html.Tr([html.Th(col) for col in dataframe.columns])
    #     ),
    #     html.Tbody([
    #         html.Tr([
    #             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    #         ]) for i in range(min(len(dataframe), max_rows))
    #     ])
    # ])
    return dash_table.DataTable(
        id=id,
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
        style_table={'overflowX': 'auto'},
    )


def data_imports(df):
    imports_departmens = {"91": "AMAZONAS", "05": "ANTIOQUIA", "81": "ARAUCA", "08": "ATLANTICO", "13": "BOLIVAR",
                          "15": "BOYACA", "17": "CALDAS", "18": "CAQUETA", "85": "CASANARE", "19": "CAUCA",
                          "20": "CESAR", "27": "CHOCO", "23": "CORDOBA", "25": "CUNDINAMARCA", "94": "GUANIA",
                          "44": "GUAJIRA", "95": "GUAVIARE", "41": "HUILA", "47": "MAGDALENA", "50": "META",
                          "52": "NARIÑO", "54": "NORTE DE SANTANDER", "86": "PUTUMAYO", "63": "QUINDIO",
                          "66": "RISARALDA", "88": "SAN ANDRES", "11": "SANTAFE DE BOGOTA", "68": "SANTANDER",
                          "70": "SUCRE", "73": "TOLIMA", "76": "VALLE DEL CAUCA", "97": "VAUPES", "99": "VICHADA"}
    origin = df
    df["PNK"] = df["PNK"].astype(str).str.replace(",", ".").astype(float)  # adjustment for 2017 and 2018
    df["PBK"] = df["PBK"].astype(str).str.replace(",", ".").astype(float)  # adjustment for 2017 and 2018
    df = df.groupby(['DEPIM', 'DEPTODES'], as_index=False).sum()

    df['DEPIM'] = df['DEPIM'].astype(str).str.zfill(2)
    df['DEPTODES'] = df['DEPTODES'].astype(str).str.zfill(2)
    df['DEPARTAMENTO'] = df['DEPIM'].apply(lambda x: imports_departmens.get(x))
    df['DEPARTAMENTO DESTINO'] = df['DEPTODES'].apply(lambda x: imports_departmens.get(x))
    # df['PESO TONELADAS'] = df['DEPTODES'].apply(lambda x: imports_departmens.get(x))

    df['PESO TONELADAS'] = df['PNK'].apply(lambda x: x / 1000)

    cols = df.columns.tolist()

    id = cols[0]
    cols = []
    # cols = cols[-1:] + cols[1:-1]
    cols.insert(0, id)
    cols.append("DEPARTAMENTO")
    cols.append("DEPTODES")
    cols.append("DEPARTAMENTO DESTINO")
    cols.append("PBK")
    cols.append("PNK")
    cols.append("PESO TONELADAS")

    df = df[cols]
    df = df.sort_values(by=['PNK'], ascending=False)

    return df


def build_card(imgTop, titles, details, img, links):
    cardbody = [html.H1(titles.capitalize(), className="card-title"),
                html.H3(str(list(details.values())[0]).capitalize(), className="card-title")]

    listgroup = dbc.ListGroup([dbc.ListGroupItem([f"{k}: {v} "]) for k, v in details.items()],
                              flush=True, style={"width": "18rem"}, )
    cardbody.append(listgroup)

    if imgTop:
        card_content = \
            [
                dbc.CardImg(src=img, top=False),
                dbc.CardBody(
                    cardbody,
                    className="home-card-body"
                ),
            ]

    else:
        card_content = \
            [
                dbc.CardBody(
                    cardbody,
                    className="home-card-body"
                ),
                dbc.CardImg(src=img, top=True),
            ]

    card = dbc.Card(
        card_content,
        className="home-card h-100"
    )

    return dbc.Col(
        [card],
        style={"margin": "0.5rem"},
    )
