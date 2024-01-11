## What is Casbin
Casbin is an authorization library that can be used in flows where we want a certain `object` or `entity` to be accessed by a specific `user` or `subject`. 

The type of access, i.e. action, can be `read`, `write`, `delete`, or any other action as set by the developer. This is how Casbin is most widely used, and it's called the "standard" or classic { subject, object, action } flow.

### What Casbin Does
1. Enforce the policy in the classic `{ subject, object, action }` form or a `customized` form as you defined. Both allow and deny authorizations are supported.
2. Handle the storage of the access control model and its policy.(like using adapter to load policy from different places)
3. Manage the role-user mappings and role-role mappings (aka role hierarchy in RBAC).
4. Support built-in superusers like root or administrator. A superuser can do anything without explicit permissions.
5. Provide multiple built-in operators to support rule matching. For example, `keyMatch` can map a resource key `/foo/bar` to the pattern `/foo*`.

### What Casbin Does NOT Do
1. Authentication
2. Manage the list of users or roles.

## New a Casbin enforcer
Casbin uses configuration files to define the access control model. There are two configuration files: 
1. model.conf: stores access model
2. policy.csv: stores the specific user permission configuration
```go
e, err := casbin.NewEnforcer("path/to/model.conf", "path/to/policy.csv")

a, err := xormadapter.NewAdapter("mysql", "mysql_username:mysql_password@tcp(127.0.0.1:3306)/")
m, err := model.NewModelFromString(`
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act
`)
e, err := casbin.NewEnforcer(m, a)
```
### Check permissions
```go
sub := "alice" // the user that wants to access a resource.
obj := "data1" // the resource that is going to be accessed.
act := "read" // the operation that the user performs on the resource.

ok, err := e.Enforce(sub, obj, act)

if err != nil {
    // handle err
}

if ok == true {
    // permit alice to read data1
} else {
    // deny the request, show an error
}

// You could use BatchEnforce() to enforce some requests in batches.
// This method returns a bool slice, and this slice's index corresponds to the row index of the two-dimensional array.
// e.g. results[0] is the result of {"alice", "data1", "read"}
results, err := e.BatchEnforce([][]interface{}{{"alice", "data1", "read"}, {"bob", "data2", "write"}, {"jack", "data3", "read"}})


roles, err := e.GetRolesForUser("alice")
```