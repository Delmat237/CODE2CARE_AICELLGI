// Service Worker for offline functionality
const CACHE_NAME = 'dgh-feedback-v1';
const STATIC_CACHE = 'dgh-static-v1';

// Files to cache for offline use
const STATIC_FILES = [
  '/',
  '/feedback',
  '/manifest.json',
  // Add other static assets as needed
];

// Install event - cache static files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(STATIC_FILES))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => cacheName !== CACHE_NAME && cacheName !== STATIC_CACHE)
            .map((cacheName) => caches.delete(cacheName))
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Handle API requests
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache successful API responses
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(event.request, responseClone));
          }
          return response;
        })
        .catch(() => {
          // Return cached response if available
          return caches.match(event.request);
        })
    );
    return;
  }

  // Handle static files
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request)
          .then((response) => {
            // Cache new responses
            if (response.ok) {
              const responseClone = response.clone();
              caches.open(STATIC_CACHE)
                .then((cache) => cache.put(event.request, responseClone));
            }
            return response;
          });
      })
      .catch(() => {
        // Return offline page for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      })
  );
});

// Background sync for offline submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'feedback-sync') {
    event.waitUntil(syncFeedback());
  }
});

async function syncFeedback() {
  try {
    // This would sync with your offline storage
    console.log('Syncing offline feedback submissions...');
    
    // Send message to client to trigger sync
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({ type: 'SYNC_FEEDBACK' });
    });
  } catch (error) {
    console.error('Sync failed:', error);
  }
}