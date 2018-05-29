FROM python:3.5-slim

MAINTAINER Beauty CRM <beautycrm@gmail.com>

RUN apt-get update && \
    apt-get install -y \
    swig \
    libssl-dev \
    dpkg-dev \
    netcat \
    python3-dev \
    supervisor

COPY ./src/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

CMD ["/bin/sh", "/opt/beautycrm/entrypoint.sh"]