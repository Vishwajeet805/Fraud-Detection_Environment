import type { FraudObservation, StepResult } from '../types/backend';

export type ActionCode = 0 | 1 | 2;

export class FraudDetectionClient {
  constructor(private readonly baseURL = 'http://localhost:8000') {}

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  reset(taskName = 'easy_fraud_detection'): Promise<FraudObservation> {
    return this.request('POST', '/reset', { task_name: taskName });
  }

  step(action: ActionCode, confidence?: number, reasoning?: string): Promise<StepResult> {
    return this.request('POST', '/step', { action, confidence, reasoning });
  }
}

export const formatINR = (value: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value);
