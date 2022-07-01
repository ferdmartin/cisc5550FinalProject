FROM python:3
RUN pip install flask
RUN pip install psycopg2-binary 
EXPOSE 5001/tcp
COPY restfulAPI.py .
ENTRYPOINT [ "python3", "restfulAPI.py" ]