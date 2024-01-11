package auth

import (
	"log"
	"time"

	"github.com/casbin/casbin/v2"
)

var CheckList = [][]any{
	{"alice", "data2", "read"},
	{"bob", "data2", "read"},
	{"smith", "data2", "read"},

	{"alan", "data1", "read"},
}

func AuthCheck() bool {
	e, err := casbin.NewEnforcer("auth/demo.conf", "auth/demo.csv")
	e.EnableLog(true)

	if err != nil {
		log.Println(err)
		return false
	}
	//e.AddNamedMatchingFunc("g", "keyMatch2", util.KeyMatch2)
	name := "max"
	path := "/user/" + name + "/cart"
	action := "GET"
	// path1 := "/user/" + "name" + "/cart"
	timeNow := time.Now()
	results, err := e.BatchEnforce([][]any{
		{"alice", "data2", "read"},
		{"bob", "data2", "read"},
		{"smith", "data2", "read"},
		{name, path, action},
	})
	elapse := time.Since(timeNow)
	log.Println(elapse)
	log.Println(e.GetRolesForUser("smith"))
	log.Println(e.GetUsersForRole("maintainer"))
	e.DeleteRolesForUser("smith")
	log.Println(e.GetRolesForUser("smith"))

	if err != nil {
		log.Println(err)
		return false
	}
	log.Println(results)
	return true
}
