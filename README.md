<div align="center">
  <img src="public/icon.png" width="120" alt="ShrinkToken Logo" />
  <h1>ShrinkToken ⚡</h1>
</div>

ShrinkToken is a local NLP-powered prompt compressor built with React and Vite. It drastically reduces the token size of massive prompts, context blocks, and code snippets *before* you send them to LLMs like ChatGPT or Claude, saving you up to 50% on API token costs.

## Features

- **Local NLP Compression**: Uses the `compromise` NLP library directly in the browser to aggressively prune adverbs, conversational fluff, and non-essential grammatical structures without losing the core intent of the prompt.
- **Real-Time Token Math**: Integrates with `gpt-tokenizer` to instantly calculate exact token counts (Original vs. Compressed) and calculate your savings percentage.
- **Lifetime Savings Tracker**: Persists your total tokens saved across all sessions using browser LocalStorage.
- **Interactive Liquid UI**: Features a custom CSS fluid-fill "Compress" button that visually represents your savings percentage as a water level.
- **OpenArc Wallet Integration**: Includes a sleek, absolute-positioned dropdown wallet linking to other OpenArc products (like Local LLM and LeadSaver).
- **Dark Mode Aesthetic**: A premium, high-contrast UI designed for developers.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **NLP Engine**: Compromise (compromise.cool)
- **Tokenization**: gpt-tokenizer
- **Icons**: Lucide React

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Run the Development Server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

3. **Build for Production**
   ```bash
   npm run build
   ```
   The optimized production bundle will be generated in the `dist` directory.

## How the Compression Works

The `compressPrompt` utility applies aggressive linguistic filtering:
1. **Punctuation Stripping**: Removes unnecessary periods and commas.
2. **Adverb Pruning**: Identifies and deletes adverbs using POS tagging.
3. **Conversational Fluff Removal**: Strips out polite filler phrases (e.g., "I hope you are having a wonderful day", "Could you please help me with").
4. **Pronoun & Conjunction Reduction**: Eliminates non-essential connecting words.

## License

MIT
