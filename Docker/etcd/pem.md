### 1. 根证书 (CA 证书)
根证书是整个证书信任链的起点。它是一个自签名的证书,由密钥对的私钥签名。根证书包含了证书元数据和公钥,用于验证由它签发的其他证书。
```bash
# 生成根证书私钥
openssl genrsa -out ca-key.pem 2048

# 生成根证书
openssl req -x509 -new -nodes -key ca-key.pem -subj "/CN=etcd-ca" -days 3650 -out ca.pem
```
### 2. 服务器证书
服务器证书用于etcd节点的HTTPS服务,客户端需要验证这个证书。
```bash
# 为每个节点生成私钥 
openssl genrsa -out etcd1-key.pem 2048 //-----BEGIN PRIVATE KEY-----

# 创建证书签名请求(CSR)
openssl req -new -key etcd1-key.pem -subj "/CN=etcd1" -out etcd1.csr //-----BEGIN CERTIFICATE REQUEST-----

# 使用根证书签发服务器证书
openssl x509 -req -in etcd1.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out etcd1.pem -days 3650 //-----BEGIN CERTIFICATE-----
```
服务器证书依赖于:
* 服务器私钥 (etcd1-key.pem)
* 证书签名请求 (etcd1.csr)
* 根证书 (ca.pem)
* 根私钥 (ca-key.pem)

### 3. 对等证书
对等证书用于etcd节点之间的安全通信
```bash
# 生成对等私钥
openssl genrsa -out peer-etcd1-key.pem 2048  

# 创建CSR 
openssl req -new -key peer-etcd1-key.pem -subj "/CN=etcd1" -out peer-etcd1.csr

# 使用根证书签发对等证书
openssl x509 -req -in peer-etcd1.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out peer-etcd1.pem -days 3650
```
对等证书依赖于:
* 对等私钥 (peer-etcd1-key.pem)
* 证书签名请求 (peer-etcd1.csr)
* 根证书 (ca.pem)
* 根私钥 (ca-key.pem)

### 4. 生成文件用途
* ca.pem - 根证书，作为信任锚点
* etcd1.pem - 服务器证书，供客户端验证
* etcd1-key.pem - 服务器私钥，服务器身份验证
* peer-etcd1.pem - 对等证书，etcd节点间通信
* peer-etcd1-key.pem - 对等私钥，etcd节点身份验证

所有的证书和私钥都是由根证书和根私钥签发和产生的。客户端和其他etcd节点需要信任根证书,才能验证服务器证书和对等证书的合法性。

### 5. 客户端如何验证服务端的证书？
客户端要拿到根证书才能完成和etcd的安全tsl通信

没有根证书,客户端将无法验证服务器证书的合法性,从而无法建立安全连接。拥有并信任正确的根证书对于 SSL/TLS 安全通信至关重要。

除了 etcd,任何基于 SSL/TLS 的安全通信都需要类似的证书验证机制。比如访问 HTTPS 网站时,浏览器也需要内置或导入可信的根证书,才能验证网站服务器证书。

### 6. 客户端也需要用根证书生成自己的证书和etcd服务端交互


```go
rootCAs, err := x509.SystemCertPool()
if rootCAs == nil {
    rootCAs = x509.NewCertPool()
}

// 从文件读取根证书
caPEM, err := ioutil.ReadFile("/etc/etcd/ssl/ca.pem") 
if err != nil {
    // 错误处理
}

// 将根证书添加到证书池
ok := rootCAs.AppendCertsFromPEM(caPEM)
if !ok {
    // 根证书解析失败
}



import "go.etcd.io/etcd/clientv3"

tlsConfig := &tls.Config{
    RootCAs: rootCAs, // 根证书集
}

cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"https://etcd1:2379"}, 
    TLS: tlsConfig,
})
if err != nil {
    // 错误处理
}
```