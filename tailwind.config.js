const colors = require('tailwindcss/colors')
module.exports = {
    content: [
        "./jembeui/templates/jembeui/s0/**/*.html"
    ],
    theme: {
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: colors.black,
            white: colors.white,
            grey: colors.neutral,
            primary: colors.sky,
            secondary: colors.cyan,
            tertiary: colors.fuchsia,
            brand: colors.green,
            success: colors.emerald,
            warn: colors.yellow,
            error: colors.red,
            privacy: colors.violet,
        },
        extend: {
            fontFamily: {
                'sans': ['Fira\\ Sans', 'sans-serif']
            },
            boxShadow: {
                'focus': '0 0 0 1px #0ea5e9 inset, 0 0 0 1px #0ea5e9, 0 0 0 4px #0ea5e94d',
            },
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
            }
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