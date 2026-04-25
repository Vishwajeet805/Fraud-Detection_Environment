import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, Line, LineChart } from 'recharts';
import { MetricCard } from '../components/MetricCard';
import { Card } from '../components/Card';
import { confidenceData, trendData } from '../data/mock';

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard label="Total Checks" value={24830} />
        <MetricCard label="Fraud Rate" value={12.7} suffix="%" />
        <MetricCard label="Avg Confidence" value={88.4} suffix="%" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <h3 className="text-lg font-semibold text-slate-100">Fraud vs Safe Over Time</h3>
          <div className="mt-4 h-72">
            <ResponsiveContainer>
              <LineChart data={trendData}>
                <CartesianGrid stroke="#1a2940" strokeDasharray="3 3" />
                <XAxis dataKey="day" stroke="#8ea3c2" />
                <YAxis stroke="#8ea3c2" />
                <Tooltip />
                <Line dataKey="fraud" stroke="#2DE2B0" strokeWidth={2} dot={false} />
                <Line dataKey="safe" stroke="#64748b" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-slate-100">Confidence Distribution</h3>
          <div className="mt-4 h-72">
            <ResponsiveContainer>
              <BarChart data={confidenceData}>
                <CartesianGrid stroke="#1a2940" strokeDasharray="3 3" />
                <XAxis dataKey="range" stroke="#8ea3c2" />
                <YAxis stroke="#8ea3c2" />
                <Tooltip />
                <Bar dataKey="value" fill="#2DE2B0" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-semibold text-slate-100">Recent Activity</h3>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr>
                <th className="py-2">Message</th>
                <th className="py-2">Prediction</th>
                <th className="py-2">Confidence</th>
              </tr>
            </thead>
            <tbody className="text-slate-200">
              {[['OTP expired verify now', 'Fraud', '91%'], ['Refund processed click link', 'Suspicious', '74%'], ['Salary credited notice', 'Safe', '88%']].map((row) => (
                <tr key={row[0]} className="border-t border-border/80">
                  <td className="py-3">{row[0]}</td>
                  <td className="py-3">{row[1]}</td>
                  <td className="py-3">{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
