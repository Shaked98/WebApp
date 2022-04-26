#
# FROM node:16-alpine
#
# WORKDIR /app
#
# COPY package.json package-lock.json ./
#
# RUN npm ci
#
# COPY . ./
#
# RUN npm run build && npm prune --production
#
# ENTRYPOINT ["node", "start"]



#FROM python:3.11.0a7-alpine3.15 #  Error: Please make sure the libxml2 and libxslt development packages are installed.
FROM python:alpine

COPY . .

#RUN apk add --no-cache --virtual .build-deps build-base
#RUN apk add --no-cache openldap-dev libxml2-dev libxslt-dev
#RUN pip install --no-cache-dir lxml python-ldap
# RUN apk del .build-deps 

#RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2 py-lxml

# RUN apk add --update --no-cache g++ gcc libxslt-dev
# RUN pip install lxml

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

#ENTRYPOINT [ "python" ]

CMD ["python3", "-u", "main.py"]
