FROM python:3.10

WORKDIR /usr/src/
COPY server.py .

RUN pip install requests python-dateutil

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["python","/usr/src/server.py"]