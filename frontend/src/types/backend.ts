export interface ExtractedFeatures {
  has_urgent_words: boolean;
  has_financial_keywords: boolean;
  suspicious_domain_score: number;
  message_length: number;
  has_external_links: boolean;
  sender_reputation_score: number;
}

export interface FraudObservation {
  message_text: string;
  url: string;
  sender: string;
  extracted_features: ExtractedFeatures;
  step_count: number;
  task_name: string;
  difficulty: 'easy' | 'medium' | 'hard';
  max_steps: number;
  action_history: number[];
  reward_history: number[];
}

export interface FraudReward {
  total: number;
  base_reward: number;
  streak_bonus: number;
  repetition_penalty: number;
  suspicious_abuse_penalty: number;
  correct: boolean;
  partial: boolean;
  explanation: string;
  money_saved: number;
  money_lost: number;
  money_at_risk: number;
}

export interface StepResult {
  observation: FraudObservation;
  reward: FraudReward;
  done: boolean;
  info: Record<string, unknown>;
}
