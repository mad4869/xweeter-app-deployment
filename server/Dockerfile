FROM python:3.10

LABEL version="1.0"

WORKDIR /xweeter-api

COPY . .
RUN pip install -r requirements.txt

ENV FLASK_APP="run.py"
ENV FLASK_DEBUG=1
ENV ENVIRONMENT="development"
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PORT="5432"
ENV TZ="Asia/Jakarta"

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]