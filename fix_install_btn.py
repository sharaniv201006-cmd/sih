# -*- coding: utf-8 -*-
with open("frontend/src/components/InstallAppButton.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Smartphone, Download } from 'lucide-react';

export const InstallAppButton = ({ isCollapsed = false }) => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstalled, setIsInstalled] = useState(() => {
    return localStorage.getItem('app_installed_dismissed') === 'true';
  });

  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    window.addEventListener('beforeinstallprompt', handler);

    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      localStorage.setItem('app_installed_dismissed', 'true');
    }

    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        setIsInstalled(true);
        localStorage.setItem('app_installed_dismissed', 'true');
        setDeferredPrompt(null);
        return;
      }
    }
    
    // Once clicked, hide it permanently as requested
    setIsInstalled(true);
    localStorage.setItem('app_installed_dismissed', 'true');
  };

  // If already installed or clicked once, hide completely from UI
  if (isInstalled) {
    return null;
  }

  return (
    <button
      onClick={handleInstallClick}
      title="Install App"
      className={`w-full py-2.5 px-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold text-xs shadow-md shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-500 transition-all flex items-center justify-center gap-2 ${
        isCollapsed ? 'p-2.5' : ''
      }`}
    >
      <Smartphone className="w-4 h-4 shrink-0" />
      {!isCollapsed && <span>Install App</span>}
    </button>
  );
};
""")

print("Updated InstallAppButton.jsx to hide permanently once clicked/installed.")
