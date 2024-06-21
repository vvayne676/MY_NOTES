```shell
ssh -Q cipher // encryption
3des-cbc
aes128-cbc
aes192-cbc
aes256-cbc
aes128-ctr
aes192-ctr
aes256-ctr
aes128-gcm@openssh.com
aes256-gcm@openssh.com
chacha20-poly1305@openssh.com

ssh -Q kex // key exchange
diffie-hellman-group1-sha1
diffie-hellman-group14-sha1
diffie-hellman-group14-sha256
diffie-hellman-group16-sha512
diffie-hellman-group18-sha512
diffie-hellman-group-exchange-sha1
diffie-hellman-group-exchange-sha256
ecdh-sha2-nistp256
ecdh-sha2-nistp384
ecdh-sha2-nistp521
curve25519-sha256
curve25519-sha256@libssh.org
sntrup761x25519-sha512@openssh.com


ssh -Q mac // message authentication code
hmac-sha1
hmac-sha1-96
hmac-sha2-256
hmac-sha2-512
hmac-md5
hmac-md5-96
umac-64@openssh.com
umac-128@openssh.com
hmac-sha1-etm@openssh.com
hmac-sha1-96-etm@openssh.com
hmac-sha2-256-etm@openssh.com
hmac-sha2-512-etm@openssh.com
hmac-md5-etm@openssh.com
hmac-md5-96-etm@openssh.com
umac-64-etm@openssh.com
umac-128-etm@openssh.com

ssh -Q key // HostKeyAlgorithms
// 当你尝试连接到 SSH 服务器时 服务器会提供他的公钥
// 客户端使用 HostKeyAlgorithms 中支持的算法来验证这个公钥
// 从而保证你连接的是争取的服务器, 而不是中间人攻击中的伪造服务器
ssh-ed25519
ssh-ed25519-cert-v01@openssh.com
sk-ssh-ed25519@openssh.com
sk-ssh-ed25519-cert-v01@openssh.com
ecdsa-sha2-nistp256
ecdsa-sha2-nistp256-cert-v01@openssh.com
ecdsa-sha2-nistp384
ecdsa-sha2-nistp384-cert-v01@openssh.com
ecdsa-sha2-nistp521
ecdsa-sha2-nistp521-cert-v01@openssh.com
sk-ecdsa-sha2-nistp256@openssh.com
sk-ecdsa-sha2-nistp256-cert-v01@openssh.com
ssh-dss
ssh-dss-cert-v01@openssh.com
ssh-rsa
ssh-rsa-cert-v01@openssh.com

ssh -Q key-plain // PubkeyAcceptedAlgorithms
ssh-ed25519
sk-ssh-ed25519@openssh.com
ecdsa-sha2-nistp256
ecdsa-sha2-nistp384
ecdsa-sha2-nistp521
sk-ecdsa-sha2-nistp256@openssh.com
ssh-dss
ssh-rsa

```


```shell
ssh -vvv -o KexAlgorithms=diffie-hellman-group-exchange-sha256 \
    -o Ciphers=aes256-ctr \
    -o MACs=hmac-sha2-256 \
    -o PubkeyAcceptedAlgorithms=+rsa-sha2-256 \
    -o HostKeyAlgorithms=+ssh-rsa \
    -i ~/.ssh/id_rsa GCNB0433@h2h-uat.sc.com -p 4022
```

```shell
Host sc
    HostName xxx.com
    Port 4022
    User username
    IdentityFile ~/.ssh/sc_given
    LogLevel DEBUG3
    KexAlgorithms +diffie-hellman-group-exchange-sha256,curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group14-sha256,diffie-hellman-group14-sha1
    Ciphers +aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr
    MACs +hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1,hmac-sha1-96
    HostKeyAlgorithms +ssh-rsa,ssh-ed25519
    PubkeyAcceptedAlgorithms +ssh-rsa,rsa-sha2-256
```

```go
// golang implementation
	config := &ssh.ClientConfig{
		User: credentials.KV["sftp_username"],
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(signer),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), //
		// HostKeyCallback: ssh.FixedHostKey(hostKey),
		HostKeyAlgorithms: []string{
			"rsa-sha2-256",
		},
		Config: ssh.Config{
			Ciphers: []string{
				"aes256-ctr",
			},
			KeyExchanges: []string{
				"diffie-hellman-group-exchange-sha256",
			},
			MACs: []string{
				"hmac-sha2-256",
			},
		},
	}
```  





 