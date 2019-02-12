## Workflow
The general purpose of the machine learning section at Bolius is to provide
information that might be usable for homeowners. This open goal means that we
want to be able to explore new data and how it correlates with existing data
quickly. Once a new data set is made available we go through the following
steps.  

### Exploratory state
The raw data is put into the _raw_data_ repo and an overview notebook is created.
This notebook must provide at least the following information.  
* A short description of how the data was obtained.
* How noisy the data is, percentage of missing values, representativity of
the data.
* Basic plots that show the interesting fields

When the exploratory state has yielded a "gut feeling" of the data, we might
present correlations and graphs for the subject-experts at Bolius to get a quick
and easy validation.


### Basic Model state
Our  goal of "helping" home owners means that there is not always a clear goal
with data. For instance, for the energy-rapport we could either predict
energyLabel, energy consumption or any other field. In the basic model state
we run several basic models on different fields of the models and examine the results to get a rough idea of what performance we can achieve.
The following procedure for data handling is used:
1. Shuffle all data in the set to remove any implicit ordering bias.
2. Split the data into three parts, A training set, a validation set, and a
test set. (The split should be at least 80%, 10%, 10%) unless the data set
allows a better split.
3. Lock the test set away and do **not** use it until the final models has has
selected.
4. Test and tune as many models as you like with cross validation on the
training set.
5. Lock the models in test them on the validation set.


Once step 5. has been reached we are ready for another round of presentations
for the subject-expert at Bolius. Present them with a confusion matrix for
classification, (possibly PCA) scatter plots with guessed and predicted.
Do an exercise where you give input from the validation set to the experts and
to model and compare performance. It is allowed to go back to step 3 and test
more models and data transformations to include improvements from the
presentation.

Once you are ready for production pick the $m$ models that should go live,
serialize them and put them in the AI model git repo. Each of the $i$ models
$h_1, \dots h_i$ should  have a graph (confusion matrix, error bar) and most importantly plug into the following generalization bound and plot it as function:
of $\delta$.
$$
    L_{out}(h_i) \leq L_{test}(h_i) + \sqrt{\frac{\ln ({\frac{m}{\delta}})}{2n}}
$$
Then we have a bound of the out of sample error that holds with probability
$1 - \delta$.

>**WARNING**
The above process is extremely prone to [data snooping][dataSnoop], the
data must handled in the way describe below or all assurances break.



[ORM_URL]: https://github.com/Bolius/machine-learning-orm
[dataSnoop]: https://en.wikipedia.org/wiki/Data_dredging
