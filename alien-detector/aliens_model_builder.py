from fastbook import *
from fastai.vision.all import *
from fastai.vision.widgets import *

# Step 1: Gather the data
# You can use APIs or manually download the data

# The name of the path where the two folders 
# with the data are located at
# ie. ./alien_or_not/alien for alien images
# ie. ./alien_or_not/not_alien for human images
path = Path('alien_or_not')

# Step 2: Establish your Data Loader object

aliens = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

dls = aliens.dataloaders(path)
dls.valid.show_batch(max_n=4, nrows=1)

# Step 3: Fine tune your model
# models you can use:
# resnet18
# resnet50

learn = vision_learner(dls, resnet50, metrics=error_rate)
learn.fine_tune(500)

# Step 4: Mistakes and Cleaning them

# Step 5: Use the model
is_alien, _, probs = learn.predict(PILImage.create('test_images/4.jpg'))

print(f"This is a: {is_alien}.")
print(f"Probability it's an alien: {probs[0]:.4f}")

# Step 6: Export the model

learn.export('model.pkl')