import pandas as pd
import datetime

# {
#     'key': 'string',
#     'date': 'string',
#     'wikidata': 'string',
#     'datacommons': 'string',
#     'country_code': 'string',
#     'country_name': 'string',
#     'subregion1_code': 'string',
#     'subregion1_name': 'string',
#     'subregion2_code': 'string',
#     'subregion2_name': 'string',
#     'locality_code': 'string',
#     'locality_name': 'string',
#     '3166-1-alpha-2': 'string',
#     '3166-1-alpha-3': 'string',
#     'aggregation_level': 'string',
#     'new_confirmed': 'string',
#     'new_deceased': 'string',
#     'new_recovered': 'string',
#     'new_tested': 'string',
#     'total_confirmed': 'string',
#     'total_deceased': 'string',
#     'total_recovered': 'string',
#     'total_tested': 'string',
#     'new_hospitalized': 'string',
#     'total_hospitalized': 'string',
#     'current_hospitalized': 'string',
#     'new_intensive_care': 'string',
#     'total_intensive_care': 'string',
#     'current_intensive_care': 'string',
#     'new_ventilator': 'string',
#     'total_ventilator': 'string',
#     'current_ventilator': 'string',
#     'population': 'string',
#     'population_male': 'string',
#     'population_female': 'string',
#     'rural_population': 'string',
#     'urban_population': 'string',
#     'largest_city_population': 'string',
#     'clustered_population': 'string',
#     'population_density': 'string',
#     'human_development_index': 'string',
#     'population_age_00_09': 'string',
#     'population_age_10_19': 'string',
#     'population_age_20_29': 'string',
#     'population_age_30_39': 'string',
#     'population_age_40_49': 'string',
#     'population_age_50_59': 'string',
#     'population_age_60_69': 'string',
#     'population_age_70_79': 'string',
#     'population_age_80_89': 'string',
#     'population_age_90_99': 'string',
#     'population_age_80_and_older': 'string',
#     'gdp': 'string',
#     'gdp_per_capita': 'string',
#     'human_capital_index': 'string',
#     'open_street_maps': 'string',
#     'latitude': 'string',
#     'longitude': 'string',
#     'elevation': 'string',
#     'area': 'string',
#     'rural_area': 'string',
#     'urban_area': 'string',
#     'life_expectancy': 'string',
#     'smoking_prevalence': 'string',
#     'diabetes_prevalence': 'string',
#     'infant_mortality_rate': 'string',
#     'adult_male_mortality_rate': 'string',
#     'adult_female_mortality_rate': 'string',
#     'pollution_mortality_rate': 'string',
#     'comorbidity_mortality_rate': 'string',
#     'hospital_beds': 'string',
#     'nurses': 'string',
#     'physicians': 'string',
#     'health_expenditure': 'string',
#     'out_of_pocket_health_expenditure': 'string',
#     'mobility_retail_and_recreation': 'string',
#     'mobility_grocery_and_pharmacy': 'string',
#     'mobility_parks': 'string',
#     'mobility_transit_stations': 'string',
#     'mobility_workplaces': 'string',
#     'mobility_residential': 'string',
#     'school_closing': 'string',
#     'workplace_closing': 'string',
#     'cancel_public_events': 'string',
#     'restrictions_on_gatherings': 'string',
#     'public_transport_closing': 'string',
#     'stay_at_home_requirements': 'string',
#     'restrictions_on_internal_movement': 'string',
#     'international_travel_controls': 'string',
#     'income_support': 'string',
#     'debt_relief': 'string',
#     'fiscal_measures': 'string',
#     'international_support': 'string',
#     'public_information_campaigns': 'string',
#     'testing_policy': 'string',
#     'contact_tracing': 'string',
#     'emergency_investment_in_healthcare': 'string',
#     'investment_in_vaccines': 'string',
#     'stringency_index': 'string',
#     'noaa_station': 'string',
#     'noaa_distance': 'string',
#     'average_temperature': 'string',
#     'minimum_temperature': 'string',
#     'maximum_temperature': 'string',
#     'rainfall': 'string',
#     'snowfall': 'string',
#     'dew_point': 'string',
#     'relative_humidity': 'string'
# }

df = pd.read_csv('./data/main.csv',
                 dtype={
                     'wikidata': 'string',
                     'datacommons': 'string',
                     'country_code': 'category',
                     'country_name': 'category',
                     'subregion1_code': 'category',
                     'subregion1_name': 'category',
                     'subregion2_code': 'category',
                     'subregion2_name': 'category',
                     'locality_code': 'category',
                     'locality_name': 'category',
                     'new_confirmed': pd.Int32Dtype(),
                     'new_deceased': pd.Int32Dtype(),
                     'new_recovered': pd.Int32Dtype(),
                     'new_tested': pd.Int32Dtype(),
                     'total_confirmed': pd.Int32Dtype(),
                     'total_deceased': pd.Int32Dtype(),
                     'total_recovered': pd.Int32Dtype(),
                     'total_tested': pd.Int32Dtype(),
                     'new_hospitalized': pd.Int32Dtype(),
                     'total_hospitalized': pd.Int32Dtype(),
                     'current_hospitalized': pd.Int32Dtype(),
                     'new_intensive_care': pd.Int32Dtype(),
                     'total_intensive_care': pd.Int32Dtype(),
                     'current_intensive_care': pd.Int32Dtype(),
                     'new_ventilator': pd.Int32Dtype(),
                     'total_ventilator': pd.Int32Dtype(),
                     'current_ventilator': pd.Int32Dtype(),
                     'population': pd.Int32Dtype(),
                     'population_male': pd.Int32Dtype(),
                     'population_female': pd.Int32Dtype(),
                     'rural_population': pd.Int32Dtype(),
                     'urban_population': pd.Int32Dtype(),
                     'largest_city_population': pd.Int32Dtype(),
                     'population_age_00_09': pd.Int32Dtype(),
                     'population_age_10_19': pd.Int32Dtype(),
                     'population_age_20_29': pd.Int32Dtype(),
                     'population_age_30_39': pd.Int32Dtype(),
                     'population_age_40_49': pd.Int32Dtype(),
                     'population_age_50_59': pd.Int32Dtype(),
                     'population_age_60_69': pd.Int32Dtype(),
                     'population_age_70_79': pd.Int32Dtype(),
                     'population_age_80_89': pd.Int32Dtype(),
                     'population_age_90_99': pd.Int32Dtype(),
                     'population_age_80_and_older': pd.Int32Dtype(),
                     'area': 'string',
                     'noaa_station': 'string',
                 },
                 parse_dates=['date'],
                 usecols=['key', 'country_name', 'subregion1_name', 'subregion2_name', 'aggregation_level', 'population', 'date', 'new_confirmed', 'new_deceased', 'total_confirmed', 'total_deceased']
                 )

df_vaccinations = pd.read_csv('./data/vaccinations.csv',
                 usecols=['date', 'key', 'total_vaccine_doses_administered', 'total_vaccine_doses_administered_janssen'],
                 parse_dates=['date'],
                 )

df = df.merge(df_vaccinations, on=['key', 'date'])

df.to_feather('./data/main.feather')

df_time_slice = df.loc[df.date > datetime.datetime.now() - pd.to_timedelta(str(30) + 'day')]

df_time_slice.reset_index(inplace=True)

df_time_slice.to_feather('./data/time_slice.feather')
