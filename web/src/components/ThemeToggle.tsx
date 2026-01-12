
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { motion } from 'framer-motion';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-surface-hover text-muted-foreground hover:text-foreground transition-colors"
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
    >
      <div className="relative w-5 h-5">
        <motion.div
          initial={false}
          animate={{ scale: theme === 'dark' ? 1 : 0, rotate: theme === 'dark' ? 0 : 90 }}
          transition={{ duration: 0.2 }}
          className="absolute inset-0"
        >
          <Moon size={20} />
        </motion.div>
        <motion.div
          initial={false}
          animate={{ scale: theme === 'light' ? 1 : 0, rotate: theme === 'light' ? 0 : -90 }}
          transition={{ duration: 0.2 }}
          className="absolute inset-0"
        >
          <Sun size={20} />
        </motion.div>
      </div>
    </button>
  );
}
