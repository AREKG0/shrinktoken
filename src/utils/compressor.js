import nlp from 'compromise'

const STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into',
  'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then',
  'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with', 'very', 'really',
  'please', 'could', 'would', 'should', 'can', 'may', 'might', 'must', 'shall', 'am', 'has', 'have', 'had', 'do', 'does', 'did', 'so', 'too'
])

export function compressPrompt(text) {
  if (!text) return ''

  // Step 1: NLP parsing
  let doc = nlp(text)

  // Step 2: Remove common conversational greetings, sign-offs, and extreme fluff
  doc.match('(hello|hi|hey|greetings) (chatgpt|claude|ai|there|assistant)').remove()
  doc.match('hope you (are|having) * (day|week|month|time|so far)').remove()
  doc.match('(thank you|thanks) *').remove()
  doc.match('(appreciate|would really appreciate) * (help|assistance|time)').remove()
  doc.match('could you (please|kindly) *').remove()
  doc.match('please take some time').remove()

  // Step 3: Remove entire grammatical classes that carry low semantic value for LLMs
  doc.pronouns().remove()       // Removes I, you, me, they, it
  doc.conjunctions().remove()   // Removes and, but, or, because
  doc.adverbs().remove()        // Removes extremely, absolutely, highly, quickly
  
  // Custom harsh fluff removal
  doc.match('(really|very|just|quite|absolutely|extremely|highly|specifically|obviously|completely|simply)').remove()

  // Get raw terms
  let terms = doc.terms().out('array')

  // Step 4: Lexical & Stopword pruning
  let compressedTerms = terms.map(term => term.trim()).filter(term => {
    if (!term) return false
    const lower = term.toLowerCase().replace(/[^a-z]/g, '')
    // Filter out strict stopwords
    if (lower && STOPWORDS.has(lower)) return false
    return true
  })

  // Step 5: Reassemble and Lexical Minification
  let compressedText = compressedTerms.join(' ')
  
  // Collapse whitespace
  compressedText = compressedText.replace(/\s{2,}/g, ' ')
  
  // Clean up floating punctuation (e.g. "word ," -> "word,")
  compressedText = compressedText.replace(/\s+([.,!?:;])/g, '$1')
  // Remove leading punctuation that got orphaned
  compressedText = compressedText.replace(/^[.,!?:;]\s*/, '')
  
  return compressedText.trim()
}
