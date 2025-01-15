module.exports = {
    content: [
        // Ajusta las rutas de tus plantillas de acuerdo con la estructura del proyecto
        './templates/**/*.html',
        './mi_blog_theme/templates/**/*.html',
        './**/templates/**/*.html',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
