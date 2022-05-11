FROM continuumio/miniconda3:4.11.0

COPY scraping /python/scraping

WORKDIR /python
RUN conda install \
    networkx \
    neo4j-python-driver \
    scipy \
    numpy \
    pandas \
    progress \
    matplotlib \
    jupyterlab
