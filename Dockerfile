FROM python:3.6.9

# copy
WORKDIR /src
COPY . .

# install reqs
RUN pip install -r requirements.txt

# run
CMD [ "python", "./cli.py" ]