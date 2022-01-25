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
                'focus-danger': '0 0 0 1px #e64f43 inset, 0 0 0 1px #e64f43, 0 0 0 4px #e64f434d',
            }
        },
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