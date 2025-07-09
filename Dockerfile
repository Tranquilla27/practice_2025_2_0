FROM python
WORKDIR /python-app
COPY . .
CMD ["python", "project.py"]
