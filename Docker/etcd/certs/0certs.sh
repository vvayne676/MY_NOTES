#!/bin/bash
# 生成 CA 私钥
openssl genrsa -out ca.key 2048 

# 生成 CA 根证书
openssl req -x509 -new -nodes -key ca.key -subj "/CN=etcd-ca" -days 3650 -out ca.crt



## etcd 1
### 服务器证书
openssl genrsa -out etcd1.key 2048
openssl req -new -key etcd1.key -subj "/CN=etcd1" -out etcd1.csr
openssl x509 -req -in etcd1.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out etcd1.crt -days 3650 



### 对等证书
openssl genrsa -out peer-etcd1.key 2048  
openssl req -new -key peer-etcd1.key -out peer-etcd1.csr -subj "/C=CN/ST=Beijing/L=PHC/O=Mono Finance/OU=Finance/CN=*.monofinance.net/emailAddress=mrikehchukwuka@gmail.com"
openssl x509 -req -in peer-etcd1.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out peer-etcd1.crt -days 3650

## etcd 2
### 服务器证书
openssl genrsa -out etcd2.key 2048 
openssl req -new -key etcd2.key -subj "/CN=etcd2" -out etcd2.csr 
openssl x509 -req -in etcd2.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out etcd2.crt -days 3650 
### 对等证书
openssl genrsa -out peer-etcd2.key 2048 

openssl req -new -key peer-etcd2.key -subj "/CN=etcd2" -out peer-etcd2.csr

openssl x509 -req -in peer-etcd2.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out peer-etcd2.crt -days 3650

## etcd 3
### 服务器证书
openssl genrsa -out etcd3.key 2048 
openssl req -new -key etcd3.key -subj "/CN=etcd3" -out etcd3.csr 
openssl x509 -req -in etcd3.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out etcd3.crt -days 3650 
### 对等证书
openssl genrsa -out peer-etcd3.key 2048
openssl req -new -key peer-etcd3.key -subj "/CN=etcd3" -out peer-etcd3.csr
openssl x509 -req -in peer-etcd3.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out peer-etcd3.crt -days 3650

## client
openssl genrsa -out client.key 2048 
openssl req -new -key client.key -subj "/CN=client" -out client.csr 
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 3650 


