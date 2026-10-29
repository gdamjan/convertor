// service worker to populate the offline first cache
//
// paths are relative to the service worker, so it works under a sub-path like GitHub Pages
const cacheId = "v1";
const cacheResources = [
  "./",
  "index.html",
  "styles.css",
  "script.js",
  "worker.js",
  "upload.svg",
];

async function addResourcesToCache(resources, cacheId) {
  const cache = await self.caches.open(cacheId);
  await cache.addAll(resources);
}

self.addEventListener("install", (event) => {
  event.waitUntil(addResourcesToCache(cacheResources, cacheId));
});

// On version update, remove old cached files
self.addEventListener("activate", function (event) {
  // Do something when the service worker is activated
  event.waitUntil(self.clients.claim());
});

console.log("serviceWorker" in navigator);
