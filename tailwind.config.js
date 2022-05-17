const colors = require('tailwindcss/colors')
module.exports = {
    content: [
        "./jembeui/templates/jembeui/s0/**/*.html"
    ],
    theme: {
        extend: {
            colors: {
                // transparent: 'transparent',
                // current: 'currentColor',
                // black: { ...colors.black },
                // white: { ...colors.white },
                grey: { ...colors.neutral },
                primary: { ...colors.emerald },
                secondary: { ...colors.cyan },
                tertiary: { ...colors.fuchsia },
                brand: { ...colors.green },
                success: { ...colors.emerald },
                warn: { ...colors.yellow },
                error: { ...colors.red },
                privacy: { ...colors.violet },
            },
            fontFamily: {
                'sans': ['Fira\\ Sans', 'sans-serif']
            },
            boxShadow: {
                'focus': '0 0 0 1px rgb(0 0 0 / 0.7) inset, 0 0 0 1px rgb(0 0 0 / 0.7), 0 0 0 4px rgb(0 0 0 / 0.3)',
            },
            ringColor: (theme) => ({
                DEFAULT: theme('colors.primary[500]'),
            }),
            animation: {
                'progress': 'running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite'
            },
            keyframes: {
                'running-progress': {
                    '0%': {
                        'margin-left': '0px',
                        'margin-right': '100%',
                    },
                    '50%': {
                        'margin-left': '25%',
                        'margin-right': '0%',
                    },
                    '100%': {
                        'margin-left': '100%',
                        'margin-right': '0',
                    }
                },
            },
            typography: ({ theme }) => ({
                DEFAULT: {
                    css: {
                        '--tw-prose-body': theme('colors.grey[900]'),
                        '--tw-prose-headings': theme('colors.grey[900]'),
                        '--tw-prose-lead': theme('colors.grey[600]'),
                        '--tw-prose-links': theme('colors.primary[700]'),
                        '--tw-prose-bold': theme('colors.grey[900]'),
                        '--tw-prose-counters': theme('colors.grey[500]'),
                        '--tw-prose-bullets': theme('colors.grey[300]'),
                        '--tw-prose-hr': theme('colors.grey[200]'),
                        '--tw-prose-quotes': theme('colors.grey[900]'),
                        '--tw-prose-quote-borders': theme('colors.grey[200]'),
                        '--tw-prose-captions': theme('colors.grey[500]'),
                        '--tw-prose-code': theme('colors.grey[900]'),
                        '--tw-prose-pre-code': theme('colors.grey[200]'),
                        '--tw-prose-pre-bg': theme('colors.grey[800]'),
                        '--tw-prose-th-borders': theme('colors.grey[300]'),
                        '--tw-prose-td-borders': theme('colors.grey[200]'),
                        '--tw-prose-invert-body': theme('colors.grey[300]'),
                        '--tw-prose-invert-headings': theme('colors.white'),
                        '--tw-prose-invert-lead': theme('colors.grey[400]'),
                        '--tw-prose-invert-links': theme('colors.white'),
                        '--tw-prose-invert-bold': theme('colors.white'),
                        '--tw-prose-invert-counters': theme('colors.grey[400]'),
                        '--tw-prose-invert-bullets': theme('colors.grey[600]'),
                        '--tw-prose-invert-hr': theme('colors.grey[700]'),
                        '--tw-prose-invert-quotes': theme('colors.grey[100]'),
                        '--tw-prose-invert-quote-borders': theme('colors.grey[700]'),
                        '--tw-prose-invert-captions': theme('colors.grey[400]'),
                        '--tw-prose-invert-code': theme('colors.white'),
                        '--tw-prose-invert-pre-code': theme('colors.grey[300]'),
                        '--tw-prose-invert-pre-bg': 'rgb(0 0 0 / 50%)',
                        '--tw-prose-invert-th-borders': theme('colors.grey[600]'),
                        '--tw-prose-invert-td-borders': theme('colors.grey[700]'),
                    }
                }
            })
        }
    },
    variants: {
        extends: {
            backgroundColor: ['disabled'],
            textColor: ['disabled'],
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms')({
            strategy: "class"
        }),
    ],
}