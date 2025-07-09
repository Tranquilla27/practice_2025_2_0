FROM python
WORKDIR /python-app
ENV PYTHONUNBUFFERED = 1
COPY . .
CMD ["python", "project.py"]
