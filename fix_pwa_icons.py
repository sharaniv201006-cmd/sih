# -*- coding: utf-8 -*-
# 1. Create a clean Network-First service worker that never blocks Vite assets
with open("frontend/public/sw.js", "w", encoding="utf-8") as f:
    f.write("""// BovineGuard AI Service Worker - Network First
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
""")

# 2. Create valid PNG icons for pwa-192 and pwa-512 using Python
import zlib, struct

def make_png(width, height, r, g, b):
    # Generates a valid minimal uncompressed PNG
    def png_chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = png_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    raw_data = b''.join(b'\x00' + bytes([r, g, b] * width) for _ in range(height))
    idat = png_chunk(b'IDAT', zlib.compress(raw_data, 9))
    iend = png_chunk(b'IEND', b'')
    return header + ihdr + idat + iend

# Emerald green color (16, 185, 129)
png_192 = make_png(192, 192, 16, 185, 129)
png_512 = make_png(512, 512, 16, 185, 129)

with open("frontend/public/pwa-192.png", "wb") as f:
    f.write(png_192)

with open("frontend/public/pwa-512.png", "wb") as f:
    f.write(png_512)

print("Created valid PNG icons and robust network-first service worker.")
