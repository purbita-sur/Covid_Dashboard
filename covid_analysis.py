import pandas as pd
import numpy as np


class covid_analysis:
    def __init__(self):
        self.world_active = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
        world_deaths = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
        world_recovered = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
        self.india = pd.read_csv("https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv ")
        self.india['Date'] = pd.to_datetime(self.india["Updated On"], format='%d/%m/%Y')
        self.world_confirmed = self.world_active.groupby("Country/Region").sum().reset_index()
        self.world_deaths = world_deaths.groupby("Country/Region").sum().reset_index()
        self.world_recovered = world_recovered.groupby("Country/Region").sum().reset_index()
        self.deaths = world_deaths.iloc[:, np.r_[0, -1]]
        self.confirmed = self.world_confirmed.iloc[:, np.r_[0, -1]]
        self.recovered = world_recovered.iloc[:, np.r_[0, -1]]

    def count_covid_cases(self):
        dead = self.deaths.iloc[:, -1].sum()
        conf = self.confirmed.iloc[:, -1].sum()
        recov = self.recovered.iloc[:, -1].sum()
        return [str(conf), str(recov), str(dead)]

    def world_graph(self):
        covid_graph = self.world_confirmed.sum(axis=0)[3:].reset_index()
        covid_graph = covid_graph.rename(columns={0: "Count", "index": "Dates"})
        return [covid_graph.iloc[:, 0].tolist(), covid_graph.iloc[:, 1].tolist()]

    def ind_count(self):
        total = self.india.groupby(by='State')['Positive'].max().sum()
        return total

    def covid_top_cases(self):
        ind_cases = self.india.groupby(by='State')['Positive'].max().reset_index()
        ind_cases = ind_cases.sort_values(by='Positive', ascending=False).head(10)
        return ind_cases

    def covid_total_tested(self):
        tot_test = self.india.groupby(by='State')['Total Tested'].max().reset_index()
        tot_test = tot_test.sort_values(by='Total Tested', ascending=False).head(10)
        return tot_test
