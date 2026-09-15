import { encode } from 'gpt-tokenizer'

export function countTokens(text) {
  if (!text) return 0
  try {
    const tokens = encode(text)
    return tokens.length
  } catch (e) {
    console.error("Tokenization error:", e)
    return 0
  }
}
