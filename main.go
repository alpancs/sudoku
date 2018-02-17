package main

import (
	"net/http"
	"os"

	"github.com/alpancs/sudoku/route"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func main() {
	http.ListenAndServe(":"+getPort(), newRouter())
}

func getPort() string {
	portEnv := os.Getenv("PORT")
	if portEnv == "" {
		return "1024"
	}
	return portEnv
}

func newRouter() http.Handler {
	router := chi.NewRouter()
	if os.Getenv("ENV") != "production" {
		router.Use(middleware.Logger)
	}
	router.Use(middleware.RequestID)
	router.Get("/", route.Home)
	fileServer(router, "/", http.Dir("public"))
	// router.Post("/solve", route.Solve)
	return router
}

func fileServer(router chi.Router, path string, root http.FileSystem) {
	fs := http.StripPrefix(path, http.FileServer(root))
	if path != "/" && path[len(path)-1] != '/' {
		router.Get(path, http.RedirectHandler(path+"/", 301).ServeHTTP)
		path += "/"
	}
	path += "*"
	router.Get(path, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fs.ServeHTTP(w, r)
	}))
}
