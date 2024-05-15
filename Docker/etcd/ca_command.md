1.

# 生成 CA 私钥
openssl genrsa -out ca-key.pem 2048 -> ca-key.pem

# 生成 CA 根证书
openssl req -x509 -new -nodes -key ca-key.pem -subj "/CN=etcd-ca" -days 3650 -out ca.pem -> ca.pem

only leave it for demo on how to use var in command
```bash
export HOST=etcd-server-1
ssh-keygen -m PEM -f server-${HOST}.key -N '' -m PEM
```

## etcd 1
### 服务器证书
1. openssl genrsa -out etcd1-key.pem 2048 (生成一个新的 2048 位 RSA 私钥。生成的私钥将被保存到 etcd1-key.pem)\
2. openssl req -new -key etcd1-key.pem -subj "/CN=etcd1" -out etcd1.csr (OpenSSL 创建一个新的证书签名请求（CSR）。它使用之前生成的私钥 etcd1-key.pem，并且设置了主题（subject）为 /CN=etcd1，其中 CN 代表通用名称（Common Name），这通常是服务器的全域名。生成的 CSR 将被保存到 etcd1.csr 文件中。)\
3. openssl x509 -req -in etcd1.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out etcd1.pem -days 3650 ( OpenSSL 将 CSR 签名为一个新的证书)



### 对等证书
1. openssl genrsa -out peer-etcd1-key.pem 2048  
2. openssl req -new -key peer-etcd1-key.pem -subj "/CN=etcd1" -out peer-etcd1.csr
3. openssl x509 -req -in peer-etcd1.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out peer-etcd1.pem -days 3650

## etcd 2
### 服务器证书
1. openssl genrsa -out etcd2-key.pem 2048 
2. openssl req -new -key etcd2-key.pem -subj "/CN=etcd2" -out etcd2.csr 
3. openssl x509 -req -in etcd2.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out etcd2.pem -days 3650 
### 对等证书
openssl genrsa -out peer-etcd2-key.pem 2048 -> peer-etcd2-key.pem

openssl req -new -key peer-etcd2-key.pem -subj "/CN=etcd2" -out peer-etcd2.csr -> peer-etcd2.csr

openssl x509 -req -in peer-etcd2.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out peer-etcd2.pem -days 3650 -> peer-etcd2.pem

## etcd 3
### 服务器证书
1. openssl genrsa -out etcd3-key.pem 2048 
2. openssl req -new -key etcd3-key.pem -subj "/CN=etcd3" -out etcd3.csr 
3. openssl x509 -req -in etcd3.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out etcd3.pem -days 3650 
### 对等证书
openssl genrsa -out peer-etcd3-key.pem 2048

openssl req -new -key peer-etcd3-key.pem -subj "/CN=etcd3" -out peer-etcd3.csr

openssl x509 -req -in peer-etcd3.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out peer-etcd3.pem -days 3650

## instructions
* ca.pem - 根 CA 证书，对应 ETCD_PEER_TRUSTED_CA_FILE
* etcd1.pem、etcd2.pem、etcd3.pem - 服务器证书，对应每个节点的 ETCD_CERT_FILE
* etcd1-key.pem、etcd2-key.pem、etcd3-key.pem - 服务器私钥，对应每个节点的 ETCD_KEY_FILE
* peer-etcd1.pem、peer-etcd2.pem、peer-etcd3.pem - 对等证书，对应每个节点的 ETCD_PEER_CERT_FILE
* peer-etcd1-key.pem、peer-etcd2-key.pem、peer-etcd3-key.pem - 对等私钥，对应每个节点的 ETCD_PEER_KEY_FILE