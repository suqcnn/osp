FROM alyf/python-redis:3.7-6.0.5
ADD . /app
RUN pip install -r /app/requirements
WORKDIR /app
CMD ["bash", "-c", "sh bin/entrypoint.sh"]
