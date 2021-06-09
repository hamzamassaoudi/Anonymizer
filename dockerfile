FROM python:3.8.8

# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt
RUN python3 -m spacy download fr_core_news_md

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app
WORKDIR /app

# run it!
ENTRYPOINT ["streamlit", "run", "streamlit_demo.py", "--server.port=8080", "--server.address=0.0.0.0"]