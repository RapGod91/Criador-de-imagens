from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import textwrap

app = Flask(__name__)

# Configuração do diretório de imagens
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Caminho para a imagem de fundo padrão
DEFAULT_BACKGROUND = 'static/images/background.jpg'

def create_image_with_text(text):
    try:
        # Abre a imagem de fundo
        background = Image.open(DEFAULT_BACKGROUND)
        
        # Cria um objeto para desenhar na imagem
        draw = ImageDraw.Draw(background)
        
        # Configura a fonte (ajuste o tamanho conforme necessário)
        font_size = 100
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Configuração do texto
        margin = 50  # Margem das bordas
        offset = 10  # Espaçamento entre linhas
        max_width = background.width - (2 * margin)  # Largura máxima do texto
        
        # Quebra o texto em múltiplas linhas
        wrapped_text = textwrap.wrap(text, width=30)  # Ajuste o número 30 conforme necessário
        
        # Calcula a altura total do texto
        total_height = len(wrapped_text) * (font_size + offset)
        
        # Posição inicial do texto (centralizado verticalmente)
        y = (background.height - total_height) // 2
        
        # Desenha cada linha do texto
        for line in wrapped_text:
            # Calcula a largura da linha atual
            line_width = draw.textlength(line, font=font)
            # Calcula a posição x para centralizar a linha
            x = (background.width - line_width) // 2
            
            # Desenha a linha
            draw.text((x, y), line, font=font, fill="#000020")
            # Atualiza a posição y para a próxima linha
            y += font_size + offset
        
        # Salva a imagem em um buffer de memória
        img_io = BytesIO()
        background.save(img_io, 'JPEG')
        img_io.seek(0)
        
        return img_io
    except Exception as e:
        print(f"Erro ao criar imagem: {str(e)}")
        return None

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Texto não fornecido'}), 400
    
    text = data['text']
    img_io = create_image_with_text(text)
    
    if img_io:
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Erro ao gerar imagem'}), 500

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Gerador de Imagens</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .container {
                    text-align: center;
                }
                input[type="text"] {
                    padding: 10px;
                    width: 300px;
                    margin: 10px;
                }
                button {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                #result {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Gerador de Imagens</h1>
                <input type="text" id="text" placeholder="Digite o texto aqui">
                <button onclick="generateImage()">Gerar Imagem</button>
                <div id="result"></div>
            </div>
            
            <script>
                function generateImage() {
                    const text = document.getElementById('text').value;
                    if (!text) {
                        alert('Por favor, digite um texto');
                        return;
                    }
                    
                    fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({text: text})
                    })
                    .then(response => response.blob())
                    .then(blob => {
                        const imageUrl = URL.createObjectURL(blob);
                        const resultDiv = document.getElementById('result');
                        resultDiv.innerHTML = `<img src="${imageUrl}" style="max-width: 100%;">`;
                    })
                    .catch(error => {
                        console.error('Erro:', error);
                        alert('Erro ao gerar imagem');
                    });
                }
            </script>
        </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 