import React from 'react'
import './ProductsWallet.css'

export default function ProductsWallet() {
  return (
    <div className="relative group inline-block z-50">
      
      {/* The Trigger Button */}
      <button className="custom-hover-btn">
        <span>OPENARC APPS</span>
      </button>

      {/* The Hidden Wallet Dropdown */}
      <div className="absolute right-0 top-full pt-4 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-[-10px] group-hover:translate-y-0 z-50 origin-top-right scale-75">
        
        <div className="wallet">
          <div className="wallet-back"></div>
          
          {/* Card 1: OpenArc Local LLM */}
          <a 
            href="https://github.com/AREKG0/Openarc" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="card-wallet-item card-1"
          >
            <div className="card-inner">
              <div className="card-top">
                <span>OpenArc</span>
                <div className="chip"></div>
              </div>
              <div className="card-bottom">
                <span className="label-desc text-white/90">Local LLM inference engine. Serverless AI.</span>
                <div className="hidden-stars">**** ****</div>
                <div className="card-link-icon">
                  View on GitHub
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </div>
              </div>
            </div>
          </a>

          {/* Card 2: LeadSaver (Chrome Plugin) */}
          <a 
            href="https://chromewebstore.google.com/detail/leadsaver-%E2%80%94-linkedin-to-s/hpfjpohfopilmhcpjejdjcacihgkfokp" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="card-wallet-item card-2"
          >
            <div className="card-inner">
              <div className="card-top">
                <span>LeadSaver</span>
                <div className="chip"></div>
              </div>
              <div className="card-bottom">
                <span className="label-desc text-white/90">LinkedIn to Sheets Chrome Web Store Plugin.</span>
                <div className="hidden-stars">**** ****</div>
                <div className="card-link-icon">
                  View on Web Store
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </div>
              </div>
            </div>
          </a>

          {/* Pocket */}
          <div className="pocket">
            <svg viewBox="0 0 280 160" preserveAspectRatio="none">
              <path d="M0,0 Q140,40 280,0 L280,160 Q140,160 0,160 Z" fill="#1e341e" />
            </svg>
            <div className="pocket-content">
              <div className="balance-stars">****</div>
              <div className="balance-real">OpenArc Products</div>
              <div className="eye-icon-wrapper">
                {/* Eye Closed */}
                <svg className="eye-icon eye-slash" viewBox="0 0 24 24" fill="none" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
                {/* Eye Open */}
                <svg className="eye-icon eye-open opacity-0" viewBox="0 0 24 24" fill="none" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
