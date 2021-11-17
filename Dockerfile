# Pull base image
FROM python:3.9
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /hasker_Project
# Install dependencies
COPY Pipfile Pipfile.lock /hasker_Project/
RUN pip install pipenv && pipenv install --system
# Copy project
COPY . /hasker_Project/