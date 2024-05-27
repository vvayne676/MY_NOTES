#!/bin/bash

# Define common variables
PASSWORD="yourpassword"
DAYS=365

# Create directories for generated files
mkdir -p ca certs etcd1 etcd2 etcd3 client

# Generate CA key and certificate
openssl genpkey -algorithm RSA -out ca/ca.key
openssl req -new -x509 -key ca/ca.key -sha256 -days $DAYS -out ca/ca.crt -subj "/C=US/ST=YourState/L=YourCity/O=YourOrg/OU=YourUnit/CN=etcd-ca" -passout pass:$PASSWORD

# Generate file and certificate for each node
for NODE in etcd1 etcd2 etcd3; do
  IP="192.168.1.10${NODE: -1}"
  mkdir -p $NODE
  # Generate node private key
  openssl genpkey -algorithm RSA -out $NODE/${NODE}.key

  # Create server CSR configuration file
  cat > $NODE/${NODE}.csr.cnf <<EOF
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

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
EOF

  # Generate the server CSR
  openssl req -new -key $NODE/${NODE}.key -out $NODE/${NODE}.csr -config $NODE/${NODE}.csr.cnf

  # Create server certificate configuration file
  cat > $NODE/${NODE}.ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $NODE
DNS.2 = $NODE.local
IP.1  = $IP
EOF

  # Generate the server certificate
  openssl x509 -req -in $NODE/${NODE}.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out $NODE/${NODE}.crt -days $DAYS -sha256 -extfile $NODE/${NODE}.ext.cnf -passin pass:$PASSWORD

done

# Generate client certificate

# Generate client private key
openssl genpkey -algorithm RSA -out client/client.key

# Create client CSR configuration file
cat > client/client.csr.cnf <<EOF
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

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
openssl req -new -key client/client.key -out client/client.csr -config client/client.csr.cnf

# Create client certificate configuration file
cat > client/client.ext.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = etcd-client
EOF

# Generate the client certificate
openssl x509 -req -in client/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out client/client.crt -days $DAYS -sha256 -extfile client/client.ext.cnf -passin pass:$PASSWORD

echo "Certificate generation completed."