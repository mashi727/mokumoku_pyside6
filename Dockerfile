# latest Ubuntu version Ubuntu最新バージョン
FROM ubuntu:latest
# information about maintainer 保守者情報
MAINTAINER mashi

RUN apt-get update
RUN apt-get -y install locales language-pack-ja && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
# 必要そうなものをinstall
RUN apt-get update && apt-get install -y --no-install-recommends wget build-essential libreadline-dev \ 
libncursesw5-dev libssl-dev libsqlite3-dev libgdbm-dev libbz2-dev liblzma-dev zlib1g-dev uuid-dev libffi-dev libdb-dev

#任意バージョンのpython install
ARG PYTHON_VER="3.10.5"
RUN wget --no-check-certificate https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tgz \
&& tar -xf Python-${PYTHON_VER}.tgz \
&& cd Python-${PYTHON_VER} \
&& ./configure --enable-optimizations\
&& make \
&& make install

# TA-libのインストール
# 以下の設定に加えて、requirementsにTa-Libを追記する必要あり
RUN wget --no-check-certificate http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
&& tar -xzf ta-lib-0.4.0-src.tar.gz \
&& cd ta-lib \
&& ./configure --prefix=/usr \
&& make \
&& make install


# 生活環境の構築
# 後半のライブラリは、Pyside6関連
RUN apt-get update && apt-get install -y --fix-missing \
  sudo \
  zsh \
  vim \
  less \
  x11-apps \
  libgl1-mesa-glx \
  libxkbcommon-x11-0 \
  libglib2.0-dev \
  libdbus-1-3 \
  libgl1-mesa-dev \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-render-util0 \
  libxcb-shape0 \
  libpython3.10-dev \
# 日本語周りの設定 \
  language-pack-ja \
  fonts-ipafont \
# fc-cacheなどをインストール \
  fontconfig \
# opengl周り
  libnss3 \
  libxcomposite-dev \
  libxdamage1 \
  libxrandr2 \
  libxtst6 \
  libxi6 \
  libasound2 \
# Video driver
  ubuntu-drivers-common


# hostnameの設定
#RUN hostnamectl set-hostname pyside6_dckr

# ユーザーを作成
# sudoをパスワードなしでできるように
ARG USERNAME=worker
ARG GROUPNAME=worker
ARG UID=1000
ARG GID=1000
ARG PASSWORD=user
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID -G sudo $USERNAME && \
    echo $USERNAME:$PASSWORD | chpasswd && \
    echo "$USERNAME   ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 作成したユーザーに切り替える
USER $USERNAME
WORKDIR /home/$USERNAME/

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
# XQuartsを再起動した場合は、xtermにて xhost + とする必要あり。
# ENV DISPLAY :0
# prepend the new path パスを追加
ENV PATH /home/$USERNAME/.local/bin:$PATH
RUN echo 'alias python="python3"' >> ~/.bashrc
RUN mkdir -p /tmp/runtime-worker
ENV XDG_RUNTIME_DIR /tmp/runtime-worker
RUN chmod 700 /tmp/runtime-worker
ENV LIBGL_ALWAYS_INDIRECT 1

RUN pip3 install --user --upgrade pip
RUN pip3 install --user --upgrade setuptools

COPY opt/requirements.txt /home/$USERNAME/opt/requirements.txt
WORKDIR /home/$USERNAME/opt
RUN pip3 install --user  -r requirements.txt

# docker から起動する場合に使用
# execute IPython when container is run コンテナでIPythonを実行
# WORKDIR /home/$USERNAME
# CMD ["zsh"]
