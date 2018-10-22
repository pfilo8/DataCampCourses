import pandas as pd
from bokeh.io import curdoc
from bokeh.models import (ColumnDataSource, CategoricalColorMapper,
Slider,FuncTickFormatter,HoverTool,Select)
from bokeh.plotting import figure
from bokeh.palettes import Category10
from bokeh.layouts import column,row,widgetbox
import matplotlib.pyplot as plt

#### DATA ####
data = pd.read_csv('olympics.csv')
data.index = data.Edition
del(data['Edition'])
cities = dict(zip(data.index.tolist(),data.City.tolist()))
code = {'RU1':'Imperium Rosyjskie','IOP':'Niezalezni uczestnicy','BWI':'Federacja Indii Zachodnich','EUN':'Wspolna reprezentacja','EUA':'Niemcy','ANZ':'Australazja','TRI':'Trynidad i Tobago','SIN':'Singapur','TCH':'Czechoslowacja','AFG': 'Afganistan', 'ALB': 'Albania', 'ALG': 'Algieria', 'AND': 'Andora', 'ANG': 'Angola', 'ANT': 'Antigua i Barbuda', 'AHO': 'Antyle Holenderskie', 'KSA': 'Arabia Saudyjska', 'ARG': 'Argentyna', 'ARM': 'Armenia', 'ARU': 'Aruba', 'AUS': 'Australia', 'AUT': 'Austria', 'AZE': 'Azerbejdzan', 'BAH': 'Bahamy', 'BRN': 'Bahrajn', 'BAN': 'Bangladesz', 'BAR': 'Barbados', 'BEL': 'Belgia', 'BIZ': 'Belize', 'BEN': 'Benin', 'BER': 'Bermudy', 'BHU': 'Bhutan', 'BLR': 'Bialorus', 'MYA': 'Mjanma', 'BOH': 'Bohemia', 'BOL': 'Boliwia', 'BOT': 'Botswana', 'BIH': 'Bosnia i Hercegowina', 'BRA': 'Brazylia', 'BRU': 'Brunei Brunei Darussalam', 'IVB': 'Brytyjskie Wyspy Dziewicze', 'BUL': 'Bulgaria', 'BUR': 'Burkina Faso', 'BDI': 'Burundi', 'CHI': 'Chile', 'CHN': 'ChRL (ChRL)', 'CRO': 'Chorwacja', 'CYP': 'Cypr', 'CHA': 'Czad', 'MNE': 'Czarnogora', 'CSV': 'Czechoslowacja', 'CZE': 'Czechy', 'DEN': 'Dania', 'COD': 'Demokratyczna Republika Konga', 'DMA': 'Dominika', 'DOM': 'Dominikana', 'DJI': 'Dzibuti', 'EGY': 'Egipt', 'ECU': 'Ekwador', 'ERI': 'Erytrea', 'EST': 'Estonia', 'ETH': 'Etiopia', 'FIJ': 'Fidzi', 'PHI': 'Filipiny', 'FIN': 'Finlandia', 'FRA': 'Francja', 'GAB': 'Gabon', 'GAM': 'Gambia', 'GHA': 'Ghana', 'VOL': 'Gorna Wolta (obecnie Burkina Faso)', 'GRE': 'Grecja', 'GRN': 'Grenada', 'GEO': 'Gruzja', 'GUM': 'Guam', 'GUY': 'Gujana', 'GUA': 'Gwatemala', 'GUI': 'Gwinea', 'GBS': 'Gwinea Bissau', 'GEQ': 'Gwinea Rownikowa', 'HAI': 'Haiti', 'ESP': 'Hiszpania', 'NED': 'Holandia', 'IHO': 'Holenderskie Indie Wschodnie (obecnie Indonezja)', 'HON': 'Honduras', 'HKG': 'Hongkong', 'IND': 'Indie', 'INA': 'Indonezja', 'IRQ': 'Irak', 'IRI': 'Iran', 'IRL': 'Irlandia', 'ISL': 'Islandia', 'ISR': 'Izrael', 'JAM': 'Jamajka', 'JPN': 'Japonia', 'YEM': 'Jemen', 'JOR': 'Jordania', 'YUG': 'Jugoslawia', 'CAY': 'Kajmany', 'CAM': 'Kambodza', 'CMR': 'Kamerun', 'CAN': 'Kanada', 'QAT': 'Katar', 'KAZ': 'Kazachstan', 'KEN': 'Kenia', 'KGZ': 'Kirgistan', 'KIR': 'Kiribati', 'COL': 'Kolumbia', 'COM': 'Komory', 'CGO': 'Kongo', 'KOR': 'Korea Poludniowa', 'PRK': 'Korea Polnocna', 'CRC': 'Kostaryka', 'CUB': 'Kuba', 'KUW': 'Kuwejt', 'LAO': 'Laos', 'LES': 'Lesotho', 'LIB': 'Liban', 'LBR': 'Liberia', 'LBA': 'Libia', 'LIE': 'Liechtenstein', 'LTU': 'Litwa', 'LUX': 'Luksemburg', 'LAT': 'lotwa', 'MKD': 'Macedonia', 'MAD': 'Madagaskar', 'MAW': 'Malawi', 'MDV': 'Malediwy', 'MAS': 'Malezja', 'MLI': 'Mali', 'MLT': 'Malta', 'MAR': 'Maroko', 'MTN': 'Mauretania', 'MRI': 'Mauritius', 'MEX': 'Meksyk', 'FSM': 'Mikronezja', 'MDA': 'Moldawia', 'MON': 'Monako', 'MGL': 'Mongolia', 'MOZ': 'Mozambik', 'NAM': 'Namibia', 'NRU': 'Nauru', 'NEP': 'Nepal', 'GER': 'Niemcy', 'GDR': 'Niemiecka Republika Demokratyczna Niemcy Wschodnie (NRD)', 'FRG': 'Republika Federalna Niemiec (1949–1990) Niemcy Zachodnie (RFN)', 'NIG': 'Niger', 'NGR': 'Nigeria', 'NCA': 'Nikaragua', 'NOR': 'Norwegia', 'NZL': 'Nowa Zelandia', 'OMA': 'Oman', 'PAK': 'Pakistan', 'PLW': 'Palau', 'PLE': 'Palestyna', 'PAL': 'Mandat Palestyny (do 1949)', 'PAN': 'Panama', 'PNG': 'Papua-Nowa Gwinea', 'PAR': 'Paragwaj', 'PER': 'Peru', 'POL': 'Polska', 'PUR': 'Portoryko', 'POR': 'Portugalia', 'RSA': 'Poludniowa Afryka', 'CAF': 'Republika srodkowoafrykańska', 'CPV': 'Republika Zielonego Przyladka', 'RHO': 'Rodezja (obecnie Zimbabwe)', 'RUS': 'Rosja', 'ROU': 'Rumunia', 'RWA': 'Rwanda', 'SKN': 'Saint Kitts i Nevis', 'LCA': 'Saint Lucia', 'VIN': 'Saint Vincent i Grenadyny', 'ESA': 'Salwador', 'SAM': 'Samoa', 'ASA': 'Samoa Amerykańskie', 'SMR': 'San Marino', 'SEN': 'Senegal', 'SRB': 'Serbia', 'SCG': 'Serbia i Czarnogora', 'SEY': 'Seszele', 'SLE': 'Sierra Leone', 'SGP': 'Singapur', 'SVK': 'Slowacja', 'SLO': 'Slowenia', 'SOM': 'Somalia', 'SRI': 'Sri Lanka', 'USA': 'Stany Zjednoczone', 'SWZ': 'Suazi', 'SUD': 'Sudan', 'SSD': 'Sudan Poludniowy', 'SUR': 'Surinam', 'SYR': 'Syria', 'SUI': 'Szwajcaria', 'SWE': 'Szwecja', 'TJK': 'Tadzykistan', 'THA': 'Tajlandia', 'TPE': 'Republika Chińska (Tajwan)', 'TAN': 'Tanzania', 'TLS': 'Timor Wschodni', 'TOG': 'Togo', 'TGA': 'Tonga', 'TTO': 'Trynidad i Tobago', 'TUN': 'Tunezja', 'TUR': 'Turcja', 'TKM': 'Turkmenistan', 'UGA': 'Uganda', 'UKR': 'Ukraina', 'URU': 'Urugwaj', 'UZB': 'Uzbekistan', 'VAN': 'Vanuatu', 'VEN': 'Wenezuela', 'HUN': 'Wegry', 'GBR': 'Wielka Brytania', 'VIE': 'Wietnam', 'ITA': 'Wlochy', 'CIV': 'Wybrzeze Kosci Sloniowej', 'COK': 'Wyspy Cooka', 'ISV': 'Wyspy Dziewicze Stanow Zjednoczonych', 'SOL': 'Wyspy Salomona', 'STP': 'Wyspy swietego Tomasza i Ksiazeca', 'ZAI': 'Zair (obecnie Demokratyczna Republika Konga)', 'ZAM': 'Zambia', 'ZIM': 'Zimbabwe', 'UAE': 'Zjednoczone Emiraty Arabskie', 'URS': 'Zwiazek Socjalistycznych Republik Radzieckich Zwiazek Radziecki', 'ZZX': 'Druzyna mieszana'}
cat = data.loc[1896].groupby(["NOC","Medal"]).Medal.count()
cat = cat.unstack().fillna(0)
cat.Bronze = cat.Bronze.astype(int)
cat.Silver = cat.Silver.astype(int)
cat.Gold = cat.Gold.astype(int)
cat['Country'] = [code[kod] for kod in cat.index]
cat = cat.sort_values(['Gold','Silver','Bronze'])
source = ColumnDataSource(data={
    'x':        range(len(cat)),
    'Country':  cat.Country,
    'Bronze':   cat.Bronze,
    'Silver':   cat.Silver,
    'Gold':     cat.Gold})

#### CALLBACK ####
def update_plot(attr,old,new):
    yr = slider.value
    select.options = data.loc[yr].Sport.unique().tolist()+['Razem']
    sport = select.value
    if sport == 'Razem':
        cat = data.loc[yr]
    else:
        cat = data.loc[yr]
        cat = cat[cat['Sport']==sport]
    cat = cat.groupby(["NOC","Medal"]).Medal.count().unstack().fillna(0)
    cat.Bronze = cat.Bronze.astype(int)
    cat.Silver = cat.Silver.astype(int)
    cat.Gold = cat.Gold.astype(int)
    cat['Country'] = [code[kod] for kod in cat.index]
    cat = cat.sort_values(['Gold','Silver','Bronze'])
    new_data = {
        'x':        range(len(cat)),
        'Country':  cat.Country,
        'Bronze':   cat.Bronze,
        'Silver':   cat.Silver,
        'Gold':     cat.Gold}
    source.data = new_data
    plot.title.text = 'Olympics Medals in %d (%s)' %(yr,cities[yr])
    label_dict = {}
    for i, s in enumerate(cat.index):
        label_dict[i] = s
    plot.xaxis.formatter = FuncTickFormatter(code="""
        var labels = %s;
        return labels[tick];
    """ % label_dict)
#### WIDGETS ####
slider = Slider(title = 'Year', start = 1896, end = 2008, step = 4,value = 1896)
slider.on_change('value',update_plot)
hover = HoverTool(tooltips=[('Country', '@Country'),('Gold','@Gold'),
                            ('Silver', '@Silver'),('Bronze','@Bronze')])
select = Select(options=data.loc[1896].Sport.unique().tolist()+['Razem'],title='Sport',value='Razem')
select.on_change('value',update_plot)

#### PLOT ####
plot = figure(title = 'Olympics Medals in 1896 (Athens)', plot_height=800,
              plot_width=1200)
plot.circle(x='x',y='Bronze',source=source,color='#965A38',size = 12)
plot.circle(x='x',y='Silver',source=source,color='#A8A8A8',size = 16,fill_alpha=0.8)
plot.circle(x='x',y='Gold',source=source,color='#D9A441',size = 20,fill_alpha=0.6)
plot.xaxis.axis_label ='Country'
plot.yaxis.axis_label = 'Number of medals'
plot.add_tools(hover)

# LABELS
label_dict = {}
for i, s in enumerate(cat.index):
    label_dict[i] = s
plot.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)

#### LAYOUT ####
layout = row(widgetbox(slider,select),plot)
curdoc().add_root(layout)
curdoc().title = 'Olympics'
