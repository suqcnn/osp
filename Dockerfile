ARG BASEIMAGE=openspacee/ospserver-base:latest
FROM $BASEIMAGE

COPY entrypoint.sh /
COPY ospserver /

CMD ["bash", "-c", "sh /entrypoint.sh"]
