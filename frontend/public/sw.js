// BovineGuard AI Service Worker - Network First
const CACHE_NAME = 'bovineguard-v2';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      );
    })
  );
  return self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // Let network handle all API and assets directly
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
