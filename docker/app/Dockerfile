FROM python:3.12.5-slim-bookworm

COPY ./docker/app/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir build \
    && rm -f /tmp/requirements.txt

COPY myapp /opt/myapp/myapp
COPY pyproject.toml setup.cfg /opt/myapp/
RUN python -m build --wheel --outdir /opt/wheel /opt/myapp > /dev/null \
    && rm -rf /opt/myapp \
    && pip install --no-cache-dir /opt/wheel/*.whl \
    && rm -rf /opt/wheel

ENV PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=0 PYTHONDONTWRITEBYTECODE=1
# Run with least privileges
WORKDIR /home/nobody
COPY ./docker/app/docker-entrypoint.sh /home/nobody/docker-entrypoint.sh
RUN chown nobody /home/nobody/docker-entrypoint.sh
RUN chmod +x /home/nobody/docker-entrypoint.sh

USER nobody

ENTRYPOINT ["/home/nobody/docker-entrypoint.sh"]
