FROM python:3.10-bullseye

WORKDIR /src

# Copy code to container
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "/src/proxy.py" ]