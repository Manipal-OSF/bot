FROM python:3.11.1-slim

# Create the working directory
WORKDIR /bot

# Set pip to have cleaner logs and no saved cache
ENV PIP_NO_CACHE_DIR=false

# Install project dependencies
RUN pip install -U pip wheel setuptools
RUN pip install poetry==1.5.1

# export requirements after copying req files
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes > requirements.txt
RUN pip uninstall poetry -y
RUN pip install -U -r requirements.txt

# Copy the source code in next to last to optimize rebuilding the image
COPY . .

# install the package using pep 517
RUN pip install . --no-deps

ENTRYPOINT ["python3", "/bot/osfbot/__main__.py"]
