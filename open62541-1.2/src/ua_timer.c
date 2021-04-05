/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. 
 *
 *    Copyright 2017, 2018 (c) Fraunhofer IOSB (Author: Julius Pfrommer)
 *    Copyright 2017 (c) Stefan Profanter, fortiss GmbH
 */

#include "ua_util_internal.h"
#include "ua_timer.h"

/* There may be several entries with the same nextTime in the tree. We give them
 * an absolute order by considering the memory address to break ties. Because of
 * this, the nextTime property cannot be used to lookup specific entries. */
static enum ZIP_CMP
cmpDateTime(const UA_DateTime *a, const UA_DateTime *b) {
    if(*a < *b)
        return ZIP_CMP_LESS;
    if(*a > *b)
        return ZIP_CMP_MORE;
    if(a == b)
        return ZIP_CMP_EQ;
    if(a < b)
        return ZIP_CMP_LESS;
    return ZIP_CMP_MORE;
}

ZIP_PROTOTYPE(UA_TimerZip, UA_TimerEntry, UA_DateTime)
ZIP_IMPL(UA_TimerZip, UA_TimerEntry, zipfields, UA_DateTime, nextTime, cmpDateTime)

/* The identifiers of entries are unique */
static enum ZIP_CMP
cmpId(const UA_UInt64 *a, const UA_UInt64 *b) {
    if(*a < *b)
        return ZIP_CMP_LESS;
    if(*a == *b)
        return ZIP_CMP_EQ;
    return ZIP_CMP_MORE;
}

ZIP_PROTOTYPE(UA_TimerIdZip, UA_TimerEntry, UA_UInt64)
ZIP_IMPL(UA_TimerIdZip, UA_TimerEntry, idZipfields, UA_UInt64, id, cmpId)

void
UA_Timer_init(UA_Timer *t) {
    memset(t, 0, sizeof(UA_Timer));
    UA_LOCK_INIT(t->timerMutex)
}

void
UA_Timer_addTimerEntry(UA_Timer *t, UA_TimerEntry *te, UA_UInt64 *callbackId) {
    UA_LOCK(t->timerMutex);
    te->id = ++t->idCounter;
    if(callbackId)
        *callbackId = te->id;
    ZIP_INSERT(UA_TimerZip, &t->root, te, ZIP_FFS32(UA_UInt32_random()));
    ZIP_INSERT(UA_TimerIdZip, &t->idRoot, te, ZIP_RANK(te, zipfields));
    UA_UNLOCK(t->timerMutex);
}

static UA_StatusCode
addCallback(UA_Timer *t, UA_ApplicationCallback callback, void *application, void *data,
            UA_DateTime nextTime, UA_UInt64 interval, UA_UInt64 *callbackId) {
    /* A callback method needs to be present */
    if(!callback)
        return UA_STATUSCODE_BADINTERNALERROR;

    /* Allocate the repeated callback structure */
    UA_TimerEntry *te = (UA_TimerEntry*)UA_malloc(sizeof(UA_TimerEntry));
    if(!te)
        return UA_STATUSCODE_BADOUTOFMEMORY;

    /* Set the repeated callback */
    te->interval = (UA_UInt64)interval;
    te->id = ++t->idCounter;
    te->callback = callback;
    te->application = application;
    te->data = data;
    te->nextTime = nextTime;

    /* Set the output identifier */
    if(callbackId)
        *callbackId = te->id;

    ZIP_INSERT(UA_TimerZip, &t->root, te, ZIP_FFS32(UA_UInt32_random()));
    ZIP_INSERT(UA_TimerIdZip, &t->idRoot, te, ZIP_RANK(te, zipfields));
    return UA_STATUSCODE_GOOD;
}

UA_StatusCode
UA_Timer_addTimedCallback(UA_Timer *t, UA_ApplicationCallback callback,
                          void *application, void *data, UA_DateTime date,
                          UA_UInt64 *callbackId) {
    UA_LOCK(t->timerMutex);
    UA_StatusCode res = addCallback(t, callback, application, data, date, 0, callbackId);
    UA_UNLOCK(t->timerMutex);
    return res;
}

/* Adding repeated callbacks: Add an entry with the "nextTime" timestamp in the
 * future. This will be picked up in the next iteration and inserted at the
 * correct place. So that the next execution takes place ät "nextTime". */
UA_StatusCode
UA_Timer_addRepeatedCallback(UA_Timer *t, UA_ApplicationCallback callback,
                             void *application, void *data, UA_Double interval_ms,
                             UA_UInt64 *callbackId) {
    /* The interval needs to be positive */
    if(interval_ms <= 0.0)
        return UA_STATUSCODE_BADINTERNALERROR;

    UA_UInt64 interval = (UA_UInt64)(interval_ms * UA_DATETIME_MSEC);
    if(interval == 0)
        return UA_STATUSCODE_BADINTERNALERROR;

    UA_DateTime nextTime = UA_DateTime_nowMonotonic() + (UA_DateTime)interval;
    UA_LOCK(t->timerMutex);
    UA_StatusCode res = addCallback(t, callback, application, data, nextTime,
                                    interval, callbackId);
    UA_UNLOCK(t->timerMutex);
    return res;
}

UA_StatusCode
UA_Timer_changeRepeatedCallbackInterval(UA_Timer *t, UA_UInt64 callbackId,
                                        UA_Double interval_ms) {
    /* The interval needs to be positive */
    if(interval_ms <= 0.0)
        return UA_STATUSCODE_BADINTERNALERROR;

    UA_LOCK(t->timerMutex);

    /* Remove from the sorted list */
    UA_TimerEntry *te = ZIP_FIND(UA_TimerIdZip, &t->idRoot, &callbackId);
    if(!te) {
        UA_UNLOCK(t->timerMutex);
        return UA_STATUSCODE_BADNOTFOUND;
    }

    /* Set the repeated callback */
    ZIP_REMOVE(UA_TimerZip, &t->root, te);
    te->interval = (UA_UInt64)(interval_ms * UA_DATETIME_MSEC); /* in 100ns resolution */
    te->nextTime = UA_DateTime_nowMonotonic() + (UA_DateTime)te->interval;
    ZIP_INSERT(UA_TimerZip, &t->root, te, ZIP_RANK(te, zipfields));

    UA_UNLOCK(t->timerMutex);
    return UA_STATUSCODE_GOOD;
}

void
UA_Timer_removeCallback(UA_Timer *t, UA_UInt64 callbackId) {
    UA_LOCK(t->timerMutex);
    UA_TimerEntry *te = ZIP_FIND(UA_TimerIdZip, &t->idRoot, &callbackId);
    if(!te) {
        UA_UNLOCK(t->timerMutex);
        return;
    }

    ZIP_REMOVE(UA_TimerZip, &t->root, te);
    ZIP_REMOVE(UA_TimerIdZip, &t->idRoot, te);
    UA_free(te);
    UA_UNLOCK(t->timerMutex);
}

UA_DateTime
UA_Timer_process(UA_Timer *t, UA_DateTime nowMonotonic,
                 UA_TimerExecutionCallback executionCallback,
                 void *executionApplication) {
    UA_LOCK(t->timerMutex);
    UA_TimerEntry *first;
    while((first = ZIP_MIN(UA_TimerZip, &t->root)) &&
          first->nextTime <= nowMonotonic) {
        ZIP_REMOVE(UA_TimerZip, &t->root, first);

        /* Reinsert / remove to their new position first. Because the callback
         * can interact with the zip tree and expects the same entries in the
         * root and idRoot trees. */

        if(first->interval == 0) {
            ZIP_REMOVE(UA_TimerIdZip, &t->idRoot, first);
            if(first->callback) {
                UA_UNLOCK(t->timerMutex);
                executionCallback(executionApplication, first->callback,
                                  first->application, first->data);
                UA_LOCK(t->timerMutex);
            }
            UA_free(first);
            continue;
        }

        /* Set the time for the next execution. Prevent an infinite loop by
         * forcing the next processing into the next iteration. */
        first->nextTime += (UA_Int64)first->interval;
        if(first->nextTime < nowMonotonic)
            first->nextTime = nowMonotonic + 1;
        ZIP_INSERT(UA_TimerZip, &t->root, first, ZIP_RANK(first, zipfields));

        if(!first->callback)
            continue;

        /* Unlock the mutes before dropping into the callback. So that the timer
         * itself can be edited within the callback. When we return, only the
         * pointer to t must still exist. */
        UA_ApplicationCallback cb = first->callback;
        void *app = first->application;
        void *data = first->data;
        UA_UNLOCK(t->timerMutex);
        executionCallback(executionApplication, cb, app, data);
        UA_LOCK(t->timerMutex);
    }

    /* Return the timestamp of the earliest next callback */
    first = ZIP_MIN(UA_TimerZip, &t->root);
    UA_DateTime next = (first) ? first->nextTime : UA_INT64_MAX;
    if(next < nowMonotonic)
        next = nowMonotonic;
    UA_UNLOCK(t->timerMutex);
    return next;
}

static void
freeEntry(UA_TimerEntry *te, void *data) {
    UA_free(te);
}

void
UA_Timer_clear(UA_Timer *t) {
    UA_LOCK(t->timerMutex);
    /* Free all nodes and reset the root */
    ZIP_ITER(UA_TimerZip, &t->root, freeEntry, NULL);
    UA_UNLOCK(t->timerMutex);
#if UA_MULTITHREADING >= 100
    UA_LOCK_DESTROY(t->timerMutex)
#endif
    ZIP_INIT(&t->root);
}
