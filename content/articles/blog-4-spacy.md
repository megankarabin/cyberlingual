Title: Intro to spaCy
Date: 2019-07-28 15:46
Tags: python, spaCy, NLP
Slug: blog_4
category: blog

spaCy is an NLP tool for language and text processing. The most well-known package for NLP is NLTK, which though it's a robust, well-respected library, comes nowhere near spaCy in terms of user-friendliness when it comes to handling, parsing and presenting language data (imho). Although spaCy definitely has ease-of-use on its side, I know there are people out there who are quite comfortable using NLTK. However, there are several features available in spaCy that simply don't exist in NLTK, so hopefully after this tutorial you'll be convinced that spaCy is the way to go!

In this tutorial, I'll go over the basics of spaCy, showing you first how to install and get started, and then helping you to become familiar with some of the core concepts and features built into spaCy.

<b> Outline</b>

- the NLP and Doc objects
- tokens / tokenization (and lexical attributes of tokens, including parts-of-speech tags, syntactic dependencies, and lemmas, among several others)
- match patterns (spaCy's superior version of regex)
- entity identification
- displaCy

displaCy is spaCy's visualization package. With displaCy, we can view the syntactic dependencies of a doc (text object) in really pretty visualizations, as well as label and colour-code entities.


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
```

## Installing and downloading


```python
!pip install spacy
!python -m spacy download en_core_web_sm
```

    ✔ Download and installation successful
    You can now load the model via spacy.load('en_core_web_sm')


## The NLP object and the Doc object

The NLP object contains the processing pipeline. Once instantiated, we can use it to analyze text!

We instantiate as such:


```python
from spacy.lang.en import English

nlp = English()
```

Next, we pass our text to the nlp object, and assign this to a variable, the standard name is `doc`. This `doc` variable now contains a Doc object, which we'll see below.


```python
doc = nlp('The alien spaceship travelled 12 billion light years to explore new galaxies.')
print(doc)
print(type(doc))
```

    The alien spaceship travelled 12 billion light years to explore new galaxies.
    <class 'spacy.tokens.doc.Doc'>


It behaves the same as a python sequence in that you can iterate over and index its contents.

We can run the `.text` method to get the full text contents of the doc object.


```python
doc.text
```




    'The alien spaceship travelled 12 billion light years to explore new galaxies.'



spaCy uses statistical models to make predictions based on context, which is critically important when processing language. Without context analysis, there's very little we can say about the words in a given sentence or phrase &mdash; one of the features of key importance of language is that words don't always mean the same thing, depending on where they occur in a sentence and with which other words.

Things we can do with statstical models:

- parts-of-speech (POS) tagging
- (named) entity identification
- syntactic dependency parsing

To use one of spaCy's models, you'll need to import spacy, then load a package, such as the `en_core_web_sm` package.

You can use:

`$ python install -m spacy download en_core_web_sm`


```python
import spacy

# now we'll simply reinstantiate
nlp = spacy.load('en_core_web_sm')

# still using our old inputs :P
doc = nlp('The SpaceX spaceship travelled 12 billion light years to explore new galaxies.')
```

## Tokens

Tokens are just another word for "item". In NLP, any individual, discrete object within the text (e.g., a word, punctuation mark, or number) would be a token. We can access individual tokens in a text by iterating over the doc object, and can thus see what types of tokens it contains, along with their lexical attributes.

_Lexical just means "relating to the words or vocabulary of a language", and so a "lexical attribute" is just some feature relating to the words/vocabulary of your doc._


```python
for token in doc:
    print(token)
```

    The
    SpaceX
    spaceship
    travelled
    12
    billion
    light
    years
    to
    explore
    new
    galaxies
    .


### Lexical Attributes in spaCy

##### Mini linguistics refresher:

**POS**: the syntactic category a word (or here, token) belongs to, e.g., noun, verb, adjective

**Dependency**: the grammatical role of a word, relative to the other words in the sentence, e.g. direct/indirect object

**Head**: the lexical node (on a tree) that governs the word in question

**Lemma**: the base form of a word (its simplest morphological realization), e.g. "run" is the lemma for "running"

**Shape**: not linguistics-related per se, but this one is actually pretty cool &mdash; the shape attribute shows you what the token "looks like" without showing you the token itself (is it a digit, does it contain capital letters, etc.).

The following are some useful and interesting token attributes.

**These return boolean values:**
```
is_alpha  (is it an alphanumeric character)
is_punct  (is it punctuation)
like_num  (is it a number)
```

**These return the index, the POS, the dependency, the lemma and the shape of a token, respectively:**
```
i
pos_
dep_
head
lemma_
shape_
```

#### Additional Attributes

We can call `doc.ents` to get the entities and iterate over this to find the label (i.e., the category) for each entity (which we'll do in a minute) using the `label_` attribute.

Below I'll run each of the attributes for every token using list comprehensions and toss those outputs into a dataframe, which will now contain all the relevant lexical information we gathered for each of the tokens.


```python
tokens = [token for token in doc]
pos = [token.pos_ for token in doc]
dep = [token.dep_ for token in doc]
heads = [token.head for token in doc]
lemmas = [token.lemma_ for token in doc]
shapes = [token.shape_ for token in doc]

df = pd.DataFrame({
    'token': tokens,
    'pos': pos,
    'dependency': dep,
    'head': heads,
    'lemma': lemmas,
    'shape': shapes
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
      <th>token</th>
      <th>pos</th>
      <th>dependency</th>
      <th>head</th>
      <th>lemma</th>
      <th>shape</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The</td>
      <td>DET</td>
      <td>det</td>
      <td>spaceship</td>
      <td>the</td>
      <td>Xxx</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SpaceX</td>
      <td>PROPN</td>
      <td>compound</td>
      <td>spaceship</td>
      <td>SpaceX</td>
      <td>XxxxxX</td>
    </tr>
    <tr>
      <th>2</th>
      <td>spaceship</td>
      <td>NOUN</td>
      <td>nsubj</td>
      <td>travelled</td>
      <td>spaceship</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>3</th>
      <td>travelled</td>
      <td>VERB</td>
      <td>ROOT</td>
      <td>travelled</td>
      <td>travel</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12</td>
      <td>NUM</td>
      <td>compound</td>
      <td>billion</td>
      <td>12</td>
      <td>dd</td>
    </tr>
    <tr>
      <th>5</th>
      <td>billion</td>
      <td>NUM</td>
      <td>nummod</td>
      <td>years</td>
      <td>billion</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>6</th>
      <td>light</td>
      <td>ADJ</td>
      <td>amod</td>
      <td>years</td>
      <td>light</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>7</th>
      <td>years</td>
      <td>NOUN</td>
      <td>dobj</td>
      <td>travelled</td>
      <td>year</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>8</th>
      <td>to</td>
      <td>PART</td>
      <td>aux</td>
      <td>explore</td>
      <td>to</td>
      <td>xx</td>
    </tr>
    <tr>
      <th>9</th>
      <td>explore</td>
      <td>VERB</td>
      <td>advcl</td>
      <td>travelled</td>
      <td>explore</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>10</th>
      <td>new</td>
      <td>ADJ</td>
      <td>amod</td>
      <td>galaxies</td>
      <td>new</td>
      <td>xxx</td>
    </tr>
    <tr>
      <th>11</th>
      <td>galaxies</td>
      <td>NOUN</td>
      <td>dobj</td>
      <td>explore</td>
      <td>galaxy</td>
      <td>xxxx</td>
    </tr>
    <tr>
      <th>12</th>
      <td>.</td>
      <td>PUNCT</td>
      <td>punct</td>
      <td>travelled</td>
      <td>.</td>
      <td>.</td>
    </tr>
  </tbody>
</table>
</div>



We can use `like_num` to find any numeric tokens in the text. This includes both digits and words for numbers.


```python
for token in doc:
    if token.like_num:
        print(f'Token: {token}   Index: {token.i}')
```

    Token: 12   Index: 4
    Token: billion   Index: 5


We can check to see if the model recognized SpaceX as an entity...


```python
for ent in doc.ents:
    print(ent.text, ent.label_)
```

    12 billion light MONEY


...Looks like it didn't. "12 billion light" is also **not** money here.

However, all is not lost! We can use a special feature called **match patterns**, along with manually adding this element to our list of entities, `doc.ents` (which we'll get to shortly), to set things straight.

## Match Patterns

<img src="https://i.imgur.com/OlxGPEH.jpg" title="source: imgur.com" style='width:400px;' />


```python
from spacy.matcher import Matcher

# initialize matcher using vocabulary shared with the nlp object
matcher = Matcher(nlp.vocab)
```

##### What do they <b>do? </b>

One of the coolest things about spaCy is its built-in ability to let us search for patterns without having to rely on regular expressions. **Match patterns** (the spaCy regex equivalent) let you search for a pattern within a text, which can be a string, a doc or a token object &mdash; regular expressions can only take string arguemnts.


Match patterns also let you customize what *kind* of pattern you're looking for &mdash; which isn't always a simple sequence of characters. When we're doing NLP analyses, we might want to look for words belonging to a particular POS category, or words with a particular lemma. For instance, setting the lemma search to "run" would return tokens that contain the base form, such as "running" or "runs".

#####  So... what exactly are match patterns? What do they look like?

Match patterns are lists of dictionaries, wherein each key is the attribute and each value is the corresponding value you're looking for.

```
pattern = [{'ATTRIBUTE': 'VALUE'}]
```

Each dictionary corresponds to exactly one token. If you have more than one dictionary, the list of dictionaries will correspond to a sequence of tokens appearing in that order (if that sequence exists in the doc).

Let's say we have a doc containing the string `"Hello world!"` as well as `"it's nice to say hello"`and we want to find all instances of `"hello"` where it's followed by a noun, as well as also all instances where it's not.

<img src="https://imgur.com/zYMm9ox.jpg" title="source: imgur.com" style='width:650px;' />


We can use the `OP` attribute with the `*` key to indicate that this token is optional (i.e., "find this element 0 or more times").

_For this particular case, this step is somewhat redundant, but I want to illustrate the optional feature in the simplest way possible._

Some attributes for rule-based matching:

```
            return bool:

TEXT        IS_ALPHA     IS_LOWER   
LOWER       IS_ASCII     IS_UPPER   
LENGTH      IS_DIGIT     IS_TITLE      
POS         IS_PUNCT     IS_SPACE
OP          IS_STOP

```

This [Matcher Explorer](https://explosion.ai/demos/matcher) is a really cool tool for checking and trying out various match patterns, and if you're using spaCy for text analysis I would highly recommend giving it a whirl!


```python
# first we set the pattern
pattern = [{'TEXT': 'SpaceX'}]

# then we add the pattern to our matcher
matcher.add('spacex', None, pattern)

# then we pass the text we want to search to the matcher
matches = matcher(doc)
matches
```




    [(1533271143234181118, 1, 2)]



The matcher returns a list of tuples, where the first value is the match ID, the second is the start index, and the third is the end index of the match.


```python
for match_id, start, stop in matches:
    matched_span = doc[start:stop]
    print(matched_span)
```

    SpaceX


### Using Matcher: Overview

**Steps:**

1. Import Matcher from `spacy.matcher`
2. Load model (e.g., `'en_core_web_sm'`)
3. Create nlp object (if not already previously done)
4. Instantiate Matcher with shared vocab (pass in `nlp.vocab`)
5. Pass your match pattern to `matcher.add`, where:
    - argument 1 = a string representing a unique ID of your choosing to identify the pattern
    - argument 2 = optional callback (if none, set `None`)
    - argument 3 = list of token desriptions, i.e., the pattern
6. Call matcher on the `doc` object (or whatever you've called your doc object) and toss this into a variable (here, I've used `matches` to keep things simple)
7. **Optional**: peek at what's inside. Remember the returned tuple contains the match ID, and the start and stop indices of the match.
8. To return the match(es) as a string (to actually see what they are &mdash; we might not always know what strings our match is going to return!), use a loop to iterate over each item in the tuple, as demonstrated above.   

## Hashing, vocab and string stores

The way we access the vocabulary in spaCy is through hash IDs and string stores. The vocabulary will depend on which package we passed into `spacy.load`, and will contain all the unique tokens within that package / dataset.

spaCy stores tokens in the vocabulary as hashes, such that every identical token string will have the same hash ID (a unique numeric identifier). Hashes enable memory efficiency since this way, if an identical string occurs multiple times (e.g. the word "the"), it only needs to be stored once in the vocabulary (and not multiple times as a string).

Every hash corresponds to a string token, and every string will have a corresponding hash. You can use either one to look up the other, as long as that string is already in the vocabulary.

If the word is new to the vocabulary, we must first hash it (as I'll show below). We can always get the hash of a word by looking up a string (if it's not already there, a new one will be generated), but if the word is new and doesn't yet have a hash, we can't search from hash ID to string (it won't exist!).


```python
# reminder of the contents of our doc object
doc.text
```




    'The SpaceX spaceship travelled 12 billion light years to explore new galaxies.'



We can search for a hash or a string using

```
nlp.vocab.strings['string']
nlp.vocab.strings[hash]
```
OR
```
doc.vocab.strings['string']
doc.vocab.strings[hash]
```

where `'string'` is the string token you're searching for (or adding to the vocab) and `hash` is an integer representing the hash ID of an existing string.



```python
spaceship_hash = nlp.vocab.strings['spaceship']
spaceship_hash
```




    2527206094249092639




```python
# this is what happens when you search for a hash that doesn't correspond to any string in the vocab
nlp.vocab.strings[4523523]
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-17-4c77b5a5c88e> in <module>
          1 # this is what happens when you search for a hash that doesn't correspond to any string in the vocab
    ----> 2 nlp.vocab.strings[4523523]


    strings.pyx in spacy.strings.StringStore.__getitem__()


    KeyError: "[E018] Can't retrieve string for hash '4523523'."


The string for hash 4523523 can't be retrieved because it doesn't match any existing item in the vocab.

Once we know the hash of a string, we can call it within `nlp.vocab.strings` to once again get back the corresponding string.


```python
spaceship_string = nlp.vocab.strings[spaceship_hash]
spaceship_string
```




    'spaceship'



### Fixing up our entities

You'll recall that spaCy incorrectly identified "12 billion light" as a `MONEY` entity, as well as missed SpaceX altogether. SpaceX should be labelled as an organization &ndash; `ORG` &ndash; while we can create a "distance" label &ndash; `DIST` &ndash; for "light years".


```python
pattern = [{'TEXT': 'SpaceX'}]
spacex_matcher = matcher.add('spacex', None, pattern)

matcher(doc)
```




    [(1533271143234181118, 1, 2)]



Now we know the start and stop indices for our SpaceX entity. Let's do the same for "light years"


```python
matcher = Matcher(nlp.vocab)

pattern = [{'LIKE_NUM': True}, {'LIKE_NUM': True}, {'POS': 'ADJ'}, {'POS': 'NOUN'}]

matcher.add('is_numeric', None, pattern)
matches = matcher(doc)
matches
```




    [(14514059297638010452, 4, 8)]



Here I'm iterating over my matches to check that `matched_span` actually returns what we want it to return, which would indicate that the indices returned by the matcher are correct.


```python
for match_id, start, stop in matches:
    matched_span = doc[start+2:stop]
    print(matched_span)
```

    light years


Yep, good to go!

**Note:** `matched_span` originally returned the whole phrase, "12 billion light years" because of how I wrote the match pattern. I only want "light years" though, so I just added 2 to the start index, to effectively jump past the first two tokens of the match ("12 billion").


```python
from spacy.tokens import Doc, Span

# using the start/stop indicies returned to us by the matcher
span_1 = Span(doc, 1, 2, label='ORG')
print(span_1.text, span_1.label_)

span_2 = Span(doc, 6, 8, label='DIST')
print(span_2.text, span_2.label_)

# Setting the doc's entities using the span object--this also overwrites the existing incorrect entity
doc.ents = [span_1, span_2]

# Print entities' text and labels
print([(ent.text, ent.label_) for ent in doc.ents])
```

    SpaceX ORG
    light years DIST
    [('SpaceX', 'ORG'), ('light years', 'DIST')]


## displaCy

This is probably one of my favourite features of spaCy. Maybe as a linguist I'm slightly biased toward neat visual respresentations of syntactic parses, but I also think this tool is just pretty objectively cool.

**displaCy takes your doc object and visually depicts its syntactic dependencies, in addition to providing the POS of each word.**

First, import displaCy, then instantiate your nlp and doc objects (if you hadn't already done so previously), and then call `displacy.render` on your doc object (or list of docs!). This will return a dependency-parsed sentence!

It's at this step, within `displacy.render`, that you may also specify any additional preferred parameters (which I'll go into more below).


```python
from spacy import displacy
```


```python
# displacy.serve(doc) returns an html page with your visualization. Useful for longer sentences!
# html = displacy.render(doc) # optional: throw this into a variable, the default in spaCy documentation is "html"
```

To simplify things a little bit, I'll create two new doc objects called "dogs" and "cats".


```python
dogs = nlp(u"Megan loves dogs.")
cats = nlp(u"Mary loves cats.")
```

In `displacy.render`, there are two style options:


- `dep` returns a visualization of the syntactic dependencies (default)
- `ent` returns a prettified sentence which highlights the entities it contains.


For example:


```python
displacy.render([dogs, cats], style='ent')
```


<div class="entities" style="line-height: 2.5; direction: ltr">
<mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    Megan
    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PERSON</span>
</mark>
 loves dogs.</div>

<div class="entities" style="line-height: 2.5; direction: ltr">
<mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    Mary
    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PERSON</span>
</mark>
 loves cats.</div>


`displacy.render([dogs, cats], style='dep')`

<img src='https://i.imgur.com/d5IHB64.png' style='width:450px;'>


```python
displacy.render(doc, style='ent')
```


<div class="entities" style="line-height: 2.5; direction: ltr">The
<mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    SpaceX
    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">ORG</span>
</mark>
 spaceship travelled 12 billion
<mark class="entity" style="background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    light years
    <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">DIST</span>
</mark>
 to explore new galaxies.</div>


#### Customization

The function signature for displaCy is as follows:

```
Signature:
displacy.render(
    docs,
    style='dep',
    page=False,
    minify=False,
    jupyter=None,
    options={},
    manual=False,
)
Docstring:
Render displaCy visualisation.
```

We can pass a dictionary of attributes into the `options` argument to ultra-customize the viz. Below is a list of valid attributes (option dict keys).

**Options:**
```
fine_grained
collapse_punct
collapse_phrases
compact
color
bg
font
offset_x
arrow_stroke
arrow_width
arrow_spacing
word_spacing
distance
```

We'll go through a few, but to read more about what each of these arguments does, check out the displaCy documentation [here](https://spacy.io/api/top-level#options).


```python
options = {'word_spacing': 25}
```

```
displacy.render(dogs, style='dep', options=options)
```

<img src='https://i.imgur.com/FUAfURZ.png' style='width:500px;'>


```python
options = {'distance': 120}
```

```
displacy.render(dogs, style='dep', options=options)
```

<img src='https://i.imgur.com/jBUcUgv.png' style='width:450px;'>

In the code block below, I'm populating the `options` dictionary with the features I want to adjust:

- `word_spacing` sets the (vertical) space between the words and the arrows
- `compact` makes the arrows squared to conserve space
- `distance` sets the distance between each of the words (basically, the width of the entire viz)
- `arrow_spacing` sets the space between arrows (so the smaller the int value you pass, the less space between arrows)
- `offset_x` is the amount of space between the "edge" of the viz and the first word that appears
- `arrow_width` sets the size of the "arrowhead"
- `color` sets the color of the text and arrows
- `bg` sets the background color.

```
options = {
    'word_spacing': 25,
    'compact': False, # default
    'distance': 85,
    'arrow_spacing': 2,
    'offset_x': 17,
    'arrow_width': 6,
    'color': '#ffffff',
    'bg': '#0be3df'
}

displacy.render(doc, style='dep', options=options)
```

<img src='https://i.imgur.com/6aV8j93.png' style='width:1100px;'>

### One last thing...

### `spacy.explain`

This method is super great when dealing with abbreviations and shorthands, which tend to be ubiquitous in a package filled with descriptors like "adverbial clause modifier". Not exactly compact. From time to time, we might encounter an abbreviation/label we're unfamiliar with, and in such cases we can call `spacy.explain`, which **takes any spaCy abbreviation, shorthand or label as a string argument and returns the full name.** Check it out:


```python
spacy.explain('JJ')
```




    'adjective'



Here's a few more:


```python
print('advcl:', spacy.explain('advcl'))
print('\namod:', spacy.explain('amod'))
print('\nnummod:', spacy.explain('nummod'))

print('\nORG:', spacy.explain('ORG'))
```

    advcl: adverbial clause modifier

    amod: adjectival modifier

    nummod: numeric modifier

    ORG: Companies, agencies, institutions, etc.



```python
tags = [token.tag_ for token in tokens]
tags
```




    ['DT',
     'NNP',
     'NN',
     'VBD',
     'CD',
     'CD',
     'JJ',
     'NNS',
     'TO',
     'VB',
     'JJ',
     'NNS',
     '.']




```python
tags_explained = [spacy.explain(i) for i in tags]
```

We can use a simple zip function to create a list of tuples containing each of the tags, along with their respective "definitions".


```python
list(zip(tags, tags_explained))
```




    [('DT', 'determiner'),
     ('NNP', 'noun, proper singular'),
     ('NN', 'noun, singular or mass'),
     ('VBD', 'verb, past tense'),
     ('CD', 'cardinal number'),
     ('CD', 'cardinal number'),
     ('JJ', 'adjective'),
     ('NNS', 'noun, plural'),
     ('TO', 'infinitival to'),
     ('VB', 'verb, base form'),
     ('JJ', 'adjective'),
     ('NNS', 'noun, plural'),
     ('.', 'punctuation mark, sentence closer')]



#### Hope you enjoyed this introduction to spaCy! Now go have some fun with words 😏
