self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('voicebill-v1').then(cache => {
            return cache.addAll([
                '/login',
                '/static/css/style.css',
                '/static/js/app.js'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
