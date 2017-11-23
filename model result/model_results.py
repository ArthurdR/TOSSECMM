#
# __________Background__________
#
# this piece of code read the model's outputs, store them into dictionaries and
# pandas DataFrames, and display graphs to show the model's results.

import pandas as pd
import matplotlib.pyplot as plt

regions = ('LONG', 'LAV', 'CN', 'CS', 'MTL')
other_regions = ('LAV', 'CN', 'CS', 'MTL')
urban_forms = ('CV', 'BF', 'BM', 'BD', 'IND', 'AGR')
energy_technologies = ('IMPE', 'IMPP', 'IMPGN', 'IMPBIO', 'IMPA')
fuels = ('E', 'P', 'GN', 'BIO', 'A')

# this function converts all data in a dataframe into numeric values.

def to_num(input_df):
    for col in input_df.columns:
        input_df[col] = pd.to_numeric(input_df[col])

# __________Importing accumulated technology gain__________

acc_tech_gain_csv = pd.read_csv('accumulated_tech_gain.csv')
acc_tech_gain_csv.rename(columns={'LONG': 'Year'}, inplace=True)

acc_tech_gain = {}

acc_tech_gain['LONG'] = acc_tech_gain_csv[:21].set_index('Year')
acc_tech_gain['LAV'] = acc_tech_gain_csv[22:43].set_index('Year')
acc_tech_gain['CN'] = acc_tech_gain_csv[44:65].set_index('Year')
acc_tech_gain['CS'] = acc_tech_gain_csv[66:87].set_index('Year')
acc_tech_gain['MTL'] = acc_tech_gain_csv[88:].set_index('Year')

for r in regions:
    acc_tech_gain[r] = acc_tech_gain[r].loc[:, urban_forms]

for reg in regions:
    to_num(acc_tech_gain[reg])


# __________Importing accumulated technology loss__________

acc_tech_loss_csv = pd.read_csv('accumulated_tech_loss.csv')
acc_tech_loss_csv.rename(columns={'LONG': 'Year'}, inplace=True)

acc_tech_loss = {}

acc_tech_loss['LONG'] = acc_tech_loss_csv[:21].set_index('Year')
acc_tech_loss['LAV'] = acc_tech_loss_csv[22:43].set_index('Year')
acc_tech_loss['CN'] = acc_tech_loss_csv[44:65].set_index('Year')
acc_tech_loss['CS'] = acc_tech_loss_csv[66:87].set_index('Year')
acc_tech_loss['MTL'] = acc_tech_loss_csv[88:].set_index('Year')

for r in regions:
    acc_tech_loss[r] = acc_tech_loss[r].loc[:, urban_forms]

for reg in regions:
    to_num(acc_tech_loss[reg])


# __________Capacity conversion__________
# from acc_tech_gain and acc_tech_loss we create a dict of dataframe containing
# accumulated technology capacity conversion for every region, urban form technology and year.

capacity_conversion = {}

for r in regions:
    capacity_conversion[r] = pd.DataFrame()

for r in regions:
    for uf in urban_forms:
        capacity_conversion[r][uf] = acc_tech_gain[r][uf] - acc_tech_loss[r][uf]

# __________Importing emission__________

emission_csv = pd.read_csv('emission.csv')
emission_csv.rename(columns={'CO2': 'Year'}, inplace=True)
emission = emission_csv.set_index('Year')


# __________Importing production__________
# first, we split the data per region

production_csv = pd.read_csv('production.csv')
production_csv.rename(columns={'LONG / CV': 'Year'}, inplace=True)

prod = {}
prod['LONG'] = production_csv[:263]
other_regions = ('LAV', 'CN', 'CS', 'MTL')
for r in other_regions:
    ind = production_csv[production_csv['Year'] == r + ' / CV'].index[0]
    prod[r] = production_csv[ind + 1:ind + 264].reset_index(drop=True)


# If you look at the data stored in the prod dictionary you'll notice that a lot of rows are 0. It's because every technology produces one and only one fuel. this function keeps only the relevant columns for each technology and stores the result into a new data frame. 

def sort_prod(input_df):
        technologies = {
                    'BF': 'HOU',
                    'BM': 'HOU',
                    'BD': 'HOU',
                    'IND': 'HOU',
                    'AGR': 'HOU',
                    'DUMMYHOUSE': 'HOU',
                    'IMPE': 'E',
                    'IMPP': 'P',
                    'IMPGN': 'GN',
                    'IMPBIO': 'BIO',
                    'IMPA': 'A'}

        df = pd.DataFrame({'Year': input_df['Year'][:21], 'CV': input_df['HOU'][:21]})
        for tech in technologies:
            ind = input_df[input_df['Year'] == tech].index[0]
            df[tech] = input_df[technologies[tech]][ind + 1:ind + 22].values
            output_df = df.set_index('Year')
        return output_df


production = {}
for reg in prod:
    production[reg] = sort_prod(prod[reg])


for reg in regions:
    to_num(production[reg])


# __________Importing total activity annual___________

total_activity_annual_csv = pd.read_csv('total_activity_annual.csv')
total_activity_annual_csv.rename(columns={'LONG': 'Year'}, inplace=True)

total_activity_annual = {}

total_activity_annual['LONG'] = total_activity_annual_csv[:21].set_index('Year')
total_activity_annual['LAV'] = total_activity_annual_csv[22:43].set_index('Year')
total_activity_annual['CN'] = total_activity_annual_csv[44:65].set_index('Year')
total_activity_annual['CS'] = total_activity_annual_csv[66:87].set_index('Year')
total_activity_annual['MTL'] = total_activity_annual_csv[88:].set_index('Year')

# converting series to numeric values

for reg in regions:
    to_num(total_activity_annual[reg])

# summing the total annual activity over the regions

total_activity_annual_cmm = pd.DataFrame()

for uf in urban_forms:
        total_activity_annual_cmm[uf] = sum(total_activity_annual[reg][uf] for reg in regions)


# __________importing total capacity annual__________

total_capacity_annual_csv = pd.read_csv('total_capacity_annual.csv')
total_capacity_annual_csv.rename(columns={'LONG': 'Year'}, inplace=True)

total_capacity_annual = {}

total_capacity_annual['LONG'] = total_capacity_annual_csv[:21].set_index('Year')
total_capacity_annual['LAV'] = total_capacity_annual_csv[22:43].set_index('Year')
total_capacity_annual['CN'] = total_capacity_annual_csv[44:65].set_index('Year')
total_capacity_annual['CS'] = total_capacity_annual_csv[66:87].set_index('Year')
total_capacity_annual['MTL'] = total_capacity_annual_csv[88:].set_index('Year')

# converting series to numeric values

for reg in regions:
    to_num(total_capacity_annual[reg])

# summing the total annual capacity over the regions

total_capacity_annual_cmm = pd.DataFrame()

for uf in urban_forms:
    total_capacity_annual_cmm[uf] = sum(total_capacity_annual[reg][uf] for reg in regions)


# __________plotting activity and capacity of urban forms__________

colors = {
    'CV': 'r',
    'BF': 'y',
    'BM': 'm',
    'BD': 'c',
    'IND': 'b',
    'AGR': 'g'
}


# this piece of code plot the total annual activity and capacity in the CMM (With and without the AGR urban form)

fig = plt.figure(figsize=(20, 10))

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

for uf in urban_forms:
    ax1.plot(total_capacity_annual_cmm.index, total_capacity_annual_cmm[uf], c=colors[uf])
    ax1.set_title('Annual Capacity')
    ax1.set_ylabel('CMM')
    ax2.plot(total_activity_annual_cmm.index, total_activity_annual_cmm[uf], c=colors[uf])
    ax2.set_title('Annual Activity')
    ax2.legend(bbox_to_anchor=(1, 0.75))
    ax2.set_ylabel('CMM')

for uf in ('CV', 'BF', 'BM', 'BD', 'IND'):
    ax3.plot(total_capacity_annual_cmm.index, total_capacity_annual_cmm[uf], c=colors[uf])
    ax3.set_title('Annual Capacity without AGR')
    ax3.set_ylabel('CMM')
    ax4.plot(total_activity_annual_cmm.index, total_activity_annual_cmm[uf], c=colors[uf])
    ax4.set_title('Annual Activity without AGR')
    ax4.legend(bbox_to_anchor=(1.125, 0.75))
    ax4.set_ylabel(CMM)

plt.show()

# this piece of code plot the total annual activity and total annual capacity of urban forms technologies for every region

fig = plt.figure(figsize=(20, 25))

for i, reg in enumerate(regions):
    ax1 = fig.add_subplot(5, 2, 2 * i + 1)
    ax2 = fig.add_subplot(5, 2, 2 * i + 2)
    for uf in urban_forms:
        ax1.plot(total_capacity_annual[reg].index, total_capacity_annual[reg][uf], c=colors[uf])
        ax1.set_title('Annual Capacity')
        ax1.set_ylabel(reg)

    for uf in urban_forms:
        ax2.plot(total_activity_annual[reg].index, total_activity_annual[reg][uf], c=colors[uf])
        ax2.set_title('Annual Activity')
        ax2.set_ylabel(reg)
        ax2.legend(bbox_to_anchor=(1, 0.75))

plt.show()


# __________plotting capacity conversion__________
# this piece of code shows the accumulated technology capacity conversion. You can see what are the choices of the model in converting urban form technologies.

fig = plt.figure(figsize=(10, 25))

for i, reg in enumerate(regions):
    ax1 = fig.add_subplot(5, 1, i + 1)
    for uf in urban_forms:
        ax1.plot(capacity_conversion[reg].index, capacity_conversion[reg][uf], c=colors[uf])
        ax1.set_title('Capacity Conversion')
        ax1.set_ylabel(reg)
        ax1.legend(bbox_to_anchor=(1, 0.75))

plt.show()
