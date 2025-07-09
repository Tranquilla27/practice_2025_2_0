FROM python
WORKDIR /python-app
RUN pip install tkinter
COPY . .
CMD ["python", "LAB#2.py"]
