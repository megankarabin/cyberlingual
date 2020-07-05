Title: Advanced Jinja: filters & variables
Date: 2019-08-06 13:43
Tags: python, jinja
Slug: blog_3
category: blog

Want to learn how to be a Jinja ninja? (I've always wanted to use those words together in a sentence and this seemed like the perfect opportunity #notsorry)

In this post I'll explain how you can use Jinja filters to access python functions and libraries from within an html doc, as well as how to create new variables from _within_ your Jinja template (rather than from the python script linked to the template). I'll be assuming that readers are familiar with basic Jinja, but if you're totally new to it and want to brush up on the basics before reading further, check out [this blog post](https://vishalsharma01.github.io/Blog/blog-3.html)!

### Recap: What is Jinja?

Jinja is a python library and a **template engine**, which is a software designed to let you produce a text output from your code. Of course, in python, we could just do that using `print('your text output')`.

So, what's special about a template engine and why might we need one?

Basically, Jinja enables your code to communicate with a template, like an HTML document, for example, which traditionally only allows for static inputs/outputs. HTML doesn't have an ability to use control flow, or encode mutable variables, for instance. There are many template engines out there, but Jinja is built specifically to interact with python. Using Jinja, we can actually use python programming within a text/HTML document such that our result outputs are consistent with any data (in models) we're using for our web application.

### Installation

If you haven't already done so, you can install Jinja by running either of the following commands:

```
easy_install Jinja2
pip install Jinja2

```

If neither of these work and you're having trouble installing, check out the documentation [here](http://jinja.pocoo.org/docs/2.10/intro/#installation) for more detailed instructions.


```python
import pandas as pd
import numpy as np
import pathlib
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from IPython.core.display import HTML

p = pathlib.Path("j-templates/")
p.mkdir(parents=True, exist_ok=True)
```


```python
file_loader = FileSystemLoader('j-templates')
            # loads files from a specified directory (the so-called "file system" -- here, the one
            # we've just created, 'j-templates')

env = Environment(loader=file_loader)
                # the "loader" argument sets the template loader for this environment.
```

- The template loader is the file system (i.e., directory) from which you'll be accessing files/templates. It's helpful to do this when you'll be spinning up toy files to practice on or for the sake of demonstration, like I'll be doing in this post.


- The template class "`Environment`" is the core component of Jinja. Instances of it are used to store global variables and load templates, but generally you won't need to configure custom instances of it when you're using Jinja in an application &mdash; most instantiate just once (automatically) upon initializing the application.

I'm going to be using a pokemon dataset, so here I'm just bringing that in and cleaning up the column names.


```python
df = pd.read_csv('hackathon/data/pokemon.csv')

df.columns = [i.lower().replace(' ', '_').replace('.', '') for i in df.columns]
```


```python
pokemon = list(df.name)
```




    'Mew'



### Filters

Filters are an incredibly helpful feature baked into Jinja &ndash; **they allow you to use any desired python functions (including ones you've written), libraries and/or modules along with their associated methods.**

Below, I want to get a randomly generated pokemon from my list of pokemon, and for that I'll need `np.random.choice`. I am **not** able to simply use code that looks like the following code block:

<img src='https://i.imgur.com/ySrLNu6.png' width=350px;>

This code is invalid and won't run. But it isn't over yet &mdash; **Jinja can still access libraries through filters!**

### `env.filters`


The filters for an environment can be viewed by calling the dot filters method, which will provide you with a dictionary whose keys are the filters (their names) and whose values are the particular object they house.

By creating our own filter as a key-value pair, we can use virtually any function (or library) available to us in Python in Jinja! Below I'm setting a new key called `"select_random"` containing the random choice function.

_Make sure to import the necessary libraries, modules and/or functions beforehand and create any aliases you want to use &mdash; e.g., I imported numpy as np earlier._


```python
env.filters['select_random'] = np.random.choice
```

Now, as you can see in the following code output, my new `select_random` key has been added to the dictionary (at the very bottom).


```python
print(len(env.filters), '\n') # this is how many actual keys there are
list(env.filters)[40:]  
# ^ here I'm indexing the last 10 just to demonstrate what the dict looks like without having 50+ k-v pairs

for i in list(env.filters)[40:]:
    print(f'\'{i}\' :', env.filters[i])
```

    54

    'striptags' : <function do_striptags at 0x115287730>
    'sum' : <function do_sum at 0x1155909d8>
    'title' : <function do_title at 0x1152999d8>
    'trim' : <function do_trim at 0x1152876a8>
    'truncate' : <function do_truncate at 0x115287378>
    'unique' : <function do_unique at 0x115299b70>
    'upper' : <function do_upper at 0x1152997b8>
    'urlencode' : <function do_urlencode at 0x1152996a8>
    'urlize' : <function do_urlize at 0x115287268>
    'wordcount' : <function do_wordcount at 0x115287488>
    'wordwrap' : <function do_wordwrap at 0x115287400>
    'xmlattr' : <function do_xmlattr at 0x1152998c8>
    'tojson' : <function do_tojson at 0x11529b2f0>
    'select_random' : <built-in method choice of mtrand.RandomState object at 0x106cd57e0>


Now we can call the function that it contains **in** Jinja! The way this is done is quite simple, though slightly different from how we're used to calling functions with the usual python syntax. For a function in python code that looks like this:
```
function(arg)

```

here's how it's formulated in Jinja:

```
{{ arg | function }}
```

See the example below using the newly created `select_random` filter.


```python
%%writefile j-templates/fun.html

<!DOCTYPE html>
<html lang="en">
<head>
    <title>My pokemon</title>
</head>

 <p>My randomly selected pokémon : {{ my_pokemon|select_random }} </p>

</html>
```

    Overwriting j-templates/fun.html



```python
template = env.get_template('fun.html')
# making a jinja template for the file we created in the above codeblock

output = template.render(my_pokemon=pokemon)
# assigning our pokemon variable (and all of its contents) to a jinja template variable, which we're calling 'my_pokemon'

HTML(output)
```





<!DOCTYPE html>
<html lang="en">
<head>
    <title>My pokemon</title>
</head>

 <p>My randomly selected pokémon : Starmie </p>

</html>



Let's break down what's happening here:

```
env.get_template()

```
> Calling this method on our environment will load whatever we input (i.e., the desired file) as a Jinja template.
This is how we "tell" Jinja that this is the file we want to use. We're then throwing the result into a variable called `template`.

```
template.render
```

> Performing the previous step sets up the file as a Jinja template, which then means we can use the `.render` method on it. The arguments passed to `template.render` are the names of all variables to be used in the script.
This step is crucial to ensuring that the template can communicate with/access variables in our python script.

### Custom functions & setting variables in Jinja

The beauty of filters is that we can write any function in python and "import" it into jinja this way.

Building on top of the last example, where we built in the random generator, let's say that I only like fire pokemon, and want to print "good" every time the randomly selected pokemon is a fire type and "bad" for every one _not_ of type fire, along with their actual type. I can write a quick function to do this and then use a filter to bring it into Jinja.

Note that because we want to reuse the randomly generated pokemon, we'll have to use a variable (Jinja's syntax isn't as flexible as python's and doesn't allow for infinite nesting using brackets). This is made fairly simple using Jinja's ```{% set x = y %}``` syntax.


```python
def is_fire_pokemon(pokemon='Charmander'):
    poketype_1 = df[df['name'] == pokemon]['type_1'].to_list()[0]
    if poketype_1 == 'Fire':
        return f'{pokemon}, Good'
    else:
        return f'{pokemon}, Bad: {poketype_1}'
```


```python
is_fire_pokemon('Rattata')
```




    'Rattata, Bad: Normal'



Now that we have our custom function, let's make a filter for it.


```python
env.filters['is_fire'] = is_fire_pokemon

env.filters['is_fire']
```




    <function __main__.is_fire_pokemon(pokemon='Charmander')>



**Sidenote of interest:**

Notice that we don't write `is_fire_pokemon(pokemon)`, rather we input it **without** the brackets. We do this when we don't want the function to be called at the point it's being written, but rather to serve as a reference to the function object. Take a look at the difference in what's being stored when we set `env.filters['is_fire'] = is_fire_pokemon` versus `is_fire_pokemon(pokemon)`:


```python
env.filters['is_fire'] = is_fire_pokemon(pokemon)
print(env.filters['is_fire'], ' \n')


env.filters['is_fire'] = is_fire_pokemon
print(env.filters['is_fire'])
```

    Charmander, Good  

    <function is_fire_pokemon at 0x114e422f0>


In the first case, what we're storing as the filter is the actual value returned by the function &ndash; essentially, we're calling our function _as_ we store it, and in doing so, saving whatever it returns as the filter, which isn't what we want. We want to set the function itself as a filter, and we do this by *not* using brackets and arguments!

### Setting variables

Now that we're familiar with the calling of functions in Jinja through filters, we can add another layer: variables!

If you've made it this far, I probably don't need to elaborate on the usefulness of local variables, so let's dive right into the code.

The instantiation process is quite straightforward: identical to how one assigns variables in regular python, with the one added step of wrapping your variable assignment inside
```
{% var = goes here %}
```



```python
%%writefile j-templates/fun2.html

<!DOCTYPE html>
<html lang="en">
<head>
    <title>My pokemon</title>
</head>

 <p>My randomly selected pokémon :
        {% set p = my_pokemon|select_random %}
        {{ p|is_fire }}
    </p>

</html>
```

    Overwriting j-templates/fun2.html


Here I've set `p = my_pokemon|select_random` in order to pass it to my `is_fire_pokemon` function (which is contained in the `is_fire` filter).


```python
template = env.get_template('fun2.html')
output = template.render(my_pokemon=pokemon)

HTML(output)
```





<!DOCTYPE html>
<html lang="en">
<head>
    <title>My pokemon</title>
</head>

 <p>My randomly selected pokémon :

        Cubone, Bad: Ground
    </p>

</html>



<img src='https://vignette.wikia.nocookie.net/looneytunes/images/e/e1/All.jpg/revision/latest?cb=20150313020828' style='width:500px;'>

Good luck on your Jinja adventures!
