import { useState, useEffect } from 'react'
import { compressPrompt } from './utils/compressor'
import { countTokens } from './utils/tokenizer'
import { Copy, Zap, ArrowRight, Check } from 'lucide-react'
import ProductsWallet from './components/ProductsWallet'
import LiquidButton from './components/LiquidButton'
import ContactCard from './components/ContactCard'

function App() {
  const [originalText, setOriginalText] = useState('')
  const [compressedText, setCompressedText] = useState('')
  const [originalTokens, setOriginalTokens] = useState(0)
  const [compressedTokens, setCompressedTokens] = useState(0)
  const [copied, setCopied] = useState(false)
  const [shareCopied, setShareCopied] = useState(false)
  const [isCompressed, setIsCompressed] = useState(false)
  
  // Fake loading state for button animation
  const [isCompressing, setIsCompressing] = useState(false)

  // Lifetime tracking
  const [lifetimeSaved, setLifetimeSaved] = useState(() => {
    const saved = localStorage.getItem('shrinktoken_lifetime')
    return saved ? parseInt(saved, 10) : 0
  })

  // Save to local storage whenever lifetime changes
  useEffect(() => {
    localStorage.setItem('shrinktoken_lifetime', lifetimeSaved.toString())
  }, [lifetimeSaved])

  // Calculate tokens whenever text changes
  useEffect(() => {
    setOriginalTokens(countTokens(originalText))
    if (!originalText) {
      setIsCompressed(false)
      setCompressedTokens(0)
    }
  }, [originalText])

  const handleCompress = () => {
    setIsCompressing(true)
    setIsCompressed(false)
    
    // Fake 600ms loading time so the user can see the animation start
    setTimeout(() => {
      const result = compressPrompt(originalText)
      const newCompressedTokens = countTokens(result)
      const newSaved = originalTokens - newCompressedTokens

      setCompressedText(result)
      setCompressedTokens(newCompressedTokens)
      setIsCompressed(true)
      setIsCompressing(false)

      if (newSaved > 0) {
        setLifetimeSaved(prev => prev + newSaved)
      }
    }, 600)
  }

  // Reset compression state if user edits original text AFTER compressing
  const handleTextChange = (e) => {
    setOriginalText(e.target.value)
    setIsCompressed(false)
    setCompressedText('')
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(compressedText)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleShareSavings = () => {
    const total = lifetimeSaved > 0 ? lifetimeSaved.toLocaleString() : (originalTokens - compressedTokens).toLocaleString()
    const boast = `⚡ I just saved ${total} tokens on my ChatGPT & Claude API calls using #ShrinkToken! Try the 100% private, local-first AI prompt compression engine by OpenArc: https://github.com/AREKG0/shrinktoken`
    navigator.clipboard.writeText(boast)
    setShareCopied(true)
    setTimeout(() => setShareCopied(false), 3500)
  }

  const tokensSaved = originalTokens - compressedTokens
  const percentageSaved = originalTokens > 0 ? Math.round((tokensSaved / originalTokens) * 100) : 0

  return (
    <div className="min-h-screen flex flex-col bg-darker p-4 md:p-8 text-white selection:bg-accent/30">
      
      {/* Header */}
      <header className="w-full max-w-6xl mx-auto flex items-center justify-between mb-8 md:mb-12 relative h-16">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center shrink-0">
              <Zap size={20} className="text-white" />
            </div>
            <h1 className="text-xl md:text-2xl font-bold tracking-tight">ShrinkToken</h1>
          </div>
          
          {/* Lifetime Savings Badge */}
          {lifetimeSaved > 0 && (
            <div className="hidden lg:flex px-3 py-1.5 bg-green-500/10 border border-green-500/20 text-green-400 rounded-full text-xs font-bold uppercase tracking-wider items-center gap-1.5 shadow-inner">
              <Zap size={12} className="text-green-400" />
              {lifetimeSaved.toLocaleString()} Lifetime Tokens Saved
            </div>
          )}
        </div>
        <div className="z-50 scale-75 md:scale-100 origin-right">
          <ProductsWallet />
        </div>
      </header>

      {/* Main Content */}
      <main className="w-full max-w-6xl mx-auto flex-1 flex flex-col gap-6 md:gap-8">
        
        {/* Metrics Dashboard */}
        <section className="w-full bg-[#111113] border border-white/5 rounded-2xl p-4 md:p-6 flex flex-col md:flex-row flex-wrap gap-4 md:gap-8 items-center shadow-xl text-center md:text-left">
          <div className="flex-1 min-w-[120px] md:min-w-[200px]">
            <h3 className="text-xs md:text-sm font-medium text-white/50 mb-1 uppercase tracking-wider">Original Tokens</h3>
            <div className="text-3xl md:text-4xl font-mono text-white/90">{originalTokens.toLocaleString()}</div>
          </div>
          
          <div className="hidden md:flex items-center justify-center text-white/20 px-4">
            <ArrowRight size={32} />
          </div>

          <div className="flex-1 min-w-[120px] md:min-w-[200px]">
            <h3 className="text-xs md:text-sm font-medium text-white/50 mb-1 uppercase tracking-wider">Compressed Tokens</h3>
            <div className="text-3xl md:text-4xl font-mono text-white">{isCompressed ? compressedTokens.toLocaleString() : '0'}</div>
          </div>

          <div className="w-full md:flex-1 min-w-[120px] md:min-w-[200px] bg-accent/10 border border-accent/20 rounded-xl p-3 md:p-4 shadow-inner mt-2 md:mt-0">
            <h3 className="text-xs md:text-sm font-medium text-accent mb-1 uppercase tracking-wider">Tokens Saved</h3>
            <div className="text-2xl md:text-3xl font-mono font-bold text-accent">
              {isCompressed ? `-${tokensSaved.toLocaleString()}` : '0'} 
              <span className="text-sm md:text-lg ml-2 opacity-80">({isCompressed ? percentageSaved : 0}%)</span>
            </div>
          </div>
        </section>

        {/* Viral Share Savings Bar */}
        {(lifetimeSaved > 0 || isCompressed) && (
          <section className="w-full bg-[#161224] border border-[#b900ff]/40 rounded-xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 shadow-[0_0_25px_rgba(185,0,255,0.15)]">
            <div className="flex items-center gap-3 text-sm text-white/90">
              <span className="text-xl">🏆</span>
              <div className="leading-relaxed">
                You've pruned <strong className="text-[#00e5ff] font-mono text-base">{lifetimeSaved > 0 ? lifetimeSaved.toLocaleString() : tokensSaved.toLocaleString()} total tokens</strong> with 0% server contact! Boast about your computational shields:
              </div>
            </div>
            <button
              onClick={handleShareSavings}
              className="w-full md:w-auto px-5 py-2.5 rounded-lg bg-gradient-to-r from-[#00e5ff] to-[#b900ff] text-[#0a0a0f] font-extrabold text-xs uppercase tracking-wider flex items-center justify-center gap-2 hover:scale-105 transition-all shadow-[0_0_15px_rgba(0,229,255,0.5)] cursor-pointer shrink-0"
            >
              {shareCopied ? <Check size={16} className="text-[#0a0a0f]" /> : <span className="text-sm">⚡</span>}
              {shareCopied ? 'Copied Boast to Clipboard!' : 'Copy Social Boast (LinkedIn & X)'}
            </button>
          </section>
        )}

        {/* Text Areas */}
        <section className="flex flex-col md:flex-row gap-6 min-h-[60vh] md:h-[50vh]">
          
          {/* Input Side */}
          <div className="flex-1 flex flex-col gap-3 min-h-[300px] md:min-h-0">
            <div className="flex justify-between items-center px-1">
              <label className="text-sm font-semibold text-white/80">Input Prompt (Original)</label>
            </div>
            <textarea
              className="flex-1 bg-[#111113] border border-white/10 rounded-xl p-4 md:p-5 text-white/90 font-mono text-sm leading-relaxed resize-none focus:outline-none focus:border-accent/50 transition-colors shadow-lg"
              placeholder="Paste your massive prompt, codebase context, or instructions here..."
              value={originalText}
              onChange={handleTextChange}
            />
            
            <LiquidButton 
              onClick={handleCompress}
              disabled={!originalText}
              isCompressing={isCompressing}
              isFinished={isCompressed}
              percentage={percentageSaved}
            />
          </div>

          {/* Output Side */}
          <div className="flex-1 flex flex-col gap-3">
            <div className="flex justify-between items-center px-1">
              <label className="text-sm font-semibold text-accent">Optimized Output</label>
              <button 
                onClick={handleCopy}
                disabled={!compressedText}
                className="text-xs flex items-center gap-1.5 px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-white/70 transition-colors disabled:opacity-50 hover:text-white"
              >
                {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
                {copied ? 'Copied!' : 'Copy to Clipboard'}
              </button>
            </div>
            <textarea
              readOnly
              className={`flex-1 bg-[#0a0a0c] border border-accent/20 rounded-xl p-5 text-accent font-mono text-sm leading-relaxed resize-none focus:outline-none shadow-lg ${isCompressing ? 'animate-pulse text-accent/50' : ''}`}
              placeholder="Your optimized, token-saving prompt will appear here."
              value={isCompressing ? 'Compressing and optimizing your prompt...' : compressedText}
            />
          </div>

        </section>

        {/* Footer / Contact Section */}
        <section className="flex justify-center mt-12 mb-8">
          <ContactCard />
        </section>

      </main>
      
    </div>
  )
}

export default App
