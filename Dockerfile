FROM python:2.7.15-alpine
LABEL maintainer="Ulord-platform HTTP Client Library Docker Maintainers <caolinan@ulord.net>"

ENV SDK_DIR "/home/py-ulord-sdk"
COPY . SDK_DIR
RUN cd $SDK_DIR \
  && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
  && python setup.py install
EXPOSE 5000
CMD ["ulordapi", "daemon"]

