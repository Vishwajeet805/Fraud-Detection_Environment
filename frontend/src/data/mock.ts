import type { FraudObservation, FraudReward } from '../types/backend';

export const mockObservation: FraudObservation = {
  message_text: 'Urgent: Your account KYC expires today. Verify immediately to avoid a freeze.',
  url: 'https://secure-kyc-verify.xyz/account',
  sender: 'alerts@bank-security-tk.com',
  extracted_features: {
    has_urgent_words: true,
    has_financial_keywords: true,
    suspicious_domain_score: 0.84,
    message_length: 116,
    has_external_links: true,
    sender_reputation_score: 0.76,
  },
  step_count: 2,
  task_name: 'hard_decision_making',
  difficulty: 'hard',
  max_steps: 30,
  action_history: [2, 1],
  reward_history: [0.6, 1],
};

export const mockReward: FraudReward = {
  total: 1.1,
  base_reward: 1,
  streak_bonus: 0.1,
  repetition_penalty: 0,
  suspicious_abuse_penalty: 0,
  correct: true,
  partial: false,
  explanation: 'Urgent financial language + suspicious domain + low sender trust indicates high-probability fraud.',
  money_saved: 18420,
  money_lost: 0,
  money_at_risk: 4200,
};

export const timeline = [
  { step: 1, status: 'Suspicious', confidence: 0.67 },
  { step: 2, status: 'Fraud', confidence: 0.86 },
  { step: 3, status: 'Fraud', confidence: 0.92 },
];

export const trendData = [
  { day: 'Mon', fraud: 64, safe: 172 },
  { day: 'Tue', fraud: 58, safe: 180 },
  { day: 'Wed', fraud: 79, safe: 169 },
  { day: 'Thu', fraud: 71, safe: 164 },
  { day: 'Fri', fraud: 88, safe: 177 },
  { day: 'Sat', fraud: 95, safe: 183 },
  { day: 'Sun', fraud: 90, safe: 179 },
];

export const confidenceData = [
  { range: '0-20', value: 6 },
  { range: '20-40', value: 14 },
  { range: '40-60', value: 22 },
  { range: '60-80', value: 37 },
  { range: '80-100', value: 52 },
];

export const rewardSeries = Array.from({ length: 20 }, (_, i) => ({
  episode: i + 1,
  baseline: 0.2 + i * 0.02,
  improved: 0.24 + i * 0.042,
}));
