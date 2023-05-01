# syntax=docker/dockerfile:1.4
FROM ubuntu:22.04

# Install OS-level packages
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get --yes upgrade && \
    apt-get --yes install --no-install-recommends \
    python3.10-full tini build-essential

# Create and activate virtual environment
ENV VIRTUAL_ENV="/root/.venv"
RUN python3.10 -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update pip
RUN pip install --upgrade pip setuptools wheel

# Setup root home directory
WORKDIR /root/take_home_project

# Install package
# COPY . .
COPY . .
RUN pip install . --requirement requirements.txt
# COPY . ./root/take_home_project
# RUN pip install -r ./root/take_home_project/requirements.txt
# EXPOSE 8888
# CMD ["python", "app.py"]
ENTRYPOINT ["tini", "-v", "--"]
