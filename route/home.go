package route

import (
	"html/template"
	"net/http"
)

var Home = newHomeHandler(parseTemplate("view/home.html"))

func parseTemplate(filePath string) *template.Template {
	parsedTemplate, err := template.ParseFiles(filePath)
	if err != nil {
		panic(err)
	}
	return parsedTemplate
}

func newHomeHandler(template *template.Template) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		template.Execute(w, nil)
	}
}
