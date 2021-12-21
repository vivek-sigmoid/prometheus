FROM python:latest
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install psutil
RUN pip3 install prometheus_client
ADD usage_info.py .
CMD [ "python", "usage_info.py" ]
EXPOSE 4444