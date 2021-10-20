package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
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
	http.HandleFunc("/directions/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, getDirections(strings.Split(r.URL.Path, "/")[2], strings.Split(r.URL.Path, "/")[3]))
	})

	log.Fatal(http.ListenAndServe(":0", nil))

}
