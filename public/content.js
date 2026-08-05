// ShrinkToken Manifest V3 - Direct DOM Injection Content Script
// Automatically injects a cyberpunk [⚡ Shrink] prompt optimization button into ChatGPT and Claude web interfaces.
// 100% Client-Side execution inside local DOM - zero HTTP network calls.

const STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into',
  'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then',
  'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with', 'very', 'really',
  'please', 'could', 'would', 'should', 'can', 'may', 'might', 'must', 'shall', 'am', 'has', 'have', 'had', 'do', 'does', 'did', 'so', 'too', 'basically', 'actually', 'obviously', 'simply', 'specifically', 'kindly'
]);

// Standalone offline semantic compression pipeline for content scripts
function localCompress(text) {
  if (!text) return '';
  let cleaned = text;

  // Step 1: Strip conversational fluff & pleasantries
  cleaned = cleaned.replace(/\b(hello|hi|hey|greetings|good morning|good evening) (chatgpt|claude|ai|there|assistant)\b/gi, '');
  cleaned = cleaned.replace(/\b(hope you are having a good day|hope you are well|thank you in advance|would really appreciate your help)\b/gi, '');
  cleaned = cleaned.replace(/\b(could you please|would you kindly|please take your time to)\b/gi, '');
  cleaned = cleaned.replace(/\b(really|very|just|quite|absolutely|extremely|highly|specifically|obviously|completely|simply)\b\s*/gi, '');

  // Step 2: Token Word Pruning
  let words = cleaned.split(/\s+/);
  let pruned = words.filter(word => {
    if (!word) return false;
    let cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
    if (cleanWord && STOPWORDS.has(cleanWord)) return false;
    return true;
  });

  // Step 3: Reassembly & formatting normalization
  let result = pruned.join(' ').replace(/\s{2,}/g, ' ').replace(/\s+([.,!?:;])/g, '$1').trim();
  return result || text; // Fallback to original if compression yields empty string
}

// Estimate token counts (approx 4 characters per token)
function approxTokens(str) {
  return Math.max(1, Math.ceil((str || '').length / 4));
}

// Inject Cyberpunk Toast Notification into DOM
function showShrinkToast(originalCount, compressedCount) {
  let existing = document.getElementById('shrinktoken-toast');
  if (existing) existing.remove();

  let toast = document.createElement('div');
  toast.id = 'shrinktoken-toast';
  let saved = Math.max(0, originalCount - compressedCount);
  let percent = originalCount > 0 ? Math.round((saved / originalCount) * 100) : 0;

  toast.innerHTML = `
    <div style="display:flex; align-items:center; gap:8px;">
      <span style="font-size:18px;">⚡</span>
      <div>
        <div style="font-weight:700; color:#00e5ff; font-family:'Courier New', monospace; font-size:13px; letter-spacing:1px;">SHRINKTOKEN OPTIMIZATION</div>
        <div style="font-size:11px; color:#ffffff; opacity:0.9;">Pruned <strong style="color:#ff007f;">${saved} tokens</strong> (${percent}% reduced)!</div>
      </div>
    </div>
  `;
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '80px',
    right: '20px',
    zIndex: '999999',
    backgroundColor: '#111113',
    border: '2px solid #b900ff',
    borderRadius: '10px',
    padding: '12px 18px',
    color: '#fff',
    boxShadow: '0 0 20px rgba(185, 0, 255, 0.5), 0 0 10px rgba(0, 229, 255, 0.3)',
    transition: 'all 0.3s ease-in-out',
    fontFamily: 'sans-serif'
  });

  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Attempt to find active text input on ChatGPT or Claude and compress its contents
function executeDirectShrink() {
  // Try finding textarea (common in Claude and older ChatGPT layouts) or contenteditable div (modern ChatGPT PROSE-MIRROR / ProseMirror)
  let inputEl = document.querySelector('textarea, [contenteditable="true"], .ProseMirror');
  if (!inputEl) return;

  let rawText = inputEl.value !== undefined ? inputEl.value : inputEl.innerText || '';
  if (!rawText.trim()) return;

  let origCount = approxTokens(rawText);
  let compressed = localCompress(rawText);
  let compCount = approxTokens(compressed);

  if (inputEl.value !== undefined) {
    inputEl.value = compressed;
    // Dispatch input events so React / Vue state management recognizes the programmatic update
    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    inputEl.dispatchEvent(new Event('change', { bubbles: true }));
  } else {
    // For ContentEditable / ProseMirror interfaces
    inputEl.focus();
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, compressed);
  }

  showShrinkToast(origCount, compCount);
}

// Inject our cyberpunk button into the interface
function createInjectButton() {
  if (document.getElementById('shrinktoken-direct-btn')) return;

  // Find suitable anchor area near input forms
  let formContainer = document.querySelector('form, [role="presentation"], nav');
  if (!formContainer && !document.body) return;

  let btn = document.createElement('button');
  btn.id = 'shrinktoken-direct-btn';
  btn.type = 'button';
  btn.innerHTML = `<span>⚡ Shrink</span>`;
  btn.title = "Compress prompt via local ShrinkToken NLP engine (-50% tokens)";

  Object.assign(btn.style, {
    position: 'fixed',
    bottom: '24px',
    right: '24px',
    zIndex: '99998',
    background: 'linear-gradient(135deg, #00e5ff 0%, #b900ff 100%)',
    color: '#0a0a0f',
    border: 'none',
    borderRadius: '25px',
    padding: '8px 16px',
    fontSize: '13px',
    fontWeight: '800',
    cursor: 'pointer',
    boxShadow: '0 0 15px rgba(0, 229, 255, 0.6)',
    transition: 'all 0.2s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    fontFamily: "'Fira Code', monospace, sans-serif"
  });

  btn.addEventListener('mouseenter', () => {
    btn.style.transform = 'scale(1.08)';
    btn.style.boxShadow = '0 0 22px rgba(185, 0, 255, 0.8)';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'scale(1)';
    btn.style.boxShadow = '0 0 15px rgba(0, 229, 255, 0.6)';
  });
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    executeDirectShrink();
  });

  document.body.appendChild(btn);
}

// Periodically check for page layout navigation (SPAs like ChatGPT/Claude alter DOM constantly)
setInterval(() => {
  createInjectButton();
}, 2000);

// Initial execution
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createInjectButton);
} else {
  createInjectButton();
}
