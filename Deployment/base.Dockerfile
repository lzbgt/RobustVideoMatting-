FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

ENV TZ=Asia/Shanghai

RUN mkdir -p /etc/conda && printf 'channels:\n\
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
  - python=3.9\n\
  - python-decouple\n\
  - pyjwt\n\
  - pydantic\n\
  - fastapi\n\
  - uvicorn\n\
  - python-multipart\n\
  - aiofiles\n\
  - av\n\
  - pims\n\
  - tqdm\n\
  - celery\n\
  - requests\n\
  - scikit-image'\
 > env.yaml

RUN conda env update --file env.yaml && conda clean -tipsy

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
#CMD [ "/bin/bash" ]