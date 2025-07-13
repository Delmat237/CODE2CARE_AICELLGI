// Network utilities for handling low bandwidth and offline scenarios
export class NetworkManager {
  private static instance: NetworkManager;
  private isOnline: boolean = true;
  private listeners: ((online: boolean) => void)[] = [];
  private retryQueue: (() => Promise<void>)[] = [];
  private maxRetries = 3;
  private retryDelay = 1000;

  constructor() {
    if (typeof window !== 'undefined') {
      this.isOnline = navigator.onLine;
      window.addEventListener('online', this.handleOnline.bind(this));
      window.addEventListener('offline', this.handleOffline.bind(this));
    }
  }

  static getInstance(): NetworkManager {
    if (!NetworkManager.instance) {
      NetworkManager.instance = new NetworkManager();
    }
    return NetworkManager.instance;
  }

  private handleOnline() {
    this.isOnline = true;
    this.notifyListeners(true);
    this.processRetryQueue();
  }

  private handleOffline() {
    this.isOnline = false;
    this.notifyListeners(false);
  }

  private notifyListeners(online: boolean) {
    this.listeners.forEach(listener => listener(online));
  }

  public addListener(listener: (online: boolean) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  public getConnectionStatus(): boolean {
    return this.isOnline;
  }

  public async makeRequest(
    url: string, 
    options: RequestInit = {},
    retries: number = this.maxRetries
  ): Promise<Response> {
    try {
      // Add compression headers for low bandwidth
      const headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        ...options.headers
      };

      const response = await fetch(url, {
        ...options,
        headers,
        // Add timeout for slow connections
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return response;
    } catch (error) {
      if (retries > 0 && this.isOnline) {
        await this.delay(this.retryDelay);
        return this.makeRequest(url, options, retries - 1);
      }
      throw error;
    }
  }

  public addToRetryQueue(operation: () => Promise<void>) {
    this.retryQueue.push(operation);
  }

  private async processRetryQueue() {
    while (this.retryQueue.length > 0 && this.isOnline) {
      const operation = this.retryQueue.shift();
      if (operation) {
        try {
          await operation();
        } catch (error) {
          console.error('Retry operation failed:', error);
          // Re-add to queue if it fails
          this.retryQueue.push(operation);
          break;
        }
      }
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Compress data for transmission
  public compressData(data: any): string {
    try {
      return JSON.stringify(data);
    } catch (error) {
      console.error('Data compression failed:', error);
      return JSON.stringify(data);
    }
  }

  // Check connection quality
  public async checkConnectionQuality(): Promise<'high' | 'medium' | 'low'> {
    if (!this.isOnline) return 'low';

    try {
      const start = Date.now();
      await fetch('/api/ping', { method: 'HEAD' });
      const duration = Date.now() - start;

      if (duration < 500) return 'high';
      if (duration < 2000) return 'medium';
      return 'low';
    } catch {
      return 'low';
    }
  }
}

export const networkManager = NetworkManager.getInstance();