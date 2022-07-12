import io
from distutils.log import debug
from flask import Flask, render_template, make_response
from flask import send_file, url_for, redirect
from flask import request
from models.model_handler import Model_Handler
from PIL import Image

app = Flask(__name__)

IMG = None
data = {}
model_handler = Model_Handler('motorcycle')

@app.route("/")
def index():
  global data
  return render_template('index.html', data=data)

def image2HTML(pil_image):
  image_io = io.BytesIO()
  pil_image.save(image_io, format='PNG')
  image_io.seek(0)
  return image_io

@app.route('/image')
def image_uploaded():
  global IMG, data
  if IMG is not None:
    image_io = image2HTML(IMG)
    return send_file(
      image_io,
      as_attachment=False,
      mimetype='image/png'
    )
  else:
    return send_file(
      'static/images/hero-media-light.svg', 
      mimetype='image/svg+xml'  
    )

@app.route('/reconize_motorcycle', methods=['POST'])
def recognize_motorcycle():
  global IMG, data
  try:
    file = request.files['filename']
    pil_image = Image.open(file)
    IMG = pil_image.copy()
    output = model_handler.inference(pil_image)
    data['output'] = output
    # print(data['output'][0])
    data['classes'] = enumerate(model_handler.get_classes())

  except Exception as e:
    response = make_response(e, 500)

  return redirect(url_for("index"))
  
@app.route('/api/reconize_motorcycle', methods=['POST'])
def recognize_motorcycle():
  pass
  # try:
  #   file = request.files['filename']
  #   pil_image = Image.open(file)
  #   IMG = pil_image.copy()
  #   output = model_handler.inference(pil_image)
  #   data['output'] = output
  #   # print(data['output'][0])
  #   data['classes'] = enumerate(model_handler.get_classes())
  # except Exception as e:
  #   response = make_response(e, 500)

if __name__ == '__main__':
  app.run(debug=False)