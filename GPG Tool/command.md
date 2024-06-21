```shell
# installation
brew install gnupg
# generate key
gpg --full-generate-key

# import existing key
gpg --import filename

# list pub keys
gpg --list-keys
# read pub key
gpg --list-key keyId
# delete pub key
gpg --delete-key keyId

# list private keys
gpg --list-secret-keys
# read private key
gpg --list-secret-key keyId
# delete private key
gpg --delete-secret-keys keyId


# export private key
gpg --armor --export-secret-keys keyId > priwoqu.asc
# export pub key
gpg --armor --export keyId > pubwoqu.asc
```