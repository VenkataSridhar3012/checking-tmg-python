import pandas as pd
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.io as to_image
from PIL import Image

# import plotly.io as pio
import os


def melt_cols(df, cols_to_melt, names, categogies):
    df_new = pd.DataFrame()
    for i, item in enumerate(cols_to_melt):
        dft = df[[x for x in df.columns if not x in cols_to_melt]].copy()
        dft.loc[:, names[0]] = df[item]
        dft.loc[:, names[1]] = categogies[i]
        df_new = pd.concat([df_new, dft])
    return df_new


colours = {
    "dark_grey": "#404040",
    "blue": "#636efa",
    "green": "#00cc96",
    "dark_blue": "#06038D",
    "pink": "#ff007f",
    "light_grey": "#D3D3D3",
    "lighter_grey": "#F2F2F2",
}
blues = sns.light_palette(colours["blue"], n_colors=6).as_hex()
blues.reverse()
greens = sns.light_palette(colours["green"], n_colors=6).as_hex()
greens.reverse()




def make_DP_overview(
        product_segment_no,
        product_no,
        material_no,
        dmd_names,
        demand_prev_scenario=None,
        demand_prev_year=None,
        DP_backlog=None,
        demand=None,
    ):
        """filter demand hierarchical and plot"""

        if product_segment_no:
            demand_plot = demand[demand.productSegmaentNumber == product_segment_no]
            # demand_prev_scenario_plot = demand_prev_scenario[
            #     demand_prev_scenario.product_segment_no == product_segment_no
            # ]
            # demand_prev_year_plot = demand_prev_year[
            #     demand_prev_year.product_segment_no == product_segment_no
            # ]
            # DP_backlog_plot = DP_backlog[
            #     DP_backlog.product_segment_no == product_segment_no
            # ]
        elif product_no:
            demand_plot = demand[demand.productNumber == product_no]
            # demand_prev_scenario_plot = demand_prev_scenario[
            #     demand_prev_scenario.product_no == product_no
            # ]
            # demand_prev_year_plot = demand_prev_year[
            #     demand_prev_year.product_no == product_no
            # ]
            # DP_backlog_plot = DP_backlog[DP_backlog.product_no == product_no]
        elif material_no:
            demand_plot = demand[demand.materialNumber == material_no]
            # demand_prev_scenario_plot = demand_prev_scenario[
            #     demand_prev_scenario.material_no == material_no
            # ]
            # demand_prev_year_plot = demand_prev_year[
            #     demand_prev_year.material_no == material_no
            # ]
            # DP_backlog_plot = DP_backlog[DP_backlog.material_no == material_no]
        else:
            demand_plot = demand
            # demand_prev_scenario_plot = demand_prev_scenario
            # demand_prev_year_plot = demand_prev_year
            # DP_backlog_plot = DP_backlog

        demand_plot = demand_plot.groupby(["date", "demand_type"]).sum().reset_index()

        x = demand["date"].unique().tolist()
        fig = make_subplots(
            rows=1,
            cols=2,
            shared_yaxes=True,
            column_widths=[0.05, 0.95],
            horizontal_spacing=0.01,
        )

        base_for_demand = [0] * len(demand_plot["date"].unique().tolist())
        for i, dem_type in enumerate(dmd_names.keys()):
            fig.add_bar(
                x=x,
                y=demand_plot[demand_plot.demand_type == dem_type]["demand"],
                name=dem_type,
                marker_color=blues[i],
                offsetgroup="dmd",
                base=base_for_demand,
                row=1,
                col=2,
            )
            base_for_demand = [
                x + y
                for x, y in zip(
                    demand_plot[demand_plot.demand_type == dem_type]["demand"].tolist(),
                    base_for_demand,
                )
            ]

        # base_for_demand_prev_scenario = [0] * len(demand_plot["date"].unique().tolist())
        # for i, dem_type in enumerate(dmd_names.keys()):
        #     fig.add_bar(
        #         x=x,
        #         y=demand_prev_scenario_plot[
        #             demand_prev_scenario_plot.demand_type == dem_type
        #         ]["demand"],
        #         name=dem_type,
        #         marker_color=greens[i],
        #         offsetgroup="dmd_prev",
        #         base=base_for_demand_prev_scenario,
        #         row=1,
        #         col=2,
        #     )
        #     base_for_demand_prev_scenario = [
        #         x + y
        #         for x, y in zip(
        #             demand_prev_scenario_plot[
        #                 demand_prev_scenario_plot.demand_type == dem_type
        #             ]["demand"].tolist(),
        #             base_for_demand_prev_scenario,
        #         )
        #     ]

        # fig.add_trace(
        #     go.Scatter(
        #         x=x,
        #         y=demand_prev_year_plot["demand"],
        #         name="previous year",
        #         marker_color=colours["dark_blue"],
        #         showlegend=True,
        #     ),
        #     row=1,
        #     col=2,
        # )

        # fig.add_bar(
        #     x=[1],
        #     y=[DP_backlog_plot["backlog"].sum()],
        #     name="backlog",
        #     marker_color=colours["dark_grey"],
        #     row=1,
        #     col=1,
        # )

        fig.update_layout(yaxis_title="pieces")
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        return fig





def make_DP_customer_specific(
    customer,
    product_segment_no,
    product_no,
    material_no,
    dmd_names,
    demand,
    demand_prev_scenario=None, demand_prev_year=None,
    DP_backlog=None,
):
    """filter demand hierarchical and plot"""
    demand = demand[demand.customer == customer]
    # demand_prev_scenario = demand_prev_scenario[demand_prev_scenario.customer == customer]
    if demand_prev_year and "customer" in demand_prev_year.columns:
        demand_prev_year = demand_prev_year[demand_prev_year.customer == customer]
    elif demand_prev_year:
        demand_prev_year = pd.DataFrame(columns=demand_prev_year.columns)
    if DP_backlog and "customer" in DP_backlog.columns:
        DP_backlog = DP_backlog[DP_backlog.customer == customer]
    elif DP_backlog:
        DP_backlog = pd.DataFrame(columns=DP_backlog.columns)

    if product_segment_no:
        demand_plot = demand[demand.productSegmaentNumber == product_segment_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.product_segment_no==product_segment_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.product_segment_no==product_segment_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.product_segment_no==product_segment_no]
    elif product_no:
        demand_plot = demand[demand.productNumber == product_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.product_no==product_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.product_no==product_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.product_no==product_no]
    elif material_no:
        demand_plot = demand[demand.materialNumber == material_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.material_no==material_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.material_no==material_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.material_no==material_no]
    else:
        demand_plot = demand
        # demand_prev_scenario_plot = demand_prev_scenario
        # demand_prev_year_plot = demand_prev_year
        # DP_backlog_plot = DP_backlog

    demand_plot = demand_plot.groupby(["date", "demand_type"]).sum().reset_index()

    x = demand["date"].unique().tolist()

    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        column_widths=[0.05, 0.95],
        horizontal_spacing=0.01,
    )

    base_for_demand = [0] * len(demand_plot["date"].unique().tolist())
    for i, dem_type in enumerate(dmd_names.keys()):
        fig.add_bar(
            x=x,
            y=demand_plot[demand_plot.demand_type == dem_type]["demand"],
            name=dem_type,
            marker_color=blues[i],
            offsetgroup="dmd",
            base=base_for_demand,
            row=1,
            col=2,
        )
        base_for_demand = [
            x + y
            for x, y in zip(
                demand_plot[demand_plot.demand_type == dem_type]["demand"].tolist(),
                base_for_demand,
            )
        ]

    # base_for_demand_prev_scenario = [0]* len(demand_plot['date'].unique().tolist())
    # for i, dem_type in enumerate(dmd_names.keys()):
    #     fig.add_bar(x=x
    #                 , y=demand_prev_scenario_plot[demand_prev_scenario_plot.demand_type == dem_type]['demand']
    #                 , name=dem_type
    #                 , marker_color=greens[i]
    #                 , offsetgroup='dmd_prev'
    #                 , base = base_for_demand_prev_scenario
    #                 , row=1, col=2)
    #     base_for_demand_prev_scenario = [x+y for x, y in zip(demand_prev_scenario_plot[demand_prev_scenario_plot.demand_type == dem_type]['demand'].tolist(), base_for_demand_prev_scenario)]

    # fig.add_trace(go.Scatter(x=x
    #                         , y=demand_prev_year_plot['demand']
    #                         , name='previous year'
    #                         , marker_color=colours['dark_blue']
    #                         , showlegend=True)
    #                         , row=1, col=2)

    # fig.add_bar(x= [1], y=[DP_backlog_plot['backlog'].sum()]
    #                         , name='backlog'
    #                         , marker_color=colours['dark_grey']
    #                         , row=1, col=1)

    fig.update_layout(yaxis_title="pieces")
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    print(fig)
    return fig



# demand = demand[demand.customer=='none']
# demand_prev_scenario= demand_prev_scenario[demand_prev_scenario.customer=='none']
# DP_backlog = DP_backlog[DP_backlog.customer=='none']

def make_DP_customer_neutral(product_segment_no , product_no , material_no 
,demand 
,dmd_names
,demand_prev_scenario=None, demand_prev_year=None,
DP_backlog=None
):
        
    '''filter demand hierarchical and plot'''
    if demand_prev_year and 'customer' in demand_prev_year.columns:
         demand_prev_year = demand_prev_year[demand_prev_year.customer=='none']
    else:
        pass

    if DP_backlog and 'customer' in DP_backlog.columns:
         DP_backlog = DP_backlog[DP_backlog.customer=='none']
    else:
        pass

    if product_segment_no:
        demand_plot = demand[demand.productSegmaentNumber==product_segment_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.product_segment_no==product_segment_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.product_segment_no==product_segment_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.product_segment_no==product_segment_no]
    elif product_no:
        demand_plot = demand[demand.productName==product_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.product_no==product_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.product_no==product_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.product_no==product_no]
    elif material_no:
        demand_plot = demand[demand.materialNumber==material_no]
        # demand_prev_scenario_plot = demand_prev_scenario[demand_prev_scenario.material_no==material_no]
        # demand_prev_year_plot = demand_prev_year[demand_prev_year.material_no==material_no]
        # DP_backlog_plot = DP_backlog[DP_backlog.material_no==material_no]
    else:
        demand_plot = demand
        # demand_prev_scenario_plot = demand_prev_scenario
        # demand_prev_year_plot = demand_prev_year
        # DP_backlog_plot = DP_backlog

    demand_plot = demand_plot.groupby(['date', 'demand_type']).sum().reset_index()

    x = demand['date'].unique().tolist()

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, column_widths=[0.05, 0.95], horizontal_spacing=0.01)

    base_for_demand = [0]* len(demand_plot['date'].unique().tolist())
    for i, dem_type in enumerate(dmd_names.keys()):
        fig.add_bar(x=x
                    , y=demand_plot[demand_plot.demand_type == dem_type]['demand']
                    , name=dem_type
                    , marker_color=blues[i]
                    , offsetgroup='dmd'
                    , base = base_for_demand
                    , row=1, col=2)
        base_for_demand = [x+y for x, y in zip(demand_plot[demand_plot.demand_type == dem_type]['demand'].tolist(), base_for_demand)]

    # base_for_demand_prev_scenario = [0]* len(demand_plot['date'].unique().tolist())
    # for i, dem_type in enumerate(dmd_names.keys()):
    #     fig.add_bar(x=x
    #                 , y=demand_prev_scenario_plot[demand_prev_scenario_plot.demand_type == dem_type]['demand']
    #                 , name=dem_type
    #                 , marker_color=greens[i]
    #                 , offsetgroup='dmd_prev'
    #                 , base = base_for_demand_prev_scenario
    #                 , row=1, col=2)
    #     base_for_demand_prev_scenario = [x+y for x, y in zip(demand_prev_scenario_plot[demand_prev_scenario_plot.demand_type == dem_type]['demand'].tolist(), base_for_demand_prev_scenario)]

    # fig.add_trace(go.Scatter(x=x
    #                         , y=demand_prev_year_plot['demand']
    #                         , name='previous year'
    #                         , marker_color=colours['dark_blue']
    #                         , showlegend=True)
    #                         , row=1, col=2)

    # fig.add_bar(x= [1], y=[DP_backlog_plot['backlog'].sum()]
    #                         , name='backlog'
    #                         , marker_color=colours['dark_grey']
    #                         , row=1, col=1)


    fig.update_layout(yaxis_title = 'pieces'
        )
    fig.update_xaxes(showticklabels=False, row=1, col=1)

    return fig