FROM python:3.6.9

# copy
WORKDIR /
COPY . .

# install reqs
RUN pip install -r requirements.txt

# run
CMD [ "python", "./client.py" ]
