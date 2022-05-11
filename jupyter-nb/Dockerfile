FROM continuumio/miniconda3:4.11.0

WORKDIR /jupyter
RUN conda install \
    networkx \
    neo4j-python-driver \
    scipy \
    numpy \
    pandas \
    progress \
    matplotlib \
    jupyterlab

EXPOSE 8888