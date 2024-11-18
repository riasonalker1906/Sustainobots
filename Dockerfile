FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /opt

RUN apt update && apt install -y \
  python3-pip \
  wget \
  xvfb \
  git

# Install chrome - versions can be found here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
RUN wget -O chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_125.0.6422.141-1_amd64.deb \
  && apt-get install -y ./chrome.deb \
  && rm chrome.deb
RUN apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

# Run as non-root
RUN useradd -m ubuntu
USER ubuntu
WORKDIR /home/ubuntu

# Install Python dependencies
COPY --chown=ubuntu ./requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

COPY --chown=ubuntu parsagon_profile.json /home/ubuntu/.parsagon_profile

COPY . /home/ubuntu/sustainobots

WORKDIR /home/ubuntu/sustainobots

CMD ["python3", "-m", "celery", "-A", "postgres_db_django", "worker", "--loglevel=info", "--concurrency=1"]