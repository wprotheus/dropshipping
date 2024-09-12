from shopping import app

# Configurações adicionais
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True)
