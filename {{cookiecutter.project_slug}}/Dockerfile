# vim:set ft=dockerfile:
FROM continuumio/miniconda3
MAINTAINER https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
LABEL Description="{{ cookiecutter.project_name }} WPS" Vendor="Birdhouse" Version="{{ cookiecutter.version }}"

# Update Debian system
RUN apt-get update && apt-get install -y \
 build-essential \
&& rm -rf /var/lib/apt/lists/*

# Update conda
RUN conda update -n base conda

# Copy WPS project
COPY . /opt/wps

WORKDIR /opt/wps

# Create conda environment
RUN conda env create -n wps -f environment.yml

# Install WPS
RUN ["/bin/bash", "-c", "source activate wps && python setup.py develop"]

# Start WPS service on port {{ cookiecutter.http_port }} on 0.0.0.0
EXPOSE {{ cookiecutter.http_port }}
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["source activate wps && exec emu start -b 0.0.0.0 -config /opt/wps/etc/demo.cfg"]

# docker build -t {{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }} .
# docker run -p {{ cookiecutter.http_port }}:{{ cookiecutter.http_port }} {{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
# http://localhost:{{ cookiecutter.http_port }}/wps?request=GetCapabilities&service=WPS
# http://localhost:{{ cookiecutter.http_port }}/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
