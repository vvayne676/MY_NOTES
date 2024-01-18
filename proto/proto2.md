### protoc 2


brew install protobuf
brew install protoc-gen-go


1. go install github.com/envoyproxy/protoc-gen-validate@latest
2. need manually add "validate.proto" to your workspace (i put it under protos folder)
3. in server.proto 
import "protos/validate.proto";
4. protoc -I .  --go_out="." --validate_out="lang=go:." protos/server.proto  
