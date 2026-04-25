export const demoScenarios = [
  {
    name: 'Payment Reversal Scam',
    message_text: 'Urgent: your payment is blocked. Verify account now to avoid reversal charges.',
    url: 'https://secure-payee-center.co/verify',
    sender: 'alerts@txn-support-payments.com',
  },
  {
    name: 'Unknown Sender (Message only)',
    message_text: 'Need immediate transfer approval for vendor settlement. Reply with OTP now.',
    url: '',
    sender: '',
  },
  {
    name: 'Routine Policy Update',
    message_text: 'Please review the updated procurement policy in the intranet before 5 PM.',
    url: 'https://intranet.company.com/policy',
    sender: 'compliance@company.com',
  },
]

export const dashboardSeries = [
  { date: 'Mon', fraud: 32, safe: 86 },
  { date: 'Tue', fraud: 37, safe: 83 },
  { date: 'Wed', fraud: 29, safe: 92 },
  { date: 'Thu', fraud: 52, safe: 69 },
  { date: 'Fri', fraud: 47, safe: 74 },
  { date: 'Sat', fraud: 34, safe: 88 },
]

export const confidenceBuckets = [
  { bucket: '0-40', checks: 16 },
  { bucket: '41-60', checks: 36 },
  { bucket: '61-80', checks: 94 },
  { bucket: '81-100', checks: 138 },
]

export const activityRows = [
  { message: 'Executive transfer request', prediction: 'Fraud', confidence: '96%' },
  { message: 'Supplier invoice update', prediction: 'Suspicious', confidence: '76%' },
  { message: 'Payroll portal reminder', prediction: 'Safe', confidence: '84%' },
  { message: 'Credential reset link', prediction: 'Fraud', confidence: '93%' },
]

export const rewardCurve = [
  { episode: 1, baseline: 15, improved: 17 },
  { episode: 2, baseline: 21, improved: 31 },
  { episode: 3, baseline: 24, improved: 44 },
  { episode: 4, baseline: 31, improved: 59 },
  { episode: 5, baseline: 37, improved: 75 },
  { episode: 6, baseline: 43, improved: 90 },
  { episode: 7, baseline: 48, improved: 108 },
]
