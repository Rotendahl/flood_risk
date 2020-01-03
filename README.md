## Bolius Flood Model

This repo contains a model that given a longitude, latitude pair returns the
risk that flooding will occur at the address. We compute two types of flood risk:
The data used comes from [_kortforsyningen_][kortforsyningen] and the [danish environment ministry][miljoegis]

#### Cloudburst

Flooding caused by excessive rain. (_Skybrud_ in danish). The
risk here is a combination of the factors following factors (english/danish).
To read more about a factor visit the linked notebook

-   **[(Hollowing/Lavning)][hollowingnotebook]:** A hollowing is a "hole" in the
    ground where water will collect.

-   **[(Fastning/Befæstelsesgrad)][fastningnotebook]:** The amount of area
    around the point that has buildings, roads or other surfaces the water can't
    drain through.

-   **[(Conductivity/Hydraulisk ledeevne)][conductivitynotebook]:** The ground
    type in the area.


-   **Housing data:** The properties of the house located at the specified
    point. For instance if the house has a basement it increases the risk of
    flooding. The [danish building registry][bbr] provides the building data.

#### Storm flood

Flooding caused by rising sea levels due to storm. This affects people who live
close to the sea. The [flood notebook][floodnotebook] provides more detail

* * *

### Technical documentation

#### The data

The data is primarily given as images served by the [_Web Map Service_][wms]
(WMS) protocol. As an example the flow for retrieving a hollowing image given
the longitude latitude is as follows:

-   Convert the longitude and latitude to [The ESPG 3857 projection][espg]. This
    projection uses meters as it's unit making computations easier.
-   Create a bounding box around the specified point
-   Request an image with the box at the projected point with.

#### The modules

The model consists of two modules the [code](./code) module containing plain
python code, it has functions for data retrieval and image handling.
The risk analysis is in the [notebooks](./notebooks) module, the notebook files
contain both python code and markdown text describing the computation.

#### The environment

The model uses the [pipenv][pipenv] package as environment manager, it specifies
the python version and packages required to run the code. To set up _pipenv_ run
see the install section in it's readme.

Before activating a pipenv shell a `.env` file should exists, copy the
`.env.example` to `.env` and fill out the variables. Creating credentials for
kortforsyningen is free.

To run the model start pipenv and run `jupyter notebook` from the project root.
See the [Rain-risk][rainnotebook] and [flood-risk][floodnotebook] notebooks to
read more about the models and see them in action.

#### Testing

To run the [tests](./tests) issue the command `python -m unittest` in an activated
pipenv shell from the project root.

#### Deployment

<!-- TODO Write this -->

* * *

#### Related projects

The react page ["When the Water comes"](https://github.com/bolius/water_comes)
presents this model as a webpage.

<!-- Links -->

[kortforsyningen]: https://download.kortforsyningen.dk/content/geodataprodukter

[miljoegis]: https://www.klimatilpasning.dk/kommuner/kortlaegning/data-til-kortlaegning/

[hollowingnotebook]: ./notebooks/hollowing.ipynb

[fastningnotebook]: ./notebooks/fastning.ipynb

[conductivitynotebook]: ./notebooks/conductivity.ipynb

[floodnotebook]: ./notebooks/flood.ipynb

[rainnotebook]: ./notebooks/rain.ipynb

[bbr]: https://bbr.dk/forside

[wms]: https://en.wikipedia.org/wiki/Web_Map_Service

[espg]: https://epsg.io/3857

[pipenv]: https://github.com/pypa/pipenv
