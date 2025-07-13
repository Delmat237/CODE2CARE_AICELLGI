// IndexedDB wrapper for offline storage
class OfflineStorage {
  private dbName = 'dgh-feedback-db';
  private version = 1;
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Create feedback store
        if (!db.objectStoreNames.contains('feedbacks')) {
          const feedbackStore = db.createObjectStore('feedbacks', { keyPath: 'id', autoIncrement: true });
          feedbackStore.createIndex('timestamp', 'timestamp', { unique: false });
          feedbackStore.createIndex('is_synced', 'is_synced', { unique: false });
        }

        // Create audio recordings store
        if (!db.objectStoreNames.contains('audio_recordings')) {
          const audioStore = db.createObjectStore('audio_recordings', { keyPath: 'id', autoIncrement: true });
          audioStore.createIndex('feedback_id', 'feedback_id', { unique: false });
        }
      };
    });
  }

  async saveFeedback(feedback: any): Promise<number> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['feedbacks'], 'readwrite');
      const store = transaction.objectStore('feedbacks');
      
      const feedbackData = {
        ...feedback,
        timestamp: Date.now(),
        is_synced: false
      };
      
      const request = store.add(feedbackData);
      request.onsuccess = () => resolve(request.result as number);
      request.onerror = () => reject(request.error);
    });
  }

  async saveAudioRecording(feedbackId: number, audioBlob: Blob): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['audio_recordings'], 'readwrite');
      const store = transaction.objectStore('audio_recordings');
      
      const audioData = {
        feedback_id: feedbackId,
        audio_data: audioBlob,
        timestamp: Date.now()
      };
      
      const request = store.add(audioData);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getUnsyncedFeedbacks(): Promise<any[]> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['feedbacks'], 'readonly');
      const store = transaction.objectStore('feedbacks');
      const index = store.index('is_synced');
      
      const request = index.getAll("false");
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async markAsSynced(id: number): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['feedbacks'], 'readwrite');
      const store = transaction.objectStore('feedbacks');
      
      const getRequest = store.get(id);
      getRequest.onsuccess = () => {
        const feedback = getRequest.result;
        if (feedback) {
          feedback.is_synced = true;
          const updateRequest = store.put(feedback);
          updateRequest.onsuccess = () => resolve();
          updateRequest.onerror = () => reject(updateRequest.error);
        } else {
          resolve();
        }
      };
      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  async clearSyncedData(): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['feedbacks'], 'readwrite');
      const store = transaction.objectStore('feedbacks');
      const index = store.index('is_synced');
      
      const request = index.openCursor("true");
      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest).result;
        if (cursor) {
          cursor.delete();
          cursor.continue();
        } else {
          resolve();
        }
      };
      request.onerror = () => reject(request.error);
    });
  }
}

export const offlineStorage = new OfflineStorage();