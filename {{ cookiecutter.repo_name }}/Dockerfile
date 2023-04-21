FROM ubuntu:22.04

RUN apt update && apt upgrade -y

# install java, curl, git, tools to compile python
RUN apt update &&  \
    apt install -y sudo && \
    sudo apt install default-jdk curl git \
    build-essential libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev wget zlib1g-dev -y && \
    rm -rf /var/lib/apt/lists/*

# add kedro user
ARG KEDRO_UID=1000
ARG KEDRO_GID=1000
ARG USER_NAME=kedro
RUN groupadd --gid ${KEDRO_GID} $USER_NAME && \
    useradd --uid ${KEDRO_UID} --gid ${KEDRO_GID} -m $USER_NAME

# switch to user / user directory
ENV HOME /home/${USER_NAME}
USER $USER_NAME
WORKDIR ${HOME}

# pyenv
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git ~/.pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

# python
ENV PYTHON_VERSION=3.10.8
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

# poetry
ENV POETRY_VERSION=1.4.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:${HOME}/.local/bin"

# requirements
RUN poetry config virtualenvs.create false
COPY --chown=${USER_NAME}:1000 pyproject.toml poetry.lock ./
RUN poetry run pip install --upgrade pip
RUN poetry install && rm -rf .cache/pypoetry && rm pyproject.toml poetry.lock
RUN pyenv rehash
