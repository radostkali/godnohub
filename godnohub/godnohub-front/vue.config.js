module.exports = {
  devServer: {
    proxy: {
      '/*': {
        target: "http://127.0.0.1:7000",
        logLevel: 'debug'
      }
    }
  },
  // outputDir must be added to Django's TEMPLATE_DIRS
  outputDir: '../dist/',
  // assetsDir must match Django's STATIC_URL
  assetsDir: 'static',
}
