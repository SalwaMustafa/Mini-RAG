# Mini-RAG
Implementation of Mini-RAG application based on Abu-Bakr Soliman's tutorial. Leveraging the principles outlined in the tutorial, this repo demonstrates the integration of retrieval-augmented generation (RAG) with a minimal setup, suitable for experimentation and further development.

## Requirements

- python 3.8 or later

#### Install python using Miniconda

1) Download and install Miniconda 
2) Create a new environment using the following command:
```bash
$ conda create -n Mini-RAG-App python=3.8
```
3) Activate the environment:
```bash
$ conda activate Mini-RAG-App
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

set your environment variables in the '.env' file like 'OPENAI_API_KEY' value.