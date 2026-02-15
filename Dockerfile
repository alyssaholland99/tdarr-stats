FROM python:3.14-slim

ARG USERNAME=tdarr-stats
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the immich-tiktok-remover user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

WORKDIR /home/tdarr-stats

ENV PIP_NO_CACHE_DIR=off 

COPY requirements.txt .
COPY get_stats.py .
COPY templates/ ./templates

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "get_stats.py"]