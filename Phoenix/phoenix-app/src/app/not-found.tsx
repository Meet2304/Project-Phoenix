'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, Home } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function NotFound() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-transparent text-white overflow-hidden relative selection:bg-white/20">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {mounted && [...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute bg-white/5 rounded-full"
            initial={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
              scale: Math.random() * 0.5 + 0.5,
              opacity: Math.random() * 0.3,
            }}
            animate={{
              y: [null, Math.random() * -100],
              opacity: [null, 0],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: "linear",
            }}
            style={{
              width: Math.random() * 4 + 1 + 'px',
              height: Math.random() * 4 + 1 + 'px',
            }}
          />
        ))}
      </div>

      <div className="relative z-10 flex flex-col items-center px-6 text-center">
        {/* Glitch Text Effect for 404 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          <h1 
            className="text-[8rem] sm:text-[12rem] md:text-[16rem] font-bold leading-none tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/10 select-none"
            style={{ fontFamily: 'var(--font-michroma)' }}
          >
            404
          </h1>
          <motion.div 
            className="absolute inset-0 text-[8rem] sm:text-[12rem] md:text-[16rem] font-bold leading-none tracking-tighter text-white/20 blur-sm select-none"
            style={{ fontFamily: 'var(--font-michroma)' }}
            animate={{ 
              x: [-2, 2, -2],
              opacity: [0.5, 0.2, 0.5] 
            }}
            transition={{ 
              duration: 0.2,
              repeat: Infinity,
              repeatType: "reverse"
            }}
          >
            404
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="space-y-6 max-w-lg mx-auto"
        >
          <h2 
            className="text-2xl sm:text-3xl md:text-4xl font-light text-white/90"
            style={{ fontFamily: 'var(--font-michroma)' }}
          >
            Page Not Found
          </h2>
          
          <p 
            className="text-base sm:text-lg text-white/60 leading-relaxed"
            style={{ fontFamily: 'var(--font-playfair)' }}
          >
            The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
            <Link href="/" className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md bg-white px-8 font-medium text-black transition-all duration-300 hover:bg-white/90 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-black">
              <div className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-12deg)_translateX(-100%)] group-hover:duration-1000 group-hover:[transform:skew(-12deg)_translateX(100%)]">
                <div className="relative h-full w-8 bg-white/20" />
              </div>
              <Home className="mr-2 h-4 w-4" />
              <span style={{ fontFamily: 'var(--font-poppins)' }}>Back to Home</span>
            </Link>
            
            <button 
              onClick={() => window.history.back()}
              className="group inline-flex h-12 items-center justify-center rounded-md border border-white/20 bg-transparent px-8 font-medium text-white transition-all hover:bg-white/10 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-black"
            >
              <ArrowLeft className="mr-2 h-4 w-4 transition-transform group-hover:-translate-x-1" />
              <span style={{ fontFamily: 'var(--font-poppins)' }}>Go Back</span>
            </button>
          </div>
        </motion.div>
      </div>

      {/* Footer decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
    </div>
  );
}
