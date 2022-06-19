# Base image
FROM python:3.10-slim-bullseye

# Add Tini (init)
ENV TINI_VERSION="v0.19.0"

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Tool update
## Remove these next two lines when we can get discord.py from pip
RUN apt update
RUN apt install -y git

RUN pip install -U \
    pip \
    setuptools \
    wheel

# Projects directory
WORKDIR /opt/hal

# Create new user
RUN useradd -m -r hal && \
    chown hal /opt/hal

# Set user
USER hal

# Copy in requirements file
COPY --chown=hal src/requirements.txt .

# Install dependencies
RUN mkdir -p deps
RUN python3 -m pip install -r ./requirements.txt --target deps

# Copy in main files
COPY --chown=hal src .

# Set entrypoint.
ENTRYPOINT ["/tini", "--", "python3", "__main__.py"]
