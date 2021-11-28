FROM nvidia/cuda:11.4.1-runtime-ubuntu18.04
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV PATH=/root/miniconda3/bin:${PATH}
WORKDIR /root

RUN printf 'deb http://mirrors.163.com/ubuntu/ bionic main restricted\n\
deb http://mirrors.163.com/ubuntu/ bionic-updates main restricted\n\
deb http://mirrors.163.com/ubuntu/ bionic universe\n\
deb http://mirrors.163.com/ubuntu/ bionic-updates universe\n\
deb http://mirrors.163.com/ubuntu/ bionic multiverse\n\
deb http://mirrors.163.com/ubuntu/ bionic-updates multiverse\n\
deb http://mirrors.163.com/ubuntu/ bionic-backports main restricted universe multiverse\n\
deb http://mirrors.163.com/ubuntu/ bionic-security main restricted\n\
deb http://mirrors.163.com/ubuntu/ bionic-security universe\n\
deb http://mirrors.163.com/ubuntu/ bionic-security multiverse'\
> /etc/apt/sources.list

RUN truncate -s0 /tmp/preseed.cfg; \
    echo "tzdata tzdata/Areas select Asia" >> /tmp/preseed.cfg; \
    echo "tzdata tzdata/Zones/Asia select Shanghai" >> /tmp/preseed.cfg; \
    debconf-set-selections /tmp/preseed.cfg && \
    rm -f /etc/timezone /etc/localtime && \
    apt update && \
    apt install libterm-readkey-perl curl  -y && \
    apt-get install -yq tzdata && \
    curl -kLO https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh && \
    chmod +x ./Miniconda3-py39_4.10.3-Linux-x86_64.sh && \
    ./Miniconda3-py39_4.10.3-Linux-x86_64.sh  -bf -p miniconda3 && \
    rm -rf ./Miniconda3-py39_4.10.3-Linux-x86_64.sh /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir -p /etc/conda

RUN printf 'channels:\n\
  - defaults\n\
show_channel_urls: true\n\
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda\n\
default_channels:\n\
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main\n\
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free\n\
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r\n\
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro\n\
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2\n\
custom_channels:\n\
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud'\
> /etc/conda/condarc

RUN printf 'name: base\n\
channels:\n\
  - conda-forge\n\
  - pytorch\n\
dependencies:\n\
  - fastapi\n\
  - python-decouple\n\
  - pyjwt\n\
  - pydantic\n\
  - uvicorn\n\
  - python-multipart\n\
  - aiofiles\n\
  - pytorch\n\
  - torchvision\n\
  - torchaudio\n\
  - cudatoolkit=11.3\n\
  - av\n\
  - pims\n\
  - tqdm\n\
  - celery\n\
  - requests\n\
  - scikit-image'\
 > env.yaml

RUN /root/miniconda3/bin/conda env update -f env.yaml && conda clean -tipsy && \
    ln -s /root/miniconda3/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
