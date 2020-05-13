FROM python:3.6 as lint
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt


FROM python:3.6-alpine

COPY requirements.txt .
RUN apk add --update bash && rm -rf /var/cache/apk/* && pip install --no-cache-dir -r requirements.txt && mkdir -p /opt/lc

WORKDIR /opt/lc

COPY philips_hue_hooks /opt/lc/philips_hue_hooks
COPY hook.sh /opt/lc

ENTRYPOINT ["/opt/lc/hook.sh"]