from fastai.vision.all import *

# Load the trained model
model_path = './model.pkl'
learn = load_learner(model_path)

# Prompt the user to enter the image path
test_image_path = input("Enter the path to the test image: ")

# Prepare your test data
img = PILImage.create(test_image_path)

# Make predictions
is_alien, _, probs = learn.predict(img)

# Print the predicted class and probabilities
if is_alien == "aliens":
    print(f"This is an alien.")
else:
    print(f"This is not an alien.")

print(f"Probability it's an alien: {probs[0]:.4f}")