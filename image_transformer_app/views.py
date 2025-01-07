from django.shortcuts import render, HttpResponse
import numpy as np
from sklearn.cluster import KMeans
from skimage import io
from PIL import Image
import base64
import io as pyio
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'home.html')


def process_image(request):
    if request.method == 'POST':
        try:
            # Parse input image
            data = json.loads(request.body)
            image_data = data['image'].split(",")[1]  # Remove 'data:image/png;base64,' part
            image_bytes = base64.b64decode(image_data)
            image = Image.open(pyio.BytesIO(image_bytes))

            k_value = int(data.get('k_value', 10))  # Default to 10 if not provided


            # Convert image to numpy array
            sample_img = np.array(image)

            # KMeans clustering
            n_colors = k_value
            w, h, _ = sample_img.shape
            reshaped_img = sample_img.reshape(w * h, 3)

            kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(reshaped_img)
            labels = kmeans.predict(reshaped_img)
            identified_palette = np.array(kmeans.cluster_centers_).astype(int)

            # Recolor image
            recolored_img = np.copy(reshaped_img)
            for index in range(len(recolored_img)):
                recolored_img[index] = identified_palette[labels[index]]
            recolored_img = recolored_img.reshape(w, h, 3)

            # Convert back to image
            output_image = Image.fromarray(recolored_img.astype('uint8'))

            # Encode to base64 for response
            buffered = pyio.BytesIO()
            output_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Send the processed image
            return JsonResponse({'output': img_str})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
