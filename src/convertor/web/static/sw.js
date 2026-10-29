// service worker to populate the offline first cache
//
const cacheId = "v1";
const cacheResources = [
  "/",
  "/index.html",
  "/styles.css",
  "/script.js",
  "/upload.svg",
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
