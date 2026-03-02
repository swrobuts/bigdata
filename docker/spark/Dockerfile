# Spark Lab - Distributed Data Processing
# PySpark with Jupyter notebook interface for big data analytics

FROM jupyter/pyspark-notebook:latest

LABEL maintainer="BigData Lab"
LABEL description="PySpark environment with MegaStore data for distributed analytics"

# Switch to root to install packages
USER root

# Install additional system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER jovyan

# Install additional Python packages for analytics
RUN pip install --quiet --no-cache-dir \
    pandas==2.2.0 \
    numpy==1.24.3 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    scikit-learn==1.3.2 \
    plotly==5.18.0 \
    pyarrow==15.0.0 \
    delta-spark==3.0.0

# Create data directory
RUN mkdir -p /home/jovyan/data

# Copy data files
COPY --chown=jovyan:users ../data/megastore/orders.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/order_items.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/clickstream.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/products.csv /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/customers.csv /home/jovyan/data/

# Copy starter notebook/script
COPY --chown=jovyan:users ./notebooks/megastore_spark_intro.py /home/jovyan/notebooks/

# Configure Spark for single-node setup
ENV SPARK_LOCAL_IP=127.0.0.1
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --ip=0.0.0.0"

# Set working directory
WORKDIR /home/jovyan

# Expose ports
EXPOSE 8888 4040

# Default command - start Jupyter notebook server
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
