## How It Works
An access control model is abstracted into a CONF file based on the PERM method `(Policy, Effect, Request, Matchers)`. You can customize your own access control model by combining the available models. For example, you can combine RBAC roles and ABAC attributes together inside one model and share one set of policy rules.
### Request
It is query template of the system. Defines the request parameters. A basic request is a tuple object, requiring at least a subject (accessing entity), object (accessed resource), and action (access method). 

For instance, a request definition may look like this: `r={sub,obj,act}`
 


### Policy
It is the assignment template of the system. Defines the model for the access strategy. It specifies the name and order of the fields in the Policy rule document.
For instance: `p={sub, obj, act}` or `p={sub, obj, act, eft}`

alice, write, data1 You are assigning permission to subject Alice to perform the action 'write' on object 'data1'.

Note: If eft (policy result) is not defined, the result field in the policy file will not be read, and the matching policy result will be allowed by default.

### Matcher
Defines the matching rules for Request and Policy.

For example: 
```bash
m = r.sub == p.sub && r.act == p.act && r.obj == p.obj
```
This simple and common matching rule means that if the requested parameters (entities, resources, and methods) are equal to those found in the policy, then the policy result (p.eft) is returned. The result of the strategy will be saved in p.eft

### Effect
This statement means that if the matching strategy result p.eft has the result of (some) allow, then the final result is true
```bash
e = some(where(p.eft == allow))
```

### Conf Example
```conf
# Request definition
[request_definition]
r = sub, obj, act
# [request_definition] section defines the arguments in the e.Enforce(...) function
# For example, you can use sub, act if you don't need to specify a particular resource, or sub, sub2, obj, act if you have two accessing entities.
# r1 = sub, obj, act
# r2 = sub, act

# Policy definition
[policy_definition]
p = sub, obj, act
# Each line in a policy is called a policy rule. Each policy rule starts with a policy type, such as p or p2. It is used to match the policy definition if there are multiple definitions. The above policy shows the following binding. The binding can be used in the matcher.
# p2 = sub, act
# p, alice, data1, read
# p2, bob, write-all-objects
# (alice, data1, read) -> (p.sub, p.obj, p.act)
# (bob, write-all-objects) -> (p2.sub, p2.act)


# Policy effect
[policy_effect]
e = some(where (p.eft == allow))
# if there's any matched policy rule of allow, the final effect is allow
# e = !some(where (p.eft == deny))
# if there are no matched policy rules of deny, the final effect is allow 
# e = some(where (p.eft == allow)) && !some(where (p.eft == deny))
# This means that there must be at least one matched policy rule of allow, and there cannot be any matched policy rule of deny


# Matchers
[matchers]
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act
# define how the policy rules are evaluated against the request.
# The above matcher is the simplest and means that the subject, object, and action in a request should match the ones in a policy rule.
# Arithmetic operators like +, -, *, / and logical operators like &&, ||, ! can be used in matchers.
```
All four sections mentioned above can use multiple types, and the syntax is r followed by a number, such as r2 or e2. By default, these four sections should correspond one-to-one. For example, your r2 section will only use the m2 matcher to match p2 policies.

You can pass an EnforceContext as the first parameter of the enforce method to specify the types. The EnforceContext is defined as follows
```go
EnforceContext{"r2","p2","e2","m2"}
type EnforceContext struct {
    RType string
    PType string
    EType string
    MType string
}

// Pass in a suffix as a parameter to NewEnforceContext, such as 2 or 3, and it will create r2, p2, etc.
enforceContext := NewEnforceContext("2")
// You can also specify a certain type individually
enforceContext.EType = "e"
// Don't pass in EnforceContext; the default is r, p, e, m
e.Enforce("alice", "data2", "read")        // true
// Pass in EnforceContext
e.Enforce(enforceContext, struct{ Age int }{Age: 70}, "/data1", "read")        //false
e.Enforce(enforceContext, struct{ Age int }{Age: 30}, "/data1", "read")   
```


An example policy for the ACL model is:
```bash
p, alice, data1, read
p, bob, data2, write
```
This means:
* alice can read data1
* bob can write data2

Multi-line mode is supported by appending '\' in the end:
```bash
# Matchers
[matchers]
m = r.sub == p.sub && r.obj == p.obj \
  && r.act == p.act
```
Furthermore, if you are using ABAC, you can try the 'in' operator as shown in the following example for the Casbin golang edition 
```bash
# Matchers
[matchers]
m = r.obj == p.obj && r.act == p.act || r.obj in ('data2', 'data3')
# But you SHOULD make sure that the length of the array is MORE than 1, otherwise it will cause a panic.
```