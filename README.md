## Bolius Public notebooks

This repo is a collection of notebooks that showcases the computations and
models behind different projects at Bolius.

### Structure

Each project has a folder which contains a notebook that serves as documentation
for the models and computations for that specific project.

The code is located in the same project folder as plain python files. This is
done such that this repo can be used as a submodule.

### Projects

- **[water-comes][water_comes]**: This projects was about predicting the risk of
  flooding and cloudbursts.

### Setup

If you want to run the notebooks locally you must copy
[.env.example][example_env] to the project root as `.env` and replace the values
with valid ones.

Dependencies are managed by [pipenv](https://github.com/pypa/pipenv).

[water_comes]: https://github.com/Bolius/notebooks/blob/master/water_comes/Hollowings.ipynb
[example_env]: https://github.com/Bolius/notebooks/blob/master/.env.example
