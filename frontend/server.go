package main

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

var mainJs []byte

func serveFile(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/static/js/main.js" {
		_, _ = w.Write(mainJs)
		return
	}
	http.ServeFile(w, r, "files/"+r.URL.Path)
}

func renderMainJs() {
	f, err := os.Open("files/static/js/main.js")
	if err != nil {
		log.Fatal("could not open main.js")
	}
	bs, err := ioutil.ReadAll(f)
	if err != nil {
		log.Fatal("could not read main.js")
	}
	target := os.Getenv("API_TARGET")
	if target == "" {
		target = "http://localhost:8081"
	}
	s := string(bs)
	mainJs = []byte(strings.ReplaceAll(s, "${API_TARGET}", target))
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	renderMainJs()
	http.HandleFunc("/", serveFile)
	log.Fatal(http.ListenAndServe(":"+port, http.DefaultServeMux))
}
