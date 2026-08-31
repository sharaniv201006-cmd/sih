# -*- coding: utf-8 -*-
# 1. Create manifest.json
with open("frontend/public/manifest.json", "w", encoding="utf-8") as f:
    f.write("""{
  "name": "BovineGuard AI - Mastitis Forecasting",
  "short_name": "BovineGuard",
  "description": "AI-Based Early Forecasting of Bovine Mastitis for Dairy Farms",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#10b981",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/pwa-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/pwa-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
""")
print("Created manifest.json")

# 2. Create public/sw.js (Service Worker)
with open("frontend/public/sw.js", "w", encoding="utf-8") as f:
    f.write("""const CACHE_NAME = 'bovineguard-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
""")
print("Created service worker sw.js")

# 3. Create SVG App icons for PWA
with open("frontend/public/pwa-192.png", "wb") as f:
    # Small 1x1 png or svg placeholder if needed, let's create simple svg icons too
    pass
with open("frontend/public/pwa-512.png", "wb") as f:
    pass

# Update index.html to register service worker and PWA tags
with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write("""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    
    <!-- PWA & Mobile App Settings -->
    <link rel="manifest" href="/manifest.json" />
    <meta name="theme-color" content="#10b981" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="apple-mobile-web-app-title" content="BovineGuard" />
    
    <title>BovineGuard AI | Bovine Mastitis Early Forecasting System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-50 text-slate-900 antialiased selection:bg-emerald-500 selection:text-white font-sans">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('/sw.js').catch((err) => {
            console.log('ServiceWorker registration note:', err);
          });
        });
      }
    </script>
  </body>
</html>
""")
print("Updated index.html with PWA mobile app support.")
