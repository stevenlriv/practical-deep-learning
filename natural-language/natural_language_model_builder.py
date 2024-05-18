from fastbook import *
from fastai.text.all import *

## Step 1: Gather and prep the data
path = untar_data(URLs.IMDB)
path.ls()

## Step 2: Establish your Data Loader object

#clean and delete uncomented codes after proof it works
#dls = TextDataLoaders.from_folder(path, valid='test')
#dls.show_batch()

jam = DataBlock(
	blocks=(TextBlock.from_folder(path), CategoryBlock),
    get_items=get_text_files,
    get_y=parent_label,
    splitter=GrandparentSplitter(valid_name='test'))

dls_lm = jam.dataloaders(path)
dls_lm.show_batch(max_n=2)

## Step 3: Fine tune your model

learn = text_classifier_learner(dls_lm, AWD_LSTM, drop_mult=0.5, metrics=accuracy)
learn.fine_tune(1, 1e-2)
learn.show_results()

## Step 4: Mistakes and Cleaning them

## Step 5: Use the model

# Lets get a prediction
learn.predict("I really liked that movie!")

## Step 6: Export the model
learn.save('finetuned')
learn.export('model.pkl')