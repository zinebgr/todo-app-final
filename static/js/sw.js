// sw.js - Service Worker لتطبيق TaskMaster PWA

const CACHE_NAME = 'taskmaster-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/icons/icon-72x72.png',
  '/static/icons/icon-96x96.png',
  '/static/icons/icon-128x128.png',
  '/static/icons/icon-144x144.png',
  '/static/icons/icon-152x152.png',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-256x256.png',
  '/static/icons/icon-384x384.png',
  '/static/icons/icon-512x512.png'
];

// تثبيت Service Worker وتخزين الملفات الأساسية في cache
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching app files');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.error('[Service Worker] Cache failed:', err))
  );
  self.skipWaiting(); // يجعل الـ SW يبدأ العمل فوراً
});

// جلب الملفات: من cache إن وُجدت، وإلا من الشبكة
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request)
          .then(response => {
            // لا نقوم بتخزين كل شيء تلقائياً (يمكن تفعيله لاحقاً)
            return response;
          });
      })
      .catch(() => {
        // يمكن عرض صفحة offline مخصصة هنا إن احتجت
        return caches.match('/');
      })
  );
});

// تفعيل Service Worker وحذف الـ caches القديمة
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  event.waitUntil(clients.claim()); // يسيطر على الصفحات المفتوحة فوراً
});