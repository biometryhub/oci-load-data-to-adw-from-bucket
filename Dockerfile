FROM fnproject/python:3.9-dev as builder
WORKDIR /function
ADD requirements.txt /function/

RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt &&\
    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
    chmod -R o+r /python
ADD . /function/
RUN rm -fr /function/.pip_cache

FROM fnproject/python:3.9
WORKDIR /function
# ADD ./.oci ./.oci
COPY --from=builder /python /python
COPY --from=builder /function /function
RUN chmod -R o+r /function
ENV PYTHONPATH=/function:/python
ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]