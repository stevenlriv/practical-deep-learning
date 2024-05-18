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

# Text Input Variable
TEXT_INPUT = "I liked this movie because"

# Prediction Output Variables
N_WORDS_OUT = 40
N_SENTENCES_OUT = 2

# Lets get a prediction
preds = [learn.predict(TEXT_INPUT, N_WORDS_OUT) 
         for _ in range(N_SENTENCES_OUT)]
         
# Lets print the prediction
print("\n".join(preds))

## Step 6: Export the model

learn.save('finetuned')
learn.export('model.pkl')

