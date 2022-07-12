import io
from flask import Flask, render_template, make_response
from flask import send_file, url_for, redirect, request
from models.model_handler import Model_Handler
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRETKEY"
app.config['JSON_SORT_KEYS'] = False

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
    classes = model_handler.get_classes()
    result = sort_results(output, classes)
    data['output'] = list(result.values())
    data['classes'] = enumerate(result.keys())

  except Exception as e:
    response = make_response({'error': str(e)}, 417)
    return response

  return redirect(url_for("index"))
  
@app.route('/api/reconize_motorcycle', methods=['GET', 'POST'])
def api_recognize_motorcycle():
  try:
    file = request.files['file']
    img = Image.open(file.stream)
    output = model_handler.inference(img)
    classes = model_handler.get_classes()
    result = sort_results(output, classes)
    
    response = make_response(result, 200)
    return response

  except Exception as e:
    response = make_response({'error': str(e)}, 417)
    return response

def sort_results(probs, classes):
  result = {}
    
  for (percent, cl) in zip(probs, classes):
    result[cl] = "{:.5f}".format(percent)
  
  result = dict(sorted(result.items(), key=lambda item: float(item[1]), reverse=True))
  return result


if __name__ == '__main__':
  app.run(debug=False, host='0.0.0.0', port='5000')