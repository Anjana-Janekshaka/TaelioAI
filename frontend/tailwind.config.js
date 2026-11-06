/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/lib/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#151515',
          soft: '#3d3a36',
          mute: '#5f5b55',
        },
        paper: '#f2f0eb',
        sheet: '#ffffff',
        rule: '#d9d5cc',
        series: {
          DEFAULT: '#e8641c',
          deep: '#b84a0e',
          tint: '#fbe3d5',
        },
        genre: {
          fantasy: '#1f7a4d',
          scifi: '#2b5fa8',
          mystery: '#5b3c96',
          romance: '#c8325a',
          horror: '#7a1f2b',
          thriller: '#b07c12',
          adventure: '#e8641c',
          drama: '#0f7480',
        },
        alert: {
          DEFAULT: '#a8231a',
          tint: '#fbecea',
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'ui-sans-serif', 'sans-serif'],
        sans: ['var(--font-ui)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        book: ['var(--font-book)', 'ui-serif', 'Georgia', 'serif'],
      },
      borderRadius: {
        card: '3px',
      },
      boxShadow: {
        book: '0 1px 1px rgba(21,21,21,0.08), 0 12px 28px -10px rgba(21,21,21,0.35)',
        lift: '0 1px 2px rgba(21,21,21,0.06), 0 6px 16px -8px rgba(21,21,21,0.25)',
      },
      maxWidth: {
        measure: '68ch',
      },
      transitionTimingFunction: {
        'out-expo': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [],
}
