# DuckDB Lab - Jupyter-based analytics
# Lightweight analytical SQL engine with Jupyter notebook interface

FROM jupyter/minimal-notebook:latest

LABEL maintainer="BigData Lab"
LABEL description="DuckDB analytics environment with MegaStore data"

# Switch to root to install packages
USER root

# Update package index and install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER jovyan

# Install Python packages
RUN pip install --quiet --no-cache-dir \
    duckdb==1.0.0 \
    pandas==2.2.0 \
    pyarrow==15.0.0 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    openpyxl==3.1.0 \
    jupyter==1.0.0

# Create data directory
RUN mkdir -p /home/jovyan/data

# Copy data files
COPY --chown=jovyan:users ../data/megastore/orders.csv /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/orders.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/order_items.csv /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/order_items.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/clickstream.csv /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/clickstream.parquet /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/products.csv /home/jovyan/data/
COPY --chown=jovyan:users ../data/megastore/customers.csv /home/jovyan/data/

# Copy starter notebook/script
COPY --chown=jovyan:users ./notebooks/megastore_duckdb_intro.py /home/jovyan/notebooks/

# Set working directory
WORKDIR /home/jovyan

# Expose Jupyter port
EXPOSE 8888

# Default command - start Jupyter notebook server
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
