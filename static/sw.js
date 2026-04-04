const CACHE_NAME = "community-app-v1";
const urlsToCache = [
  "/",
  "/jobs",
  "/post",
  "/static/style.css"
];

self.addEventListener("install", function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("fetch", function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});