FROM python:2.7

RUN echo "umask 042" >> /etc/bash.bashrc

# Set a default user. Available via runtime flag `--user bob`;
RUN useradd bob \
    && mkdir -p /cfcore/output \
    && chown -R bob:bob /cfcore

RUN pip install matplotlib

RUN mkdir -p /cfcore/output
RUN chmod -R u=rwx,g=rwx,o=rx /cfcore
RUN chmod -R u=rwx,g=rwx,o=rx /cfcore/output && cd /cfcore

USER bob
COPY . /cfcore


CMD ["python", "/cfcore/read_data.py"]
