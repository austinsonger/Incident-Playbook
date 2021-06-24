/**
 * Regex used to get the level from the notification title.
 * @type {RegExp}
 */
var LEVEL_REGEX = /^(.*):/;

/**
 * Regex that gets the alert id from the notification tag.
 * @type {RegExp}
 */
var ALERT_ID_REGEX = /^cyphon-alert-(\d+)/;

/**
 * Regex that
 * @type {RegExp}
 */
var ALERT_PAGE_REGEX = /^\/app\/alerts/;

/**
 * Icons to display based on alert level.
 * @type {Object<string, string>}
 */
var ICONS = {
  CRITICAL: '/static/img/cyphon-push-notification-critical.png',
  HIGH: '/static/img/cyphon-push-notification-high.png',
  MEDIUM: '/static/img/cyphon-push-notification-medium.png',
  LOW: '/static/img/cyphon-push-notification-low.png',
  INFO: '/static/img/cyphon-push-notification-info.png',
};

/**
 * @typedef {Object} AlertNotification
 * @property {string} title Alert level and source.
 * @property {string} message Alert title.
 * @property {string} tag ID of this alert notification. Formatted as
 *   cyphon-alert-{alertId}.
 * @property {string} icon Icon related to the alert. This has become
 *   deprecated.
 */

/**
 * Get the urls of the icons.
 * @returns {Array.<string>}
 */
function getIconUrls() {
  var levels = Object.keys(ICONS);

  return levels.map(function(level) {
    return ICONS[level];
  });
}



/**
 * Gets the notification icon to display based on the alert level in the
 * notification title.
 * @param {string} title Title of the notification.
 * @returns {string} URL of the icon image or an empty string if there is
 *   no icon that matches the alter level.
 */
function getNotificationIcon(title) {
  var level = LEVEL_REGEX.exec(title)[1];

  return ICONS[level] || '';
}

/**
 * Gets the alert id from the notification tag.
 * @param noticationTag
 */
function getAlertId(noticationTag) {
  return ALERT_ID_REGEX.exec(noticationTag)[1];
}

/**
 * Shows a chrome push notification.
 * @param {string} data.title Title of the notification.
 * @param {string} data.body Message of the notification.
 * @param {string} data.tag Unique identifier of the notification.
 * @returns {Promise}
 */
function showNotification(data) {
  return self.registration.showNotification(data.title, {
    body: data.body,
    tag: data.tag,
    icon: getNotificationIcon(data.title),
  });
}

/**
 * Creates a custom object that stores a promise and it's resolve/reject
 * functions on the same scope.
 * @return {Deferred}
 */
function defer() {
  var deferred = {};

  deferred.promise = new Promise(function(resolve, reject) {
    deferred.resolve = resolve;
    deferred.reject = reject;
  });

  return deferred;
}

// --------------------------------------------------------------------------
// Service Worker Database
// --------------------------------------------------------------------------

// Database constants
var CACHE_NAME = 'cyphon-cache-v1';
var DB_NAME = 'cyphonPushNotifications';
var DB_VERSION = 1;
var OBJECT_STORE_NAME = DB_NAME;
var OBJECT_STORE_KEY_PATH = 'owner';
var DEFAULT_KEY_VALUE = 'self';
var NOTIFICATION_URL_KEY = 'notificationUrl';

// Globals for database operations
var db;
var openDBPromise;

/**
 * Creates a database schema on the given database object.
 * @param {IDBDatabase} db
 *     https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase
 */
function createDatabase(db) {
  var objectStore = db.createObjectStore(OBJECT_STORE_NAME, {
    keyPath: OBJECT_STORE_KEY_PATH
  });

  objectStore.createIndex(NOTIFICATION_URL_KEY, NOTIFICATION_URL_KEY, {
    unique: true
  });
}

/**
 * Returns the database that holds the notification url needed for getting
 * notification data. If there are any errors opening the database, it
 * returns the event data associated with the error.
 * @return {Promise.<IDBDatabase || Event>}
 *     https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase
 */
function getDB() {
  var deferred = defer();
  var request;

  // If database has already been opened, return resolved promise.
  if (openDBPromise) {
    return openDBPromise;
  }

  // If database has not been opened, set the promise to the current
  // deferred object's promise so that any subsequent calls do not try
  // to open the database again.
  openDBPromise = deferred.promise;
  request = indexedDB.open(DB_NAME, DB_VERSION);

  request.onerror = function(event) {
    // console.error('Opening DB ERROR', event.target.errorCode);
    deferred.reject(event);
  };

  request.onsuccess = function(event) {
    db = this.result;
    deferred.resolve(db);
  };

  request.onupgradeneeded = function(event) {
    createDatabase(event.currentTarget.result);
  };

  return deferred.promise;
}

/**
 * Returns the object store holding the notification URL.
 * @param {String} method The transaction method to use.
 * @return {Promise.<IDBObjectStore>}
 *     https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore
 */
function getObjectStore(method) {
  return getDB().then(function(db) {
    return db.transaction([OBJECT_STORE_NAME], method)
      .objectStore(OBJECT_STORE_NAME);
  });
}

/**
 * Returns the stored notification object if there is one. If not, then it
 * returns undefined.
 * @return {Promise.<NotificationObject>}
 */
function getNotificationObject() {
  var deferred = defer();

  getObjectStore('readonly').then(function(objectStore) {
    var request = objectStore.get(DEFAULT_KEY_VALUE);

    request.onerror = function() {
      if (this.error.name === 'DataError') { deferred.resolve(); }
      else { deferred.reject(this.error); }
    };

    request.onsuccess = function() {
      deferred.resolve(this.result);
    };
  });

  return deferred.promise;
}


/**
 * Returns the current notification url if there is one. If not, then it
 * returns undefined.
 * @return {Promise.<String>}
 */
function getNotificationUrl() {
  return getNotificationObject().then(function(object) {
    if (!object) { return; }
    return object[NOTIFICATION_URL_KEY];
  });
}

/**
 * Returns the notification information.
 * @returns {Promise.<AlertNotification>}
 */
function getNotificationData() {
  return getNotificationUrl()
    .then(function(url) {
      return fetch(url);
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Response status: ' + response.status);
      }

      return response.json();
    });
}

/**
 * Creates a notification object from the given url.
 * @param {String} url The notificaiton url to use.
 * @return {NotificationObject}
 */
function createNotificationObject(url) {
  var object = {};

  object[OBJECT_STORE_KEY_PATH] = DEFAULT_KEY_VALUE;
  object[NOTIFICATION_URL_KEY] = url;

  return object;
}

/**
 * Updates the url of a notification object.
 * @param {String} url The new notification url to use.
 * @param {NotificationObject} object The notification object to update.
 */
function updateNotificationObject(url, object) {
  object[NOTIFICATION_URL_KEY] = url;
}

/**
 * Adds a notification object with the given notification url.
 * @param {String} url The url to use as the notification url.
 * @return {Promise.<undefined>}
 */
function addNotificationUrl(url) {
  var deferred = defer();

  getObjectStore('readwrite').then(function(objectStore) {
    var notificationObject = createNotificationObject(url);
    var request = objectStore.add(notificationObject);

    request.onsuccess = function() {
      deferred.resolve(this.result);
    };

    request.onerror = function() {
      deferred.reject(this.error);
    };
  });

  return deferred.promise;
}

/**
 * Updates an existing notification object with a new notification url.
 * @param {String} url The new url to use.
 * @param {NotificationObject} object The notification object to update.
 * @return {Promise.<undefined>}
 */
function updateNotificationUrl(url, object) {
  var deferred = defer();

  getObjectStore('readwrite').then(function(objectStore) {
    var request;

    updateNotificationObject(url, object);
    request = objectStore.put(object);

    request.onsuccess = function() {
      deferred.resolve(this.result);
    };

    request.onerror = function() {
      deferred.reject(this.error);
    };
  });

  return deferred.promise;
}

/**
 * Saves the given notification url to the database.
 * @param {String} url
 * @return {Promise.<undefined>}
 */
function saveNotificationUrl(url) {
  return getNotificationObject().then(function(object) {
    if (!object) { return addNotificationUrl(url); }
    else { return updateNotificationUrl(url, object); }
  });
}


// --------------------------------------------------------------------------
// Listeners
// --------------------------------------------------------------------------

/**
 * Service worker install step.
 */
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('cyphon-icon-urls').then(function(cache) {
      return cache.addAll(getIconUrls()).then(function() {
      });
    })
  );
});

/**
 * Service worker push notification received.
 */
self.addEventListener('push', function(event) {
  event.waitUntil(
    getNotificationData().then(function(json) {

      return showNotification({
        title: json.title,
        body: json.message,
        tag: json.tag,
      });
    }).catch(function(error) {
      // console.error(error);
    })
  );
});

self.addEventListener('message', function(event) {
  saveNotificationUrl(event.data.notificationUrl);
});

self.addEventListener('notificationclick', function(event) {
  var alertId = getAlertId(event.notification.tag);
  var url = '/app/alerts/' + alertId + '/';

  event.notification.close();

  event.waitUntil(clients.openWindow(url));
});







