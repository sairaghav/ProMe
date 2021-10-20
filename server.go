package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

var apiKey string = "RErLEHOyAx6DKiFoJeJv8uDAkLe9LnGR"
var baseUrl string = "http://open.mapquestapi.com"

func getDirections(from string, to string) string {
	fmt.Println(from, to)
	finalUrl := baseUrl + "/directions/v2/route?key=" + apiKey + "&from=" + from + "&to=" + to
	response, _ := http.Get(finalUrl)

	responseData, _ := ioutil.ReadAll(response.Body)
	return string(responseData)
}

func main() {
	port := os.Getenv("PORT")

	if port == "" {
		port = "8000"
	}
	http.HandleFunc("/directions/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, getDirections(strings.Split(r.URL.Path, "/")[2], strings.Split(r.URL.Path, "/")[3]))
	})

	log.Fatal(http.ListenAndServe(":"+port, nil))

}
