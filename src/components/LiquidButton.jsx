import React from 'react'
import { Zap } from 'lucide-react'
import './LiquidButton.css'

export default function LiquidButton({ 
  onClick, 
  disabled, 
  isCompressing, 
  isFinished, 
  percentage 
}) {
  
  // Determine if the text needs to flip to white for readability
  const isFilledHigh = isFinished && percentage > 45;

  return (
    <button
      onClick={onClick}
      disabled={disabled || isCompressing}
      className={`liquid-btn ${isFilledHigh ? 'filled-high' : ''}`}
    >
      {/* The Liquid Fill */}
      {isFinished && (
        <div 
          className="liquid-fill" 
          style={{ height: `${percentage}%` }}
        />
      )}

      {/* Button Content */}
      <span className="liquid-text flex items-center gap-2">
        {isCompressing ? (
          <span className="animate-pulse flex items-center gap-2">
            <Zap size={18} className="animate-spin" />
            Compressing...
          </span>
        ) : isFinished ? (
          <span className="flex items-center gap-2">
            <Zap size={18} />
            {percentage}% Tokens Saved
          </span>
        ) : (
          <span className="flex items-center gap-2">
            <Zap size={18} />
            Compress Prompt
          </span>
        )}
      </span>
    </button>
  )
}
