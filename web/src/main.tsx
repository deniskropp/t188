import { StrictMode } from 'react'
import { ThemeProvider } from './context/ThemeContext'
import App from './App'
import { createRoot } from 'react-dom/client'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
