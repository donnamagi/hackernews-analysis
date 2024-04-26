# Analysis of Hacker News

The objective of this project was to create my own dataset of stories and articles from Hacker News, an to find insightful correlations between the popular discourse in the tech community and real world events.

## Setup instructions 

Some steps are required to get started with this project. 

### External dependencies

This project has external dependencies that need to be set up in order to successfully run the code. All services are free to use (as of April 2024).

**Zilliz - vector DB**

This project setup heavily depends on integration with an external data source, a cloud vector database called [Zilliz](https://zilliz.com). Successfully running many of the scripts requires [setting up Zilliz](https://docs.zilliz.com/docs/quick-start) or reconfiguring for a different data storage method.

**Voyage - embeddings** 

[Voyage AI](https://www.voyageai.com) was, at the time of my research, the industry leader in large text embeddings. I chose to integrate their API as part of my data preprocessing workflow. Setup instructions [here](https://docs.voyageai.com/docs/api-key-and-installation).

**Llama 2 - text synthesis**

To clean and synthesize text coming from third party websites, I found [Llama 2-7B](https://llama.meta.com/llama2/), a locally running LLM, to work best. Get started by installing Ollama ([instructions](https://github.com/ollama/ollama)), and sequentially [following this guide](https://ollama.com/library/llama2) for setting up Llama to run on local port.

### Internal dependencies

It is recommended to set up a virtual environment.

To install project dependencies:
``` 
pip install -r requirements.txt
```

## Running the code

### Get the source data

Pulling data from Hacker News itself is a simple script that could be executed without setting up external dependencies. 
Get started by allowing the bash script to run on your machine.

In the source folder, run the following terminal command to grant execution rights:
```
chmod +x top_hn/fetch_best.sh
 ```

You can now run the bash script to pull articles from Hacker News:

```
./top_hn/fetch_best.sh
```

This will create a json file in your ./results folder, containing the 200 most trending articles as of right now. The list is a ID representation of each individual article. 

More on the Hacker News API [here](https://github.com/HackerNews/API).

### Process the articles

Processing the articles requires having set up or reconfigured the external dependencies. 

The source script for processing the articles is in [./process.py](https://github.com/donnamagi/newsletter-backend/blob/main/process.py).

If in the source folder, it can be triggered by running:

```
python process.py
```

### View findings

My preliminary work with this data is deployed on Streamlit. 

The source code can be found in [./streamlit.py](https://github.com/donnamagi/newsletter-backend/blob/main/streamlit.py), or deployed on [https://hackernews-demo.streamlit.app](https://hackernews-demo.streamlit.app).
