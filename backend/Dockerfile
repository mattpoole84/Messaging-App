FROM python:3.7
RUN mkdir /main
COPY . /main
WORKDIR /main

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["/bin/bash", "./start.sh" ]
