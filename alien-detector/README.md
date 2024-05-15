---
license: mit
---

# Practical Alien Detector

Finetuned resnet50 for detecting if the image you show it is an alien or not. 

You can try it out as an API by following the `How to run an API and test your model` instructions.

This model was created for fun!

## Installation

```shell
pip3 install fastbook

pip3 install fastai

pip3 install flask
```

## How to build your model

```shell
python3 aliens_model_builder.py
```

## How to test your model

After running it wil ask the image path.

```shell
python3 aliens_model_test.py
```

## How to run an API and test your model

After running it, visit `http://localhost:5000/`

```shell
python3 aliens_api.py
```