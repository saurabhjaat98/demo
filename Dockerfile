ARG PYTHON_VERSION=3.10-bullseye
FROM python:${PYTHON_VERSION} as builder
RUN pip install --upgrade pip


RUN groupadd -g 999 app && \
    useradd -r -u 999 -g app app

USER app
WORKDIR /home/app

COPY requirements.txt /tmp/requirements.txt
WORKDIR /home/app
USER root
RUN pip install --upgrade pip && pip install --no-cache-dir --user -r /tmp/requirements.txt
COPY . /home/app
RUN python setup.py --quiet bdist_egg --exclude-source-files && wheel convert --verbose dist/*.egg --dest-dir dist   && rm -rf ./*.egg-info/  dist/*.egg build/lib  build/bdist*


FROM python:${PYTHON_VERSION} as main
ENV PYTHONUNBUFFERED 1
LABEL name="CCP"
LABEL version="v1.0.0"
LABEL author="Manik Sidana"
LABEL description="CCP API Server."

RUN groupadd -g 999 app && \
    useradd -r -u 999 -g app app
WORKDIR /home/app
COPY --from=builder /root/.local /home/app/.local
COPY --from=builder /home/app/dist  /home/app/dist
COPY --chown=app:app requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir --user -r /tmp/requirements.txt
ENV PATH="/home/app/.local/bin:${PATH}"
RUN pip install --no-cache-dir /home/app/dist/*
RUN mkdir -p /etc/ccp
COPY --chown=app:app clouds.yaml /etc/ccp/clouds.yaml
EXPOSE 7080
ENV PATH="/home/app/.local/bin:${PATH}"
ENTRYPOINT ["uvicorn", "ccp_server.main:app", "--host", "0.0.0.0", "--port", "7080"]
