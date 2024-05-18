from fastbook import *
from fastai.tabular.all import *
from pathlib import Path
import os, zipfile, kaggle

## Step 1: Gather and prep the data
path = Path('titanic')

# If the directory is not here it means we need to download it
if not path.exists():
    kaggle.api.competition_download_cli(str(path))
    zipfile.ZipFile(f'{path}.zip').extractall(path)

# We'll import the fastai tabular library, set a random seed so 
# the code is reproducible, and pick a reasonable number of significant figures to display in our tables:
pd.options.display.float_format = '{:.2f}'.format
set_seed(42)

# Prep the data
df = pd.read_csv(path/'train.csv')

# Feature engineering
# @https://www.kaggle.com/code/gunesevitan/titanic-advanced-feature-engineering-tutorial/
def add_features(df):
    df['LogFare'] = np.log1p(df['Fare'])
    df['Deck'] = df.Cabin.str[0].map(dict(A="ABC", B="ABC", C="ABC", D="DE", E="DE", F="FG", G="FG"))
    df['Family'] = df.SibSp+df.Parch
    df['Alone'] = df.Family==0
    df['TicketFreq'] = df.groupby('Ticket')['Ticket'].transform('count')
    df['Title'] = df.Name.str.split(', ', expand=True)[1].str.split('.', expand=True)[0]
    df['Title'] = df.Title.map(dict(Mr="Mr",Miss="Miss",Mrs="Mrs",Master="Master"))

# Lets call the function with the features
add_features(df)

## Step 2: Establish your Data Loader object

# We can use RandomSplitter to separate out the training and validation sets:
splits = RandomSplitter(seed=42)(df)

dls = TabularPandas(
    df, splits=splits,
    procs = [Categorify, FillMissing, Normalize],
    cat_names=["Sex","Pclass","Embarked","Deck", "Title"],
    cont_names=['Age', 'SibSp', 'Parch', 'LogFare', 'Alone', 'TicketFreq', 'Family'],
    y_names="Survived", y_block = CategoryBlock(),
)

dls = dls.dataloaders(path=".")
dls.show_batch()

## Step 3: Fine tune your model

# To create one, we say what the data is (dls), and the size of each hidden layer ([10,10]), 
# along with any metrics we want to print along the way:
learn = tabular_learner(dls, metrics=accuracy, layers=[10,10])
learn.fit(100, lr=0.03)

## Step 4: Mistakes and Cleaning them

## Step 5: Use the model

tst_df = pd.read_csv(path/'test.csv')
tst_df['Fare'] = tst_df.Fare.fillna(0)
add_features(tst_df)

# To specify we want to apply the same steps to a new dataset, use the test_dl() method:
tst_dl = learn.dls.test_dl(tst_df)

# Now we can use get_preds to get the predictions for the test set:
preds,_ = learn.get_preds(dl=tst_dl)

# Finally, let's create a submission CSV just like we did in the previous notebook...
tst_df['Survived'] = (preds[:,1]>0.5).int()
sub_df = tst_df[['PassengerId','Survived']]
sub_df.to_csv('sub.csv', index=False)

## Step 6: Export the model

learn.export('model.pkl')