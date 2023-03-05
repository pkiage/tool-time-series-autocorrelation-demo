---
title: Time Series Autocorrelation Demo
emoji: 📈
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.17.0
app_file: app.py
pinned: false
license: openrail
---

# Time series autocorrelation tool

Tool demonstrating time series autocorrelation analysis with Python

Assumes uploaded data is clean.

## Built With

- [Streamlit](https://streamlit.io/)


## Local setup

### Obtain the repo locally and open its root folder

#### To potentially contribute

```shell
git clone https://github.com/pkiage/tool-time-series-autocorrelation-demo
```

or

```shell
gh repo clone pkiage/tool-time-series-autocorrelation-demo
```

#### Just to deploy locally

Download ZIP

### (optional) Setup virtual environment:

```shell
python -m venv venv
```

### (optional) Activate virtual environment:

#### If using Unix based OS run the following in terminal:

```shell
.\venv\bin\activate
```

#### If using Windows run the following in terminal:

```shell
.\venv\Scripts\activate
```

### Install requirements by running the following in terminal:

#### Required packages

```shell
pip install -r requirements.txt
```

## Build and install local package

```shell
python setup.py build
```

```shell
python setup.py install
```

### Run the streamlit app (app.py) by running the following in terminal (from repository root folder):

```shell
streamlit run src/app.py
```


<p><small>Project structure based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>.</small></p>

## Hugging Face Tips

- [When syncing with Hugging Face via Github Actions](https://huggingface.co/docs/hub/spaces-github-actions) the [User Access Token](https://huggingface.co/docs/hub/security-tokens) created on Hugging Face (HF) should have write access
- [When creating the Spaces Configuration Reference](https://huggingface.co/docs/hub/spaces-config-reference) ensure the [Streamlit Space](https://huggingface.co/docs/hub/spaces-sdks-streamlit) version (sdk_version) specified is supported by HF