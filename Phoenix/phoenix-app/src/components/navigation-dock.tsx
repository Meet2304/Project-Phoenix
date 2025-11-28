"use client";

import React from "react";
import { Home, Info, Users } from "lucide-react";
import Link from "next/link";

interface NavigationDockProps {
  className?: string;
}

export const NavigationDock: React.FC<NavigationDockProps> = ({ className = "" }) => {
  return (
    <div className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-full max-w-[calc(100vw-2rem)] px-4 ${className}`}>
      <div className="flex items-center justify-center gap-1 rounded-[20px] bg-neutral-900/80 px-2 py-1.5 shadow-2xl ring-1 ring-white/10 backdrop-blur-lg sm:gap-5 sm:rounded-[36px] sm:px-6 sm:py-3 mx-auto w-fit overflow-hidden">
        <DockIcon icon={Home} label="Home" href="/" />
        <DockIcon icon={Info} label="About" href="/about" />
        <DockIcon icon={Users} label="Team" href="/team" />
      </div>
    </div>
  );
};

interface DockIconProps {
  icon: React.ElementType;
  label: string;
  href: string;
}

function DockIcon({ icon: Icon, label, href }: DockIconProps) {
  return (
    <Link href={href}>
      <button
        className="group relative grid h-9 w-9 place-items-center rounded-lg ring-1 ring-white/10 bg-gradient-to-b from-neutral-800/60 to-neutral-900/70 backdrop-blur-xl shadow-lg transition-all duration-200 hover:-translate-y-1 hover:scale-105 sm:h-14 sm:w-14 sm:rounded-xl before:absolute before:inset-0 before:rounded-lg sm:before:rounded-xl before:opacity-0 before:transition-opacity before:duration-300 hover:before:opacity-100 hover:before:shadow-[0_0_15px_rgba(255,255,255,0.15)]"
        aria-label={label}
      >
        <Icon
          className="h-4 w-4 text-white/85 transition-transform duration-200 group-hover:scale-110 sm:h-6 sm:w-6"
          strokeWidth={2.1}
        />
        <span className="absolute -bottom-8 whitespace-nowrap text-[10px] tracking-wide text-white/90 bg-neutral-900/90 px-2 py-1 rounded-md sm:text-[11px] opacity-0 invisible translate-y-1.5 transition-all duration-200 pointer-events-none group-hover:opacity-100 group-hover:visible group-hover:translate-y-0">
          {label}
        </span>
      </button>
    </Link>
  );
}

export default NavigationDock;
