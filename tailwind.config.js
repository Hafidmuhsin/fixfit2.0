/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './fixfit/settings.py',
        './accounts/templates/**/*.html',
        './dashboard/templates/**/*.html',
        './nutrition/templates/**/*.html',
        './hydration/templates/**/*.html',
        './sleep/templates/**/*.html',
        './exercise/templates/**/*.html',
        './achievements/templates/**/*.html',
        './feedback/templates/**/*.html',
        // also scan views for class names if dynamic
        './**/views.py',
    ],
    theme: {
        extend: {
            colors: {
                'luxury-dark': '#0f172a',
                'luxury-accent': '#38bdf8',
                'glass-bg': 'rgba(255, 255, 255, 0.05)',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            backdropBlur: {
                xs: '2px',
            }
        },
    },
    plugins: [],
}
