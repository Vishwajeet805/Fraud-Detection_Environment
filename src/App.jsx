import { useState } from 'react'
import { NavLink, Route, Routes, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import LandingPage from './pages/LandingPage'
import DetectionPage from './pages/DetectionPage'
import DashboardPage from './pages/DashboardPage'
import InsightsPage from './pages/InsightsPage'
import HowItWorksPage from './pages/HowItWorksPage'

const navItems = [
  { to: '/', label: 'Platform' },
  { to: '/detect', label: 'Detection Engine' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/insights', label: 'Training Insights' },
  { to: '/how-it-works', label: 'How It Works' },
]

function App() {
  const location = useLocation()
  const [cursor, setCursor] = useState({ x: 0, y: 0, active: false })

  return (
    <div
      className="relative min-h-screen overflow-hidden bg-base bg-mesh-soft text-slate-100"
      onMouseMove={(event) => setCursor({ x: event.clientX, y: event.clientY, active: true })}
      onMouseLeave={() => setCursor((prev) => ({ ...prev, active: false }))}
    >
      <motion.div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-0 transition-opacity duration-500"
        animate={{ opacity: cursor.active ? 1 : 0 }}
        style={{
          background: `radial-gradient(320px circle at ${cursor.x}px ${cursor.y}px, rgba(41,211,255,0.16), rgba(124,140,255,0.10) 30%, rgba(4,7,15,0) 68%)`,
        }}
      />

      <div className="relative z-10 mx-auto flex min-h-screen w-full max-w-7xl flex-col px-6 py-6 lg:px-10">
        <header className="sticky top-4 z-30 mb-10 rounded-2xl border border-white/10 bg-surface/70 p-4 shadow-soft backdrop-blur-xl">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-slate-400">FraudShield AI</p>
              <h1 className="text-lg font-semibold text-slate-100">Decision Intelligence Platform</h1>
            </div>
            <nav className="flex flex-wrap gap-2">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `rounded-xl px-4 py-2 text-sm transition ${
                      isActive
                        ? 'bg-accent/20 text-accent shadow-glow'
                        : 'text-slate-300 hover:bg-white/5 hover:text-white'
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
        </header>

        <main className="flex-1">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.32, ease: 'easeOut' }}
            >
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/detect" element={<DetectionPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/insights" element={<InsightsPage />} />
                <Route path="/how-it-works" element={<HowItWorksPage />} />
              </Routes>
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}

export default App
