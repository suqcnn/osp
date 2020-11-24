ARG BASEIMAGE=openspacee/ospserver-base:latest
FROM $BASEIMAGE

COPY ospserver /
COPY entrypoint.sh /

CMD ["bash", "-c", "sh /entrypoint.sh"]
