const CACHE_NAME = 'image_converter_cache_v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/jpg-to-png',
  '/jpg-to-png/index.html',
  '/png-to-jpg',
  '/png-to-jpg/index.html',
  '/compress-image',
  '/compress-image/index.html',
  '/favicon.svg',
  '/manifest.json',
  '/assets/css/style.css',
  '/assets/js/app.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
  'https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Try network first, map to cache on failure. (Stale-While-Revalidate pattern or Network First)
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) return cachedResponse;
      
      return fetch(event.request).then(response => {
        // Optionally cache new elements
        return response;
      }).catch(() => {
        // On error (offline), fallback if nothing in cache.
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      }));
    })
  );
});
