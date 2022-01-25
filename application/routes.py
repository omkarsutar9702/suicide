### import libraries ---------------------------------------------------------------
from turtle import title
from flask import render_template , url_for
import pandas as pd
import numpy as np
import plotly 
import json
import plotly.express as px


from flask import Flask

app = Flask(__name__)

### read data ----------------------------------------------------------------------
data=pd.read_csv('master.csv')
### data manupulation --------------------------------------------------------------
df=data.drop(columns='HDI for year')
data.rename(columns={"suicides/100k pop":"suicides_pop","HDI for year":"HDI_for_year",
                  " gdp_for_year ($) ":"gdp_for_year"," gdp_per_capita ($) ":"gdp_per_capita",
                    "gdp_per_capita ($)":"gdp_per_capita"}, inplace=True)

### plot 1 -------------------------------------------------------------------------
data["gdp_for_year"] = data["gdp_for_year"].str.replace(",","").astype(np.int64)
data["age"] = data["age"].str.replace("5-14 years","05-14 years")
data_sex=data.groupby(['year','sex'] , as_index=False)['suicides_no'].mean()
data_sex=pd.DataFrame(data_sex)

### plot 2 -------------------------------------------------------------------------
data_age=data.groupby(['year','age'] , as_index=False)['suicides_no'].mean()
data_age=pd.DataFrame(data_age)

### plot 3 -------------------------------------------------------------------------
suicides_gen=data.groupby(['generation'] , as_index=False)['suicides_no'].sum()
suicides_gen=pd.DataFrame(suicides_gen)


### plot 4 -------------------------------------------------------------------------
data_country=data.groupby(['country'] , as_index=False)['suicides_no'].sum()
data_country=pd.DataFrame(data_country)
data_country_10=data_country.sort_values(['suicides_no'],ascending=False).head(20)

### plot 5 -------------------------------------------------------------------------
data_country_gdp=data.groupby(['country'] ,as_index=False)['gdp_per_capita'].mean()
data_country_gdp=pd.DataFrame(data_country_gdp)
data_country_gdp=data_country_gdp.sort_values(['gdp_per_capita'],ascending=False).head(20)

### plot 6 -------------------------------------------------------------------------
data_sex_country=data.groupby(['country','sex'] , as_index=False)['suicides_no'].sum()
data_sex_country=pd.DataFrame(data_sex_country)
data_sex_country=data_sex_country.sort_values(['suicides_no'],ascending=False).head(20)

####### analysis by countries-------------------------------------------------------

#United States----------------------------------------------------------------------
US=data[data['country']=='United States']
#US male and female suicides from year 1985-2015
US_sex=US.groupby(['year','sex']  , as_index=False)['suicides_no'].sum()
US_sex=pd.DataFrame(US_sex)

### plot 1 -------------------------------------------------------------------------
US_gen=US.groupby(['generation'] , as_index=False)['suicides_no'].sum()
US_gen=pd.DataFrame(US_gen)

### plot 2 -------------------------------------------------------------------------
US_gdpvssuicides=US.groupby(['year'] , as_index=False)['suicides_no','gdp_per_capita'].sum()
US_gdpvssuicides=pd.DataFrame(US_gdpvssuicides)

#united kingdom --------------------------------------------------------------------
UK=data[data['country']=='United Kingdom']
#UK male and female suicides from year 1985-2015
UK_sex=UK.groupby(['year','sex'] , as_index=False)['suicides_no'].sum()
UK_sex=pd.DataFrame(UK_sex)

####plot 1 -------------------------------------------------------------------------
UK_gen=UK.groupby(['generation'] , as_index=False)['suicides_no'].sum()
UK_gen=pd.DataFrame(UK_gen)

#### plot 2 ------------------------------------------------------------------------
UK_gdpvssuicides=UK.groupby(['year'] , as_index=False)['suicides_no','gdp_per_capita'].sum()
UK_gdpvssuicides=pd.DataFrame(UK_gdpvssuicides)


#Russia ----------------------------------------------------------------------------
Russia=data[data['country']=='Russian Federation']
#Russian male and female suicides from year 1985-2015
Russia_sex=Russia.groupby(['year','sex'] , as_index=False)['suicides_no'].sum()
Russia_sex=pd.DataFrame(Russia_sex)

### plot 1 -------------------------------------------------------------------------
Russia_gdpvssuicides=Russia.groupby(['year'] , as_index=False)['suicides_no','gdp_per_capita'].sum()
Russia_gdpvssuicides=pd.DataFrame(Russia_gdpvssuicides)

### plot 2 -------------------------------------------------------------------------
Russia_gen=Russia.groupby(['generation'] , as_index=False)['suicides_no'].sum()
Russia_gen=pd.DataFrame(Russia_gen)

#japan -----------------------------------------------------------------------------
#Japan
Japan=data[data['country']=='Japan']
#Japan male and female suicides from year 1985-2015
Japan_sex=Japan.groupby(['year','sex'] , as_index=False)['suicides_no'].sum()
Japan_sex=pd.DataFrame(Japan_sex)

### plot 2 -------------------------------------------------------------------------
Japan_gen=Japan.groupby(['generation'] , as_index=False)['suicides_no'].sum()
Japan_gen=pd.DataFrame(Japan_gen)

### plot 3 -------------------------------------------------------------------------
Japan_gdpvssuicides=Japan.groupby(['year']  ,as_index=False)['suicides_no','gdp_per_capita'].sum()
Japan_gdpvssuicides=pd.DataFrame(Japan_gdpvssuicides)


### france -------------------------------------------------------------------------
France=data[data['country']=='France']
#France male and female suicides from year 1985-2015
France_sex=France.groupby(['year','sex'] , as_index=False)['suicides_no'].sum()
France_sex=pd.DataFrame(France_sex)

# plot 1 ---------------------------------------------------------------------------
France_gen=France.groupby(['generation'] , as_index=False)['suicides_no'].sum()
France_gen=pd.DataFrame(France_gen)

#plot 2 ----------------------------------------------------------------------------
France_gdpvssuicides=France.groupby(['year'] , as_index=False)['suicides_no','gdp_per_capita'].sum()
France_gdpvssuicides=pd.DataFrame(France_gdpvssuicides)

#Germany----------------------------------------------------------------------------
Germany=data[data['country']=='Germany']
#Germany male and female suicides from year 1985-2015
Germany_sex=Germany.groupby(['year','sex'] , as_index=False)['suicides_no'].sum()
Germany_sex=pd.DataFrame(Germany_sex)

#Germany suicides per generation----------------------------------------------------
Germany_gen=Germany.groupby(['generation'] , as_index=False)['suicides_no'].sum()
Germany_gen=pd.DataFrame(Germany_gen)

#Germany gdp and suicides
Germany_gdpvssuicides=Germany.groupby(['year'] , as_index=False)['suicides_no','gdp_per_capita'].sum()
Germany_gdpvssuicides=pd.DataFrame(Germany_gdpvssuicides)



@app.route("/")
def index():
  return render_template("index.html")

@app.route("/landing")
def landing():
    
    fig1=px.line(data_sex,x='year',y='suicides_no',color='sex' , labels={"suicides_no": "Average suicides"})
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig2=px.bar(data_sex_country,x='country',y='suicides_no',color='sex',barmode='group')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig3=px.bar(data_country_gdp,x='country',y='gdp_per_capita',color='country' , color_continuous_scale=px.colors.sequential.Viridis )
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig4=px.bar(data_country_10,x='country',y='suicides_no' , labels={"suicides_no":"Total suicides"} , color="country",color_continuous_scale=px.colors.sequential.Viridis,)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig5=px.pie(suicides_gen,values='suicides_no',names='generation')
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig6=px.line(data_age,x='year',y='suicides_no',color='age', labels={"suicides_no": "Average suicides"})
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("landing.html" , title="Home" , graph1JSON=graph1JSON ,  graph2JSON=graph2JSON , graph3JSON=graph3JSON  ,graph4JSON=graph4JSON , graph5JSON=graph5JSON , graph6JSON=graph6JSON)
  
@app.route("/us")
def us():
  fig_us_1=px.line(US_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_us_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_us_2=px.pie(US_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_us_2 , cls=plotly.utils.PlotlyJSONEncoder)  
  
  fig_us_3=px.scatter(US_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_us_3 , cls=plotly.utils.PlotlyJSONEncoder)  
  
  fig_us_4=px.histogram(US_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_us_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("us.html" , graph1JSON=graph1JSON , graph2JSON=graph2JSON  ,graph3JSON=graph3JSON , graph4JSON=graph4JSON)

@app.route("/uk")
def uk():
  fig_uk_1=px.line(UK_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_uk_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_uk_2=px.pie(UK_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_uk_2 , cls=plotly.utils.PlotlyJSONEncoder)  
  
  fig_uk_3=px.scatter(UK_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_uk_3 , cls=plotly.utils.PlotlyJSONEncoder)  
  
  fig_uk_4=px.histogram(UK_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_uk_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("uk.html" , graph1JSON=graph1JSON , graph2JSON=graph2JSON  ,graph3JSON=graph3JSON , graph4JSON=graph4JSON)


@app.route("/Russia")
def Russia():
  
  fig_r_1=px.line(Russia_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_r_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_r_2=px.pie(Russia_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_r_2 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_r_3=px.scatter(Russia_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_r_3 , cls=plotly.utils.PlotlyJSONEncoder) 
  
  fig_r_4=px.histogram(Russia_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_r_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("Russia.html" , graph1JSON=graph1JSON ,graph2JSON=graph2JSON , graph3JSON=graph3JSON  , graph4JSON=graph4JSON)

@app.route("/japan")
def japan():
  
  fig_j_1=px.line(Japan_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_j_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_j_2=px.pie(Japan_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_j_2 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_j_3=px.scatter(Japan_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_j_3 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_j_4=px.histogram(Japan_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_j_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("japan.html" , graph1JSON=graph1JSON ,graph2JSON=graph2JSON , graph3JSON=graph3JSON  , graph4JSON=graph4JSON)


@app.route("/france")
def france():
  
  fig_f_1=px.line(France_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_f_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_f_2=px.pie(France_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_f_2 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_f_3=px.scatter(France_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_f_3 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_f_4=px.histogram(France_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_f_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("france.html" , graph1JSON=graph1JSON ,graph2JSON=graph2JSON , graph3JSON=graph3JSON  , graph4JSON=graph4JSON)


@app.route("/garmany")
def garmany():
  
  fig_g_1=px.line(Germany_sex,x='year',y='suicides_no',color='sex')
  graph1JSON = json.dumps(fig_g_1 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_g_2=px.pie(Germany_gen,names='generation',values='suicides_no')
  graph2JSON = json.dumps(fig_g_2 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_g_3=px.scatter(Germany_gdpvssuicides,x='gdp_per_capita',y='suicides_no')
  graph3JSON = json.dumps(fig_g_3 , cls=plotly.utils.PlotlyJSONEncoder)
  
  fig_g_4=px.histogram(Germany_gdpvssuicides,x='year',y='gdp_per_capita',nbins=20)
  graph4JSON = json.dumps(fig_g_4 , cls=plotly.utils.PlotlyJSONEncoder)
  
  return render_template("garmany.html" , graph1JSON=graph1JSON ,graph2JSON=graph2JSON , graph3JSON=graph3JSON  , graph4JSON=graph4JSON)


if __name__ == '__main__':
   app.run()