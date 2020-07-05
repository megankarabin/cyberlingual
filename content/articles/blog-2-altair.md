Title: Altair to the Rescue    
Date: 2019-07-07 8:00       
Tags: python, altair, data visualization    
Slug: blog_2
category: blog

### Bad charts made better: A beginner-friendly altair tutorial

Some charts are confusing, some hard to interpret, and others are just boring, while still others (albeit a special, minority few) require that the rules of math and logic break in order to establish a reality in which they make sense&mdash;though at first glance, they might not appear as pernicious as they really are. By manipulating data, not only is it possible to tell a story, but to frame it in a way that fits a particular narrative. How we choose to represent data visually is of the utmost importance as a data scientist, of course, but also as anyone who needs to depict information in a meaningful way.

In this blog, I'll take some bad charts (boring, misleading, logic-breaking, etc.) and remake them into their best selves.


But first, I'll go over the basics of Altair, walking through the first few steps needed to create a visualization.


```python
import altair as alt
import pandas as pd
import numpy as np
alt.renderers.enable('notebook');
```

## ✨Before & Afters ✨

#### Chart 1



  <tr>
    <td> <img src="images\images\donut-complaints.png" alt="Drawing" style="width: 300px;"/> </td>
    <td> <img src="images\images\complaints.svg" alt="Drawing" style="width: 650px;"/> </td>
    </tr>



#### Chart 2



  <tr>
    <td> <img src="images\ghg-emissions.jpeg" alt="Drawing" style="width: 600px;"/> </td>
    <td> <img src="images\emissions-1.svg" alt="Drawing" style="width: 700px;"/> </td>
    </tr>



#### Chart 3



  <tr>
    <td> <img src="images\aul-fakenews.jpeg" alt="Drawing" style="width: 500px;"/> </td>
    <td> <img src="images\pp-visualization.svg" alt="Drawing" style="width: 500px;"/> </td>
    </tr>

The "bad" chart depicting Ontario's greenhouse gas emissions might actually look a bit prettier than the one I made, but it's not the better viz. Read why below.

## Making bar charts in Altair  

Humans aren't great at estimating area or visual divisions of area. A donut chart just isn't a great way to compare two proportions visually&mdash;a bar chart works much better.

<img src="images\donut-complaints.png" alt="Drawing" style="width: 400px;"/>

_This graphic is a breakdown of the discrimination complaints received by the Canadian Human Rights Commission in 2017-18. In that year, disability complaints represented 59% of complaints while 41% of complaints were other._ (From the 2018 Federal budget)

#### The easiest way to fix this is to spin up a super simple dataset representing these data.

Altair charts take pandas dataframes as arguments, so we throw our simple dataset into one with `pd.DataFrame()`.


```python
df = pd.DataFrame({
    'complaint type': ['disability-related', 'other'],
    'quantity': [0.59, 0.41]
})

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>complaint type</th>
      <th>quantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>disability-related</td>
      <td>0.59</td>
    </tr>
    <tr>
      <th>1</th>
      <td>other</td>
      <td>0.41</td>
    </tr>
  </tbody>
</table>
</div>



Now we'll try out the simplest visualization possible (one that is hopefully already a more successful representation of data than donut chart up there).


```python
alt.Chart(df).mark_bar().encode(
    x='sum(quantity)', # the 'x' channel
    y=alt.Y('complaint type') # the 'y' channel
)
```


    <vega.vegalite.VegaLite at 0x109f02908>










![png](images/blog-2-altair_24_2.png)


**Here's a quick breakdown of what's happening here:**

> `alt.Chart(df)` specifies the data you want to use in your chart (where df = your pandas dataframe)

> `.mark_bar()` specifies a bar chart as the type of visualization you want to use.

> `.encode()` is where you input (i.e., encode) your chart axes.
 - You can map any column in your dataset to either the 'x' or 'y' encoding channel (each channel corresponds to the x- and y-axis, respectively).
 - Read more in the Altair documentation [here](https://altair-viz.github.io/getting_started/starting.html#basic-tutorial-encodings-and-marks).

### Using colours


```python
color = alt.Color('complaint type') # setting colour to correspond to the selected column

alt.Chart(df).mark_bar().encode(
    x='sum(quantity)',
    y=alt.Y('complaint type'),
    color=color
)
```


    <vega.vegalite.VegaLite at 0x10a01aa58>










![png](images/blog-2-altair_27_2.png)


To set a particular colour scheme, use `scale=alt.Scale(scheme='scheme name')` in the `alt.Color` method.


```python
color = alt.Color('complaint type', scale=alt.Scale(scheme='reds'))

alt.Chart(df).mark_bar().encode(
    x='sum(quantity)',
    y=alt.Y('complaint type'),
    color=color
)
```


    <vega.vegalite.VegaLite at 0x10a815e48>










![png](images/blog-2-altair_29_2.png)


**Here are a few more single-hue colour schemes:**

- teals
- oranges
- reds
- purples (...you get the point.)



**The following are several more categorical and multi-hue schemes I like:**

- plasma
- magma
- accent
- dark2
- set3
- tableau10


Visit Vega's [colour scheme page](https://vega.github.io/vega/docs/schemes/#categorical) for even more options!

A default legend is provided when you set colour on a column to show you what category/value each colour corresponds to. This can be helpful but might actually be redundant, and therefore unnecessary in this case, since the information provieded by the legend is already encoded and labelled on the chart itself. To remove the legend, simply set `legend=None` in the color property. It should look something like this:

`alt.Color('column to set color on', legend=None)`

#### What if I want to swap the colours of the bars?

In the `alt.Color()` method, which uses Vega's colour schemes, discrete colours are assigned such that the index of the value in the column you've set `color` on matches the index of the colour in the scheme (at the row that corresponds to the number of values present in your column). I encoded the values for `'complaint type'` as `['disability-related', 'other']`, so the default setting assigns `'disability-related'` the lighter, first-appearing colour in the image below at row 2.

<img src="images/colour_scheme.png" style="width: 400px;">

In the `domain` argument of Scale &ndash; inside `alt.Color(scheme=alt.Scale())`) &ndash; we can rearrange the order of the values so that they correspond to the order of the colours we want to assign them. Since the categories were originally encoded as `['disability-related', 'other']`, and we want to switch the colour assignments, we do so such that the order matches the order of the colours&mdash;so, in this case we'd want:

> `domain=['other', 'disability-related']`.

Of course alternatively we could just go back and change the order of the values where we first encoded them into the dataset, but this is an easy way to alter things without having to go back and make actual changes to the data.


```python
color = alt.Color('complaint type',
                  legend=None,
                  scale=alt.Scale(scheme='reds', domain=['other', 'disability-related']))

alt.Chart(df).mark_bar().encode(
    x='sum(quantity)',
    y=alt.Y('complaint type'),
    color=color
)
```


    <vega.vegalite.VegaLite at 0x10a8390f0>










![png](images/blog-2-altair_36_2.png)


### Specifying axis information

We use `alt.X()` when we want to encode more than just the column name&mdash;maybe we want to include an axis title, formatting (e.g., displaying as percentage, adjusting scale), labels and ticks, etc.

To add formatting and set the axis title, I'll use `alt.Axis()` with the arguments "format", which sets the text formatting pattern, and "title" (as shown in the following code). I like to keep the code in the chart specification as clean as possible, so I prefer building up this extra information outside of the `alt.Chart()` function. I'll assign `alt.Axis(format='%', title='percentage of total complaints')` to a variable called `x_axis` so that I can simply call it from within `alt.X()` and pass it as the axis argument.


```python
x_axis = alt.Axis(format='%', title='percentage of total complaints')
```

### Size

#### Bars:
You can alter the width of the bars by setting `size=desired size as float or int` in the `mark_*` method, as I've done below to make the bars a bit wider than the default width.

#### Chart:

To adjust the size of the chart, we can set custom measurements with `width` and `height` in the `.properties()` method.


```python
chart = alt.Chart(df).mark_bar(size=30).encode(
    x=alt.X('sum(quantity)', axis=x_axis),
    y=alt.Y('complaint type'),
    color=color

).properties(
    width=600,
    height=90,
    title='Breakdown of complaints made to Canadian Human Rights Commission (2018)'
)
```

### Title

Every chart should have a title&mdash;donut chart is lacking here. To customize your chart title, use `chart.configure_title` .

Some useful attributes:

- `anchor` sets the title alignment. Valid inputs are 'start' (right alignment), 'middle' (centre) and 'end' (left).
- `orient` set the position of the title. Valid inputs are 'top', 'bottom', 'left' and 'right' (with top/bottom corresponding to above/below the chart).
- `fontSize`
- `font`
- `color`

Note: By throwing our chart into a variable called `chart`, we can access it in other instances without having to repeatedly include all of the code for the visualization.


```python
chart.configure_title(
    fontSize=14,
    font='Helvetica',
    anchor='middle',
    color='black',
)
```


    <vega.vegalite.VegaLite at 0x10a83c4e0>










![png](images/blog-2-altair_45_2.png)


Voilà! Now this data is truly living its best life.

## Line charts

<img src='images/ghg-emissions.jpeg' style="width: 700px;">

_Taken from the provinical government's [2019 budget](http://budget.ontario.ca/2019/chapter-1c.html#c1-20)_

### What's wrong with this picture?

There's no unit given for the scale on the y-axis. At first glance, it seems that while Ontario and Canada begin at the same starting point ("1") in 2005, Ontario's GHG emissions decline sharply while "the rest of Canada" experiences little variation over the same period. Notice, however, the incongruency between the title and subtitle (which supposedly describes what's being measured)&mdash;"Ontario & Friends' Greenhouse Gas _Emissions_ from 2005 to 2016" versus "GHG Emissions _Index_". An index of emissions is quite different from actual emissions in a valid unit of measurement, like megatonnes (Mt) of CO2. This is the unit used in the source data, and the unit I'll be using in my reconstructed visualization.

Just doing some basic data cleaning here so I can access the relevant data from the [National Inventory Report from Environment Canada](http://publications.gc.ca/collections/collection_2018/eccc/En81-4-2016-1-eng.pdf) (the same source used for the above chart).


```python
df = pd.read_csv("ghg-emissions-data.csv")

df.columns = [i.strip() for i in df.columns]
df.columns = [i.replace('–','-') for i in df.columns]

df.drop(['2005-2016', '1990'], axis=1, inplace=True)

df = df.reset_index()
df.rename(columns={'index': 'province'}, inplace=True)


provinces = []
ordered_vals = []
year = []

for c in df.columns:
    for i in df[c]:
        if c != 'province':
            ordered_vals.append(i)
            index = df[df[c] == i].index[0]
            prov = df.iloc[index][0]
            provinces.append(prov)
            year.append(c)


data = pd.DataFrame()
data['emissions'] = ordered_vals
data['province'] = provinces
data['year'] = year

nat_drop = list(data[data['province'] == 'Canada'].index)
provs = data.drop(nat_drop, axis=0)
```

Here I've created a dataframe containing data on Canada's greenhouse gas (GHG) emissions and including the number of emissions (in Mt of CO2), the year over which the emissions were released, and the province the emissions came from. `provs` is a second dataset not including the national total of emissions, whereas this figure is included in `data` .

There's also a `point` argument for the `mark_line()` method. If we set `point=True`, we get the line as well as a visual representation of each of the individual data points it intersects. This can be useful for when the data is on the sparse side, and makes it clear where the actual data sit. Remember, unless you have an inordinate number of datapoints, the line is just the trend between two points. Anywhere on the line _between_ two points&mdash;say, Canada's line at the x-value halfway between 2012 and 2013&mdash;isn't necessarily representative of the true y-values (emissions) at that value of x (circa July 2012).


```python
chart = alt.Chart(provs).mark_line(point=True).encode(
    x=alt.X('year:N'),
    y=alt.Y('emissions:Q'),
    color=alt.Color('province:N',
                   scale=alt.Scale(
                   scheme='category20')
                   )
).properties(
    width=400,
    height=400,
    title='GHG emissions by province')

chart.configure_axisX(labelAngle=0) # this sets the angle of the x-ticks
```


    <vega.vegalite.VegaLite at 0x1092646d8>










![png](images/blog-2-altair_55_2.png)


As we can see, Ontario is actually still producing a far greater quantity of emissions than any other province except for Alberta. The following is the text accompanying the original chart:

_Ontario has been a leader in the efforts to tackle climate change. Compared with 2005, the province’s total greenhouse gas emissions have dropped by 22 per cent — even while the rest of Canada saw emissions increase by three per cent during the same time period._

In splitting the data this way (Ontario vs. the rest of Canada) the trend observed for "the rest of Canada" is highly influenced by Alberta's emissions. That is, the only reason the rest of Canada saw a 3% increase in emissions is because Alberta saw a substantial increase, while most other provinces either stayed the same or saw a decrease in emissions.

<img src='images/i-see-u.jpeg' style="width: 200px;">



```python
canada_tot = data[data['province'] == 'Canada']

ontario = data[data['province'] == 'ON']

ontario.rename(columns={'emissions':'emissions_on', 'province': 'province_on'}, inplace=True)

can_on = pd.merge(canada_tot, ontario, on='year')


# Subtracting Ontario's yearly emissions from Canada's total yearly emissions in order to plot
# Ontario against the rest of Canada
rest_of_canada = []

for i in can_on['emissions']:           
    index = can_on[can_on['emissions'] == i].index[0]
    on = can_on.iloc[index][3]
    rest_of_canada.append(i - on)


can_on['rest_of_canada'] = rest_of_canada

rest_of_canada # this now includes all the values of GHG emissions from every province but Ontario.


# spinning up a new dataframe with the values for the rest of Canada
canada_minus_on = pd.DataFrame({
    'emissions': rest_of_canada,
    'province': ['rest_of_canada','rest_of_canada','rest_of_canada','rest_of_canada','rest_of_canada',\
                 'rest_of_canada','rest_of_canada'],
    'year': [2005, 2011, 2012, 2013, 2014, 2015, 2016]
})

totals = provs.append(canada_minus_on)

# comparing Ontario and the rest of Canada
can_vs_on = totals[(totals['province'] == 'rest_of_canada') | (totals['province']== 'ON')]
```

    /anaconda3/lib/python3.7/site-packages/pandas/core/frame.py:4025: SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame

    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      return super(DataFrame, self).rename(**kwargs)


#### Finally, a slightly more accurate visual depiction of these data.


```python
axis = alt.Axis(title='emissions (in Mt of CO2)')

chart = alt.Chart(can_vs_on).mark_line(point=True).encode(
    x=alt.X('year:N'),
    y=alt.Y('emissions:Q', axis=axis),
    color=alt.Color('province:N',
                   scale=alt.Scale(
                   scheme='plasma')
                   )
).properties(
    width=500,
    height=400,
    title='Ontario and the Rest of Canada\'s GHG Emissions from 2005 to 2016')

chart.configure_axisX(labelAngle=0) # this sets the angle of the x-ticks
```


    <vega.vegalite.VegaLite at 0x10a83c6d8>










![png](images/blog-2-altair_60_2.png)


From this representation, it's clear that Ontario and the rest of Canada have drastically different starting points&mdash;quite contrary to what the chart from the budget would have you think!

## More line charts

<img src="images/aul-fakenews.jpeg" style="width: 600px;">  

#### What's wrong with this picture?

- No scale for y-axis


- Missing axis labels


- Differing y-axes for each line, since the number of prevention services performed in 2013 still far exceeds the number of abortions (in the order of 600,000), and yet the prevention data at 2013 is depicted as below the data for abortions at the exact same x-value.

<img src='images/side-eye.png' style="width: 300px;">

- You'll also notice the slopes of the lines are about the same, upon quick visual inspection. The difference between abortions performed in 2006 (289,750) and those performed in 2013 (327,000) is much less than the difference between prevention services performed in 2006 (2,007,371) and those performed in 2013 (935,573). We can further quantify this by comparing the slopes:


```python
print(f'The slope of A (abortions) is: {round((327_000 - 289_750) / (2013 - 2006), 2)}')
print(f'The slope of B (cancer screening and prevention services) is: {(935_573 - 2_007_371) / (2013 - 2006)}')
```

    The slope of A (abortions) is: 5321.43
    The slope of B (cancer screening and prevention services) is: -153114.0


<center>
$m_A = 5321.43$

<center>
$m_B = -153114.0$

 </center>
 </center>

> Every year (i.e., for every 1 unit in increase along the x-axis), there are 5321 more abortions performed.

>Every year, there are 153114 fewer prevention and screening services performed.


```python
aul_df = pd.DataFrame({
    'service': ['abortion', 'abortion', 'cancer screening & prevention', \
                'cancer screening & prevention'],
    'services performed':[289_750, 327_000, 2_007_371, 985_573],
    'year': [2006, 2013, 2006, 2013]
})

aul_df.year = pd.to_datetime(aul_df.year, format='%Y')

aul_df['services performed'] = [i/1000 for i in aul_df['services performed']]
```


```python
x_axis = alt.Axis(title='Year', titleFontSize=13)
y_axis = alt.Axis(title='Services Performed (in thousands)', titleFontSize=13)

color = alt.Color('service', scale=alt.Scale(scheme='magma'))   

ppchart = alt.Chart(aul_df).mark_line().encode(
    x=alt.X('year', axis=x_axis),
    y=alt.Y('services performed', axis=y_axis),
    color=color

).properties(
    title= 'Planned Parenthood Services Performed in 2006 and 2013',
    width=500,
    height=400
)

ppchart.configure_title(
    anchor='middle',
    fontSize=20,
    color='black',
    font='Helvetica'
)

ppchart.configure_legend(
    columns=1,
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=6,
    cornerRadius=10,
    orient='top-right'
)
```


    <vega.vegalite.VegaLite at 0x10acf5860>










![png](images/blog-2-altair_70_2.png)


How this chart is better:

- uses a valid, to-scale y-axis

- labels for both axes

- it has a consistent, shared y-axis for both lines.


### Hope you enjoyed! Good luck making great visualizations with Altair 🚀
