FROM python:3.11

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

EXPOSE 80
ENV FORWARDED_ALLOW_IPS *

CMD ["uvicorn", "test.app:app", "--host", "0.0.0.0", "--port", "80", "--forwarded-allow-ips", "*", "--proxy-headers"]

# Need to include the following amendments
# Mod langchain_community by replacing langchain_community/vectorstores/azure_cosmos_db.py
# Mod langchain_core by replacing langchain_core/documents/base.py