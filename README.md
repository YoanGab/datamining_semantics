# Overview

In this project, you will find a Web application that integrates different point of interest which are geospatial data from mutiple sources, including dynamic data about mechanical and electrical bicycles.

We defined an ontology that describes the types of entities that are stored in the knowledge base.

And then we displayed information on Web pages together with structured data, for best search engine optimisation.

## Installation

To install packages, run :
```
> pip3 install virtualenv
> virtualenv dataming_semantics --python=python3.9
> source dataming_semantics/bin/activate
> pip3 install -r requirements.txt
```
 OR 
 
-   Clone this repo :
    `git clone https://github.com/YoanGab/dataming_semantics.git`
-   In the shell, go into the repository using `cd PATH_TO_REPO`
-   Install necessery packages by running the following command in the shell
    `pip install -r requirements.txt`


## Run the server
```
> python3 main.py
```

### Then you can go to http://localhost:5000/ to use the web interface




## How to use

You can click on the left panel where there are all the results. It will show you the selected bicycle station.
You can also filter by type of bicycle available: either mechanic or electric.




