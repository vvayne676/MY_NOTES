#!/bin/bash

# Define common variables
PASSWORD="wocao"
DAYS=365



# Generate CA key and certificate
openssl genpkey -algorithm RSA -out ./ca.key
openssl req -new -x509 -key ./ca.key -sha256 -days $DAYS -out ./ca.crt -subj "/C=US/ST=YourState/L=YourCity/O=YourOrg/OU=YourUnit/CN=etcd-ca" -passout pass:$PASSWORD

# Generate file and certificate for each node
for NODE in etcd1 etcd2 etcd3; do
  IP="192.168.1.10${NODE: -1}"
  # Generate node private key
  openssl genpkey -algorithm RSA -out ./${NODE}.key

  # Create server CSR configuration file
  cat > ./${NODE}.csr.cnf <<EOF
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no
default_md = sha256

[ req_distinguished_name ]
C  = US
ST = YourState
L  = YourCity
O  = YourOrg
OU = YourUnit
CN = $NODE

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = $NODE
DNS.2 = $NODE.local
IP.1  = $IP
IP.2  = 127.0.0.1
EOF

  # Generate the server CSR
  openssl req -new -key ./${NODE}.key -out ./${NODE}.csr -config ./${NODE}.csr.cnf

  # Create server certificate configuration file
  cat > ./${NODE}.ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth,clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $NODE
DNS.2 = $NODE.local
IP.1  = $IP
IP.2  = 127.0.0.1
EOF

  # Generate the server certificate
  openssl x509 -req -in ./${NODE}.csr -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -out ./${NODE}.crt -days $DAYS -sha256 -extfile ./${NODE}.ext.cnf -passin pass:$PASSWORD

done

# Generate client certificate

# Generate client private key
openssl genpkey -algorithm RSA -out ./client.key

# Create client CSR configuration file
cat > ./client.csr.cnf <<EOF
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no
default_md = sha256

[ req_distinguished_name ]
C  = US
ST = YourState
L  = YourCity
O  = YourOrg
OU = YourUnit
CN = etcd-client

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = etcd-client
EOF

# Generate the client CSR
openssl req -new -key ./client.key -out ./client.csr -config ./client.csr.cnf

# Create client certificate configuration file
cat > ./client.ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = etcd-client
EOF

# Generate the client certificate
openssl x509 -req -in ./client.csr -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -out ./client.crt -days $DAYS -sha256 -extfile ./client.ext.cnf -passin pass:$PASSWORD

echo "Certificate generation completed."

curl -vL --cacert ca.crt --cert client.crt --key client.key https://etcd1:2379/v3/kv/put -XPOST -d '{"key":"d2k=","value":"aGVsbG8="}'


curl -vL --cacert ca.crt --cert client.crt --key client.key https://etcd2:2379/v3/kv/range -XPOST -d '{"key":"d2k="}'



